import logging
import cv2
import numpy as np
import yaml
import json

from service import constants as const

tracelogger = logging.getLogger('trace')

NIGHT_DIST_THRESHOLD = 110
NIGHT_ERODE_WEIGHT = 0.01

# first_erode_size: 0.003
# second_erode_size: 0.025
# dilate_size: 0.05

MOTION_THRESHOLD = [
    # blur, first_erode, second_erod, dilate
    [1, 0.003, 0.025, 0.09],   # 0
    [1, 0.004, 0.025, 0.08],   # 1
    [1, 0.005, 0.025, 0.09],   # 2
    [1, 0.006, 0.025, 0.09],   # 3
    [3, 0.003, 0.025, 0.09],   # 4
    [3, 0.005, 0.025, 0.07],   # 5
    [3, 0.007, 0.025, 0.05],   # 6
    [5, 0.003, 0.025, 0.04],   # 7
    [5, 0.003, 0.025, 0.03],   # 8
    [5, 0.001, 0.025, 0.02]    # 9
]
MOTION_THRESHOLD_LEVEL = 5

class FiresmokeDetector:
    def __init__(self, id=None, reload=False, cfg_json=None):
        self.id = id
        self._frame_queue = []
        self._considering_frame_width = 1
        self._queue_size = self._considering_frame_width + 1  # hardcoded
        self.adapt_time = None
        self.reload = reload
        self.debug = False
        self.subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()  # etectShadows=False)
        self.cfg_json = json.dumps(cfg_json)
        self.erode_kernels = []
        self.dilate_kernel = None

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
        if len(config['firesmoke']['minimum_bbox']) == 1:
            self.minimum_bbox = (config['firesmoke']['minimum_bbox'][0], config['firesmoke']['minimum_bbox'][0])
        else:
            self.minimum_bbox = config['firesmoke']['minimum_bbox']
        self.size = None
        self.debug = config['firesmoke']['debug']
        self.sens_level = config['firesmoke']['sens_level']

        self.set_sensitivity(self.sens_level)

    def set_sensitivity(self, sens_level):

        self.blur_size = (MOTION_THRESHOLD[sens_level][0], MOTION_THRESHOLD[sens_level][0])
        self.erode_kernel_sizes = (MOTION_THRESHOLD[sens_level][1], MOTION_THRESHOLD[sens_level][2])
        self.dilate_kernel_size = MOTION_THRESHOLD[sens_level][3]

        # if len(config['firesmoke']['blur_size']) == 1:
        #     self.blur_size = (config['firesmoke']['blur_size'][0], config['firesmoke']['blur_size'][0])
        # else:
        #     self.blur_size = config['firesmoke']['blur_size']
        # self.erode_kernels = []
        # self.dilate_kernel = None
        #
        # self.erode_kernel_sizes = (config['firesmoke']['first_erode_size'], config['firesmoke']['second_erode_size'])
        # self.dilate_kernel_size = config['firesmoke']['dilate_size']


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
        return np.mean(v) < NIGHT_DIST_THRESHOLD

    def run_single_image(self, image, cfg_json):
        if self.reload:
            while True:
                try:
                    self.config_load()
                    break
                except:
                    pass
        else:
            sens_level = MOTION_THRESHOLD_LEVEL

            if cfg_json is not None and const.FIRESMOKE_NAME.upper() in cfg_json:
                if 'sens_level' in cfg_json[const.FIRESMOKE_NAME.upper()]:
                    sens_level = cfg_json[const.FIRESMOKE_NAME.upper()]['sens_level']
            self.set_sensitivity(sens_level)

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
            # print('diff %0.3f'%difScore)

            # motion 적응시간
            if self.current_adapt_time > 0:
                self._frame_queue.clear()
                self.subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()
                if self.current_adapt_time > 0:
                    self.current_adapt_time -= 1
                else:
                    self.current_adapt_time = self.adapt_time
                return []

            # preset 수행 중 또는 근접 인경우
            if difScore > self.diff_threshold :
                # self._frame_queue.clear()
                self.current_adapt_time = self.adapt_time
                self._frame_queue.clear()
                self.subtractor.clear()
                return None

            thresh = self.subtractor.apply(self._frame_queue[-1]).astype(np.uint8)
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