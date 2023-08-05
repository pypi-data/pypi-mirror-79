import cv2

from misc import labelmap_util
from models.classify import Classify
from service import constants as const
from service.va_service import VAService


class FalldownVA(VAService):
    def __init__(self, config, va_type):
        super(FalldownVA, self).__init__(config, va_type)
        self.default_image_size = 299   # inception_resnet_v2 : 233
        self.classify = Classify(self.enabled, config, 'falldown', (self.default_image_size, self.default_image_size))

    def _set_lables(self, path_to_labels):
        labels = labelmap_util.create_categories_from_labelmap(path_to_labels)
        return dict([(item['id'] + -1, item['name']) for item in labels])

    # override
    def _execute(self, sc):
        # channel 순서를 가지고 있는 image numpy
        # list -> [ch_idx, image]
        images_by_ch = sc.get_in_by_vatype(self.is_support_vatype_fc)
        # 처리할 정보가 없는 경우 return
        if len(images_by_ch) == 0: return sc

        # person detection 결과 (channel 순서로 detection 저장 )
        detect_by_ch = sc.get_out_by_vatype(const.DETECT_VA)

        for (ch, falldown, _, cfg_json) in images_by_ch:
            detect = detect_by_ch[ch]
            boxes, fall_down_corp_np_list = self.expend_box_n_padding_zero(falldown, detect)

            # falldown이 없으면 깡통list 추가
            if len(fall_down_corp_np_list) == 0:
                sc.set_out_by_ch(self.va_type, ch, [[], [], []])
                continue

            # debug.show_images(fall_down_corp_np_list)
            inf_result = self.classify._inference(fall_down_corp_np_list)

            # falldown class id 만 추출하여 response 정보 생성
            # response format : boxes, score, class
            sc.set_out_by_ch(self.va_type, ch, self.aggregte_result(boxes, inf_result))

        return sc;

    '''
        return :  response format : [boxes, score, class]
    '''
    def aggregte_result(self, boxes, inf_result):
        res_boxes = []
        res_scores = []
        res_classes = []

        for box, logits in zip(boxes, inf_result):
            prob = logits[0:]
            sorted_inds = [i[0] for i in sorted(enumerate(-prob), key=lambda x: x[1])]
            if sorted_inds[0] == 1 :   # falldown
                # response format : boxes, score, class
                res_boxes.append(box)
                res_scores.append(prob[sorted_inds[0]])
                res_classes.append(self.label_map[1])

        return [res_boxes, res_scores, res_classes]

    def expend_box_n_padding_zero(self, image_np, person_detect):

        fall_down_crop_list = list()

        boxes, scores, classes = person_detect
        for idx in range(len(boxes)):
            box_t = tuple(boxes[idx])
            crop, box = self.__crop_expend_ares(image_np, box_t, 0.1)
            crop = self.__resize_and_padding_zero(crop, self.default_image_size)
            fall_down_crop_list.append(crop)

        return boxes, fall_down_crop_list

    '''
        bound ract를 image size에 맞게 구성 및 여백은 zero padding
    '''
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

    '''
        입력되는 rect 에 비율에 맞게 확장/축소 
    '''
    def __crop_expend_ares(self, image_np, box, ratio=0.2, coordiante=True):
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