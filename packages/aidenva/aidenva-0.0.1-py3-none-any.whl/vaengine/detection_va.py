import logging

from service.va_service import VAService
from models.objectdetect import ObjectDetect
from misc import labelmap_util

tracelogger = logging.getLogger('trace')

class DetectionVA(VAService):
    def __init__(self, config, va_type, min_threshold=0.5):
        super(DetectionVA, self).__init__(config, va_type)
        self.detection = ObjectDetect(self.enabled, config, 'detect')
        self.min_score_threshold = config.getvalue(self.conf_prefix + 'min_score_threshold', min_threshold)


    def _set_lables(self, path_to_labels):
        labels = labelmap_util.create_categories_from_labelmap(path_to_labels)
        return dict([(item['id'], item['name']) for item in labels])

    '''
        get_in_by_vatype_gen() generator examples  
    '''
    # def _execute(self, sc):
    #     start = time.time()
    #     for ch_idx, image_np, width_height, va in sc.get_in_by_vatype_gen(self.is_support_vatype_fc):
    #         inf_result = self.detection.inference(np.expand_dims(image_np, axis=0))
    #         sc.set_out_ch(const.DETECT_VA, ch_idx, inf_result[0])
    #
    #     tracelogger.debug('[%s] total detection inference elapesed: [%.2f], images [%d]',
    #                       const.VA_TYPES[self.va_type], (time.time() - start), ch_idx)
    #
    #     return sc;

    def _execute(self, sc):
        # channel 순서를 가지고 있는 image numpy
        # list -> [ch_idx, image]
        image_by_ch  = sc.get_in_by_vatype(self.is_support_vatype_fc)

        # 처리할 정보가 없는 경우 return
        if len(image_by_ch) == 0: return sc

        # debug.show_images(extract_by_ch[:, 1].tolist())

        # image array만 inference 처리
        inf_result = self.detection._inference(image_by_ch[:, 1].tolist())

        for (ch_id, _, _, cfg_json), inference in zip (image_by_ch, inf_result):
            sc.set_out_by_ch(self.va_type, ch_id, self.aggregate_result(inference))

        return sc;

    def aggregate_result(self, inference):
        boxes, scores, classes = inference

        valid = [idx for idx, score in enumerate(scores) if score > self.min_score_threshold]
        if len(valid) > 0:
            valid_scores = scores[valid].tolist()
            valid_boxes  = boxes[valid].tolist()
            valid_class = [self.label_map[int(a_class)] for a_class in classes[valid]]
            return [valid_boxes, valid_scores, valid_class]
        else: # invalid image
            return [[],[],[]]
