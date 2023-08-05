import logging
from service.va_service import VAService
from models.objectdetect import ObjectDetect
import numpy as np


from misc.MotionDetection_EXC import MotionDetection
from misc import labelmap_util
tracelogger = logging.getLogger('trace')
systemlogger = logging.getLogger('system')

class CCTVExcavatorVA(VAService):
    previousGrayFrames = {}
    previousFrames = {}
    diffscorethreshold = 0.2

    useMotionDetection = False

    def __init__(self, config, va_type, min_threshold=0.5):
        super(CCTVExcavatorVA, self).__init__(config, va_type)
        self.detector = ObjectDetect(self.enabled, config, 'cctvexc')
        self.min_score_threshold = config.getvalue(self.conf_prefix + 'min_score_threshold', min_threshold)
        self.motionDetection = MotionDetection()

    # def _set_lables(self, path_to_labels):
    #     labels = label_map_util.create_categories_from_labelmap(path_to_labels)
    #     return dict([(item['id'], item['name']) for item in labels])

    def _set_lables(self, path_to_labels):
        labels = labelmap_util.create_categories_from_labelmap(path_to_labels)
        return dict([(item['id'], item['name']) for item in labels])


    def aggregate_result(self, inference):
        boxes, scores, classes = inference
        valid = [idx for idx, score in enumerate(scores) if score > self.min_score_threshold ]

        if len(valid) > 0:
            valid_scores = scores[valid].tolist()
            valid_boxes = boxes[valid].tolist()
            valid_class = [self.label_map[int(a_class)] for a_class in classes[valid]]
            return [valid_boxes, valid_scores, valid_class]
        else:
            return [[],[],[]]


    def getInferenceResult(self, image):
        inferences = self.detector._inference(image)
        newInferences = []

        for inf in inferences:
            newInferences.append(self.aggregate_result(inf))

        return np.array(newInferences)

    def _execute(self, sc):

        image_by_ch = sc.get_in_by_vatype(self.is_support_vatype_fc)

        if len(image_by_ch) == 0 : return sc

        if self.useMotionDetection :
            images = []
            useDetections = []

            #### motion detection
            for n, row in enumerate(image_by_ch):
                image = row[1]
                ch_id = str(row[2])
                self.motionDetection.initByChannel(image, ch_id)
                isMotionDetected = self.motionDetection.isFrameChanged(ch_id, diffScoreThreshold=self.diffscorethreshold)

                if isMotionDetected == True:
                    images.append(image)
                    useDetections.append(True)

                else:
                    tracelogger.debug('skip detection ch_id:     [%s]', ch_id)
                    useDetections.append(False)

            ##### detection excavator
            detection_inf_result = []
            tmp_detection_inf_result = self.getInferenceResult(np.array(images))

            idx = 0

            for n2, ut in enumerate(useDetections):
                if ut == True:
                    detection_inf_result.append(tmp_detection_inf_result[idx])
                    idx = idx + 1

                else:
                    detection_inf_result.append(([],[],[]))

            for (ch_id, _, ch_uuid, cfg_json), inference in zip(image_by_ch, detection_inf_result):
                sc.set_out_by_ch(self.va_type, ch_id, inference)

        else:
            inf_result = self.getInferenceResult(image_by_ch[:,1].tolist())

            for (ch_id, _, _, cfg_json), inference in zip(image_by_ch, inf_result):
                sc.set_out_by_ch(self.va_type, ch_id, inference)

        return sc;



