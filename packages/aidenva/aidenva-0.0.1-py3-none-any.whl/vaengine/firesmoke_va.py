import logging
import cv2
import numpy as np
import os

from service.va_service import VAService
from models.objectdetect import ObjectDetect
from misc import labelmap_util

tracelogger = logging.getLogger('trace')
MotionBase = True


class ChangeDetector:
    def __init__(self, id=None):
        self.id = id
        self._frame_queue = []
        self._considering_frame_width = 1
        self._queue_size = self._considering_frame_width + 1# hardcoded
        self.diff_threshold = 0.15
        self.adapt_frame = 15

    def insert(self, item):
        if len(self._frame_queue) >= self._queue_size:
            del self._frame_queue[0]
        self._frame_queue.append(item)

    def __call__(self, file_path):
        if os.path.exists(file_path):
            video = cv2.VideoCapture(file_path)
            prev=None
            count = 0
            while True:
                ret, image = video.read()
                key = cv2.waitKey(1) & 0xFF
                if key == ord("s"):
                    count=count+300
                    video.set(cv2.CAP_PROP_POS_FRAMES, count)
                    continue
                if ret:
                    self.insert(cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (21, 21), 0))
                    self.isChnageImage(image)
                    # prev = image
                    # image = cv2.resize(image, _TEST_IMAGE_SIZE)
                    # frame_per_video.append(
                    #     [cv2.cvtColor(image, cv2.COLOR_RGB2BGR), None, type_to_bit[args.type], TEST_CH_ID_STR + "0"]
                    # )
                    # time_per_video.append(
                    #     datetime.timedelta(seconds=1/args.fps * (len(frame_per_video)+1))
                    # )
                else:
                    break
                count += 1
        video.release()

    def frame_diff_between(self, a, b):
        d1 = cv2.absdiff(a, b)
        thresh = cv2.threshold(d1, 5, 255, cv2.THRESH_BINARY)[1]

        return thresh
        # b = cv2.GaussianBlur(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY), (21, 21), 0)
    
    def run_in_batch(self, batches):
        results = []
        for b in batches:
            # ks = int(min(b.shape[:2]) * 0.03)
            # if ks % 2 == 0:
            #     ks += 1
            self.insert(cv2.GaussianBlur(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY), (21, 21), 0))
            results.append(self.get_moving_object())
        return results

    def run_single_image(self, image):
        self.insert(cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (21, 21), 0))
        return self.get_moving_object()

    def get_moving_object(self):
        
        if len(self._frame_queue) > 1:
            current_frame = self._frame_queue[-1]
            height, width = current_frame.shape[:2]

            m = min(height, width)
            m = int(m * 0.07)
            iter_ = min(len(self._frame_queue), self._considering_frame_width)
            
            thresh = self.frame_diff_between(current_frame, self._frame_queue[-2])
            difScore = cv2.mean((thresh > 0).astype(np.uint8))[0]
            if difScore > self.diff_threshold or self.adapt_time > 0:
                self._frame_queue.clear()
                if self.adapt_time > 0:
                    self.adapt_time -= 1
                else:
                    self.adapt_time = 15
                return []
            for i in range(iter_ - 1):
                thresh += self.frame_diff_between(current_frame, self._frame_queue[-2-i])
            # cv2.imshow('t', thresh)
            ekernel = np.ones((int(m/4), int(m/4)), np.uint8)
            kernel = np.ones((m, m), np.uint8)
            thresh = cv2.erode(thresh, ekernel, iterations = 1)
            thresh = cv2.dilate(thresh, kernel, iterations = 1)
            
            contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
            results =[]
            for c in contours:
                bbox = cv2.boundingRect(c)
                results.append([bbox[1] / height, bbox[0] / width, (bbox[1] + bbox[3]) / height, (bbox[0] + bbox[2]) / width])
            return results
            # return [cv2.boundingRect(c) for c in contours]
        else:
            return []


class FiresmokeVA(VAService):
    def __init__(self, config, va_type, min_threshold=0.5):
        super().__init__(config, va_type)
        self.detection = ObjectDetect(self.enabled, config, 'firesmoke')
        self.min_score_threshold = config.getvalue(self.conf_prefix + 'min_score_threshold', min_threshold)
        self.motion = {}#ChangeDetector()

    # def dominant_color(self, image_patch):
    #     hsv = cv2.cvtColor(image_patch, cv2.COLOR_BGR2HSV)
    #     hist = cv2.calcHist([hsv], [0], None, [180], [0, 256])

    def _set_lables(self, path_to_labels):
        labels = label_map_util.create_categories_from_labelmap(path_to_labels)
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
        if not MotionBase:
            inf_result = self.detection._inference(image_by_ch[:, 1].tolist())
            for (ch_id, _, _, cfg_json), inference in zip (image_by_ch, inf_result):
                sc.set_out_by_ch(self.va_type, ch_id, self.aggregate_result(inference))
        else:
            # inf_result = self.motion.run_in_batch(image_by_ch[:, 1].tolist())
            inf_result = []
            for ch_id, image, _, cfg_json in image_by_ch:
                if ch_id not in self.motion:
                    self.motion[ch_id] = ChangeDetector(ch_id)
                inf_result.append(self.motion[ch_id].run_single_image(image))
            for (ch_id, _, _, cfg_json), inference in zip (image_by_ch, inf_result):
                sc.set_out_by_ch(self.va_type, ch_id, [inference, [1 for i in range(len(inference))], ['fire' for i in range(len(inference))]])
        return sc

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
