import logging
import cv2
import numpy as np

import service.constants as const

from service.va_service import VAService
from models.objectdetect import ObjectDetect
from models.classify import Classify
from misc import labelmap_util
from misc.firesmoke_detector_v3 import FiresmokeDetector
from misc.estimator.condition_estimate import ConditionEstimator

tracelogger = logging.getLogger('trace')

class FiresmokeVA(VAService):

    def __init__(self, config, va_type, min_threshold=0.5):
        super().__init__(config, va_type)
        self.detection = ObjectDetect(self.enabled, config, 'firesmoke')
        self.min_score_threshold = config.getvalue(self.conf_prefix + 'min_score_threshold', min_threshold)

        self.classify_shape = 299
        self.reload_conf = config.getbool(self.conf_prefix + 'reload_conf')

        self.classify = Classify(self.enabled, config, 'firesmoke_clz')
        clz_labels = labelmap_util.create_categories_from_labelmap(config.getvalue(self.conf_prefix + 'classify_path_to_label'))
        self.classify_labals = dict([(item['id'], item['name']) for item in clz_labels])

        self.motion = {}
        self.estimator = {}

    def _set_lables(self, path_to_labels):
        labels = labelmap_util.create_categories_from_labelmap(path_to_labels)
        return dict([(item['id'], item['name']) for item in labels])

    def _execute(self, sc):
        # channel 순서를 가지고 있는 image numpy
        # list -> [ch_idx, image]
        image_by_ch  = sc.get_in_by_vatype(self.is_support_vatype_fc)

        # 처리할 정보가 없는 경우 return
        if len(image_by_ch) == 0: return sc

        motion_inference = []
        for ch_id, image, _, cfg_json in image_by_ch:
            if ch_id not in self.motion:
                self.motion[ch_id] = FiresmokeDetector(ch_id, self.reload_conf)
            if ch_id not in self.estimator:
                self.estimator[ch_id] = ConditionEstimator(image.shape[:2],
                                                             self.config.getvalue(self.conf_prefix + 'queue_size'),
                                                             self.config.getvalue(self.conf_prefix + 'activation_per_queue'),
                                                             self.config.getvalue(self.conf_prefix + 'iou_threshold'))

            motion_inference.append(self.motion[ch_id].run_single_image(image))

        # for debug
        for (ch_id, _, _, cfg_json), inference in zip (image_by_ch, motion_inference):
            if self.motion[ch_id].debug:
                if inference is not None:
                    sc.set_out_by_ch(const.DETECT_VA, ch_id, [inference, [1 for i in range(len(inference))], ['fire' for i in range(len(inference))]])


        motion_firesmoke = dict()
        chaged_image_by_ch = []

        for (ch_id, image_np, ch_uuid, cfg_json), inference in zip (image_by_ch, motion_inference):
            # preset 또는 화면 변화 시 근접인 경우 detection 으로 처리
            if inference is None:
                motion_firesmoke[ch_id] = [[], [], []]
                chaged_image_by_ch.append([ch_id, image_np, ch_uuid])
            else:
                # motion 개수가 많은 경우 detection 으로 처리
                if len(inference) > 20 :
                    motion_firesmoke[ch_id] = [[], [], []]
                else :
                    motion_firesmoke[ch_id] = [inference, [1 for i in range(len(inference))], ['fire' for i in range(len(inference))]]

                # 화면 변화가 있는 경우에만 detection 처리
                if len(inference) > 0 :
                    chaged_image_by_ch.append([ch_id, image_np, ch_uuid])

        chaged_image_by_ch = np.array(chaged_image_by_ch)

        # detection inference
        detection_firesmoke = dict()

        if len(chaged_image_by_ch) > 0 :
            detection_inference = self.detection._inference(chaged_image_by_ch[:, 1].tolist())
            for (ch_id, _, _), inference in zip (chaged_image_by_ch, detection_inference):
                detection_firesmoke[ch_id] = self.aggregate_result(inference)
                if self.motion[ch_id].debug:
                    sc.set_out_by_ch(const.FALLDOWN_VA, ch_id, self.aggregate_result(inference))

        for (ch, firesmoke, ch_uuid, cfg_json) in image_by_ch:
            # motion detection box를 이용하여 classification
            motion_detect = motion_firesmoke[ch]
            boxes, firesmoke_corp_np_list = self.expend_box_n_resize(firesmoke, motion_detect)
            # boxes, firesmoke_corp_np_list = self.expend_box_n_padding_zero(firesmoke, motion_detect)

            detection_result = [[],[],[]]
            motion_inference = None


            if len(firesmoke_corp_np_list) > 0:
                motion_inference = self.classify._inference(firesmoke_corp_np_list)

            if ch in detection_firesmoke:
                detection_result = detection_firesmoke[ch]

            # motion 및 detection 없으면 skip
            if motion_inference is None and len(motion_detect) == 0:
                sc.set_out_by_ch(self.va_type, ch, [[], [], []])
                continue

            # falldown class id 만 추출하여 response 정보 생성
            # response format : boxes, score, class
            sc.set_out_by_ch(self.va_type, ch, self.aggregate_classify_result(boxes, motion_inference, detection_result, self.estimator[ch]))

        return sc


    def aggregate_result(self, inference):
        boxes, scores, classes = inference
        # valid = [idx for idx, score in enumerate(scores) if score > self.min_score_threshold]
        # for detection c5
        valid = [idx for idx, (score, clas) in enumerate(zip(scores, classes)) if score > self.min_score_threshold and clas > 1]
        if len(valid) > 0:
            valid_scores = scores[valid].tolist()
            valid_boxes  = boxes[valid].tolist()
            valid_class = [self.label_map[int(a_class)] for a_class in classes[valid]]
            return [valid_boxes, valid_scores, valid_class]
        else: # invalid image
            return [[],[],[]]

    def aggregate_classify_result(self, boxes, inf_result, detection_result, e):
        detects = []
        canditate = []

        res_boxes = []
        res_scores = []
        res_classes = []

        if inf_result is not None:
            for box, logits in zip(boxes, inf_result):
                prob = logits[0:]
                sorted_inds = [i[0] for i in sorted(enumerate(-prob), key=lambda x: x[1])]
                if sorted_inds[0] > 0 :   # 1: fire, 2: smoke
                    # response format : boxes, score, class
                    res_boxes.append(box)
                    res_scores.append(prob[sorted_inds[0]])
                    res_classes.append(self.label_map[1])
                    canditate.append(box)
                else:
                    detects.append(box)

        # detection 결과가 있는 경우
        d_boxes = []
        d_scores = []
        d_classes = []
        if len(detection_result[0]) > 0:
            for d_box, d_score, d_class in zip(*detection_result):
                d_boxes.append(d_box)
                d_scores.append(d_score)
                d_classes.append(d_class)
                canditate.append(d_box)

                # find_flag = False
                # # motion classification 대상에 detection area 존재 여부
                # for m_box in canditate:
                #     # if e.bb_intersection_over_union(m_box, d_box) > 0:
                #     if e.bb_intersection_over_union(d_box, m_box) > 0 :
                #         find_flag = True
                #         break
                # # motion iou에 인접하지 않은 detection 인 경우
                # if not find_flag:
                #     d_boxes.append(d_box)
                #     d_scores.append(d_score)
                #     d_classes.append(d_class)
                #     canditate.append(d_box)

        find_conditions = e.estimate(detects, canditate)

        f_boxes = []
        f_scores = []
        f_classes = []

        # motion detection box취합
        for fd_box in find_conditions:
            find_flag = False
            for f_box, f_score, f_classe in zip(res_boxes, res_scores, res_classes):
                if np.array_equal(fd_box,f_box):
                    f_boxes.append(f_box)
                    f_scores.append(f_score)
                    f_classes.append(f_classe)
                    find_flag = True
                    break

            if not find_flag:
                f_boxes.append(fd_box)
                f_scores.append(0.7)
                f_classes.append(self.label_map[1])

        # object detect detection box취합
        # for fd_box in find_conditions:
        #     for d_box, d_score, d_classe in zip(d_boxes, d_scores, d_classes):
        #         if np.array_equal(fd_box,d_box):
        #             f_boxes.append(d_box)
        #             f_scores.append(d_score)
        #             f_classes.append(d_classe)
        #             break

        return [f_boxes, f_scores, f_classes]

    def expend_box_n_resize(self, image_np, detects):

        fall_down_crop_list = list()

        boxes, scores, classes = detects
        for idx in range(len(boxes)):
            box_t = tuple(boxes[idx])
            crop, box = self.__crop_expend_ares(image_np, box_t, 0.1)
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
