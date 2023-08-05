import logging
import cv2
import numpy as np
from skimage.measure import label
import yaml
from scipy import signal
import time

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
        self.subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()#etectShadows=False)
        self.color_model = ColorModel()
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
        return self.get_moving_object(self.ir_image_estim(image), image)

    def get_moving_object(self, ir_image, color_image):

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

            diff = self.frame_diff_between(current_frame, self._frame_queue[-2])
            difScore = cv2.mean((diff > 0).astype(np.uint8))[0]

            # motion 적응시간
            if self.current_adapt_time > 0:
                self._frame_queue.clear()
                self.subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()
                self.color_model.reset()
                if self.current_adapt_time > 0:
                    self.current_adapt_time -= 1
                else:
                    self.current_adapt_time = self.adapt_time
                return []

            # preset 수행 중 또는 근접 인경우
            if difScore > self.diff_threshold :
                # self._frame_queue.clear()
                return None
            thresh = self.subtractor.apply(self._frame_queue[-1]).astype(np.uint8)
            # for i in range(iter_ - 1):
            #     thresh += self.frame_diff_between(current_frame, self._frame_queue[-1 - i])
            # cv2.imshow('t', thresh)
            thresh = cv2.erode(thresh, self.erode_kernels[0], iterations=1)
            thresh = cv2.dilate(thresh, self.dilate_kernel, iterations=1)
            # thresh = cv2.erode(thresh, self.erode_kernels[1], iterations=1)
            
            if ir_image:
                thresh *= self.color_model.run(color_image, thresh)
            
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


class ColorModel:
    def __init__(self, subtractor='MOG'):
        self.frames = []
        self.fore_accu_img_fire = []
        self.fore_accu_img_smoke = []
        self.b1 = 5
        self.b2 = 1
        self.block_resolution = 25
        self.fire_t = int(self.block_resolution * 0.7)
        self.smoke_t = int(self.block_resolution * 0.7)
        # self.sub_name = subtractor
        # if subtractor == 'MOG':
        #     self.subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()#etectShadows=False)
        # elif subtractor == 'GMG':
        #     self.subtractor = cv2.bgsegm.createBackgroundSubtractorGMG()

    def reset(self):
        # self.fore_accu_img_fire = []
        self.fore_accu_img_smoke = []
        # if self.sub_name == 'MOG':
        #     self.subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()#etectShadows=False)
        # elif self.sub_name == 'GMG':
        #     self.subtractor = cv2.bgsegm.createBackgroundSubtractorGMG()

    def run(self, frame, fgmask):
        # frame: numpy bgr
        # frame[:, :, 0] = cv2.equalizeHist(frame[:, :, 0])
        # frame[:, :, 1] = cv2.equalizeHist(frame[:, :, 1])
        # frame[:, :, 2] = cv2.equalizeHist(frame[:, :, 2])

        # frame = cv2.GaussianBlur(frame, (3, 3), 0)
        
        # if len(self.fore_accu_img_fire) == 0:
        #     self.fore_accu_img_fire.append(np.zeros((frame.shape[0], frame.shape[1], 1)))
        if len(self.fore_accu_img_smoke) == 0:
            self.fore_accu_img_smoke.append(np.zeros((frame.shape[0], frame.shape[1], 1)))
        # fgmask = self.moving_pixel_and_region_extracting(frame)
        # kernel = np.ones((5, 5), np.uint8) 
        # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        # cv2.imshow('mask', fgmask)
        fgmask = fgmask == 255
        # flame_color_mask = self.flame_color(frame) * fgmask
        smoke_color_mask = self.smoke_color(frame) * fgmask
        # self.foreground_accumulation_image(flame_color_mask, self.fore_accu_img_fire)

        self.foreground_accumulation_image(smoke_color_mask, self.fore_accu_img_smoke)

        # fire = self.block_image_proc(self.fore_accu_img_fire[-1], self.fire_t)
        smoke = self.block_image_proc(self.fore_accu_img_smoke[-1], self.smoke_t)

        # smoke = self.mask_to_flood_fill(self.fore_accu_img_smoke[-1], smoke, frame)

        # fire_area = self.mask_to_flood_fill(self.fore_accu_img_fire[-1], fire, frame)

        # cv2.imshow('area_smoke', smoke_area)
        # cv2.imshow('area_fire', fire_area)
        # del self.fore_accu_img_fire[0]
        del self.fore_accu_img_smoke[0]
        return smoke.squeeze(-1)

    def moving_pixel_and_region_extracting(self, frame):
        fgmask = self.subtractor.apply(frame)
        return fgmask

    def flame_color(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        return (0 <= hsv[:, :, 0]) * (hsv[:, :, 0] <= 30) * (127 <= hsv[:, :, 2]) * (hsv[:, :, 2] <= 255) * (hsv[:, :, 1] < 72)# * ((frame[:, :, 0] > 230) + (frame[:, :, 1] > 230) + (frame[:, :, 2] > 230))

    def smoke_color(self, frame):
        #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        m = cv2.max(cv2.max(frame[:, :, 0], frame[:, :, 1]), frame[:, :, 2])
        n = cv2.min(cv2.min(frame[:, :, 0], frame[:, :, 1]), frame[:, :, 2])

        # i = self.to_hsi(frame)[:, :, 2]
        r = m - n
        # return i < 50
        return ((0 <= r) * (r <= 30))# * (hsv[:, :, 1] < 20))

    def foreground_accumulation_image(self, fgmask, fore_accu_img):
        fgmask = np.expand_dims(fgmask, 2)
        new_accu = np.zeros_like(fgmask)
        new_accu[fgmask] = fore_accu_img[-1][fgmask] + self.b1
        new_accu[np.logical_not(fgmask)] = np.clip(fore_accu_img[-1][np.logical_not(fgmask)] - self.b2, a_min=0, a_max=None)
        fore_accu_img.append(new_accu)

    def block_image_proc(self, frame, t):
        height, width = frame.shape[:2]
        height_iter = int(height / self.block_resolution)
        width_iter = int(width / self.block_resolution)
        # layer = np.ones([self.block_resolution, self.block_resolution])
        # frame = frame.reshape(height, width)
        padded = np.pad(frame.reshape(height, width), ((0, self.block_resolution - height % self.block_resolution), (0, self.block_resolution - width % self.block_resolution)), 'constant', constant_values=((0, 0), (0, 0)))
        padded_height, padded_width = padded.shape[:2]
        conved = padded.reshape(int(padded_height/self.block_resolution), self.block_resolution, -1).sum(1)\
                       .reshape(int(padded_height/self.block_resolution), int(padded_width/self.block_resolution), self.block_resolution).sum(2) > 0
        # conved = signal.convolve2d(frame.reshape(height, width), layer, 'same')
        # # conved = np.convolve(padded, layer)
        # conved = conved[::self.block_resolution, ::self.block_resolution] > t
        # conved = np.expand_dims(conved, -1)
        results = np.zeros_like(frame)
        for h in range(height_iter + 1):
            h_from = h * self.block_resolution
            if h_from + self.block_resolution > height:
                h_to = height + 1
            else:
                h_to = h_from + self.block_resolution
            
            for w in range(width_iter + 1):
                w_from = w * self.block_resolution
                if w_from + self.block_resolution > width:
                    w_to = width + 1
                else:
                    w_to = w_from + self.block_resolution
                
                if conved[h, w]:
                    results[h_from:h_to, w_from:w_to, :] = frame[h_from:h_to, w_from:w_to, :]
                # block = frame[h_from:h_to, w_from:w_to, :]
                    
                # if np.sum(block) > t:
                #     # print(np.sum(block))
                #     # print('fire detected in frame')
                    
        
        return results.astype(np.bool)# * 255

    def mask_to_flood_fill(self, origin_mask, detected_mask, frame):
        detected_mask = detected_mask.astype(np.bool)
        flood_fill = label(origin_mask)
        points = np.unique(flood_fill * detected_mask)
        
        area = np.zeros_like(origin_mask)
        for p in points:
            if p == 0: continue
            cal_area = (flood_fill == p)
            if self.analyse_hist(frame, cal_area):
                area = area + cal_area

        return area.astype(np.uint8) * 255

    def analyse_hist(self, frame, mask):
        hist, _ = np.histogram(np.expand_dims(frame[:, :, 2], 2)[mask], bins=32, range=(0, 255))
        fire_count = 0
        total = len(hist) - 1
        for index in range(total):
            if hist[index] < hist[index+1]:
                fire_count += 1
            elif np.abs(hist[index] - hist[index+1]) < 10:
                fire_count += 1
        # print(fire_count/total)
        return fire_count/total > 0.9