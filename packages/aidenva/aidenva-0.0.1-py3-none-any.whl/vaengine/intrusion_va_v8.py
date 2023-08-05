import logging
import random
import math
import cv2
import statistics
from service import constants as const
from service.va_service import VAService
from models.objectdetect import ObjectDetect
import misc.detection_utils  as utils
import numpy as np
import time
import os
from collections import deque

tracelogger = logging.getLogger('trace')
systemlogger = logging.getLogger('system')
from models.classify import Classify
from misc import labelmap_util
from misc.MotionDetection_v2 import MotionDetection


category = {1: {'id': 1, 'name': 'person'}, 2: {'id': 2, 'name': 'car'}, 3: {'id': 3, 'name': 'bicycle'}, 4: {'id': 4, 'name': 'motorcycle'}}
class IntrusionVA(VAService):
    MAX_CHANNEL_COUNT = 30
    SCORE_THRESHOLD = 0.3
    SCORE_THRESHOLD_SUB = 0.3
    DIFF_THRESHOLD = 0.03  # 이하값이면 움직임이 전혀없는것으로 간주

    USE_BGS = True
    MAX_TRACKING_OBJECT = 5
    MAX_TRACKING_FRAME = 10
    USE_TRACKING = True
    INPUT_SHAPE = (1280, 720)
    USE_ENHANCECONTRAST = True
    CLISSIFICATION_SIZE = (233, 233)
    DETECTION_MAX_WIDTH_RATE=0.4
    SKIP_DETECTION=True
    SKIP_BG=False
    SKIP_FRAME_RATE=2

    count = -1
    trackingCount = 0
    previousGrayFrames = dict([])
    previousFrames = dict([])
    previousMerged = dict([])
    trackingConsecutiveUseCounts = dict([])  # tracking 연속 사용 횟수
    lastUseTracking = None
    IS_DEBUG = False
    motionDetection = None

    clsList = ['car', 'others', 'person']
    SAVE_CLASSIFICATION_IMAGE = False

    def __init__(self, config, va_type, min_threshold=0.5):
        super(IntrusionVA, self).__init__(config, va_type)
        self.detector = ObjectDetect(self.enabled, config, 'detect_intrusion', in_shape=self.INPUT_SHAPE)
        self.min_score_threshold = config.getvalue(self.conf_prefix + 'min_score_threshold', min_threshold)
        self.SKIP_BG = config.getvalue(self.conf_prefix + 'skip_bg', self.SKIP_BG)
        self.SKIP_DETECTION = config.getvalue(self.conf_prefix + 'skip_detection', self.SKIP_DETECTION)

        self.CLISSIFICATION_SIZE =eval( config.getvalue('va_engines.models.intrusion.'+ 'classification_image_size', self.CLISSIFICATION_SIZE))
        self.classify = Classify(self.enabled, config, 'intrusion', in_shape= self.CLISSIFICATION_SIZE )
        self.SCORE_THRESHOLD = config.getvalue(self.detector.conf_prefix + 'min_score_threshold',
                                               self.min_score_threshold)
        self.motionDetection = MotionDetection(isDebug=self.IS_DEBUG)


    def _set_lables(self, path_to_labels):
        labels = labelmap_util.create_categories_from_labelmap(path_to_labels)
        return dict([(item['id'], item['name']) for item in labels])

    '''
        get_in_by_vatype_gen() generator examples
    '''

    def useBgSubstraction(self, ch_uuid):
        (diffScore, isImgChange, gray) = self.motionDetection.isChnageImage(ch_uuid, self.DIFF_THRESHOLD)

        if isImgChange == True and self.getMaxDiffValueWhenNotFound(ch_uuid) > diffScore:
            isImgChange=False

        self.previousGrayFrames[ch_uuid] = gray

        if self.trackingConsecutiveUseCounts.get(ch_uuid) is None:
            self.trackingConsecutiveUseCounts[ch_uuid] = 0

            # self.isObjectDetectorEfficient(ch_uuid,threthold=0.65)== False
        if self.USE_TRACKING and (isImgChange == False ) \
                and self.trackingConsecutiveUseCounts.get(ch_uuid) < self.MAX_TRACKING_FRAME \
                and (self.previousMerged.get(ch_uuid) is None or len(
                    self.previousMerged.get(ch_uuid)) <= self.MAX_TRACKING_OBJECT):
            self.trackingConsecutiveUseCounts[ch_uuid] = self.trackingConsecutiveUseCounts[ch_uuid] + 1
            return (diffScore, False)
        else:
            self.trackingConsecutiveUseCounts[ch_uuid] = 0
            return (diffScore, True)


    def isNotDuplicatedBox(self, box2, boxes, classes, scores, iouThreshold=0.15):
        for k1 in range(len(boxes)):
            _box = boxes[k1]
            # if utils.isValidBox(boxes[k1], scores[k1], classes[k1], 1):
            iou = utils.getIou(box2, _box)
            if iou > iouThreshold:
                return False
        return True

    def detectNotFoundBoxesFromTracking3(self, _image, boxes, ch_id,returnTensorType=False):
        ttt=time.time()
        if self.previousMerged.get(ch_id) is None:
            return []

        height, width = _image.shape[:2]
        if type(boxes) is not list:
            boxes = boxes.tolist()

        resultBoxes = []
        cc=0
        for k, __box in enumerate(self.previousMerged[ch_id][0]):
            if True:
                if self.isNotDuplicatedBox(__box, boxes, None, None, iouThreshold=0.5):
                    cc+=1
                    tlx = int(__box[1] * width)
                    tly = int(__box[0] * height)
                    brx = int(__box[3] * width)
                    bry = int(__box[2] * height)

                    boxOffset=1
                    if brx-tlx<boxOffset*2 or bry-tly<boxOffset*2:
                        continue

                    # tracker =cv2.TrackerCSRT_create()
                    tracker = cv2.TrackerMedianFlow_create()
                    # tracker = cv2.TrackerKCF_create()
                    # tracker = cv2.TrackerMOSSE_create()


                    preframeImg=self.previousFrames[ch_id]

                    offsetRate=3
                    cropWidthOffset=int((brx-tlx)*offsetRate)
                    cropHeightOffset=int((bry-tly)*offsetRate)

                    top_y=tly-cropHeightOffset if tly-cropHeightOffset>0 else 0
                    bottom_y=bry+cropHeightOffset if bry+cropHeightOffset<height else height

                    left_x=tlx-cropWidthOffset if tlx-cropWidthOffset>0 else 0
                    right_x=brx+cropWidthOffset if brx+cropWidthOffset<width else width
                    cropImage=preframeImg[top_y:bottom_y, left_x:right_x]  # 이전 박스 주변 이미지만 crop 해서 tracking

                    # boxInPreviousFrame = (tlx-left_x, tly-top_y, (brx - tlx), (bry - tly))  # 이전 Box 좌표변환
                    boxInPreviousFrame = (tlx-left_x+boxOffset, tly-top_y+boxOffset, (brx - tlx)-(2*boxOffset), (bry - tly)-(2*boxOffset))  # 이전 Box 좌표변환
                    tracker.init(cropImage, boxInPreviousFrame)
                    currentFrameCrop=_image[top_y:bottom_y, left_x:right_x]
                    (success, box) = tracker.update(currentFrameCrop)

                    # cropImage2=cropImage.copy()
                    # currentFrameCrop2=currentFrameCrop.copy()
                    if success:
                        (x, y, w, h) = [int(v) for v in box]
                        if w<boxOffset or h<boxOffset or x<0 or y<0:
                            continue
                        (x, y, w, h)=(x+left_x,y+top_y,w,h) # 전체 이미지로 좌표변환

                        if returnTensorType:
                            _box = (float(y / height), float(x / width), float((y + h) / height), float((x + w) / width))
                            resultBoxes.append(_box)
                        else:
                            resultBoxes.append((x, y, w, h))

                        if self.IS_DEBUG:
                            tracelogger.debug(' success detectNotFoundBoxesFromTracking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                            cv2.rectangle(_image, (x, y), (x + w, y + h), (255, 0, 0), 3)

                    else:

                        if self.IS_DEBUG:
                            tracelogger.debug(' fail detectNotFoundBoxesFromTracking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                            cv2.rectangle(_image, (tlx, tly), (brx, bry), (0, 255, 0), 1)
        if cc>0:
            tracelogger.debug('tracking time >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> '+ str(time.time()-ttt)+  ' count :' +str(cc))
        return resultBoxes


    def detectNotFoundBoxesFromTracking2(self, _image, _inference, ch_id, returnTensorType=False):
        (boxes, classes, scores) = _inference
        return self.detectNotFoundBoxesFromTracking3(_image,boxes,ch_id,returnTensorType)


    def mergeBoxesResult(self, _image, _inference, _inference2, checkDup=True, iouThreshold=0.6):
        (boxes, classes, scores) = _inference
        if type(boxes) is not list:
            boxes = boxes.tolist()
            if classes is not None:
                classes = classes.tolist()
                scores = scores.tolist()

        for k, __box in enumerate(_inference2[0]):
            if checkDup == False or self.isNotDuplicatedBox(__box, boxes, classes, scores, iouThreshold=iouThreshold):
                boxes.append(__box)
                if classes is not None:
                    classes.append(_inference2[1][k])
                    scores.append(_inference2[2][k])
                else:
                    classes.append(__box)
                    scores.append(__box)
        return (np.array(boxes), np.array(classes), np.array(scores))

    def filteringInnerBoxes(self, boxes, targetBoxes, interceptionAreaThreshold=0.9,isSelf=False):
        newBoxes = []
        for k, __box in enumerate(boxes):
            if self.checkInnerBoxes(__box, targetBoxes, interceptionAreaThreshold,isSelf,currentIdx=k) == False:
                newBoxes.append(__box)
        # return np.array(newBoxes)
        return newBoxes

    def checkInnerBoxes(self, box, targetBoxes, interceptionAreaThreshold=0.9, isSelf=False,currentIdx=-1):
        area = utils._getArea(box)
        for j,tbox in enumerate(targetBoxes):

            if isSelf:
               if j == currentIdx:
                   continue
            # if area >= utils._getArea(tbox):
            #     continue
            interArea = utils._getIntersectionArea(tbox, box)
            if interArea > int(area * interceptionAreaThreshold):  # interceptionAreaThreshold 이상 겹치면
                return True
        return False

    def doObjectDetection(self, images, _count):

        score = self.SCORE_THRESHOLD
        ___detector = self.detector
        inferences = ___detector._inference(images)
        newInferences = []
        for inf in inferences:
            newInferences.append(self.aggregate_result(inf, score))
        return np.array(newInferences)

    def aggregate_result(self, inference, _score):
        boxes, scores, classes = inference

        valid = [idx for idx, score in enumerate(scores) if score > _score and boxes[idx][3]-boxes[idx][1] < self.DETECTION_MAX_WIDTH_RATE]
        if len(valid) > 0:
            valid_scores = scores[valid].tolist()
            valid_boxes = boxes[valid].tolist()
            valid_class = [self.label_map[int(a_class)] for a_class in classes[valid]]
            return [valid_boxes, valid_scores, valid_class]
        else:  # invalid image
            return [[], [], []]


    OD_DICT={}
    queueMaxlen = 10
    DECTION_SKIP_DICT={}
    def isObjectDetectorEfficient(self,ch_id,threthold=0.3):
        queue=self.OD_DICT.get(ch_id)
        skipDict=self.DECTION_SKIP_DICT.get(ch_id)

        if(queue is None):
            return True

        if(skipDict is None):
            self.DECTION_SKIP_DICT[ch_id]=0
            return True

        if skipDict>=self.MAX_TRACKING_FRAME:
            self.DECTION_SKIP_DICT[ch_id]=0
            return True

        if len(queue) <10 or np.mean(queue)   <threthold:
            self.DECTION_SKIP_DICT[ch_id]=0
            return True
        else:
            self.DECTION_SKIP_DICT[ch_id]=self.DECTION_SKIP_DICT[ch_id]+1
            return False

    def setObjectDetectorEfficiency(self,ch_id,allResultBoxes,detectionBoxes):
        # if tracelogger.isEnabledFor(10):
        #     tracelogger.debug(ch_id +' detection box : ' +str( len(detectionBoxes)) + ' all Boxes : ' +str(len(allResultBoxes)))
        queue=self.OD_DICT.get(ch_id)
        if(queue is None):
            queue = deque(maxlen=self.queueMaxlen)
            self.OD_DICT[ch_id]=queue

        # 검색 건수가 없거나
        if len(allResultBoxes)==0 or (len(allResultBoxes)>0 and len(detectionBoxes)>0) :
            queue.append(0)
        else:
            queue.append(1)


    def convertOpencvbox2Tensorboxes(self, opencvboxes,image):
        height,width=image.shape[:2]
        resultBoxes=[]
        for bb in  opencvboxes:
            (x1, y1, w1, h1) = bb
            _box = (float(y1 / height), float(x1 / width), float((y1 + h1) / height), float((x1 + w1) / width))
            resultBoxes.append(_box)
        return resultBoxes

    def convertTensorboxes2Opencvbox(self,tensorboxes,image):
        _height,_width=image.shape[:2]
        if tensorboxes is None or len(tensorboxes)==0:
            return []
        resultBoxes = [ (int(_box[1] * _width)
                                ,int(_box[0] * _height)
                                ,int((_box[3]-_box[1])*_width)
                                ,int((_box[2]-_box[0])*_height)) for _box in tensorboxes]
        return resultBoxes

    def doClassification(self,image_by_ch,classification_images,movingBoxes_ch):

        bgs_inf_result=[]
        totalBoxSize=len(classification_images)
        MAX_BATCH_SIZE=20
        tmp_total_classification_result=[]
        features=[]
        tmpFeatures=[]
        #classification
        for n in range(0,totalBoxSize,MAX_BATCH_SIZE):
            if n+MAX_BATCH_SIZE<totalBoxSize:
                batch1=classification_images[n :(n+MAX_BATCH_SIZE)]
            else:
                batch1=classification_images[n:totalBoxSize]

            rr4 = self.classify._inference(batch1)
            tmp_total_classification_result.extend(rr4[0])
            tmpFeatures.extend(rr4[1])

        idx=0
        if len(movingBoxes_ch)>0:
            for n,boxes in enumerate(movingBoxes_ch):
                boxesSize=len(boxes)
                if boxesSize==0:
                    bgs_inf_result.append(([],[],[]))
                    continue

                clsResults=tmp_total_classification_result[idx:idx+boxesSize]
                clsFeature=tmpFeatures[idx:idx+boxesSize]
                idx=idx+boxesSize
                _image = image_by_ch[n][1]
                _height,_width=_image.shape[:2]

                bgBoxes=[]
                bgScores=[]
                bgClasses=[]
                chFeature=[]
                for k,box in enumerate(boxes):
                    (x1, y1, w1, h1) = box
                    _box = (float(y1 / _height), float(x1 / _width), float((y1 + h1) / _height), float((x1 + w1) / _width))
                    resultSoftmax=clsResults[k]
                    order = np.argmax(resultSoftmax)
                    score = resultSoftmax[order]
                    className = self.clsList[order]
                    if className != 'others':
                        bgBoxes.append(_box)
                        bgScores.append(score)
                        bgClasses.append(className)
                        chFeature.append(clsFeature[k])
                    if self.IS_DEBUG:
                        cv2.rectangle(_image, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 1)
                        color = (0, 0, 255) if className != 'others' else (255, 255, 0)
                        cv2.putText(_image, className + ":" + str(score)[0:3], (x1, y1 - 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

                bgs_inf_result.append((bgBoxes,bgScores,bgClasses))
                features.append(chFeature)

        return (bgs_inf_result,features)

    DIFF_DICT={}
    def getMaxDiffValueWhenNotFound(self, ch_id):
        queue=self.DIFF_DICT.get(ch_id)
        if(queue is None):
            return 0
        if len(queue)> 10 :
            # print(len(queue) ,' np.mean(queue) ' , np.measn(queue) ,' std ' ,np.std(queue)   , 'var ' ,np.var(queue)  )
            # maxValue=(np.mean(queue )+np.std(queue )*2); # 95%
            maxValue=(np.mean(queue )+np.std(queue )*1.3); # 80%
            # maxValue=(np.mean(queue )+np.std(queue )*1); # 65%
            # if maxValue<self.DIFF_THRESHOLD:
            #     maxValue=np.mean(queue )*0.7
            return maxValue
        else:
            return 0

    def setAvgDiffWhenNotFound(self,diff,ch_id,count):
        queue=self.DIFF_DICT.get(ch_id)
        if(queue is None):
            queue = deque(maxlen=150)
            self.DIFF_DICT[ch_id]=queue

        if diff >150 or count%500==0:
            queue = deque(maxlen=150)
            self.DIFF_DICT[ch_id]=queue

        else:
            queue.append(float(diff if diff<20 else 20))


    def isSkipBG(self,count):
        return self.SKIP_BG and count%self.SKIP_FRAME_RATE!=0

    def isSkipDetection(self,count):
        return self.SKIP_DETECTION and count%self.SKIP_FRAME_RATE!=0

    pq = deque(maxlen=100)

    def _execute(self, sc):
        start = time.time()
        # channel 순서를 가지고 있는 image numpy
        # list -> [ch_idx, image]
        image_by_ch = sc.get_in_by_vatype(self.is_support_vatype_fc)
        # 처리할 정보가 없는 경우 return
        if len(image_by_ch) == 0: return sc

        self.count  =self.count+ 1

        movingBoxes_ch=[]
        classification_images=[]
        new_inf_result = []

        #diff check >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        useBackgroundSubtractor = []
        diffScores =[]
        image_batch=[]
        useDetections = []
        t0=time.time()

        for n, row in enumerate(image_by_ch):
            image = row[1]
            ch_id = str(row[2])
            self.motionDetection.initByChannel(image, ch_id)
            diffscore, _useBackgroundSubtractor = self.useBgSubstraction(ch_id) if self.USE_TRACKING else False

            useBackgroundSubtractor.append(_useBackgroundSubtractor)
            diffScores.append(diffscore)

            if self.isSkipDetection(self.count)==False and (self.isObjectDetectorEfficient(ch_id,threthold=0.6) or _useBackgroundSubtractor == False) :
                image_batch.append(image)
                useDetections.append(True)
            else:
                tracelogger.debug('skip detection ch_id:  [%.s]',ch_id)
                useDetections.append(False)
        tracelogger.debug('check diff  [%.4f]',(time.time() - t0))

        #detection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        detection_inf_result=[]
        if len(image_batch)>0:
            tmp_detection_inf_result = self.doObjectDetection(np.array(image_batch), self.count)
            idx=0
            for n2,ut in enumerate(useDetections):
                if ut==True:
                    detection_inf_result.append(tmp_detection_inf_result[idx])
                    idx=idx+1
                else:
                    detection_inf_result.append(([],[],[]))
        else:
            detection_inf_result.extend( [[[],[],[]] for uu in range(len(useDetections))])

        #BackgroundSubtractor & tracking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        tb = time.time()
        for kk,row in enumerate(image_by_ch):
            _image = row[1]
            ch_id = str(row[2])
            ttt02=time.time()
            tracelogger.debug('motionDetection init time : [%.5f] ' ,  time.time()-ttt02)

            tmpMovingBoxes=[]
            movingBoxes =[]

            tracelogger.debug('diff score : [%.4f]',diffScores[kk])
            ##BackgroundSubtractor
            if  self.isSkipBG(self.count)==False and useBackgroundSubtractor[kk]==True :
            # if  useBackgroundSubtractor[kk]==True :
                movingBoxes_1,valid = self.motionDetection.detectByBackgroundSubtractor(ch_id, diffScore=diffScores[kk], isDebug=self.IS_DEBUG)

                if valid:
                    if len(movingBoxes_1)==0  :
                        self.setAvgDiffWhenNotFound(diffScores[n],ch_id,self.count)
                    tmpMovingBoxes=self.convertOpencvbox2Tensorboxes(movingBoxes_1,_image)  # tensorflow box
            else:
                tracelogger.debug('skip detectByBackgroundSubtractor>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [%.5f]' , diffScores[kk] )
                tracelogger.debug('skip getMaxDiffValueWhenNotFound>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [%.5f]' , self.getMaxDiffValueWhenNotFound(ch_id) )

            # ##filtering by Object detection
            detectionBoxes=detection_inf_result[kk][0]
            if len(detectionBoxes)>0:
                tmpMovingBoxes=self.filteringInnerBoxes(tmpMovingBoxes,detectionBoxes,interceptionAreaThreshold=0.95)
                tmpMovingBoxes.extend(detectionBoxes)

            # ##traking
            ttt=time.time()
            trackingBoxes = self.detectNotFoundBoxesFromTracking3(_image, tmpMovingBoxes  , ch_id,returnTensorType=True)
            if len(trackingBoxes)!=0:
                tracelogger.debug('tracking count : [%.f] ' ,  (len(trackingBoxes)))
                trackingBoxes=self.filteringInnerBoxes(trackingBoxes,tmpMovingBoxes, interceptionAreaThreshold=0.95,isSelf=True)
                tmpMovingBoxes.extend(trackingBoxes)
            tracelogger.debug('tracking time : [%.4f]',  time.time()-ttt)

            if len(tmpMovingBoxes)>0:
                movingBoxes=self.convertTensorboxes2Opencvbox(tmpMovingBoxes,_image)
            # movingBoxes_ch.append(movingBoxes)
            tracelogger.debug('bg substraction count  [%.2f]',len(movingBoxes))

            ##add classification image
            newMovingBoxes=[]
            for bb in movingBoxes:
                (x, y, w, h) = bb
                try:
                    classification_images.append(cv2.resize(_image[y:y + h, x:x + w], self.CLISSIFICATION_SIZE) / 255)
                    newMovingBoxes.append(bb)
                except:
                    tracelogger.debug('classification image crop error : ' ,bb)
            movingBoxes_ch.append(newMovingBoxes)

            if self.IS_DEBUG:
                cv2.putText(_image, str(diffScores[kk]) + "::: "+ str(useBackgroundSubtractor[kk]), (20,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
        tracelogger.debug('bg substraction time  [%.4f]',(time.time() - tb))


        #classification
        t3=time.time()
        (new_inf_result,features)=self.doClassification(image_by_ch,classification_images,movingBoxes_ch)
        tracelogger.debug('classification total time  [%.4f]',   (time.time() - t3) )
        # [END] Background subtraction

        inputSize = len(image_by_ch)


        ## 후처리
        for n in range(inputSize):
            ch_id = image_by_ch[n][2]
            _image = image_by_ch[n][1]
            _inference = new_inf_result[n]
            self.previousMerged[ch_id] = _inference
            self.previousFrames[ch_id] = _image
            if len(_inference)>0:
                self.setObjectDetectorEfficiency(ch_id,_inference[0],detection_inf_result[n][0])

        self.lastUseTracking = useBackgroundSubtractor


        for (ch_id, _, ch_uuid, cfg_json), inference,feature in zip(image_by_ch, new_inf_result,features):
            sc.set_out_by_ch(self.va_type, ch_id, inference,extvalue=feature)
        tracelogger.debug('Intrusion elapsed time [%.4f]', time.time() - start)

        if self.count > 1000000000:
            self.count = -1

        if tracelogger.isEnabledFor(10):
            self.pq.append((time.time()-start)*1000)
            tracelogger.debug('elapsed time avg [%.4f]', np.mean(self.pq))
        return sc;
