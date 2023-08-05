import logging
import random

import cv2

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
from misc.MotionDetection import MotionDetection

category = {1: {'id': 1, 'name': 'person'}, 2: {'id': 2, 'name': 'car'}, 3: {'id': 3, 'name': 'bicycle'}, 4: {'id': 4, 'name': 'motorcycle'}}
class IntrusionVA(VAService):
    MAX_CHANNEL_COUNT = 30
    SCORE_THRESHOLD = 0.3
    SCORE_THRESHOLD_SUB = 0.3
    DIFF_THRESHOLD = 0.03  # 이하값이면 움직임이 전혀없는것으로 간주
    BG_DIFF_THRESHOLD = 10

    USE_BGS = True
    MAX_TRACKING_OBJECT = 4
    MAX_TRACKING_FRAME = 3
    USE_TRACKING = True
    SWITCH_RATE = 2
    USE_SUB = False
    USE_SWITCH = False
    INPUT_SHAPE = (1280, 720)
    USE_TRACKING = True
    USE_ENHANCECONTRAST = True
    CLISSIFICATION_SIZE = (233, 233)
    DETECTION_MAX_WIDTH_RATE=0.4

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
        if va_type == const.INTRUSION_VA:  # 침입탐지용
            self.detector = ObjectDetect(self.enabled, config, 'detect_intrusion', in_shape=self.INPUT_SHAPE)
        else:
            self.detector = ObjectDetect(self.enabled, config, 'detect', in_shape=self.INPUT_SHAPE)
        self.sub_detector = ObjectDetect(self.enabled, config, 'detect_sub', in_shape=self.INPUT_SHAPE)
        self.min_score_threshold = config.getvalue(self.conf_prefix + 'min_score_threshold', min_threshold)
        self.CLISSIFICATION_SIZE =eval( config.getvalue('va_engines.models.intrusion.'+ 'classification_image_size', (224,224)))
        self.classify = Classify(self.enabled, config, 'intrusion', in_shape= self.CLISSIFICATION_SIZE )
        self.SCORE_THRESHOLD = config.getvalue(self.detector.conf_prefix + 'min_score_threshold',
                                               self.min_score_threshold)
        self.SCORE_THRESHOLD_SUB = config.getvalue(self.sub_detector.conf_prefix + 'min_score_threshold',
                                                   self.min_score_threshold)
        self.motionDetection = MotionDetection(isDebug=self.IS_DEBUG)


    def _set_lables(self, path_to_labels):
        labels = labelmap_util.create_categories_from_labelmap(path_to_labels)
        return dict([(item['id'], item['name']) for item in labels])

    '''
        get_in_by_vatype_gen() generator examples
    '''

    def useTracking(self, ch_uuid):
        (diffScore, isBigChange, gray) = self.motionDetection.isChnageImage(ch_uuid, self.DIFF_THRESHOLD)
        self.previousGrayFrames[ch_uuid] = gray

        if self.trackingConsecutiveUseCounts.get(ch_uuid) is None:
            self.trackingConsecutiveUseCounts[ch_uuid] = 0

         # self.isObjectDetectorEfficient(ch_uuid,threthold=0.65)== False
        if self.USE_TRACKING and (isBigChange == False ) \
                and self.trackingConsecutiveUseCounts.get(ch_uuid) < self.MAX_TRACKING_FRAME \
                and (self.previousMerged.get(ch_uuid) is None or len(
                    self.previousMerged.get(ch_uuid)) <= self.MAX_TRACKING_OBJECT):
            self.trackingConsecutiveUseCounts[ch_uuid] = self.trackingConsecutiveUseCounts[ch_uuid] + 1
            return (diffScore, True)
        else:
            self.trackingConsecutiveUseCounts[ch_uuid] = 0
            return (diffScore, False)


    def isNotDuplicatedBox(self, box2, boxes, classes, scores, iouThreshold=0.15):
        for k1 in range(len(boxes)):
            _box = boxes[k1]
            # if utils.isValidBox(boxes[k1], scores[k1], classes[k1], 1):
            iou = utils.getIou(box2, _box)
            if iou > iouThreshold:
                return False
        return True

    def detectNotFoundBoxesFromTracking2(self, _image, _inference, ch_id):
        ttt=time.time()
        (boxes, classes, scores) = _inference
        if self.previousMerged.get(ch_id) is None:
            return []

        height, width = _image.shape[:2]
        if type(boxes) is not list:
            boxes = boxes.tolist()

        resultBoxes = []
        cc=0
        for k, __box in enumerate(self.previousMerged[ch_id][0]):
            if True:
                if self.isNotDuplicatedBox(__box, boxes, classes, scores, iouThreshold=0.5):
                    cc+=1
                    tlx = int(__box[1] * width)
                    tly = int(__box[0] * height)
                    brx = int(__box[3] * width)
                    bry = int(__box[2] * height)

                    boxOffset=3
                    if brx-tlx<boxOffset*2 or bry-tly<boxOffset*2:
                        continue

                    # tracker =cv2.TrackerCSRT_create()
                    tracker = cv2.TrackerMedianFlow_create()
                    # tracker = cv2.TrackerKCF_create()
                    # tracker = cv2.TrackerMOSSE_create()


                    preframeImg=self.previousFrames[ch_id]

                    offsetRate=2
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
                        resultBoxes.append((x, y, w, h))
                        if self.IS_DEBUG:
                            tracelogger.debug(' success detectNotFoundBoxesFromTracking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                            cv2.rectangle(_image, (x, y), (x + w, y + h), (255, 0, 0), 3)

                        # cv2.rectangle(cropImage2,(boxInPreviousFrame[0],boxInPreviousFrame[1]), (boxInPreviousFrame[0]+boxInPreviousFrame[2],boxInPreviousFrame[1]+boxInPreviousFrame[3]), (255, 255, 255), 1)
                        # # cv2.rectangle(currentFrameCrop,(boxInPreviousFrame[0],boxInPreviousFrame[1]), (boxInPreviousFrame[0]+boxInPreviousFrame[2],boxInPreviousFrame[1]+boxInPreviousFrame[3]), (255, 255, 255), 1)
                        # cv2.rectangle(currentFrameCrop2,(x,y), (x+w,y+h), (0, 255, 0), 2)
                        # cv2.rectangle(cropImage2,(x,y), (x+w,y+h), (0, 255, 0), 2)
                        #
                        # kk=np.hstack((cropImage2,currentFrameCrop2))
                        # cv2.imshow('merged ' ,kk )
                    else:

                        if self.IS_DEBUG:
                            tracelogger.debug(' fail detectNotFoundBoxesFromTracking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                            cv2.rectangle(_image, (tlx, tly), (brx, bry), (0, 255, 0), 1)

                        # cv2.rectangle(cropImage2,(boxInPreviousFrame[0],boxInPreviousFrame[1]), (boxInPreviousFrame[0]+boxInPreviousFrame[2],boxInPreviousFrame[1]+boxInPreviousFrame[3]), (255, 255, 255), 1)
                        # cv2.rectangle(currentFrameCrop2,(boxInPreviousFrame[0],boxInPreviousFrame[1]), (boxInPreviousFrame[0]+boxInPreviousFrame[2],boxInPreviousFrame[1]+boxInPreviousFrame[3]), (255, 255, 255), 1)
                        # kk=np.hstack((cropImage2,currentFrameCrop2))
                        #
                        # cv2.imshow('merged fail ' ,kk )
        if cc>0:
            tracelogger.debug('tracking time >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> '+ str(time.time()-ttt)+  ' count :' +str(cc))
        return resultBoxes

    def mergeBoxesResult(self, _image, _inference, _inference2, checkDup=True, iouThreshold=0.7):
        (boxes, classes, scores) = _inference
        height, width = _image.shape[:2]
        if type(boxes) is not list:
            boxes = boxes.tolist()
            classes = classes.tolist()
            scores = scores.tolist()

        for k, __box in enumerate(_inference2[0]):
            if checkDup == False or self.isNotDuplicatedBox(__box, boxes, classes, scores, iouThreshold=iouThreshold):
                boxes.append(__box)
                classes.append(_inference2[1][k])
                scores.append(_inference2[2][k])
        return (np.array(boxes), np.array(classes), np.array(scores))

    def filteringInnerBoxes(self, boxes, targetBoxes, interceptionAreaThreshold=0.9):
        newBoxes = []
        for k, __box in enumerate(boxes):
            if self.checkInnerBoxes(__box, targetBoxes, interceptionAreaThreshold) == False:
                newBoxes.append(__box)
        # return np.array(newBoxes)
        return newBoxes

    def checkInnerBoxes(self, box, targetBoxes, interceptionAreaThreshold=0.9):
        area = utils._getArea(box)
        for tbox in targetBoxes:
            # if area >= utils._getArea(tbox):
            #     continue
            interArea = utils._getIntersectionArea(tbox, box)
            if interArea > int(area * interceptionAreaThreshold):  # interceptionAreaThreshold 이상 겹치면
                return True
        return False

    def doObjectDetection(self, images, _count):

        score = self.SCORE_THRESHOLD
        # detector
        if self.USE_SUB == False or _count % self.SWITCH_RATE != 0:
            ___detector = self.detector
        else:
            score = self.SCORE_THRESHOLD_SUB
            ___detector = self.sub_detector

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

    def classifyBoxes(self, movingBoxes, _image):
        height, width = _image.shape[:2]

        bgBoxes = []
        bgScores = []
        bgClasses = []

        bgBoxesInvalid = []
        bgScoresInvalid = []
        bgClassesInvalid = []


        # [START] Background subtraction
        if len(movingBoxes) > 0:
            classificationList = []
            tmpList = []
            for bb in movingBoxes:
                (x, y, w, h) = bb
                classificationList.append(cv2.resize(_image[y:y + h, x:x + w], self.CLISSIFICATION_SIZE) / 255)
                tmpList.append(_image[y:y + h, x:x + w])
            rr4 = self.classify._inference(classificationList)

            for (k, softmax) in enumerate(rr4):
                order = np.argmax(softmax)
                className = self.clsList[order]
                score = softmax[order]
                (x1, y1, w1, h1) = movingBoxes[k]

                _box = (float(y1 / height), float(x1 / width), float((y1 + h1) / height), float((x1 + w1) / width))
                if className != 'others':
                    bgBoxes.append(_box)
                    bgScores.append(score)
                    bgClasses.append(className)
                else:
                    bgBoxesInvalid.append(_box)
                    bgScoresInvalid.append(score)
                    bgClassesInvalid.append(className)
                if self.SAVE_CLASSIFICATION_IMAGE:
                    if x1 < 200 and y1 < 200:
                        continue
                    SAVE_IMAGE_TARGET_FOLDER = '/home/ocrusr/다운로드/folder/save'
                    cropImage = tmpList[k]
                    folder = os.path.join(SAVE_IMAGE_TARGET_FOLDER, className)
                    if os.path.exists(folder) == False:
                        os.mkdir(folder)
                    cropImage = cv2.cvtColor(cropImage, cv2.COLOR_BGR2RGB)
                    cv2.imwrite(
                        os.path.join(folder, str(random.randint(1, 100000000)) + "_" + str(int(score * 100)) + ".jpg"),
                        cropImage)

                tracelogger.debug('bg substract find object :' + className)

                if self.IS_DEBUG:
                    cv2.rectangle(_image, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 1)
                    color = (0, 0, 255) if className != 'others' else (255, 255, 0)
                    cv2.putText(_image, className + ":" + str(score)[0:3], (x1, y1 - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

        return (bgBoxes, bgScores, bgClasses),(bgBoxesInvalid,bgScoresInvalid,bgClassesInvalid)

    ODF_DICT={}
    queueMaxlen = 10
    DECTION_SKIP_DICT={}
    def isObjectDetectorEfficient(self,ch_id,threthold=0.4):
        queue=self.ODF_DICT.get(ch_id)
        skipDict=self.DECTION_SKIP_DICT.get(ch_id)

        if(queue is None):
            return True

        if(skipDict is None):
            self.DECTION_SKIP_DICT[ch_id]=0
            return True

        if skipDict>=self.MAX_TRACKING_FRAME:
            self.DECTION_SKIP_DICT[ch_id]=0
            return True

        sum=0
        for n,q in enumerate(queue):
            sum=sum+q

        if sum == 0 or sum/(n+1)>threthold:
            self.DECTION_SKIP_DICT[ch_id]=0
            return True
        else:
            self.DECTION_SKIP_DICT[ch_id]=self.DECTION_SKIP_DICT[ch_id]+1
            return False

    def setObjectDetectorEfficiency(self,ch_id,bgBoxes,detectionBoxes):
        if tracelogger.isEnabledFor(10):
            tracelogger.debug(ch_id +' detection box : ' +str( len(detectionBoxes)) + ' bgBoxes : ' +str(len(bgBoxes)))
        queue=self.ODF_DICT.get(ch_id)
        if(queue is None):
            queue = deque(maxlen=self.queueMaxlen)
            self.ODF_DICT[ch_id]=queue

        if len(detectionBoxes)>0:
            queue.append(1)
        else:
            queue.append(1/(1+len(bgBoxes)))

    def _execute(self, sc):
        start = time.time()
        # channel 순서를 가지고 있는 image numpy
        # list -> [ch_idx, image]
        image_by_ch = sc.get_in_by_vatype(self.is_support_vatype_fc)
        # 처리할 정보가 없는 경우 return
        if len(image_by_ch) == 0: return sc
        self.count += 1

        useTracking = []
        image_batch = []
        diffScores = []
        useDetections = []

        # tracking 적용 여부 확인
        for n, row in enumerate(image_by_ch):
            image = row[1]

            ch_id = str(row[2])
            self.motionDetection.initByChannel(image, ch_id)
            diffscore, _useTracking = self.useTracking(ch_id) if self.USE_TRACKING else False
            useTracking.append(_useTracking)
            diffScores.append(diffscore)

            # if self.count%2==0:
            #     ttt=time.time()
            #     image = imutils.rotate(image, 1)
            #     print('time :' , (time.time()-ttt))
            # cv2.imshow('lkkk' ,image)
            if self.IS_DEBUG:
                cv2.putText(image, str(diffscore)[0:4], (140, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1,
                            cv2.LINE_AA)

            if self.isObjectDetectorEfficient(ch_id,threthold=0.6) and _useTracking == False :
                # if True:
                # if (self.motionDetection.isDayByChId(ch_id) == False):
                #     image = self.motionDetection.enhanceContrast(image)
                #     if self.IS_DEBUG:
                #         cv2.imshow('contrast :', cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                image_batch.append(image)
                useDetections.append(True)
            else:
                useDetections.append(False)

        tracelogger.debug('Tracking check time >>>>>>> [%.2f]', (time.time() - start))

        # detection batch 실행
        if len(image_batch) > 0:
            detection_inf_result_tmp = self.doObjectDetection(np.array(image_batch), self.count)


        tmpResult=[]
        orderk=0
        for g,useDetection in enumerate(useDetections):
            if useDetection==False :
                tmpResult.append(([],[],[]))
            else:
                tmpResult.append(detection_inf_result_tmp[orderk])
                if self.IS_DEBUG:
                    height,width=image.shape[:2]
                    for t,box in enumerate(detection_inf_result_tmp[orderk][0]):
                        tlx = int(box[1] * width)
                        tly = int(box[0] * height)
                        brx = int(box[3] * width)
                        bry = int(box[2] * height)
                        cv2.rectangle(image,(tlx,tly),(brx,bry),(255,255,0),1)
                        classname=str(detection_inf_result_tmp[orderk][2][t])
                        cv2.putText(image, classname , (tlx, tly - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0))
                orderk=orderk+1

        detection_inf_result=tmpResult

        # bg substraction
        tb = time.time()
        bgs_inf_result = []
        bgs_inf_result_invalid = []
        if len(diffScores) > 0:
            for n, row in enumerate(image_by_ch):
                _image = row[1]
                ch_id = str(row[2])
                # if diffScores[n] > self.BG_DIFF_THRESHOLD:
                if useTracking[n] == True or diffScores[n] > self.BG_DIFF_THRESHOLD:
                    bgs_inf_result.append(([], [], []))
                    bgs_inf_result_invalid.append(([], [], []))
                    continue

                movingBoxes = self.motionDetection.detectByBackgroundSubtractor(ch_id, diffScore=diffScores[n], isDebug=self.IS_DEBUG)

                detectionBoxes=detection_inf_result[n][0]
                movingBoxes=self.filteringInnerBoxes(movingBoxes,detectionBoxes,interceptionAreaThreshold=0.8)
                if len(movingBoxes)==0:
                    bgs_inf_result.append(([], [], []))
                    bgs_inf_result_invalid.append(([], [], []))
                    continue
                bg_result,bg_result_invalid=self.classifyBoxes(movingBoxes, _image)
                bgs_inf_result.append(bg_result)
                bgs_inf_result_invalid.append(bg_result_invalid)

        # [END] Background subtraction
        tracelogger.debug('bg substraction   time >>>>>>> [%.2f]', (time.time() - tb))

        new_inf_result = []
        inputSize = len(image_by_ch)
        ## 결과 취합 : tracking & detection
        for n in range(inputSize):
            ch_id = image_by_ch[n][2]
            _image = image_by_ch[n][1]

            self.setObjectDetectorEfficiency(ch_id,bgs_inf_result[n][0],detection_inf_result[n][0])

            if useTracking[n] == False:
                _inference = detection_inf_result[n]
                _inference = self.mergeBoxesResult(_image, _inference, bgs_inf_result[n])
            else:
                _inference = bgs_inf_result[n]

            if True:
                ttt=time.time()
                _inferenceTmp = self.mergeBoxesResult(_image, _inference, bgs_inf_result_invalid[n])
                trackingBoxes = self.detectNotFoundBoxesFromTracking2(_image, _inferenceTmp, ch_id)
                tracelogger.debug('tracking time :'+ str(time.time()-ttt))
                bgs_inf_result2,_ = self.classifyBoxes(trackingBoxes, _image)
                self.previousMerged[ch_id] = _inference
                if len(bgs_inf_result2) > 0:
                    _inference = self.mergeBoxesResult(_image, _inference, bgs_inf_result2)


            self.previousFrames[ch_id] = _image
            new_inf_result.insert(n, _inference)
        self.lastUseTracking = useTracking

        for (ch_id, _, _, cfg_json), inference in zip(image_by_ch, new_inf_result):
            sc.set_out_by_ch(self.va_type, ch_id, inference)
        tracelogger.debug('DetectionVA elapsed time [%.2f]', time.time() - start)

        if self.count > 1000000000:
            self.count = -1
        return sc;
