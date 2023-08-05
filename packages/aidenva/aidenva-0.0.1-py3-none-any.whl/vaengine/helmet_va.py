import cv2

from models.classify import Classify
from service import constants as const
from service.va_service import VAService
import time
import misc.detection_utils  as utils
import logging


tracelogger = logging.getLogger('trace')
systemlogger = logging.getLogger('system')

class HelmetVA(VAService):
    INPUT_SHARP = (299, 299)

    SCORE_THRESHOLD = 0.5
    CLASSIFICATION_BATCH_SIZE = 8
    BATCH_BY_CHANNEL = True
    DEBUG_MODE = False
    count = -1

    def __init__(self, config, va_type):
        super(HelmetVA, self).__init__(config, va_type)
        self.classify = Classify(self.enabled, config, 'helmet')
        self.default_image_size = 299

    def _set_lables(self, path_to_labels):
        label_file = open(path_to_labels, 'r')
        lines = label_file.readlines()
        return [str(w).replace("\n", "") for w in lines]

    # override

    def _execute(self, sc):
        self.count += 1

        t1 = time.time()
        # channel 순서를 가지고 있는 image numpy
        images_by_ch = sc.get_in_by_vatype(self.is_support_vatype_fc)
        # 처리할 정보가 없는 경우 return
        if len(images_by_ch) == 0: return sc
        # person detection 결과 (channel 순서로 detection 저장 )
        detect_by_ch = sc.get_out_by_vatype(const.DETECT_VA)

        corp_np_list = []
        total_inf_result = []

        # [START] classification *********************************************************************
        # crop image를 batch 사이즈 만큼 모아서 classification
        for (ch, image, _, cfg_json) in images_by_ch:

            detect = detect_by_ch[ch]
            boxes, scores, classes = detect
            #print(boxes)
            self.createCropImages(self.count, image, boxes, corp_np_list)
           # print(len(corp_np_list))
            if (self.BATCH_BY_CHANNEL == True and len(corp_np_list) > 0) or len(
                    corp_np_list) > self.CLASSIFICATION_BATCH_SIZE:
                total_inf_result.extend(self.classify._inference(corp_np_list))
                corp_np_list = []

        if len(corp_np_list) > 0:
            total_inf_result.extend(self.classify._inference(corp_np_list))
       # print(total_inf_result)
        # [END] classification *********************************************************************

        # get classification result by ch and make result
        # lastPosition = 0
        for n, (ch, image, _, cfg_json) in enumerate(images_by_ch):
            detect = detect_by_ch[ch]
            boxes, scores, classes = detect

            if len(boxes) == 0:
                sc.set_out_by_ch(self.va_type, ch, [[], [], []])
                continue

            if self.DEBUG_MODE:
                clone = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                utils.drawResult(clone, ch, boxes, [k[1] for k in total_inf_result], score_threthold=self.SCORE_THRESHOLD)
            # response format : boxes, score, class
            sc.set_out_by_ch(self.va_type, ch, self.aggregte_result(boxes, total_inf_result))
            #print(new_inf_result)
        if self.count > 10000000:
            self.count = -1
        tracelogger.debug('HelmetVA elapse time :[%.2f] ', (time.time() - t1))
        return sc;


    def createCropImages(self,_count,image,boxes,inputlist):
        height, width = image.shape[:2]


        for box in boxes:
            tlx = int(box[1] * width)
            tly = int(box[0] * height)
            brx = int(box[3] * width)
            bry = int(box[2] * height)

            _width = brx - tlx
            _height = bry - tly

            # inputlist.append(cv2.resize(image[tly:int(bry), tlx:brx], self.INPUT_SHARP)/ 255)
            inputlist.append(self.__resize_and_padding_zero(image[tly:int(bry), tlx:brx]) / 255)
    '''
        return :  response format : [boxes, score, class]
    '''

    def aggregte_result(self, boxes, inf_result):
        res_boxes = []
        res_scores = []
        res_classes = []

        for box, logits in zip(boxes, inf_result):
            score = logits[1]
            if score > self.SCORE_THRESHOLD:  # 안했을 확률
                # response format : boxes, score, class
                res_boxes.append(box)
                res_scores.append(score)
                res_classes.append('helmet')

        return [res_boxes, res_scores, res_classes]

    def expend_box_n_padding_zero(self, image_np, person_detect):

        fall_down_crop_list = list()

        boxes, scores, classes = person_detect
        for idx in range(len(boxes)):
            box_t = tuple(boxes[idx])
            crop, box = self.__crop_expend_ares(image_np, box_t)
            crop = self.__resize_and_padding_zero(crop, self.default_image_size)
            fall_down_crop_list.append(crop)

        return boxes, fall_down_crop_list

    '''
          bound ract를 image size에 맞게 구성 및 여백은 zero padding
      '''

    def __resize_and_padding_zero(self, image, desired_size=299):
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
