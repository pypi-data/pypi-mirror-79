import logging
import cv2
from service import constants as const
from service.va_service import VAService
from models.objectdetect import ObjectDetect
from misc import labelmap_util
import misc.detection_utils  as utils
import numpy as np
import time
tracelogger = logging.getLogger('trace')
systemlogger = logging.getLogger('system')


class DetectionVA(VAService):
    MAX_CHANNEL_COUNT = 30
    SCORE_THRESHOLD = 0.3
    SCORE_THRESHOLD_SUB = 0.3
    DIFF_THRESHOLD=0.2
    MAX_TRACKING_OBJECT = 4
    MAX_TRACKING_FRAME = 1
    USE_TRACKING = True
    SWITCH_RATE = 2
    USE_SWITCH = True
    INPUT_SHAPE = (1024, 600)
    USE_ENHANCECONTRAST=False
    count = -1
    trackingCount = 0
    previousGrayFrames =dict([])
    previousFrames = dict([])
    previousMerged = dict([])
    trackingConsecutiveUseCounts=dict([]) #tracking 연속 사용 횟수
    lastUseTracking=None
    IS_DEBUG=False
    def __init__(self, config, va_type, min_threshold=0.5):
        super(DetectionVA, self).__init__(config, va_type)
        self.detector = ObjectDetect(self.enabled, config, 'detect', in_shape=self.INPUT_SHAPE)
        self.sub_detector = ObjectDetect(self.enabled, config, 'detect_sub', in_shape=self.INPUT_SHAPE)
        self.min_score_threshold = config.getvalue(self.conf_prefix + 'min_score_threshold', min_threshold)

        self.SCORE_THRESHOLD=config.getvalue(self.detector.conf_prefix+'min_score_threshold',self.min_score_threshold)
        self.SCORE_THRESHOLD_SUB=config.getvalue(self.sub_detector.conf_prefix+'min_score_threshold',self.min_score_threshold)

    def _set_lables(self, path_to_labels):
        labels = labelmap_util.create_categories_from_labelmap(path_to_labels)
        return dict([(item['id'], item['name']) for item in labels])

    '''
        get_in_by_vatype_gen() generator examples  
    '''


    def isChnageImage(self,image, _previousGrayFrame, diffScoreThreshold=0.2):
        difScore = 10.0000
        isBigChange = True
        ti1=time.time()
        grayAndBlurImage = cv2.GaussianBlur( cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) , (21, 21), 0)
        if _previousGrayFrame is not None:
            frameDelta = cv2.absdiff(grayAndBlurImage, _previousGrayFrame)
            thresh = cv2.threshold(frameDelta, 15, 255, cv2.THRESH_BINARY)[1]
            # thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
            difScore = cv2.mean(thresh)[0]
            if difScore < diffScoreThreshold:
                isBigChange = False
        return (difScore, isBigChange, grayAndBlurImage)


    def useTracking(self,image,ch_uuid):
        previousGrayImage=self.previousGrayFrames.get(ch_uuid)
        # imgUmat=cv2.UMat(image)
        (diffScore, isBigChange, gray)=self.isChnageImage(image,previousGrayImage,self.DIFF_THRESHOLD)
        self.previousGrayFrames[ch_uuid]=gray

        if self.trackingConsecutiveUseCounts.get(ch_uuid) is None:
            self.trackingConsecutiveUseCounts[ch_uuid]=0

        if self.IS_DEBUG:
            cv2.putText(image, str(diffScore), (300,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)

        if self.USE_TRACKING and  isBigChange == False \
                and self.trackingConsecutiveUseCounts.get(ch_uuid)<self.MAX_TRACKING_FRAME \
                and (self.previousMerged.get(ch_uuid) is None or len(self.previousMerged.get(ch_uuid))<=self.MAX_TRACKING_OBJECT):
                self.trackingConsecutiveUseCounts[ch_uuid]=self.trackingConsecutiveUseCounts[ch_uuid]+1
                return True
        else:
            self.trackingConsecutiveUseCounts[ch_uuid]=0
            return False

    def isNotDuplicatedBox(self, box2, boxes, classes, scores,iouThreshold=0.15):
        for k1 in range(len(boxes)):
            _box = boxes[k1]
            # if utils.isValidBox(boxes[k1], scores[k1], classes[k1], 1):
            iou = utils.getIou(box2, _box)
            if iou > iouThreshold:
                return False
        return True
    def addLiedownBoxesFromPreviousResult(self, _image, _inference, ch_id):
        (boxes, classes, scores) = _inference
        height, width = _image.shape[:2]
        if  type(boxes) is not list:
            boxes = boxes.tolist()
            classes = classes.tolist()
            scores = scores.tolist()

        if self.previousMerged.get(ch_id) is None or len(self.previousMerged.get(ch_id)) ==0 \
                or len(self.previousMerged[ch_id][0])==0 or len(self.previousMerged[ch_id][0][0]) !=4 :
            return _inference

        for k, __box in enumerate(self.previousMerged[ch_id][0]):
            if ((__box[3] - __box[1]) / (__box[2] - __box[0]) > 0.8): ## 옆으로 긴 물체중
                if self.isNotDuplicatedBox(__box, boxes, classes, scores, iouThreshold=0.7):
                    tlx = int(__box[1] * width)
                    tly = int(__box[0] * height)
                    brx = int(__box[3] * width)
                    bry = int(__box[2] * height)
                    tracker = cv2.TrackerCSRT_create()
                    # tracker = cv2.TrackerKCF_create()
                    # tracker = cv2.TrackerMOSSE_create()
                    bbb = (tlx, tly, (brx - tlx), (bry - tly))

                    tracker.init(self.previousFrames[ch_id], bbb)
                    (success, box) = tracker.update(_image)
                    if success:
                        (x, y, w, h) = [int(v) for v in box]
                        newBox = (y / height, x / width, (y + h) / height, (x + w) / width)
                        boxes.append(newBox)
                        classes.append(self.previousMerged[ch_id][1][k])
                        scores.append(self.previousMerged[ch_id][2][k])
        _inference = (np.array(boxes), np.array(classes), np.array(scores))
        return _inference

    def getBrightness(self,image):
        if image.ndim==2:
            return int (cv2.mean(image)[0])
        else:
            return int (cv2.mean(image[:,:,0])[0])


    def detectNotFoundBoxesFromTracking(self, _image, _inference, ch_id):
        ttt=time.time()
        (boxes, classes, scores) = _inference
        if self.previousMerged.get(ch_id) is None:
            return []

        if type(boxes) is not list:
            boxes = boxes.tolist()

        resultBoxes = []
        newClasses=[]
        newScores=[]
        cc=0
        height, width = _image.shape[:2]
        for k, __box in enumerate(self.previousMerged[ch_id][0]):
            if True:
                if self.isNotDuplicatedBox(__box, boxes, classes, scores, iouThreshold=0.5):
                    cc+=1
                    tlx = int(__box[1] * width)
                    tly = int(__box[0] * height)
                    brx = int(__box[3] * width)
                    bry = int(__box[2] * height)

                    boxOffset=1
                    if brx-tlx<boxOffset*2 or bry-tly<boxOffset*2:
                        resultBoxes.append(__box)
                        newClasses.append(classes[k])
                        newScores.append(scores[k])
                        continue

                    # tracker =cv2.TrackerCSRT_create()
                    tracker = cv2.TrackerMedianFlow_create()
                    # tracker = cv2.TrackerKCF_create()
                    # tracker = cv2.TrackerMOSSE_create()


                    preframeImg=self.previousFrames[ch_id]

                    offsetRate=0.7
                    cropWidthOffset=int((brx-tlx)*offsetRate)
                    cropHeightOffset=int((bry-tly)*offsetRate)

                    if cropWidthOffset>cropHeightOffset:
                        cropHeightOffset=cropWidthOffset
                    else:
                        cropWidthOffset=cropHeightOffset

                    top_y=tly-cropHeightOffset if tly-cropHeightOffset>0 else 0
                    bottom_y=bry+cropHeightOffset if bry+cropHeightOffset<height else height

                    left_x=tlx-cropWidthOffset if tlx-cropWidthOffset>0 else 0
                    right_x=brx+cropWidthOffset if brx+cropWidthOffset<width else width
                    cropImage=preframeImg[top_y:bottom_y, left_x:right_x]  # 이전 박스 주변 이미지만 crop 해서 tracking


                    boxWidth=(brx - tlx)
                    boxHeight= (bry - tly)

                    # boxInPreviousFrame = (tlx-left_x, tly-top_y, (brx - tlx), (bry - tly))  # 이전 Box 좌표변환
                    boxInPreviousFrame = (tlx-left_x+boxOffset, tly-top_y+boxOffset, (brx - tlx)-(2*boxOffset), (bry - tly)-(2*boxOffset))  # 이전 Box 좌표변환
                    tracker.init(cropImage, boxInPreviousFrame)
                    currentFrameCrop=_image[top_y:bottom_y, left_x:right_x]
                    (success, box) = tracker.update(currentFrameCrop)
                    (x, y, w, h) = [int(v) for v in box]
                    if success and (x<0 or y<0 or w>boxWidth*1.5 or h> boxHeight>1.5) == False:
                    # if success and (x<0 or y<0  ) == False:
                        (x, y, w, h)=(x+left_x,y+top_y,w,h) # 전체 이미지로 좌표변환
                        newBox = (y / height, x / width, (y + h) / height, (x + w) / width)
                        resultBoxes.append(newBox)
                        newClasses.append(self.previousMerged[ch_id][1][k])
                        newScores.append(self.previousMerged[ch_id][2][k])
                        if self.IS_DEBUG:
                            tracelogger.debug(' success detectNotFoundBoxesFromTracking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                            # cv2.rectangle(_image, (x, y), (x + w, y + h), (255, 0, 0), 3)
                            # cv2.rectangle(_image, (left_x, top_y), (right_x, bottom_y), (255, 255, 0), 4)
                    else:
                        # resultBoxes.append(__box)
                        if self.IS_DEBUG:
                            tracelogger.debug(' fail detectNotFoundBoxesFromTracking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                            # cv2.rectangle(_image, (tlx, tly), (brx, bry), (0, 255, 0), 1)

                    # newClasses.append(self.previousMerged[ch_id][1][k])
                    # newScores.append(self.previousMerged[ch_id][2][k])
        if cc>0:
            tracelogger.debug('tracking time >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> '+ str(time.time()-ttt)+  ' count :' +str(cc))
        return (resultBoxes,newClasses,newScores)


    def detectByTraking(self,image,previouResult,ch_uuid):
        tt=time.time()
        # previouResult [valid_boxes, valid_scores, valid_class]
        height, width = image.shape[:2]
        newBoxes=[]
        if previouResult is None:
            return [[], [], []]
        for n,_box in enumerate(previouResult[0]):
            tlx = int(_box[1] * width)
            tly = int(_box[0] * height)
            brx = int(_box[3] * width)
            bry = int(_box[2] * height)
            # tracker = cv2.TrackerCSRT_create()
            tracker = cv2.TrackerKCF_create()
            # tracker = cv2.TrackerMOSSE_create()
            bbb=(tlx,tly,(brx-tlx),(bry-tly))

            tracker.init(self.previousFrames[ch_uuid],bbb)
            (success, box) = tracker.update(image )
            if success:
                (x, y, w, h) = [int(v) for v in box]
                newBox = (y/height, x/width, (y + h)/height, (x + w)/width)
                newBoxes.append(newBox)
            else:
                newBoxes.append(_box)
        tracelogger.debug('detectByTraking  time >>>>>>> [%.2f]' ,(time.time()-tt))
        return [np.array(newBoxes),previouResult[1],previouResult[2]]


    def doObjectDetection(self,images,_count):

        score=self.SCORE_THRESHOLD
        # detector
        if _count % self.SWITCH_RATE != 0 or self.USE_SWITCH==False:
            ___detector= self.detector
        else:
            score=self.SCORE_THRESHOLD_SUB
            ___detector=self.sub_detector

        inferences= ___detector._inference(images)
        newInferences=[]
        for inf in inferences:
            newInferences.append(self.aggregate_result(inf,score))
        return np.array(newInferences)

    def aggregate_result(self, inference,_score):
        boxes, scores, classes = inference

        valid = [idx for idx, score in enumerate(scores) if score > _score]
        if len(valid) > 0:
            valid_scores = scores[valid].tolist()
            valid_boxes = boxes[valid].tolist()
            valid_class = [self.label_map[int(a_class)] for a_class in classes[valid]]
            return [valid_boxes, valid_scores, valid_class]
        else:  # invalid image
            return [[], [], []]

    def _execute(self, sc):
        start=time.time()
        # channel 순서를 가지고 있는 image numpy
        # list -> [ch_idx, image]
        image_by_ch = sc.get_in_by_vatype(self.is_support_vatype_fc)

        # 처리할 정보가 없는 경우 return
        if len(image_by_ch) == 0: return sc
        self.count += 1

        useTracking=[]
        image_batch = []
        # trackin 적용 여부 확인
        for n,row in enumerate(image_by_ch):
            image=row[1]
            _useTracking=self.useTracking(image,str(row[2])) if self.USE_TRACKING else False
            useTracking.append(_useTracking)
            if _useTracking==False:

                #저조도일 경우 contrast 향상
                if self.USE_ENHANCECONTRAST==True and self.getBrightness(image)<90:
                    image=utils.enhanceContrast(image)

                image_batch.append(image)
        tracelogger.debug('Tracking check time >>>>>>> [%.5f]' ,(time.time()-start))

        # detection batch 실행
        if len(image_batch)>0:
            inf_result=self.doObjectDetection(np.array(image_batch),self.count)

        new_inf_result=[]
        order=0
        inputSize=len(image_by_ch)
        ## 결과 취합 : tracking & detection
        for n in range(inputSize):
            ch_id=image_by_ch[n][2]
            _image=image_by_ch[n][1]
            previouResult=self.previousMerged.get(ch_id)
            if useTracking[n]==True:
                # _inference=self.detectByTraking(_image,previouResult,ch_id)
                _inference= self.detectNotFoundBoxesFromTracking (_image, ([],[],[]), ch_id)
            else:
                _inference=inf_result[order]
                order=order+1

                try:
                    if self.lastUseTracking is not None and len(self.lastUseTracking) > n and  self.lastUseTracking[n] is not None:
                        if self.count % self.SWITCH_RATE != 0 and self.lastUseTracking is not None and self.lastUseTracking[n]==False:
                            _inference = self.addLiedownBoxesFromPreviousResult(_image, _inference, ch_id)
                except:
                    tracelogger.log('index range check')

            self.previousMerged[ch_id]=_inference
            self.previousFrames[ch_id]=_image
            new_inf_result.insert(n,_inference)

        self.lastUseTracking=useTracking
        for (ch_id, _, _, cfg_json), inference in zip(image_by_ch, new_inf_result):
            sc.set_out_by_ch(self.va_type, ch_id, inference)
        tracelogger.debug('DetectionVA elapsed time [%.4f]', time.time() - start)

        if self.count>1000000000:
            self.count=-1
        return sc;


