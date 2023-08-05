from models.classify import Classify
from service import constants as const
from service.va_service import VAService
import cv2
import numpy as np
import time
import logging
from misc import debug
import misc.detection_utils  as utils

tracelogger = logging.getLogger('trace')
systemlogger = logging.getLogger('system')
class HarnessVA(VAService):
    INPUT_IMAGE_SIZE=(299,299)
    SCORE_THRESHOLD = 0.6
    # CROP_COUNT=3
    # CROP_BOX_DIFF_RATE = 0.2
    CROP_COUNT=3
    CROP_BOX_DIFF_RATE = 0.15
    CLASSIFICATION_BATCH_SIZE=20
    BATCH_BY_CHANNEL=True
    USE_ORIGIN_BOX=True
    DEBUG_MODE=False
    count = -1
    def __init__(self, config, va_type):
        super(HarnessVA, self).__init__(config, va_type)
        self.classify = Classify(self.enabled, config, 'harness',in_shape=self.INPUT_IMAGE_SIZE)

    def _set_lables(self, path_to_labels):
        label_file = open(path_to_labels, 'r')
        lines = label_file.readlines()
        return [str(w).replace("\n", "") for w in lines]

  # override

    def _execute(self, sc):
        self.count += 1

        t1=time.time()
        # channel 순서를 가지고 있는 image numpy
        images_by_ch = sc.get_in_by_vatype(self.is_support_vatype_fc)
        # 처리할 정보가 없는 경우 return
        if len(images_by_ch) == 0: return sc
        # person detection 결과 (channel 순서로 detection 저장 )
        detect_by_ch = sc.get_out_by_vatype(const.DETECT_VA)

        corp_np_list=[]
        total_inf_result=[]


        #[START] classification *********************************************************************
        #crop image를 batch 사이즈 만큼 모아서 classification
        for (ch, image, _, cfg_json) in images_by_ch:
            detect = detect_by_ch[ch]
            boxes, scores, classes = detect

            self.createCropImages( self.count,image,boxes,self.CROP_BOX_DIFF_RATE,self.CROP_COUNT,corp_np_list,useOriginBox=self.USE_ORIGIN_BOX)

            if (self.BATCH_BY_CHANNEL==True and len(corp_np_list)>0) or len(corp_np_list)>self.CLASSIFICATION_BATCH_SIZE:
                total_inf_result.extend( self.classify._inference(corp_np_list))
                corp_np_list=[]

        if len(corp_np_list)>0:
            total_inf_result.extend( self.classify._inference(corp_np_list))
        #[END] classification *********************************************************************

        # get classification result by ch and make result
        lastPosition=0
        for n,(ch, image, _, cfg_json) in enumerate(images_by_ch):
            detect = detect_by_ch[ch]
            boxes, scores, classes = detect

            if len(boxes) == 0:
                sc.set_out_by_ch(self.va_type, ch, [[], [], []])
                continue

            inf_result=total_inf_result[lastPosition:lastPosition+(len(boxes)*self.CROP_COUNT)]
            lastPosition=lastPosition+(len(boxes)*self.CROP_COUNT)

            new_inf_result=[]
            for n in range(0,len(inf_result),self.CROP_COUNT):
                sum= 0
                for k in range(self.CROP_COUNT):
                    sum  =sum+ inf_result[n+k]
                sum=sum/self.CROP_COUNT
                new_inf_result.append(sum)

            if self.DEBUG_MODE:
                clone=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                utils.drawResult(clone,ch,boxes, [k[0] for k in  new_inf_result], score_threthold=self.SCORE_THRESHOLD)
            # response format : boxes, score, class
            sc.set_out_by_ch(self.va_type, ch, self.aggregte_result(boxes, new_inf_result))

        if self.count>10000000:
            self.count=-1
        tracelogger.debug('HarnessVA elapse time :[%.2f] ' ,(time.time()-t1))
        return sc;

    '''
        return :  response format : [boxes, score, class]
    '''

    def createCropImages(self,_count,image,boxes,diffRate,totalBoxCount,inputlist,useOriginBox=False,):
        height, width = image.shape[:2]

        for box in boxes:
            tlx = int(box[1] * width)
            tly = int(box[0] * height)
            brx = int(box[3] * width)
            bry = int(box[2] * height)

            _width = brx - tlx
            _height = bry - tly

            difInit = int(_height * diffRate)
            if (_height < _width):
                difInit = int(_width * diffRate)

            for n in range(totalBoxCount):
                difX = int(difInit * (n if useOriginBox==False else n+1))
                if (n % 2 + _count % 2) % 2 == 0:
                    tlx1 = tlx - difX if tlx - difX > 0 else 0
                    brx1 = brx + int(difX / 3) if brx + int(difX / 3) < width else width
                else:
                    tlx1 = tlx - int(difX / 3) if tlx - int(difX / 3) > 0 else 0
                    brx1 = brx + difX if brx + difX < width else width

                tly1 = tly - int(difX / 2) if tly - int(difX / 2) > 0 else 0
                bry1 = bry + int(difX / 3) if bry + int(difX / 3) > 0 else height
                inputlist.append(cv2.resize(image[tly1:bry1, tlx1:brx1], self.INPUT_IMAGE_SIZE)/ 255)



    def aggregte_result(self, boxes, inf_result):
        res_boxes = []
        res_scores = []
        res_classes = []

        for box, logits in zip(boxes, inf_result):
            score=logits[0]
            if score>self.SCORE_THRESHOLD :   # 안했을 확률
                # response format : boxes, score, class
                res_boxes.append(box)
                res_scores.append(score)
                res_classes.append('harness')

        return [res_boxes, res_scores, res_classes]

    def expend_box_n_padding_zero(self, image_np, person_detect):

        person_crop_list = list()
        height, width = image_np.shape[:2]
        boxes, scores, classes = person_detect
        for idx in range(len(boxes)):
            box_t = tuple(boxes[idx])
            tlx = int(box_t[1] * width)
            tly = int(box_t[0] * height)
            brx = int(box_t[3] * width)
            bry = int(box_t[2] * height)
            # crop = self.__resize_and_padding_zero(crop, self.default_image_size)
            person_crop_list.append(cv2.resize(image_np[tly:bry, tlx:brx], self.INPUT_IMAGE_SIZE)/ 255)

        return boxes, person_crop_list

    def expend_box_n_padding_zero2(self, image_np, person_detect):

        person_crop_list = list()
        height, width = image_np.shape[:2]
        boxes, scores, classes = person_detect
        for idx in range(len(boxes)):
            box_t = tuple(boxes[idx])
            tlx = int(box_t[1] * width)
            tly = int(box_t[0] * height)
            brx = int(box_t[3] * width)
            bry = int(box_t[2] * height)

            person_crop_list.append(cv2.resize(image_np[tly:bry, tlx:brx], self.INPUT_IMAGE_SIZE)/ 255)

        return person_crop_list



    def _execute_bak(self, sc):
        self.count += 1

        t1=time.time()
        # channel 순서를 가지고 있는 image numpy
        images_by_ch = sc.get_in_by_vatype(self.is_support_vatype_fc)
        # 처리할 정보가 없는 경우 return
        if len(images_by_ch) == 0: return sc
        # person detection 결과 (channel 순서로 detection 저장 )
        detect_by_ch = sc.get_out_by_vatype(const.DETECT_VA)


        for (ch, image, _, cfg_json) in images_by_ch:
            detect = detect_by_ch[ch]

            boxes, scores, classes = detect

            # person 없으면 깡통list 추가
            if len(boxes) == 0:
                sc.set_out_by_ch(self.va_type, ch, [[], [], []])
                continue
            corp_np_list=[]
            self.createCropImages( self.count,image,boxes,self.CROP_BOX_DIFF_RATE,self.CROP_COUNT,corp_np_list)

            inf_result = self.classify._inference(corp_np_list)

            new_inf_result=[]

            for n in range(0,len(inf_result),self.CROP_COUNT):
                sum= 0
                for k in range(self.CROP_COUNT):
                    sum  =sum+ inf_result[n+k]
                sum=sum/self.CROP_COUNT
                new_inf_result.append(sum)


            print('score: ',sum[0],'>>>>>>>>>>>>>>>' , inf_result[n][0])
            # response format : boxes, score, class

            sc.set_out_by_ch(self.va_type, ch, self.aggregte_result(boxes, new_inf_result))


        tracelogger.debug('HarnessVA elapse time :[%.2f] ' ,(time.time()-t1))
        return sc;