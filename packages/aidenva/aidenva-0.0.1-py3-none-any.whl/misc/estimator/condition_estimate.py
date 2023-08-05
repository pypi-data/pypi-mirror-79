import random
import logging
import numpy as np
import copy

from misc.estimator.cqueue import cQueue

random.seed(random.randint(0, 10000))

logger = logging.getLogger(__name__)

class ConditionEstimator:

    def __init__(self, hw, queue_size=10, activation_per_queue=0.3, iou_threshold=0.5):
        self.area_dict = dict()
        self.queue_size = queue_size
        self.activation_per_queue = activation_per_queue
        self.iou_threshold = iou_threshold
        self.is_alarm_start = False
        self.alarm_start_time = None
        self.im_height = hw[0]
        self.im_width = hw[1]
        self.lastbound = []

    def _reset(self):
        self.area_dict.clear()

    def _add_candidate(self, lbox):
        for key in self.area_dict:
            last_dbox = self.area_dict[key].peek()
            # print('-----> check ', last_dbox is not None, ' iou:', bb_intersection_over_union(last_dbox, lbox), ' result ', bb_intersection_over_union(last_dbox, lbox) > self.iou_threshold)
            if last_dbox is not None and self.bb_intersection_over_union(last_dbox, lbox) > self.iou_threshold:
                self.area_dict[key].enqueue(lbox)
                # print('add exist liedown :', self.area_dict)
                # activation ratio 계산
                if (self.area_dict[key].q_size() / self.queue_size > self.activation_per_queue):
                    return lbox
                else :
                    return None

        q = cQueue(self.queue_size)
        q.enqueue(lbox)
        self.area_dict[random.random()] = q
        # print('add new liedown', lbox, self.area_dict)
        return None

    def _decrease_candidate(self, detect_boxs):

        for key in self.area_dict.keys():
            last_dbox = self.area_dict[key].peek()
            find = False
            for box in detect_boxs:
                if last_dbox is not None and (self.bb_intersection_over_union(last_dbox, box) >= self.iou_threshold):
                    find = True

            # 관심 area에 맞지 않은 rect는 제외
            if find == False:
                self.area_dict[key].dequeue()

        self.area_dict = dict((k, v) for k, v in self.area_dict.items() if self.area_dict[k].q_size() > 0)
        # print('decrease end:', self.area_dict)

    def _find_candidate(self, dbox):
        for key in self.area_dict:
            last_dbox = self.area_dict[key].peek()
            if last_dbox is not None:
                if(self.bb_intersection_over_union(last_dbox, dbox) > self.iou_threshold):
                    # print('find exist key: %s, qsize: %d, ratio: %.2f, th: %.2f' % (key, self.area_dict[key].q_size(), self.area_dict[key].q_size() / self.queue_size, self.bb_intersection_over_union(last_dbox, dbox)))
                    if(self.area_dict[key].q_size()/self.queue_size > self.activation_per_queue):
                        # 후보군에서 빼준다.
                        self.area_dict[key].dequeue()
                        return dbox
        return None


    def estimate(self, detect_boxs, candidate_boxs, cur_frame=0):
        logger.debug('detect: %d candidate: %d', len(detect_boxs), len(candidate_boxs))

        detections = list()
        if self.queue_size > 0:
            if len(candidate_boxs) > 0:
                for lbox in candidate_boxs:
                    box = self._add_candidate(lbox)
                    if box is not None:
                        detections.append(box)

            if len(detect_boxs) > 0:
                for dbox in detect_boxs:
                    v = self._find_candidate(dbox)
                    if v is not None:
                        detections.append(v)

            detect_boxs.extend(candidate_boxs)

            if len(detect_boxs) > 0 :
                self._decrease_candidate(detect_boxs)
        else:
            detections.extend(candidate_boxs)

        # 이전 detection box에 동일한 위치 bound box가 있는 경우 skip
        _last = copy.copy(detections)

        if len(self.lastbound) > 0:
            for l_box in self.lastbound:
                for idx, c_box in enumerate(detections):
                    if np.array_equal(l_box, c_box):
                        del detections[idx]

        self.lastbound = _last

        return detections

    def bb_intersection_over_union(self, bb1, bb2):
        # ymin, xmin, ymax, xmax = box
        # (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
        #                               ymin * im_height, ymax * im_height)

        (bb1_top, bb1_left, bb1_bottom, bb1_right) = bb1
        (bb2_top, bb2_left, bb2_bottom, bb2_right) = bb2

        # coordiante position
        (bb1_left, bb1_right, bb1_top, bb1_bottom) = (bb1_left * self.im_width, bb1_right * self.im_width, bb1_top * self.im_height, bb1_bottom * self.im_height)
        (bb2_left, bb2_right, bb2_top, bb2_bottom) = (bb2_left * self.im_width, bb2_right * self.im_width, bb2_top * self.im_height, bb2_bottom * self.im_height)

        # assert bb1['x1'] < bb1['x2']
        # assert bb1['y1'] < bb1['y2']
        # assert bb2['x1'] < bb2['x2']
        # assert bb2['y1'] < bb2['y2']

        assert bb1_left < bb1_right
        assert bb1_top < bb1_bottom
        assert bb2_left < bb2_right
        assert bb2_top < bb2_bottom

        # determine the coordinates of the intersection rectangle
        x_left = max(bb1_left, bb2_left)
        y_top = max(bb1_top, bb2_top)
        x_right = min(bb1_right, bb2_right)
        y_bottom = min(bb1_bottom, bb2_bottom)

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        # The intersection of two axis-aligned bounding boxes is always an
        # axis-aligned bounding box
        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        # compute the area of both AABBs
        bb1_area = (bb1_right - bb1_left) * (bb1_bottom - bb1_top)
        bb2_area = (bb2_right - bb2_left) * (bb2_bottom - bb2_top)

        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
        assert iou >= 0.0
        assert iou <= 1.0
        return iou

if __name__ == '__main__':
    c = ConditionEstimator( (480, 640))
    c.bb_intersection_over_union()