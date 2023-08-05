import logging
import cv2
import numpy as np
import yaml

tracelogger = logging.getLogger('trace')

NIGHT_DIST_THESHOLD = 110
NIGHT_ERODE_WEIGHT = 0.01

class FiresmokeDetector:
    def __init__(self, id=None, reload=False):
        self.id = id
        self._frame_queue = []
        self._considering_frame_width = 1
        self._queue_size = self._considering_frame_width + 1  # hardcoded
        self.adapt_time = None
        self.reload = reload
        self.debug = False
        if not reload:
            self.config_load()

    def config_load(self):
        with open('conf/firesmoke-cfg.yml', 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.diff_threshold = config['firesmoke']['diff_threshold']
        if self.adapt_time == None:
            self.adapt_time = config['firesmoke']['adapt_time']
            self.current_adapt_time = self.adapt_time
        self.binary_threshold = config['firesmoke']['binary_threshold']
        if len(config['firesmoke']['blur_size']) == 1:
            self.blur_size = (config['firesmoke']['blur_size'][0], config['firesmoke']['blur_size'][0])
        else:
            self.blur_size = config['firesmoke']['blur_size']

        self.erode_kernels = []
        self.dilate_kernel = None
        if len(config['firesmoke']['minimum_bbox']) == 1:
            self.minimum_bbox = (config['firesmoke']['minimum_bbox'][0], config['firesmoke']['minimum_bbox'][0])
        else:
            self.minimum_bbox = config['firesmoke']['minimum_bbox']
        self.size = None
        self.erode_kernel_sizes = (config['firesmoke']['first_erode_size'], config['firesmoke']['second_erode_size'])
        self.dilate_kernel_size = config['firesmoke']['dilate_size']
        self.debug = config['firesmoke']['debug']

    def insert(self, item):
        if len(self._frame_queue) >= self._queue_size:
            del self._frame_queue[0]
        self._frame_queue.append(item)

    def frame_diff_between(self, a, b):
        d1 = cv2.absdiff(a, b)
        thresh = cv2.threshold(d1, self.binary_threshold[0], self.binary_threshold[1], cv2.THRESH_BINARY)[1]

        return thresh

    def run_in_batch(self, batches):
        results = []
        for b in batches:
            # ks = int(min(b.shape[:2]) * 0.03)
            # if ks % 2 == 0:
            #     ks += 1
            self.insert(cv2.GaussianBlur(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY), self.blur_size, 0))
            results.append(self.get_moving_object())
        return results

    # hsv 의 value값이 NIGHT_DIST_THESHOLD 작은경우 ir image
    def ir_image_estim(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        return np.mean(v) < NIGHT_DIST_THESHOLD

    def run_single_image(self, image):
        if self.reload:
            while True:
                try:
                    self.config_load()
                    break
                except:
                    pass
        self.insert(cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), self.blur_size, 0))
        return self.get_moving_object(self.ir_image_estim(image))

    def get_moving_object(self, ir_image):

        if len(self._frame_queue) > 1:
            current_frame = self._frame_queue[-1]
            if self.size == None or self.size != current_frame.shape[:2]:
                self.size = current_frame.shape[:2]
                m = min(self.size)
                self.erode_kernels.append(
                    np.ones((int(m * (self.erode_kernel_sizes[0] + (NIGHT_ERODE_WEIGHT if ir_image else 0))),
                             int(m * (self.erode_kernel_sizes[0] + (NIGHT_ERODE_WEIGHT if ir_image else 0)))), np.uint8))
                self.erode_kernels.append(
                    np.ones((int(m * self.erode_kernel_sizes[1]), int(m * self.erode_kernel_sizes[1])), np.uint8))
                self.dilate_kernel = np.ones((int(m * self.dilate_kernel_size), int(m * self.dilate_kernel_size)),
                                             np.uint8)

            iter_ = min(len(self._frame_queue), self._considering_frame_width)

            thresh = self.frame_diff_between(current_frame, self._frame_queue[-2])
            difScore = cv2.mean((thresh > 0).astype(np.uint8))[0]

            # motion 적응시간
            if self.current_adapt_time > 0:
                self._frame_queue.clear()
                if self.current_adapt_time > 0:
                    self.current_adapt_time -= 1
                else:
                    self.current_adapt_time = self.adapt_time
                return []

            # preset 수행 중 또는 근접 인경우
            if difScore > self.diff_threshold :
                # self._frame_queue.clear()
                return None

            for i in range(iter_ - 1):
                thresh += self.frame_diff_between(current_frame, self._frame_queue[-1 - i])
            # cv2.imshow('t', thresh)
            thresh = cv2.erode(thresh, self.erode_kernels[0], iterations=1)
            thresh = cv2.dilate(thresh, self.dilate_kernel, iterations=1)
            thresh = cv2.erode(thresh, self.erode_kernels[1], iterations=1)
            # cv2.imshow('t1', thresh)

            contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            results = []
            for c in contours:
                bbox = cv2.boundingRect(c)
                if bbox[2] < self.minimum_bbox[0] or bbox[3] < self.minimum_bbox[1]:
                    continue
                results.append([bbox[1] / self.size[0], bbox[0] / self.size[1], (bbox[1] + bbox[3]) / self.size[0],
                                (bbox[0] + bbox[2]) / self.size[1]])
            return results
            # return [cv2.boundingRect(c) for c in contours]
        else:
            return []