import logging
import cv2
from service.va_service import VAService
from models.objectdetect import ObjectDetect
from misc import labelmap_util
import misc.detection_utils  as utils
import numpy as np
import time
tracelogger = logging.getLogger('trace')
systemlogger = logging.getLogger('system')
from collections import deque

class DetectionVA(VAService):
    MAX_CHANNEL_COUNT = 30
    SCORE_THRESHOLD = 0.3
    DIFF_THRESHOLD=0.2
    MAX_TRACKING_OBJECT = 4
    MAX_TRACKING_FRAME = 1
    MAX_TRACKING_FRAME_WHEN_NOT_CHANGED=2
    USE_TRACKING = True
    INPUT_SHAPE = (1024, 600)
    count = 1
    trackingCount = 0
    previousGrayFrames =dict([])
    previousFrames = dict([])
    previousMerged = dict([])
    trackingConsecutiveUseCounts=dict([]) #tracking 연속 사용 횟수
    IS_DEBUG=True
    elapse_time=0
    DIFF_DICT={}

    def __init__(self, config, va_type, min_threshold=0.5):
        super(DetectionVA, self).__init__(config, va_type)
        self.detector = ObjectDetect(self.enabled, config, 'detect', in_shape=self.INPUT_SHAPE)
        # self.sub_detector = ObjectDetect(self.enabled, config, 'detect_sub', in_shape=self.INPUT_SHAPE)
        self.min_score_threshold = config.getvalue(self.conf_prefix + 'min_score_threshold', min_threshold)
        self.SCORE_THRESHOLD=config.getvalue(self.detector.conf_prefix+'min_score_threshold',self.min_score_threshold)
        self.IS_DEBUG=self.config.getbool('debug')


    def _set_lables(self, path_to_labels):
        labels = labelmap_util.create_categories_from_labelmap(path_to_labels)
        return dict([(item['id'], item['name']) for item in labels])

    def getMaxDiffValueWhenNotFound(self, ch_id):
        queue=self.DIFF_DICT.get(ch_id)
        if(queue is None):
            return 0
        if len(queue)> 10 :
            # maxValue=(np.mean(queue )+np.std(queue )*2); # 95%
            maxValue=(np.mean(queue )+np.std(queue )*1.3); # 80%
            # maxValue=(np.mean(queue )+np.std(queue )*1); # 65%
            # if maxValue<self.DIFF_THRESHOLD:
            #     maxValue=np.mean(queue )*0.7
            return maxValue
        else:
            return 0

    def setDiffWhenNotFound(self,diff,ch_id,count):
        queue=self.DIFF_DICT.get(ch_id)
        if(queue is None):
            queue = deque(maxlen=150)
            self.DIFF_DICT[ch_id]=queue

        if diff >150 or count%500==0:
            queue = deque(maxlen=150)
            self.DIFF_DICT[ch_id]=queue
        else:
            queue.append(float(diff if diff<20 else 20))

    def use_tracking(self,image,ch_uuid):

        previousGrayImage=self.previousGrayFrames.get(ch_uuid)

        is_frame_change = True
        grayAndBlurImage = cv2.GaussianBlur( cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) , (21, 21), 0)
        diffScoreThreshold=self.getMaxDiffValueWhenNotFound(ch_uuid)

        diff_score=100
        trackingMaxDiff=80
        if previousGrayImage is not None:
            frameDelta = cv2.absdiff(grayAndBlurImage, previousGrayImage)
            thresh = cv2.threshold(frameDelta, 10, 255, cv2.THRESH_BINARY)[1]
            diff_score = cv2.mean(thresh)[0]
            if diff_score <= diffScoreThreshold:
                is_frame_change = False

        self.previousGrayFrames[ch_uuid]=grayAndBlurImage

        if self.trackingConsecutiveUseCounts.get(ch_uuid) is None:
            self.trackingConsecutiveUseCounts[ch_uuid]=0

        if self.IS_DEBUG:
            cv2.putText(image, str(diff_score), (300,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)

        use_tracking=False
        if self.USE_TRACKING and (self.previousMerged.get(ch_uuid) is None or len(self.previousMerged.get(ch_uuid)[0])<=self.MAX_TRACKING_OBJECT) :
            if is_frame_change:
                if  self.trackingConsecutiveUseCounts.get(ch_uuid)<self.MAX_TRACKING_FRAME \
                        and diff_score < trackingMaxDiff: # 화면 변화가 너무 심할 경우 tracking 안함
                    use_tracking =  True

            # 화면의 변화가 없을 경우 max_tracking_frame_count_when_not_changed 이하의 Frame 동안 tracking 사용
            elif self.trackingConsecutiveUseCounts.get(ch_uuid)<self.MAX_TRACKING_FRAME_WHEN_NOT_CHANGED :
                    use_tracking =  True

        if use_tracking:
            self.trackingConsecutiveUseCounts[ch_uuid]+=1
        else:
            self.trackingConsecutiveUseCounts[ch_uuid]=0
        return (use_tracking,diff_score)



    def isNotDuplicatedBox(self, box2, boxes, classes, scores,iouThreshold=0.15):
        for k1 in range(len(boxes)):
            _box = boxes[k1]
            # if utils.isValidBox(boxes[k1], scores[k1], classes[k1], 1):
            iou = utils.getIou(box2, _box)
            if iou > iouThreshold:
                return False
        return True

    def detectNotFoundBoxesFromTracking(self, _image, _inference, ch_id):
        ttt=time.time()
        (boxes, classes, scores) = _inference
        if self.previousMerged.get(ch_id) is None:
            return ([],[],[])

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

                    # tracker =cv2.TrackerCSRT_create()
                    tracker = cv2.TrackerKCF_create()
                    # tracker = cv2.TrackerMedianFlow_create()
                    preframeImg=self.previousFrames[ch_id]

                    boxInPreviousFrame = (tlx, tly, (brx - tlx), (bry - tly))  # 이전 Box 좌표변환
                    tracker.init(preframeImg, boxInPreviousFrame)
                    (success, box) = tracker.update(_image)

                    (x, y, w, h) = [int(v) for v in box]
                    if success and (x<0 or y<0  ) == False:
                        newBox = (y / height, x / width, (y + h) / height, (x + w) / width)
                        resultBoxes.append(newBox)
                        newClasses.append(self.previousMerged[ch_id][1][k])
                        newScores.append(self.previousMerged[ch_id][2][k])
                        if self.IS_DEBUG:
                            tracelogger.debug(' success detectNotFoundBoxesFromTracking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                    else:
                        if self.IS_DEBUG:
                            tracelogger.debug(' fail detectNotFoundBoxesFromTracking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        if cc>0:
            tracelogger.debug('tracking time >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> '+ str(time.time()-ttt)+  ' count :' +str(cc))
        return (np.array(resultBoxes),np.array(newClasses),np.array(newScores) )

    def doObjectDetection(self,images,_count):
        inferences= self.detector._inference(images)
        newInferences=[]
        for inf in inferences:
            newInferences.append(self.aggregate_result(inf,self.SCORE_THRESHOLD))
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
        diffValues=[]

        # tracking 적용 여부 확인
        for k,row in enumerate(image_by_ch):
            image=row[1]
            ch_id=image_by_ch[k][2]
            (_useTracking,diff)=self.use_tracking(image,str(ch_id))
            useTracking.append(_useTracking)
            diffValues.append(diff)
            if _useTracking==False:
                image_batch.append(image)
        tracelogger.debug('Tracking check time >>>>>>> [%.5f]' ,(time.time()-start))

        # detection batch 실행
        if len(image_batch)>0:
            inf_result=self.doObjectDetection(np.array(image_batch),self.count)

        new_inf_result=[]
        order=0
        ## 결과 취합 : tracking & detection
        for n,row in enumerate(image_by_ch):
            ch_id=image_by_ch[n][2]
            _image=image_by_ch[n][1]

            if useTracking[n]==True:
                _inference= self.detectNotFoundBoxesFromTracking (_image, ([],[],[]), ch_id)
            else:
                _inference=inf_result[order]
                order=order+1

            detection_count=len(_inference[0])
            self.previousMerged[ch_id]=_inference
            self.previousFrames[ch_id]=_image
            new_inf_result.insert(n,_inference)
            if detection_count==0:
                self.setDiffWhenNotFound(diffValues[n],ch_id,self.count)

        for (ch_id, _, _, cfg_json), inference in zip(image_by_ch, new_inf_result):
            sc.set_out_by_ch(self.va_type, ch_id, inference)
        tracelogger.debug('DetectionVA elapsed time [%.4f]', time.time() - start)

        self.elapse_time+=(time.time() - start)
        tracelogger.debug('DetectionVA avg elapse time [%.4f]' , (self.elapse_time/ self.count))

        if self.count>1000000000:
            self.count=-1
        return sc;

