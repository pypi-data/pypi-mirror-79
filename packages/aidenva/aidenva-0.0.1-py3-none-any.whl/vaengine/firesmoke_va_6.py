import logging
import cv2
import numpy as np

from service.va_service import VAService

from models.classify import Classify
from misc import labelmap_util
from misc.firesmoke_detector_v4 import FiresmokeDetector
from misc.estimator.condition_estimate import ConditionEstimator
from misc.estimator.action_estimate import ActionFrameEstimate

tracelogger = logging.getLogger('trace')

# motion으로 탐지된 최대 box 개수
MOTION_MAX_NUM = 30
# num of classification batch size
CLASSIFICATION_IMG_SIZE = 20
CROP_EXPEND_RATIO = 0.5


class FiresmokeVA(VAService):
    def __init__(self, config, va_type, min_threshold=0.5):
        super().__init__(config, va_type)
        self.classify_shape = 299
        self.action_classify_shape = 224

        self.classify = Classify(self.enabled, config, 'firesmoke', in_shape=(self.classify_shape, self.classify_shape))
        self.action_classify = Classify(self.enabled, config, 'firesmoke_action', in_shape=(16, self.action_classify_shape, self.action_classify_shape))
        self.min_score_threshold = config.getvalue(self.conf_prefix + 'min_score_threshold', min_threshold)

        self.reload_conf = config.getbool(self.conf_prefix + 'reload_conf')

        self.motion = {}
        self.estimator = {}
        self.action = {}

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
        for _, image, ch_id, cfg_json in image_by_ch:
            if ch_id not in self.motion:
                self.motion[ch_id] = FiresmokeDetector(ch_id, self.reload_conf)
            if ch_id not in self.estimator:
                self.estimator[ch_id] = ConditionEstimator(image.shape[:2],
                                                             self.config.getvalue(self.conf_prefix + 'queue_size'),
                                                             self.config.getvalue(self.conf_prefix + 'activation_per_queue'),
                                                             self.config.getvalue(self.conf_prefix + 'iou_threshold'))
            if ch_id not in self.action:
                self.action[ch_id] = ActionFrameEstimate()

            motion_inference.append(self.motion[ch_id].run_single_image(image, cfg_json))

        # for debug
        debug_dict = {}
        for (_, _, ch_id, cfg_json), inference in zip (image_by_ch, motion_inference):
            if self.motion[ch_id].debug:
                if inference is not None:
                    debug_dict[ch_id] = [inference, [1 for i in range(len(inference))], ['fire' for i in range(len(inference))]]

        motion_firesmoke = {}

        for (_, image_np, ch_id, cfg_json), inference in zip (image_by_ch, motion_inference):
            # preset 또는 화면 변화 시 근접인 경우 detection 으로 처리
            if inference is None:
                motion_firesmoke[ch_id] = [[], [], []]
            else:
                # motion 개수가 많은 경우 제외
                if len(inference) > MOTION_MAX_NUM :
                    motion_firesmoke[ch_id] = [[], [], []]
                else :
                    motion_firesmoke[ch_id] = [inference, [1 for i in range(len(inference))], ['fire' for i in range(len(inference))]]

        crop_img_np = []
        crop_box_np = []
        inf_results = []
        crop_per_channels = {}

        for (_, firesmoke, ch_id, cfg_json) in image_by_ch:
            # motion detection box를 이용하여 classification
            motion_detect = motion_firesmoke[ch_id]
            b, _, _ = motion_detect
            self.action[ch_id].add_frame(firesmoke, b)
            boxes, firesmoke_corp_np_list = self.expend_box_n_resize(firesmoke, motion_detect, self.classify_shape)
            if len(firesmoke_corp_np_list) > 0 :
                crop_img_np.extend(firesmoke_corp_np_list)
                crop_box_np.extend(boxes)
            crop_per_channels[ch_id] = len(firesmoke_corp_np_list)

        if len(crop_img_np) > 0 :
            if len(crop_img_np) < CLASSIFICATION_IMG_SIZE:
                inf_results.extend(self.classify._inference(crop_img_np))
            else:
                for i in range(0, len(crop_img_np), CLASSIFICATION_IMG_SIZE):
                    c = crop_img_np[i: i + CLASSIFICATION_IMG_SIZE]
                    inf_results.extend(self.classify._inference(c))

        idx = 0
        # motion 및 detection 없으면 skip
        for (seq, firesmoke, ch_id, cfg_json) in image_by_ch:
            num = crop_per_channels[ch_id]
            if num == 0:
                sc.set_out_by_ch(self.va_type, seq, [[], [], []])
                continue

            # falldown class id 만 추출하여 response 정보 생성
            # response format : boxes, score, class
            if ch_id in debug_dict:
                r = self.aggregate_classify_result(crop_box_np[idx:idx+num], inf_results[idx:idx+num], self.estimator[ch_id])
                r[0] = r[0] + debug_dict[ch_id][0]
                r[1] = r[1] + debug_dict[ch_id][1]
                r[2] = r[2] + debug_dict[ch_id][2]
                sc.set_out_by_ch(self.va_type, seq, r)
            else:
                # tracelogger.debug('slice ch %d : %d, %d', ch, idx, idx+num)
                sc.set_out_by_ch(self.va_type, seq, self.fire_action(self.aggregate_classify_result(crop_box_np[idx:idx+num], inf_results[idx:idx+num], self.estimator[ch_id]), self.action[ch_id]))
            idx = idx + num
        return sc

    def fire_action(self, target, action):
        action_resulit = [[],[],[]]

        for box, score, classes in zip(*target):
            action_frame = []
            frames = action.frames()
            if len(frames) == 16:
                crop_frame = []
                box_t = tuple(box)
                for idx, f in enumerate(frames):
                    crop, _ = self.__crop_expend_ares(f, box_t, 1.8)
                    crop = cv2.resize(crop, (self.action_classify_shape, self.action_classify_shape))
                    crop_frame.append(crop)
                action_frame.append(np.stack(crop_frame, 0))
                logits = self.action_classify._inference(action_frame)

                for i, l in enumerate(logits):
                    prob = l[0:]
                    sorted_inds = [i[0] for i in sorted(enumerate(-prob), key=lambda x: x[1])]
                    # print(' ====> idx %d, score %.2f, FireSmoke score %.2f  2: %d-%.2f, 3: %d-%.2f' % (sorted_inds[0], prob[sorted_inds[0]] * 100, prob[101]* 100, sorted_inds[1], prob[sorted_inds[1]] * 100, sorted_inds[2], prob[sorted_inds[2]] * 100))
                    if sorted_inds[0] == 101 and ( prob[sorted_inds[0]] * 100 > 50):
                        action_resulit[0].append(box)
                        action_resulit[1].append(score)
                        action_resulit[2].append(classes)

        return action_resulit

    def aggregate_classify_result(self, boxes, inf_result, e):
        detects = []
        canditate = []

        res_boxes = []
        res_scores = []
        res_classes = []


        if inf_result is not None:
            for box, logits in zip(boxes, inf_result):
                prob = logits[0:]
                sorted_inds = [i[0] for i in sorted(enumerate(-prob), key=lambda x: x[1])]

                # if sorted_inds[0] < 2 and prob[sorted_inds[0]] > self.min_score_threshold:   # 0: fire, 1: smoke, 2: unknown
                if sorted_inds[0] > 0 and prob[sorted_inds[0]] > self.min_score_threshold:   # 0: unknown, 1: fire, 2: smoke
                    # response format : boxes, score, class
                    res_boxes.append(box)
                    res_scores.append(prob[sorted_inds[0]])
                    res_classes.append(self.label_map[1])
                    canditate.append(box)
                else:
                    detects.append(box)

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

        return [f_boxes, f_scores, f_classes]

    def expend_box_n_resize(self, image_np, detects, shape, ratio=CROP_EXPEND_RATIO):

        crop_list = []

        boxes, scores, classes = detects
        for idx in range(len(boxes)):
            box_t = tuple(boxes[idx])
            crop, box = self.__crop_expend_ares(image_np, box_t, ratio)
            crop = cv2.resize(crop, (shape, shape))
            crop_list.append(crop)

        return boxes, crop_list


    def __crop_expend_ares(self, image_np, box, ratio=0, coordiante=True):
        im_height, im_width = image_np.shape[:2]
        ymin, xmin, ymax, xmax = box

        if (coordiante):
            (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                          ymin * im_height, ymax * im_height)
        else:
            (left, right, top, bottom) = (xmin, xmax, ymin, ymax)

        if ratio > 0:
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
