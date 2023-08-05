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
from collections import defaultdict

warnings.filterwarnings("ignore")
tracelogger = logging.getLogger('trace')
systemlogger = logging.getLogger('system')



class TrackingVA(VAService):

    IMAGE_SIZE = (64, 128)
    # IMAGE_SIZE = (128, 256)
    IS_DEBUG=True
    TRACKING_BUDGET_COUNT=1000
    MAX_BATCH_SIZE=32
    frameCount=0
    elapseTimeCheckQueue = deque(maxlen=100)


    # metric = nn_matching.NearestNeighborDistanceMetric("euclidean", 0.5,1000)
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", 0.5,TRACKING_BUDGET_COUNT)
    colors = [(np.random.randint(256),np.random.randint(256),np.random.randint(256))
              for i in range(TRACKING_BUDGET_COUNT)]
    trackerDict={}

    def __init__(self, config, va_type):
        super().__init__(config, va_type)
        self.classify = Classify(self.enabled, config, 'tracking', in_shape= self.IMAGE_SIZE )
        self.IS_DEBUG=self.config.getbool('debug')

    def _set_lables(self, path_to_labels):
        labels = labelmap_util.create_categories_from_labelmap(path_to_labels)
        return dict([(item['id'], item['name']) for item in labels])

    def extract_features(self, detection_results, image_by_ch):
        crop_images = []
        features=[]
        for n, row in enumerate(image_by_ch):
            image = row[1]
            height, width = image.shape[:2]
            result = detection_results[n]
            if result is not None and len(result) > 0:
                crop_images.extend([cv2.resize( image[int(box[0] * height):int(box[2] * height), int(box[1] * width):int(box[3] * width)], self.IMAGE_SIZE) for box in result[0]])

        total_box_size=len(crop_images)
        tmp_features =list()
        for n in range(0,total_box_size,self.MAX_BATCH_SIZE):
            if n+self.MAX_BATCH_SIZE<total_box_size:
                batch1=crop_images[n :(n+self.MAX_BATCH_SIZE)]
            else:
                batch1=crop_images[n:total_box_size]

            tmp_features.extend(self.classify._inference(np.array(batch1)))

        idx = 0
        for k in range(len(image_by_ch)):
            if len(detection_results[k][0]) != 0:
                features.append( tmp_features[idx:idx + len(detection_results[k][0])])
            else:
                features.append([])
            idx += len(detection_results[k][0])
        return features



    def _execute(self, sc):
        start = time.time()
        image_by_ch = sc.get_in_by_vatype(self.is_support_vatype_fc)

        # 처리할 정보가 없는 경우 return
        if len(image_by_ch) == 0: return sc

        detection_results=sc.get_out_by_vatype(const.DETECT_VA)
        features=self.extract_features(detection_results, image_by_ch)
        inf_result = self.execute_mot(detection_results, features, image_by_ch )

        for (ch_id, _, ch_uuid, cfg_json), inference  in zip(image_by_ch, inf_result ):
            sc.set_out_by_ch(self.va_type, ch_id, inference)

        if tracelogger.isEnabledFor(10):
            self.elapseTimeCheckQueue.append((time.time() - start) * 1000)
            tracelogger.debug('elapsed time avg [%.4f]', np.mean(self.elapseTimeCheckQueue))
            tracelogger.debug('LoiteringVA elapsed time [%.4f]', time.time() - start)

        return sc;

    def execute_mot(self, detection_results, features, image_by_ch):
        inf_result = []
        for n, row in enumerate(image_by_ch):
            image = row[1]
            height, width = image.shape[:2]
            ch_id = str(row[2])
            feature = features[n]
            result = detection_results[n]
            boxes = []
            scores = []
            classes = []

            if result is not None and len(result) > 0:
                tracker = self.trackerDict.get(ch_id)
                if tracker is None:
                    tracker = Tracker(self.metric)
                detection_list = []
                for y in range(len(result[0])):
                    _scores = result[1][y]
                    box = result[0][y]
                    tlx = int(box[1] * width)
                    tly = int(box[0] * height)
                    brx = int(box[3] * width)
                    bry = int(box[2] * height)
                    if width != 0 and height != 0 and brx - tlx > 0 and result[2][y] == 'person':
                        detection_list.append(Detection(np.array([tlx, tly, brx - tlx, bry - tly]), _scores, feature[y]))
                        # detection_list.append(Detection(np.array([tlx,tly,brx-tlx,bry-tly]), np.array(1),feature[y]))
                        # detection_list.append(Detection(np.array([tlx,tly,brx-tlx,bry-tly]), np.array(1),np.ones((0,))))

                if len(detection_list)>0:
                    _boxes = np.array([d.tlwh for d in detection_list])
                    _scores = np.array([d.confidence for d in detection_list])
                    indices = preprocessing.non_max_suppression(_boxes, 1, _scores)
                    detections = [detection_list[i] for i in indices]

                    ti = time.time()
                    tracker.predict()
                    tracker.update(detections)

                    tracelogger.debug('tracker.update time :' + str((time.time() - ti) * 1000) )
                    # if len(detections)!=len( [ track for track in tracker.tracks if   track.is_confirmed() and  track.time_since_update <=1 ]  ):
                    #     print(len(detections) ,'>>>>>>>>>>>>>>>>>>>>.', len( [ track for track in tracker.tracks if   track.is_confirmed() and  track.time_since_update <=1 ]  ))

                    for idx, track in enumerate(tracker.tracks):
                        if not track.is_confirmed() or track.time_since_update > 1:
                            continue
                        bbox = track.to_tlwh()
                        tlx = float(bbox[0] / width)
                        tly = float(bbox[1] / height)
                        brx = float((bbox[0] + bbox[2]) / width)
                        bry = float(int(bbox[1] + bbox[3]) / height)
                        scores.append(1)
                        classes.append(track.track_id) # tracking uuid
                        boxes.append((tly, tlx, bry, brx))

                        if self.IS_DEBUG:
                            cv2.rectangle(image, (int(bbox[0]), int(bbox[1])),
                                          (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), self.colors[track.track_id],
                                          2)
                            cv2.putText(image, str(track.track_id), (int(bbox[0]), int(bbox[1])),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                inf_result.append((boxes, scores, classes))
                self.trackerDict[ch_id] = tracker

                if self.IS_DEBUG:
                    cv2.imshow('>>', cv2.resize(image, (1280, 720)))

        return inf_result

