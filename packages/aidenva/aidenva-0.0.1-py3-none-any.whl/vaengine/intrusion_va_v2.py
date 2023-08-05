import logging
import random

import cv2

from service import constants as const
from service.va_service import VAService
from models.objectdetect import ObjectDetect
from misc import labelmap_util
import misc.detection_utils  as utils
import numpy as np
import time
import os
tracelogger = logging.getLogger('trace')
systemlogger = logging.getLogger('system')
from models.classify import Classify

from misc.MotionDetection import MotionDetection


class IntrusionVA(VAService):
    MAX_CHANNEL_COUNT = 30
    SCORE_THRESHOLD = 0.3
    SCORE_THRESHOLD_SUB = 0.3
    DIFF_THRESHOLD = 0.2
    BG_DIFF_THRESHOLD = 10
    MAX_BG_DETECTION_COUNT=15

    USE_BGS = True
    MAX_TRACKING_OBJECT = 4
    MAX_TRACKING_FRAME = 1
    USE_TRACKING = True
    SWITCH_RATE = 2
    USE_SUB = False
    USE_SWITCH = False
    INPUT_SHAPE = (1280, 720)
    USE_TRACKING = True
    USE_ENHANCECONTRAST = True
    # CLISSIFICATION_SIZE = (331, 331)
    CLISSIFICATION_SIZE = (299, 299)
    # CLISSIFICATION_SIZE = (101, 101)


    count = -1
    trackingCount = 0
    previousGrayFrames = dict([])
    previousFrames = dict([])
    previousMerged = dict([])
    trackingConsecutiveUseCounts = dict([])  # tracking 연속 사용 횟수
    lastUseTracking = None
    IS_DEBUG = False
    motionDetection = None

    clsList = [ 'car', 'others', 'person']
    # clsList = ['bicycle', 'car', 'motorcycle', 'others', 'person']
    SAVE_CLASSIFICATION_IMAGE=False
    def __init__(self, config, va_type, min_threshold=0.5):
        super(IntrusionVA, self).__init__(config, va_type)
        if va_type == const.INTRUSION_VA:  # 침입탐지용
            self.detector = ObjectDetect(self.enabled, config, 'detect_intrusion', in_shape=self.INPUT_SHAPE)
        else:
            self.detector = ObjectDetect(self.enabled, config, 'detect', in_shape=self.INPUT_SHAPE)
        self.sub_detector = ObjectDetect(self.enabled, config, 'detect_sub', in_shape=self.INPUT_SHAPE)
        self.min_score_threshold = config.getvalue(self.conf_prefix + 'min_score_threshold', min_threshold)

        self.SCORE_THRESHOLD = config.getvalue(self.detector.conf_prefix + 'min_score_threshold',
                                               self.min_score_threshold)
        self.SCORE_THRESHOLD_SUB = config.getvalue(self.sub_detector.conf_prefix + 'min_score_threshold',
                                                   self.min_score_threshold)
        self.motionDetection = MotionDetection(isDebug=self.IS_DEBUG)
        self.classify = Classify(self.enabled, config, 'intrusion',in_shape=self.CLISSIFICATION_SIZE)

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

        if self.USE_TRACKING and isBigChange == False \
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
        (boxes, classes, scores) = _inference
        if self.previousMerged.get(ch_id) is None:
            return []

        height, width = _image.shape[:2]
        if type(boxes) is not list:
            boxes = boxes.tolist()

        resultBoxes=[]
        for k, __box in enumerate(self.previousMerged[ch_id][0]):
            if True:
                if self.isNotDuplicatedBox(__box, boxes, classes, scores, iouThreshold=0.5):
                    tlx = int(__box[1] * width)
                    tly = int(__box[0] * height)
                    brx = int(__box[3] * width)
                    bry = int(__box[2] * height)
                    # tracker =cv2.TrackerCSRT_create
                    tracker = cv2.TrackerKCF_create()
                    # tracker = cv2.TrackerMOSSE_create()
                    bbb = (tlx, tly, (brx - tlx), (bry - tly))

                    tracker.init(self.previousFrames[ch_id], bbb)
                    (success, box) = tracker.update(_image)

                    if success:

                        (x, y, w, h) = [int(v) for v in box]
                        resultBoxes.append((x, y, w, h))
                        if self.IS_DEBUG:
                            print(' success detectNotFoundBoxesFromTracking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' )
                            cv2.rectangle(_image, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    else:

                        if self.IS_DEBUG:
                            print(' fail detectNotFoundBoxesFromTracking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' )
                            cv2.rectangle(_image, (tlx, tly), (brx, bry), (0, 255, 0), 1)
        return resultBoxes


    def mergeBoxesResult(self, _image, _inference, _inference2,checkDup=True,iouThreshold=0.7):
        (boxes, classes, scores) = _inference
        height, width = _image.shape[:2]
        if type(boxes) is not list:
            boxes = boxes.tolist()
            classes = classes.tolist()
            scores = scores.tolist()

        for k, __box in enumerate(_inference2[0]):
            if checkDup==False or self.isNotDuplicatedBox(__box, boxes, classes, scores, iouThreshold=iouThreshold):
                boxes.append(__box)
                classes.append(_inference2[1][k])
                scores.append(_inference2[2][k])
        _inference = (np.array(boxes), np.array(classes), np.array(scores))
        return _inference

    def detectByTraking(self, image, previouResult, ch_uuid):
        tt = time.time()
        # previouResult [valid_boxes, valid_scores, valid_class]
        height, width = image.shape[:2]
        newBoxes = []
        if previouResult is None:
            return [[], [], []]
        for n, _box in enumerate(previouResult[0]):
            tlx = int(_box[1] * width)
            tly = int(_box[0] * height)
            brx = int(_box[3] * width)
            bry = int(_box[2] * height)
            # tracker = cv2.TrackerCSRT_create()
            tracker = cv2.TrackerKCF_create()
            # tracker = cv2.TrackerMOSSE_create()
            bbb = (tlx, tly, (brx - tlx), (bry - tly))

            tracker.init(self.previousFrames[ch_uuid], bbb)
            (success, box) = tracker.update(image)
            if success:
                (x, y, w, h) = [int(v) for v in box]
                newBox = (y / height, x / width, (y + h) / height, (x + w) / width)
                newBoxes.append(newBox)
            else:
                newBoxes.append(_box)
        tracelogger.debug('detectByTraking  time >>>>>>> [%.2f]', (time.time() - tt))
        return [np.array(newBoxes), previouResult[1], previouResult[2]]

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

        valid = [idx for idx, score in enumerate(scores) if score > _score]
        if len(valid) > 0:
            valid_scores = scores[valid].tolist()
            valid_boxes = boxes[valid].tolist()
            valid_class = [self.label_map[int(a_class)] for a_class in classes[valid]]
            return [valid_boxes, valid_scores, valid_class]
        else:  # invalid image
            return [[], [], []]

    def classifyBoxes(self,movingBoxes,_image):
        height, width = _image.shape[:2]
        # [START] Background subtraction
        if len(movingBoxes) > 0 and len(movingBoxes)<self.MAX_BG_DETECTION_COUNT:
            classificationList=[]
            bgBoxes = []
            bgScores = []
            bgClasses = []
            for bb in movingBoxes:
                (x, y, w, h) = bb
                classificationList.append(cv2.resize(_image[y:y + h, x:x + w], self.CLISSIFICATION_SIZE) / 255)


            rr4 = self.classify._inference(classificationList)

            for (k, softmax) in enumerate(rr4):
                order = np.argmax(softmax)
                className = self.clsList[order]
                score = softmax[order]
                (x1, y1, w1, h1) = movingBoxes[k]

                if className != 'others':
                    _box = (float(y1/height), float(x1/width), float((y1 + h1)/height),float( (x1 + w1)/width))
                    bgBoxes.append(_box)
                    bgScores.append(score)
                    bgClasses.append(className)


                if self.SAVE_CLASSIFICATION_IMAGE:
                    SAVE_IMAGE_TARGET_FOLDER='/home/ocrusr/다운로드/folder'
                    cropImage=classificationList[k]*255
                    folder=os.path.join(SAVE_IMAGE_TARGET_FOLDER,className)
                    if os.path.exists(folder)==False:
                        os.mkdir(folder)
                    cv2.imwrite(os.path.join(folder,str(random.randint(1,100000000))+".jpg"),cropImage)

                tracelogger.debug('bg substract find object :'+className)

                if self.IS_DEBUG:
                    cv2.rectangle(_image, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 255), 1)
                    cv2.putText(_image, className + ":" + str(score)[0:3], (x1, y1 - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            return (bgBoxes,bgScores,bgClasses)

        else:
            return [],[],[]

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

        # tracking 적용 여부 확인
        for n, row in enumerate(image_by_ch):
            image = row[1]
            ch_id = str(row[2])
            self.motionDetection.initByChannel(image, ch_id)
            diffscore, _useTracking = self.useTracking(ch_id) if self.USE_TRACKING else False
            useTracking.append(_useTracking)
            diffScores.append(diffscore)
            if self.IS_DEBUG:
                cv2.putText(image, str(diffscore)[0:4], (140, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1,
                            cv2.LINE_AA)

            # if _useTracking == False:
            if True:
                if(self.motionDetection.isDay(image)==False):
                    image=self.motionDetection.enhanceContrast(image)
                    if self.IS_DEBUG:
                        cv2.imshow('contrast :', cv2.cvtColor(image,cv2.COLOR_BGR2RGB)  )
                image_batch.append(image)

        tracelogger.debug('Tracking check time >>>>>>> [%.2f]', (time.time() - start))

        # detection batch 실행
        if len(image_batch) > 0:
            detection_inf_result = self.doObjectDetection(np.array(image_batch), self.count)
        # detection_inf_result = self.doObjectDetection(np.array([row[1] for row in image_by_ch]), self.count)

        # bg substraction
        tb=time.time()
        bgs_inf_result=[]
        if len(diffScores) > 0 :
            for n, row in enumerate(image_by_ch):
                _image = row[1]
                ch_id = str(row[2])
                if diffScores[n]>self.BG_DIFF_THRESHOLD:
                    bgs_inf_result.append(([],[],[]))
                    continue
                movingBoxes = self.motionDetection.detectByBackgroundSubtractor(ch_id, diffScore=diffScores[n],isDebug=self.IS_DEBUG)

                # if width*self.BG_MAX_SIZE_RATE<x or height *self.BG_MAX_SIZE_RATE< y:
                #     continue

                bgs_inf_result.append(self.classifyBoxes(movingBoxes,_image))
        # [END] Background subtraction
        tracelogger.debug('bg substraction   time >>>>>>> [%.2f]', (time.time() - tb))


        new_inf_result = []
        order = 0
        inputSize = len(image_by_ch)
        ## 결과 취합 : tracking & detection
        for n in range(inputSize):
            ch_id = image_by_ch[n][2]
            _image = image_by_ch[n][1]

            _inference = detection_inf_result[order]
            _inference=self.mergeBoxesResult(_image,_inference,bgs_inf_result[n])

            if True:
                trackingBoxes=self.detectNotFoundBoxesFromTracking2(_image, _inference, ch_id)
                bgs_inf_result2=self.classifyBoxes(trackingBoxes,_image)
                self.previousMerged[ch_id] = _inference
                if len(bgs_inf_result2)>0:
                    _inference=self.mergeBoxesResult(_image,_inference,bgs_inf_result2)

            order = order + 1

            self.previousFrames[ch_id] = _image
            new_inf_result.insert(n, _inference)

        self.lastUseTracking = useTracking

        for (ch_id, _, _, cfg_json), inference in zip(image_by_ch, new_inf_result):
            sc.set_out_by_ch(self.va_type, ch_id, inference)
        tracelogger.debug('DetectionVA elapsed time [%.2f]', time.time() - start)

        if self.count > 1000000000:
            self.count = -1
        return sc;
