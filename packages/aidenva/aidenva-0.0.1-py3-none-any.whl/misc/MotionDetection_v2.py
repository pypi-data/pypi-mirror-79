import cv2
import numpy as np
import time;
import logging

tracelogger = logging.getLogger('trace')


class MotionDetection:
    rectElement = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 7))
    _fgbgMap = {}

    _currentFrameMap = {}
    _previousFrameMap = {}
    _currentGrayMap = {}
    _previousGrayMap = {}
    _previousGray2Map = {}
    _isDayMap = {}
    _brightnessMap = {}
    MAX_DETECTION_COUNT = 25
    THRESHOLD_LOW = 5
    THRESHOLD_LOW_NIGHT = 30
    MIN_HEIGHT_NIGHT = 30
    MIN_WIDTH_NIGHT = 40

    MIN_HEIGHT_DAY = 5
    MIN_WIDTH_DAY = 10

    MAX_WIDTH_RATE = 0.3
    MAX_HEIGHT_RATE = 0.3

    MIN_DAY_BRIGHTNESS = 90
    IS_DEBUG = False
    BG_SUB_WIDTH = 960
    BG_SUB_HEIGHT = 540

    def __init__(self, isDebug=False):
        self.IS_DEBUG = isDebug

    def initByChannel(self, image, ch_id):

        previousFrame = self._currentFrameMap.get(ch_id)

        self._currentFrameMap[ch_id] = image
        gray = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (15, 15), 0)

        self._brightnessMap[ch_id] = self._getBrightness(gray)
        self._isDayMap[ch_id] = self.isDay(gray, brightness=self._brightnessMap[ch_id])

        currentGray = self._currentGrayMap.get(ch_id)
        previousGray = self._previousGrayMap.get(ch_id)

        self._currentGrayMap[ch_id] = gray

        if currentGray is not None:
            self._previousGrayMap[ch_id] = currentGray

        if previousGray is not None:
            self._previousGray2Map[ch_id] = previousGray

        if previousFrame is not None:
            self._previousFrameMap[ch_id] = previousFrame

    def isChnageImage(self, ch_id, diffScoreThreshold=0.2):
        diffScore = 10
        isBigChange = True
        gray = self._currentGrayMap[ch_id]
        thresholdLowPoint = 6
        _previousFrame = self._previousGrayMap.get(ch_id)

        if _previousFrame is not None:
            d1 = cv2.absdiff(gray, _previousFrame)
            thresh = cv2.threshold(d1, thresholdLowPoint, 255, cv2.THRESH_BINARY)[1]
            diffScore = cv2.mean(thresh)[0]
            if diffScore < diffScoreThreshold:
                isBigChange = False
            self._previousGray2Map[ch_id] = _previousFrame

        return (diffScore, isBigChange, gray)

    def _getBrightness(self, image):
        # return int (np.sum(cv2.mean(image))/3)
        if image.ndim == 2:
            return int(cv2.mean(image)[0])
        else:
            return int(cv2.mean(image[:, :, 0])[0])

    def isDay(self, image, brightness=0):
        if brightness == 0:
            brightness = self._getBrightness(image)
        return True if brightness > self.MIN_DAY_BRIGHTNESS else False

    def isDayByChId(self, ch_id):
        return self._isDayMap[ch_id]

    def doModtionDetectByDiff(self, ch_id, isDebug=True):
        ti = time.time()
        currentGray = self._currentGrayMap[ch_id]
        previous1 = self._previousGrayMap.get(ch_id)
        previous2 = self._previousGray2Map.get(ch_id)
        height, width = currentGray.shape[:2]
        thresholdLowPoint = 5
        boxes = []

        if previous1 is not None:
            d1 = cv2.absdiff(currentGray, previous1)
            if previous2 is None:
                frameDelta = d1
                thresh = cv2.threshold(frameDelta, thresholdLowPoint, 255, cv2.THRESH_BINARY)[1]
            else:
                t1 = cv2.threshold(d1, thresholdLowPoint, 255, cv2.THRESH_BINARY)[1]
                d2 = cv2.absdiff(previous1, previous2)
                t2 = cv2.threshold(d2, thresholdLowPoint, 255, cv2.THRESH_BINARY)[1]

                k1 = cv2.bitwise_and(t1, t2)
                thresh = cv2.bitwise_xor(t1, k1)

            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, self.rectElement)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, self.rectElement)

            kkk, contours, hierachy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if isDebug:
                cv2.imshow('delta', cv2.resize(d1, (int(width / 2), int(height / 2))))
                cv2.imshow('thresh', cv2.resize(thresh, (int(width / 2), int(height / 2))))

            orgImg = self._currentFrameMap[ch_id]
            isDay = self.isDay(orgImg)

            offset = 10
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                if self._isValidBoxes((x, y, w, h), width, height, isDay):
                    x = x - offset if x - offset > 0 else x
                    y = y - offset if y - offset > 0 else y
                    w = w + offset if w + offset < width else w
                    h = h + offset if h + offset < height else h

                    boxes.append((x, y, w, h))
                    if isDebug:
                        self._show((x, y, w, h), currentGray)

            tracelogger.debug('motion detection : ' + str(time.time() - ti))

        return boxes

    def detectByBackgroundSubtractor(self, ch_id, diffScore=3, isDebug=True):
        ti = time.time()

        # orgImg = self._currentFrameMap[ch_id]
        currentGray = self._currentGrayMap[ch_id]
        orgImg=currentGray

        isDay = self._isDayMap[ch_id]
        height, width = orgImg.shape[:2]

        heightRate = height / self.BG_SUB_HEIGHT
        widthRate = width / self.BG_SUB_WIDTH

        isResize = False
        if heightRate > 1.2 or widthRate > 1.2:
            orgImg = cv2.resize(orgImg, (self.BG_SUB_WIDTH, self.BG_SUB_HEIGHT))
            width,height = (self.BG_SUB_WIDTH, self.BG_SUB_HEIGHT)
            isResize = True
        else:
            heightRate = 1
            widthRate = 1

        # frame = cv2.blur(orgImg, (5, 5))
        frame = orgImg
        boxes = []

        if self._fgbgMap.get(ch_id) == None:
            fgbg = cv2.createBackgroundSubtractorMOG2(history=70, detectShadows=False)
            # fgbg = cv2.createBackgroundSubtractorKNN(history=50, detectShadows=False)
            self._fgbgMap[ch_id] = fgbg
        else:
            fgbg = self._fgbgMap[ch_id]
        fgmask = fgbg.apply(frame, learningRate=-1)

        if isDebug:
            cv2.putText(fgmask, str(diffScore)[0:3] + ": detection count :" + str(len(boxes)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.imshow('fgmask', fgmask)
        maxDiffScore=15 if isDay else 60;
        if diffScore > maxDiffScore:
            return ([],False)

        diffScore = cv2.mean(fgmask)[0]
        if diffScore > (12 if isDay else 25):
        # if diffScore > (3 if isDay else 6):
            if isDebug:
                cv2.putText(fgmask, str(diffScore)[0:3], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.imshow('fgmask not', fgmask)
            return ([],False)

        threshold=self.THRESHOLD_LOW if isDay else  self.THRESHOLD_LOW_NIGHT

        if isDay:
            thresh = cv2.threshold(fgmask, threshold, 255, cv2.THRESH_BINARY)[1]
        else:
            #밤에는 너무 밝은것은 헤드라이트
            thresh = cv2.threshold(fgmask, threshold, threshold+60, cv2.THRESH_BINARY)[1]
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, self.rectElement)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        offset = 5 if isDay else 0
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if isDebug:
                cv2.rectangle(thresh,(x,y),((x+w),(y+h)),(255,255,255),1)
            (x, y, w, h) = (int(x * widthRate), int(y * heightRate), int(w * widthRate), int(h * heightRate))  # 좌표변환
            if self._isValidBoxes((x, y, w, h),( width* widthRate), height* heightRate,isDay):
                x = x - offset if x - offset > 0 else x
                y = y - offset if y - offset > 0 else y
                w = w + offset if w + offset < width else w
                h = h + offset if h + offset < height else h

                boxes.append((x, y, w, h))

        if isDebug:
            cv2.imshow('thresh', thresh)
            # cv2.putText(fgmask, str(diffScore)[0:3] + ": detection count :" + str(len(boxes)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            # cv2.imshow('fgmask', fgmask)

        tracelogger.debug('motion detection : ' + str(time.time() - ti) +  'detection count :' + str(len(boxes)))

        isValid=True
        if len(boxes) > ( self.MAX_DETECTION_COUNT if isDay else self.MAX_DETECTION_COUNT - 5):  # 탐지된 객체가 많을 경우 방금 화면변환된 확률이 높음
            isValid=False
        return (boxes,isValid)

    def detectByTraking(self, previouResult, ch_uuid):
        tt = time.time()
        image = self._currentFrameMap[ch_uuid]
        currentGray = self._currentGrayMap[ch_uuid]

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
                # else:
                #     newBoxes.append(_box)
        return [np.array(newBoxes), previouResult[1], previouResult[2]]

    def _isValidBoxes(self, rect, width, height, isDay):

        # if isDay==False:
        #     return self._isValidBoxesForNightCar(rect, width, height, isDay)
        min_width = self.MIN_WIDTH_DAY if isDay else self.MIN_WIDTH_NIGHT
        min_height = self.MIN_HEIGHT_DAY if isDay else self.MIN_HEIGHT_NIGHT

        max_width = width * self.MAX_WIDTH_RATE if isDay else width * self.MAX_WIDTH_RATE*1.3
        max_height = height * self.MAX_HEIGHT_RATE if isDay else height * self.MAX_HEIGHT_RATE *1.3

        (x, y, w, h) = rect

        if x < 0 or y < 0:
            return False
        if w > min_width and h > min_height \
                and ((w / h) > 10 or (h / w > 10)) == False \
                and w < max_width and h < max_height:
            return True
        else:
            return False

    def _isValidBoxesForNightCar(self, rect, width, height, isDay):
        min_width = self.MIN_WIDTH_DAY if isDay else self.MIN_WIDTH_NIGHT
        min_height = self.MIN_HEIGHT_DAY if isDay else self.MIN_HEIGHT_NIGHT

        (x, y, w, h) = rect
        if x < 0 or y < 0:
            return False
        if w > min_width and h > min_height \
                and w < width * 0.5 and h < height * 0.5:
            return True
        else:
            return False

    def _show(self, rect, gray):
        (x, y, w, h) = rect
        cv2.rectangle(gray.copy(), (x, y), (x + w, y + h), (0, 255, 0), 1)

    def enhanceContrast(self, org):
        '''
        contras
        :param org:
        :return:
        '''
        clahe = cv2.createCLAHE(2, (8, 8))
        l_channel, a_channel, b_channel = cv2.split(org)
        l_channel = clahe.apply(l_channel)
        a_channel = clahe.apply(a_channel)
        b_channel = clahe.apply(b_channel)
        return cv2.merge((l_channel, a_channel, b_channel))
