import logging
import cv2
import numpy as np

import service.constants as const

from service.va_service import VAService
from models.objectdetect import ObjectDetect
from models.classify import Classify
from misc import labelmap_util

tracelogger = logging.getLogger('trace')
MotionBase = True

import yaml
import os

class ChangeDetector:
    def __init__(self, id=None, reload=False):
        self.id = id
        self._frame_queue = []
        self._considering_frame_width = 1
        self._queue_size = self._considering_frame_width + 1# hardcoded
        self.adapt_time = None
        self.reload = reload
        if not reload:
            self.config_load()

    def config_load(self):
        with open('conf/config-firesmoke.yml', 'r') as f:
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

    def run_single_image(self, image):
        if self.reload:
            while True:
                try:
                    self.config_load()
                    break
                except:
                    pass
        self.insert(cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), self.blur_size, 0))
        return self.get_moving_object()


    def get_moving_object(self):
        

        if len(self._frame_queue) > 1:
            current_frame = self._frame_queue[-1]
            if self.size == None or self.size != current_frame.shape[:2]:
                self.size = current_frame.shape[:2]
                m = min(self.size)
                self.erode_kernels.append(np.ones((int(m * self.erode_kernel_sizes[0]), int(m * self.erode_kernel_sizes[0])), np.uint8))
                self.erode_kernels.append(np.ones((int(m * self.erode_kernel_sizes[1]), int(m * self.erode_kernel_sizes[1])), np.uint8))
                self.dilate_kernel = np.ones((int(m * self.dilate_kernel_size), int(m * self.dilate_kernel_size)), np.uint8)

            iter_ = min(len(self._frame_queue), self._considering_frame_width)
            
            thresh = self.frame_diff_between(current_frame, self._frame_queue[-2])
            difScore = cv2.mean((thresh > 0).astype(np.uint8))[0]
            if difScore > self.diff_threshold or self.current_adapt_time > 0:
                self._frame_queue.clear()
                if self.current_adapt_time > 0:
                    self.current_adapt_time -= 1
                else:
                    self.current_adapt_time = self.adapt_time
                return []
            for i in range(iter_ - 1):
                thresh += self.frame_diff_between(current_frame, self._frame_queue[-1-i])
            # cv2.imshow('t', thresh)
            thresh = cv2.erode(thresh, self.erode_kernels[0], iterations = 1)
            thresh = cv2.dilate(thresh, self.dilate_kernel, iterations = 1)
            thresh = cv2.erode(thresh, self.erode_kernels[1], iterations=1)
            # cv2.imshow('t1', thresh)

            contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            results =[]
            for c in contours:
                bbox = cv2.boundingRect(c)
                if bbox[2] < self.minimum_bbox[0] or bbox[3] < self.minimum_bbox[1]:
                    continue
                results.append([bbox[1] / self.size[0], bbox[0] / self.size[1], (bbox[1] + bbox[3]) / self.size[0], (bbox[0] + bbox[2]) / self.size[1]])
            return results
            # return [cv2.boundingRect(c) for c in contours]
        else:
            return []


class FiresmokeVA(VAService):

    def __init__(self, config, va_type, min_threshold=0.5):
        super().__init__(config, va_type)
        self.detection = ObjectDetect(self.enabled, config, 'firesmoke')
        self.min_score_threshold = config.getvalue(self.conf_prefix + 'min_score_threshold', min_threshold)
        self.motion = {}#ChangeDetector()
        self.classify_shape = 299
        self.reload_conf = config.getbool(self.conf_prefix + 'reload_conf')
        
        if MotionBase:
            self.classify = Classify(self.enabled, config, 'firesmoke_clz')
            clz_labels = label_map_util.create_categories_from_labelmap(config.getvalue(self.conf_prefix + 'classify_path_to_label'))
            self.classify_labals = dict([(item['id'], item['name']) for item in clz_labels])


    # def dominant_color(self, image_patch):
    #     hsv = cv2.cvtColor(image_patch, cv2.COLOR_BGR2HSV)
    #     hist = cv2.calcHist([hsv], [0], None, [180], [0, 256])

    def _set_lables(self, path_to_labels):
        labels = label_map_util.create_categories_from_labelmap(path_to_labels)
        return dict([(item['id'], item['name']) for item in labels])

    '''
        get_in_by_vatype_gen() generator examples  
    '''
    # def _execute(self, sc):
    #     start = time.time()
    #     for ch_idx, image_np, width_height, va in sc.get_in_by_vatype_gen(self.is_support_vatype_fc):
    #         inf_result = self.detection.inference(np.expand_dims(image_np, axis=0))
    #         sc.set_out_ch(const.DETECT_VA, ch_idx, inf_result[0])
    #
    #     tracelogger.debug('[%s] total detection inference elapesed: [%.2f], images [%d]',
    #                       const.VA_TYPES[self.va_type], (time.time() - start), ch_idx)
    #
    #     return sc;

    def _execute(self, sc):
        # channel 순서를 가지고 있는 image numpy
        # list -> [ch_idx, image]
        image_by_ch  = sc.get_in_by_vatype(self.is_support_vatype_fc)

        # 처리할 정보가 없는 경우 return
        if len(image_by_ch) == 0: return sc

        # debug.show_images(extract_by_ch[:, 1].tolist())
        # image array만 inference 처리
        if not MotionBase:
            inf_result = self.detection._inference(image_by_ch[:, 1].tolist())
            for (ch_id, _, _, cfg_json), inference in zip (image_by_ch, inf_result):
                sc.set_out_by_ch(self.va_type, ch_id, self.aggregate_result(inference))
        else:
            # inf_result = self.motion.run_in_batch(image_by_ch[:, 1].tolist())
            inf_result = []
            for ch_id, image, _, cfg_json in image_by_ch:
                if ch_id not in self.motion:
                    self.motion[ch_id] = ChangeDetector(ch_id, self.reload_conf)
                inf_result.append(self.motion[ch_id].run_single_image(image))

            detect_firesmoke = dict()

            for (ch_id, _, _, cfg_json), inference in zip (image_by_ch, inf_result):
                # sc.set_out_by_ch(const.DETECT_VA, ch_id, [inference, [1 for i in range(len(inference))], ['fire' for i in range(len(inference))]])
                detect_firesmoke[ch_id] = [inference, [1 for i in range(len(inference))], ['fire' for i in range(len(inference))]]

            # detect_by_ch = sc.get_out_by_vatype(const.DETECT_VA)
            for (ch, firesmoke, _, cfg_json) in image_by_ch:
                # detect = detect_by_ch[ch]
                detect = detect_firesmoke[ch]
                # boxes, firesmoke_corp_np_list = self.expend_box_n_resize(firesmoke, detect)
                boxes, firesmoke_corp_np_list = self.expend_box_n_padding_zero(firesmoke, detect)

                # falldown이 없으면 깡통list 추가
                if len(firesmoke_corp_np_list) == 0:
                    sc.set_out_by_ch(self.va_type, ch, [[], [], []])
                    continue

                # debug.show_images(fall_down_corp_np_list)
                inf_result = self.classify._inference(firesmoke_corp_np_list)

                # falldown class id 만 추출하여 response 정보 생성
                # response format : boxes, score, class
                sc.set_out_by_ch(self.va_type, ch, self.aggregate_classify_result(boxes, inf_result))
        return sc

    def aggregate_result(self, inference):
        boxes, scores, classes = inference
        valid = [idx for idx, score in enumerate(scores) if score > self.min_score_threshold]
        if len(valid) > 0:
            valid_scores = scores[valid].tolist()
            valid_boxes  = boxes[valid].tolist()
            valid_class = [self.label_map[int(a_class)] for a_class in classes[valid]]
            return [valid_boxes, valid_scores, valid_class]
        else: # invalid image
            return [[],[],[]]

    def aggregate_classify_result(self, boxes, inf_result):
        res_boxes = []
        res_scores = []
        res_classes = []

        for box, logits in zip(boxes, inf_result):
            prob = logits[0:]
            sorted_inds = [i[0] for i in sorted(enumerate(-prob), key=lambda x: x[1])]
            if sorted_inds[0] > 0 :   # 1: fire, 2: smoke
                # response format : boxes, score, class
                res_boxes.append(box)
                res_scores.append(prob[sorted_inds[0]])
                res_classes.append(self.label_map[1])

        return [res_boxes, res_scores, res_classes]

    def expend_box_n_resize(self, image_np, detects):

        fall_down_crop_list = list()

        boxes, scores, classes = detects
        for idx in range(len(boxes)):
            box_t = tuple(boxes[idx])
            crop, box = self.__crop_expend_ares(image_np, box_t)
            crop = cv2.resize(crop, (self.classify_shape, self.classify_shape))
            fall_down_crop_list.append(crop)

        return boxes, fall_down_crop_list

    def expend_box_n_padding_zero(self, image_np, detects):

        fall_down_crop_list = list()

        boxes, scores, classes = detects
        for idx in range(len(boxes)):
            box_t = tuple(boxes[idx])
            crop, box = self.__crop_expend_ares(image_np, box_t, 0.4)
            crop = self.__resize_and_padding_zero(crop, self.classify_shape)
            fall_down_crop_list.append(crop)

        return boxes, fall_down_crop_list

    def __resize_and_padding_zero(self, image, desired_size=233):
        old_size = image.shape[:2]  # old_size is in (height, width) format
        ratio = float(desired_size) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        image = cv2.resize(image, (new_size[1], new_size[0]))

        delta_w = desired_size - new_size[1]
        delta_h = desired_size - new_size[0]
        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)

        color = [0, 0, 0]
        return cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)


    def __crop_expend_ares(self, image_np, box, ratio=0, coordiante=True):
        im_height, im_width = image_np.shape[:2]
        ymin, xmin, ymax, xmax = box

        if (coordiante):
            (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                          ymin * im_height, ymax * im_height)
        else:
            (left, right, top, bottom) = (xmin, xmax, ymin, ymax)

        vh_ratio = (bottom - top) / (right - left)
        hv_ratio = (right - left) / (bottom - top)
        if vh_ratio > 0:  # 세로가 긴 경우
            width_ratio = int(((right - left) * (ratio * vh_ratio)) / 2)
            height_ratio = int(((bottom - top) * ratio) / 2)
        else:
            width_ratio = int(((right - left) * ratio) / 2)
            height_ratio = int(((bottom - top) * (ratio * hv_ratio)) / 2)

        top = (top - height_ratio) if 0 < (top - height_ratio) else 0
        bottom = (bottom + height_ratio) if im_height > (bottom + height_ratio) else im_height
        left = (left - width_ratio) if 0 < (left - width_ratio) else 0
        right = (right + width_ratio) if im_width > (right + width_ratio) else im_width

        return image_np[int(top):int(bottom), int(left):int(right), :], (left, right, top, bottom)
