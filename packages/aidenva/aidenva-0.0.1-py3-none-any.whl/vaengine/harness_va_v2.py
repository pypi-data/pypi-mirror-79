from models.classify import Classify
from service import constants as const
from service.va_service import VAService
import cv2
import numpy as np
import time
import logging
import misc.detection_utils  as utils
from collections import deque

tracelogger = logging.getLogger('trace')
systemlogger = logging.getLogger('system')


class DetectHelper:
    bufferSize=10
    detectionFrame = 10
    maxKeepTime = 60
    maxTrackingCount = 20
    detectionResultBuffer = [None] * bufferSize
    queuelist = [None] * maxTrackingCount
    traker = [None] * maxTrackingCount
    ch_id=1
    maxlen = 5

    def __init__(self, ch_id,channel_count=1):
        self.ch_id=ch_id
        self.detectionFrame=channel_count

    def findRectUUID(self,  count,   currentResultBoxes):
        isNew = False
        position = int((count / self.detectionFrame)) % self.bufferSize
        beforePosition = position - 1 if position != 0 else len(self.detectionResultBuffer) - 1

        newResult = []
        op = []
        for n in range(len(currentResultBoxes)):

            (currentBox) = currentResultBoxes[n]
            newResult.append((0, currentBox))

            if beforePosition == -1 or self.detectionResultBuffer[beforePosition] == None:
                isNew = True
            else:
                beforeResult = self.detectionResultBuffer[beforePosition]
                iouResult = []
                # 이전결과에서 찾음

                for k in range(len(self.detectionResultBuffer)):
                    cc=0
                    if beforeResult ==None:
                        continue
                    for gg in range(len(beforeResult)):
                        (__order, __box) = beforeResult[gg]
                        if __order != -1 and __order not in op:
                            iouResult.append(utils.getIou(__box, currentBox))
                            cc=cc+1
                        else:
                            iouResult.append(0)
                    if cc!=0:
                        break
                    else:
                        iouResult = []
                        beforePosition = beforePosition - 1 if beforePosition != 0 else len(self.detectionResultBuffer) - 1
                        beforeResult = self.detectionResultBuffer[beforePosition]


                if (len(iouResult) > 0):
                    iii = np.argmax(iouResult)
                    if (iouResult[iii] > 0):
                        (____order, ____box) = beforeResult[iii]
                        op.append(____order)
                        newResult[n] = (____order, currentBox)
                        continue
                    else:
                        isNew = True

            # 신규 할당
            if (isNew):

                _order = -1
                if len(self.traker) == 0:
                    _order = 0

                for kk in range(len(self.traker)):
                    if (self.traker[kk] == None or time.time() - self.traker[kk] > self.maxKeepTime):
                        _order = kk
                        break
                    elif kk == len(self.traker) - 1 and len(self.traker) < self.maxTrackingCount:
                        _order = kk + 1
                        break

                if (self.traker != None and len(self.traker) > 0 and _order == -1):
                    _order = np.argmin(self.traker)
                self.traker[_order] = time.time()
                # currentResultBoxes[n]=(_order,currentBox)
                newResult[n] = (_order, currentBox)
                self.queuelist[_order]=None
        self.detectionResultBuffer[position] = newResult
        return newResult

    def getSoftMaxInQueue(self,results, _order):
        _queue = self.queuelist[_order]
        if _queue == None:
            _queue = deque(maxlen=self.maxlen)
        _queue.append(results)
        self.queuelist[_order] = _queue

        sum = [0, 0]
        for q in _queue:
            sum = sum + q

        totalSum = 0
        for k in sum:
            totalSum = totalSum + k

        return sum / totalSum


class HarnessVA(VAService):
    INPUT_IMAGE_SIZE=(299,299)
    SCORE_THRESHOLD = 0.7 # 수치가 높을수록 negative가 적게나옴
    # CROP_COUNT=3
    # CROP_BOX_DIFF_RATE = 0.2
    # CROP_COUNT=3
    # CROP_BOX_DIFF_RATE = 0.13

    CROP_COUNT=5
    CROP_BOX_DIFF_RATE = 0.09
    CLASSIFICATION_BATCH_SIZE=20
    BATCH_BY_CHANNEL=True
    USE_ORIGIN_BOX=True
    DEBUG_MODE=False
    USE_QUEUE=True
    count = 0
    last = ()
    CHANNEL_COUNT=1
    def __init__(self, config, va_type):
        super(HarnessVA, self).__init__(config, va_type)
        self.INPUT_IMAGE_SIZE =eval( config.getvalue('va_engines.models.harness.'+ 'classification_image_size', self.INPUT_IMAGE_SIZE))
        self.CROP_COUNT = ( config.getvalue('va_engines.models.harness.'+ 'crop_count', 3))
        self.CROP_BOX_DIFF_RATE = ( config.getvalue('va_engines.models.harness.'+ 'crop_box_diff_rate', 0.13))
        self.USE_QUEUE = ( config.getvalue('va_engines.models.harness.'+ 'use_queue', True))
        self.classify = Classify(self.enabled, config, 'harness',in_shape=self.INPUT_IMAGE_SIZE)
        tracelogger.debug('self.CROP_COUNT :[%.2s] ' ,self.CROP_COUNT)
    def _set_lables(self, path_to_labels):
        label_file = open(path_to_labels, 'r')
        lines = label_file.readlines()
        return [str(w).replace("\n", "") for w in lines]


    # override

    helper_dic={}

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
        for n, row in enumerate(images_by_ch):
            ch =  (row[0])
            image = row[1]

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
        # for n,(ch, image, _) in enumerate(images_by_ch):
        for n, row in enumerate(images_by_ch):
            ch=row[0]
            image = row[1]
            ch_id = str(row[2])
            detect = detect_by_ch[ch]
            helper=self.helper_dic.get(ch_id)
            if helper is None:
                helper=DetectHelper(ch_id)
                self.helper_dic[ch_id]=helper

            boxes, scores, classes = detect

            if len(boxes) == 0:
                sc.set_out_by_ch(self.va_type, ch, [[], [], []])
                continue

            if self.USE_QUEUE:
                currentResultUuid=helper.findRectUUID(self.count,boxes)


            inf_result=total_inf_result[lastPosition:lastPosition+(len(boxes)*self.CROP_COUNT)]
            lastPosition=lastPosition+(len(boxes)*self.CROP_COUNT)

            new_inf_result=[]
            for n in range(0,len(inf_result),self.CROP_COUNT):
                sum= 0
                for k in range(self.CROP_COUNT):
                    sum  =sum+ inf_result[n+k]
                sum=sum/self.CROP_COUNT
                if self.USE_QUEUE:
                    _order=currentResultUuid[int(n/self.CROP_COUNT)][0]
                    # print('_order >>' , _order)
                    sum=helper.getSoftMaxInQueue(sum,_order)
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

                if self.DEBUG_MODE:
                    cv2.rectangle(image,(tlx1,tly1),(brx1,bry1),(255,0,255),2)


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



