import logging
import random
import math
import cv2
import statistics
from service import constants as const
from service.constants import LOITERING_VA
from service.va_service import VAService
from models.objectdetect import ObjectDetect
import misc.detection_utils  as utils
import numpy as np
import time
import os
from collections import deque
from misc.deep_sort import nn_matching
from misc.deep_sort.detection import Detection
from misc.deep_sort.tracker import Tracker
from misc.deep_sort.detection import Detection
from misc.application_util import preprocessing
from models.classify import Classify
from misc import labelmap_util
from misc.loitering.loitering_tracker import LoieringTracker
import warnings
from pprint import pprint
warnings.filterwarnings("ignore")
tracelogger = logging.getLogger('trace')
systemlogger = logging.getLogger('system')



class LoiteringVA(VAService):

    IMAGE_SIZE = (64, 128)
    IS_DEBUG=True
    TRACKING_BUDGET_COUNT=1000
    MAX_BATCH_SIZE=32
    frameCount=0
    elapseTimeCheckQueue = deque(maxlen=100)
    trackerDict={}

    # metric = nn_matching.NearestNeighborDistanceMetric("euclidean", 0.5,1000)
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", 0.5,TRACKING_BUDGET_COUNT)
    colors = [(np.random.randint(256),np.random.randint(256),np.random.randint(256))
              for i in range(TRACKING_BUDGET_COUNT)]

    def __init__(self, config, va_type, min_threshold=0.5):
        super().__init__(config, va_type)
        self.IS_DEBUG=self.config.getbool('debug')
        self.loieringTracker=LoieringTracker(is_debug=self.IS_DEBUG)

    def _set_lables(self, path_to_labels):
        labels = labelmap_util.create_categories_from_labelmap(path_to_labels)
        return dict([(item['id'], item['name']) for item in labels])

    def _execute(self, sc):
        start = time.time()
        image_by_ch = sc.get_in_by_vatype(self.is_support_vatype_fc)

        # 처리할 정보가 없는 경우 return
        if len(image_by_ch) == 0: return sc
        self.frameCount  += 1
        inf_result=sc.get_out_by_vatype(const.TRACKING_VA)
        inf_result=self.loieringTracker.get_loitering_object_and_add_track(image_by_ch,inf_result)

        if self.frameCount > 1000000000:
            self.frameCount = -1

        for (ch_id, _, ch_uuid, cfg_json), inference  in zip(image_by_ch, inf_result ):
            sc.set_out_by_ch(self.va_type, ch_id, inference)

        if tracelogger.isEnabledFor(10):
            self.elapseTimeCheckQueue.append((time.time() - start) * 1000)
            tracelogger.debug('elapsed time avg [%.4f]', np.mean(self.elapseTimeCheckQueue))
        tracelogger.debug('LoiteringVA elapsed time [%.4f]', time.time() - start)

        return sc;

