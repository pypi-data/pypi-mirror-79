import cv2
import time
import logging

tracelogger = logging.getLogger('trace')

class MotionDetection:

    _currentFrameMap = {}
    _currentGrayMap = {}
    _previousFrameMap = {}
    _previousGrayMap = {}
    _previousGray2Map = {}

    IS_DEBUG = False

    def __init__(self, isDebug=False):
        self.IS_DEBUG = isDebug

    def initByChannel(self, image, ch_id):
        previousFrame = self._currentFrameMap.get(ch_id)

        self._currentFrameMap[ch_id] = image
        gray = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (15,15), 0)

        currentGray = self._currentGrayMap.get(ch_id)
        previousGray = self._previousGrayMap.get(ch_id)

        self._currentGrayMap[ch_id] = gray

        if currentGray is not None:
            self._previousGrayMap[ch_id] = currentGray

        if previousGray is not None:
            self._previousGray2Map[ch_id] = previousGray

        if previousFrame is not None:
            self._previousFrameMap[ch_id] = previousFrame


    def isFrameChanged(self, ch_id, diffScoreThreshold=0.5):
        valid_change = True
        gray = self._currentGrayMap[ch_id]
        thresholdLowPoint = 50
        _previousFrame = self._previousGrayMap.get(ch_id)
        t1 = time.time()

        if _previousFrame is not None:
            diff = cv2.absdiff(_previousFrame, gray)
            thresh = cv2.threshold(diff, thresholdLowPoint, 255, cv2.THRESH_BINARY)[1]
            diffScore = cv2.mean(thresh)[0]
            tracelogger.debug('diffscore :      ' + str(diffScore))

            if diffScore < diffScoreThreshold:
                valid_change = False
                tracelogger.debug('************ not big change *****' )

            self._previousGray2Map[ch_id] = _previousFrame

        # tracelogger.debug('[cctvexc   ]motion detection : ' + str(time.time() - t1))
        # tracelogger.debug('>>>>'+str(diffScore))

        return valid_change
