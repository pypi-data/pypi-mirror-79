from misc.loitering.track import Track
import time
import cv2
import numpy as np
import logging
tracelogger = logging.getLogger('trace')

class LoieringTracker:

    UNIT_FRAME_SEC=5  # 단위 프레임 시간
    MONITORING_SECONDS= UNIT_FRAME_SEC * 4
    UNIT_FRAME_PASS_RATE=0.3
    MAX_TRACKING_OBJECT=1000
    MIN_PASS_UNIT_RATE=0.7
    MIN_INTERSECTION_AREA_RATE=0.5
    MIN_FRAME_COUNT=10
    track_dic={}
    IS_DEBUG=False
    def __init__(self,is_debug=False):
        self.IS_DEBUG=is_debug

    def get_loitering_object_and_add_track(self,image_by_ch,inf_result):
        new_inf_result=[]
        currentTime=time.time()
        unit_count=int(self.MONITORING_SECONDS / self.UNIT_FRAME_SEC)

        for n, row in enumerate(image_by_ch):
            image = row[1]
            height, width = image.shape[:2]
            ch_id = str(row[2])
            roi=self.get_roi(row)

            if self.IS_DEBUG:
                roi2=[ (x*width,y*height)   for (x , y) in roi]
                # cv2.rectangle(image,(int(roi[1]*width) ,int (roi[0]  *height) ) , (int(roi[3]*width),int(roi[2]*height)) ,(255,255,0))
                cv2.polylines(image,[np.array(roi2,np.int32) .reshape((-1,1,2))],True,(0,255,255))
            new_track_list_by_ch = []
            boxes = []
            scores = []
            classes = []
            total_frame_count_in_monitoring_seconds=0

            if self.track_dic.get(ch_id) is not None:
                for track in self.track_dic.get(ch_id):
                    if currentTime-track.created_time < self.MONITORING_SECONDS:  ##  모니터링 시간 내에 발생한 이벤트만 추출
                        new_track_list_by_ch.append(track)
                        if track.id==str(self.MAX_TRACKING_OBJECT):
                            total_frame_count_in_monitoring_seconds+=1

            avg_frame_count_per_unit_sec= int(total_frame_count_in_monitoring_seconds / self.MONITORING_SECONDS) * self.UNIT_FRAME_SEC
            min_pass_frame_count=int(avg_frame_count_per_unit_sec*self.UNIT_FRAME_PASS_RATE)

            result=inf_result[n]

            for n,box in enumerate(result[0]):
                if self.IS_DEBUG:
                    cv2.circle(image,(int(((box[1]+box[3])/2)*width),int(((box[0]+box[2])/2)*height)),5,(255,255,0),2)
                # area=self._getArea(box)
                # if self._boxesIntersect(roi, box) and self. _getIntersectionArea(roi, box)/area> self.MIN_INTERSECTION_AREA_RATE:

                if self._isInnerBox(box,row):
                    uuid=result[2][n]
                    score=result[1][n]
                    firstDetectedTime=None # 해당 객체 최초 탐지 시간
                    block_result=np.zeros(unit_count)
                    if self.IS_DEBUG:
                        cv2.rectangle(image,(int(box[1]*width) ,int (box[0]  *height) ) , (int(box[3]*width),int(box[2]*height)) ,(255,255,255),thickness=5)

                    for track2 in new_track_list_by_ch:
                        if uuid==track2.id:
                            time_block_idx=int(int(track2.created_time/self.UNIT_FRAME_SEC) % unit_count)
                            block_result[time_block_idx]+=1
                            if firstDetectedTime is None:
                                firstDetectedTime=track2.created_time

                    # if totalFrameCount>self.MIN_FRAME_COUNT and count/totalFrameCount>self.MIN_PASS_UNIT_RATE:

                    if self._isOK(total_frame_count_in_monitoring_seconds,block_result,min_pass_frame_count,firstDetectedTime,currentTime):
                        if self.IS_DEBUG:
                            cv2.rectangle(image,(int(box[1]*width) ,int (box[0]  *height) ) , (int(box[3]*width),int(box[2]*height)) ,(0,0,255),thickness=10)
                        boxes.append(box)
                        scores.append(score)
                        classes.append(uuid)

                    new_track_list_by_ch.append(Track(uuid,box,score,1))

            new_track_list_by_ch.append(Track(str(self.MAX_TRACKING_OBJECT),(0,0,0,0),1,1)) # counter 용 tracker
            self.track_dic[ch_id]=new_track_list_by_ch
            new_inf_result.append((boxes, scores, classes))

            tracelogger.debug('loitering check elapse time : {} ms'.format (int(time.time()-currentTime)*1000 ))
            if self.IS_DEBUG:
                cv2.imshow('>>', cv2.resize(image, (1280, 720)))
        return new_inf_result

    def _isOK(self,totalFrameCount,block_result,min_pass_frame_count,firstDetectedTime,currntTime):
        if firstDetectedTime is not None and totalFrameCount>self.MIN_FRAME_COUNT:
            tracelogger.debug('>>totalFrameCount>self.MIN_FRAME_COUNT >>>>>>>>>' + str(currntTime-firstDetectedTime))
            minPassUnitCnt= ((self.MONITORING_SECONDS / self.UNIT_FRAME_SEC) * self.MIN_PASS_UNIT_RATE) # 최소 단위 유닛 통과 갯수
            passUnitCnt=0
            for rr in block_result:
                if rr>min_pass_frame_count:
                    passUnitCnt+=1
            if currntTime-firstDetectedTime >self.MONITORING_SECONDS*0.8 and   passUnitCnt>minPassUnitCnt:
                return True
        return False

    def get_roi(self,image_by_ch_by_row):
        #(top left x, top left y, width, height)
        image = image_by_ch_by_row[1]
        height, width = image.shape[:2]
        ch_id = str(image_by_ch_by_row[2])
        # return (0.3, 0.4, 0.8, 0.6)
        # pp=[ (0.5,0.5),(0.8,0.5),(0.8,0.8),(0.5,0.8) ,(0.2,0.6)]
        # pp=[ (0.5,0.5),(0.9,0.5),(0.8,1),(0.4,1) ,(0.2,0.6) ]
        pp=[ (1280/1280,81/720),(782/1280,85/720),(312/1280,119/720),(96/1280,302/720) ,(910/1280,544/720),(1280/1280,555/720) ]
        return pp

    def _getArea(self,box):
        return (box[2] - box[0] ) * (box[3] - box[1]  )

    def _isInnerBox(self,box,row):
        roi=self.get_roi(row)

        points=[(box[3],box[2]),(box[1],box[0]),(box[3],box[0]),(box[1],box[2])]

        for pp in points:
            if not self.point_inside_polygon(pp[0],pp[1],roi):
                return False

        if self.point_inside_polygon((box[3]+box[1])/2,(box[2]+box[0])/2,roi):  # check box center point
            return True
        else:
            return False

    def point_inside_polygon(self,x,y,poly):
        n = len(poly)
        inside =False
        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside