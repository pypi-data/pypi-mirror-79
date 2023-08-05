from typing import DefaultDict
import cv2

from models.classify import Classify
from service import constants as const
from service.va_service import VAService
import time
import misc.detection_utils  as utils
import logging
import json
from collections import defaultdict
import numpy as np
from misc import labelmap_util
tracelogger = logging.getLogger('trace')
systemlogger = logging.getLogger('system')

class ClusterVA(VAService):
    
    def __init__(self, config, va_type):
        super(ClusterVA, self).__init__(config, va_type)
        self.threshold_people =  config.getvalue(self.conf_prefix + 'threshold_people', 3)
        # 이미지를 grid map으로 나누어 해당 그리드 셀 안에 n명 이상 들어가면 알람
        self.grid_map = (8, 12) # h, w
        # n명이 cluster rectangle 사이즈 만큼 군집해있으면 알람
        self.cluster_rectangle = (100, 100) # h, w
        # unsupervised clustering method DBSCAN based
        mode = 'cluster_rectangle'
        mode_mapper = {
            'cluster_rectangle': self.detect_cluster_rectangle,
            'grid_map': self.detect_grid_map
        }
        self.cluster_function = mode_mapper[mode]

    # def _set_lables(self, path_to_labels):
    #     labels = label_map_util.create_categories_from_labelmap(path_to_labels)
    #     return dict([(item['id'], item['name']) for item in labels])
    def _set_lables(self, path_to_labels):
        labels = labelmap_util.create_categories_from_labelmap(path_to_labels)
        return dict([(item['id'], item['name']) for item in labels])
    def get_center_xy(self, boxes):
        return np.stack([
            (boxes[:, 1] + boxes[:, 3]) / 2,
            (boxes[:, 0] + boxes[:, 2]) / 2], axis=1)
        # y, x, y, x
        # x, y
        return (box[1] + box[3]) / 2, (box[0] + box[2]) / 2

    def to_origin_size(self, boxes, image_size):
        boxes[:, [0, 2]] *= image_size[0]
        boxes[:, [1, 3]] *= image_size[1]
        return boxes
        # y, x, y, x
        return box[0] * image_size[0], box[1] * image_size[1], box[2] * image_size[0], box[3] * image_size[1]

    def points_to_cell(self, points):
        # points (num of points, 2(x,y))
        pos_points = np.stack(
            [points[:, 0] + self.cluster_rectangle[1],
            points[:, 1] + self.cluster_rectangle[0]], axis=1)
        neg_points = np.stack(
            [points[:, 0] - self.cluster_rectangle[1],
            points[:, 1] - self.cluster_rectangle[0]], axis=1)

        # x, y, x, y
        first_boxes = np.concatenate([
            points, pos_points
        ], axis=1)

        second_boxes = np.concatenate([
            neg_points, points
        ], axis=1)

        third_boxes = np.copy(first_boxes)
        third_boxes[:, [0, 2]] -= self.cluster_rectangle[1]

        fourth_boxes = np.copy(second_boxes)
        fourth_boxes[:, [0, 2]] += self.cluster_rectangle[1]
        boxes = np.concatenate([
            first_boxes, second_boxes, third_boxes, fourth_boxes
        ], axis=0)
        # neg_check = np.sum(boxes >= 0, axis=1)
        # boxes = boxes[neg_check == 4]
        return boxes

    def detect_grid_map(self, person_detections, image_size):
        section_h, section_w = [s / g for s, g in zip(image_size, self.grid_map)]
        results = defaultdict(list)
        boxes, _, classes = person_detections
        classname_filter = [c == 'person' for c in classes]
        boxes = np.asarray(boxes.tolist())[classname_filter]

        origin_box = self.to_origin_size(np.copy(boxes), image_size)
        xy = self.get_center_xy(origin_box)
        xy[:, 0] = xy[:, 0] // section_w + 1
        xy[:, 1] = xy[:, 1] // section_h + 1
        for box, xy_ in zip(boxes, xy):
            results[(xy_[0], xy_[1])].append(box)
        
        cluster_cells = []
        dummy_scores = []
        dummy_classes = []
        for _, boxes in results.items():
            if len(boxes) >= self.threshold_people:
                # boxes, 4(y, x, y, x)
                boxes = np.asarray(boxes)
                boxes = boxes[:, [0, 2, 1, 3]]
                ymax, ymin = np.amax(boxes[:, :2]), np.amin(boxes[:, :2])
                xmax, xmin = np.amax(boxes[:, 2:]), np.amin(boxes[:, 2:])
                cluster_cells.append([ymin, xmin, ymax, xmax])
                dummy_classes.append('cluster')
                dummy_scores.append(1.0)
        
        return [cluster_cells, dummy_scores, dummy_classes]

    def detect_cluster_rectangle(self, person_detections, image_size):
        boxes, _, classes = person_detections
        # print('classes: ', classes)
        classname_filter = [c == 'person' for c in classes]
        # print(type(boxes))
        boxes = np.asarray(boxes.tolist())[classname_filter]

        origin_box = self.to_origin_size(np.copy(boxes), image_size)
        xy = self.get_center_xy(origin_box)
        
        # xyxy = np.concatenate([xy, xy], axis=1)
        # num of boxes, 4(xyxy)
        cells = self.points_to_cell(xy)
        # cells = np.transpose(cells)
        # num of boxes, num of points, 2
        min_cells = cells[:, None, :2] <= xy
        min_cells = np.sum(min_cells, axis=2) == 2
        max_cells = cells[:, None, 2:] >= xy
        max_cells = np.sum(max_cells, axis=2) == 2
        # num of boxes, num of points
        cells = np.logical_and(min_cells, max_cells)
        # print(cells)
        cells = cells[np.sum(cells, axis=1) >= self.threshold_people]
        if cells.shape[0] == 0:
            return [[], [], []]
        # # num of boxes
        num_of_points_per_box = np.sum(cells, axis=1)

        clusters = [[] for _ in range(cells.shape[0])]
        # clusterid_per_point = {}
        for point_index in range(xy.shape[0]):
            if np.sum(cells[:, point_index]) > 0:
                # num_of_points_per_box = np.sum(cells, axis=1)
                filtered_num_of_points_per_box = num_of_points_per_box * cells[:, point_index]
                max_value = np.amax(filtered_num_of_points_per_box)
                
                clusterids = np.argwhere(filtered_num_of_points_per_box == max_value)
                clusterids = clusterids.flatten().tolist()
                # print(clusterids)
                # cells[:, point_index] = 0
                # cells[clusterid, point_index] = True
                for clusterid in clusterids:
                    clusters[clusterid].append(point_index)
        
        results = []
        dummy_scores = []
        dummy_classes = []
        boxes = np.asarray(boxes)
        boxes = boxes[:, [0, 2, 1, 3]]
        for cluster in clusters:
            if len(cluster) >= self.threshold_people:
                filtered_boxes = boxes[cluster]
                ymax, ymin = np.amax(filtered_boxes[:, :2]), np.amin(filtered_boxes[:, :2])
                xmax, xmin = np.amax(filtered_boxes[:, 2:]), np.amin(filtered_boxes[:, 2:])
                results.append([ymin, xmin, ymax, xmax])
                dummy_classes.append('cluster')
                dummy_scores.append(1.0)

        return [results, dummy_scores, dummy_classes]

    # sc.set_out_by_ch(self.va_type, ch_id, self.aggregate_result(inference))
    # [valid_boxes, valid_scores, valid_class]
    def _execute(self, sc):

        t1 = time.time()
        # channel 순서를 가지고 있는 image numpy
        images_by_ch = sc.get_in_by_vatype(self.is_support_vatype_fc)
        # 처리할 정보가 없는 경우 return
        if len(images_by_ch) == 0: return sc
        # person detection 결과 (channel 순서로 detection 저장 )
        detect_by_ch = sc.get_out_by_vatype(const.DETECT_VA)
        # print(detect_by_ch)
        # return
        for (ch, image, ch_id, cfg_json) in images_by_ch:
            detect = detect_by_ch[ch]
            if len(detect[0]) >= self.threshold_people:
                sc.set_out_by_ch(self.va_type, ch, self.cluster_function(detect, image.shape[:2]))
            else:
                sc.set_out_by_ch(self.va_type, ch, [[], [], []])
            
        tracelogger.debug('ClusterVA elapse time :[%.2f] ', (time.time() - t1))
        return sc
