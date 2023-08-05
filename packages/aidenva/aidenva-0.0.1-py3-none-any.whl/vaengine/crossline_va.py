import logging
import math
import cv2
from service import constants as const
from service.va_service import VAService
import numpy as np
import time
from collections import deque
from misc import labelmap_util
import warnings

warnings.filterwarnings("ignore")
tracelogger = logging.getLogger('trace')
systemlogger = logging.getLogger('system')


def get_crossline( image_by_ch_by_row):
    #(top left x, top left y, width, height)
    image = image_by_ch_by_row[1]
    height, width = image.shape[:2]
    ch_id = str(image_by_ch_by_row[2])
    pp=[ (0.3,0.4), (0.8, 0.6) ]
    direction_point=  [( 0.2, 0.8) , ( 0.6, 0.1)]
    # pp=[ (int(width *0.3),int(height *0.4)), ( int(width *0.8), int(height *0.6)) ]
    # direction_point=  [( int(width *0.2), int(height *0.8)) , ( int(width *0.6), int(height *0.1))]
    return (pp,direction_point)


def get_crosspt( x11,y11, x12,y12, x21,y21, x22,y22):
    if x12==x11 or x22==x21:
        return None
    m1 = (y12 - y11) / (x12 - x11)
    m2 = (y22 - y21) / (x22 - x21)
    if m1==m2:
        return None
    cx = (x11 * m1 - y11 - x21 * m2 + y21) / (m1 - m2)
    cy = m1 * (cx - x11) + y11

    if np.maximum(x11,x12)<cx or np.minimum(x11,x12)>cx:
        return None

    if np.maximum(x21,x22)<cx or np.minimum(x21,x22)>cx:
        return None
    return cx, cy

def transform_point(p1,width,height):
    return (int(p1[0]*width),int(p1[1]*height))

def get_angle(p1, p2):
    rad = math.atan2(p2[1] - p1[1], p2[0] - p1[0]) *180 /math.pi;
    rad+=90 # p1 기준 12 시 방향이 0 도
    if rad <0:
        rad+=360
    return rad ;
'''
    p1,p2 가 만드는 직선에 대한 o1의 위치 시계방향쪽이면 +
'''
def direction_in_line(p1,p2,o1):
    gradient=(p2[1]-p1[1])/(p2[0]-p1[0])
    kkd=o1[1]-p1[1]- (gradient*(o1[0]-p1[0]))
    if kkd<0:
        return -1
    else:
        return 1

class TrackingHistoryVo():
    uuid = -1
    max_history_size=100
    boxes=None
    last_update_time=None
    max_live_sec=600
    cross_line=False

    def __init__(self,uuid,max_live_sec=600):
        self.uuid=uuid
        self.max_live_sec=max_live_sec
        self.last_update_time=time.time()
        self.boxes=deque(maxlen=self.max_history_size)

    def add(self, box):
        self.boxes.append(box)
        self.last_update_time=time.time()

    def set_crossline(self):
        self.cross_line=True

    def is_crossline(self):
        return self.cross_line

    def getLastBox(self):
        if len(self.boxes) !=0:
            return self.boxes[len(self.boxes)-1]
        return None

    def get_lastbox_centerpoint(self):
        if len(self.boxes) !=0:
            box= self.boxes[len(self.boxes)-1]
            return (((box[1]+box[3])/2)),(((box[0]+box[2])/2))
        return None

    def get_tracking_history(self):
        if len(self.boxes) !=0:
            return list(self.boxes)
        return None

    def is_valid(self):
        if time.time()-self.last_update_time>self.max_live_sec:
            return False
        return True



class CrossLineVA(VAService):

    IS_DEBUG=True
    TRACKING_BUDGET_COUNT=100
    frameCount=0
    elapseTimeCheckQueue = deque(maxlen=100)
    tracking_history_dic={}

    # colors = [ tuple(np.random.randint(256, size=3)) for i in range(TRACKING_BUDGET_COUNT)]

    colors = [(np.random.randint(256),np.random.randint(256),np.random.randint(256))
              for i in range(1000)]

    def __init__(self, config, va_type, min_threshold=0.5):
        super().__init__(config, va_type)
        self.IS_DEBUG=self.config.getbool('debug')

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
        inf_new_result=[]

        for n, row in enumerate(image_by_ch):
            image = row[1]
            height, width = image.shape[:2]
            ch_id = str(row[2])
            (cross_line,direction_point)=get_crossline(row)
            direction=direction_in_line(cross_line[0],cross_line[1],direction_point[1] )

            if self.IS_DEBUG:
                cv2.line(image,transform_point(cross_line[0],width,height),transform_point(cross_line[1],width,height),(255,0,0),thickness=3)
                cv2.arrowedLine(image,transform_point(direction_point[0],width,height),transform_point(direction_point[1],width,height),(0,0,255),thickness=3)
            tracking_history=self.tracking_history_dic.get(ch_id)

            if tracking_history is None:
                tracking_history={}

            result=inf_result[n]

            boxes = []
            scores = []
            classes = []

            for kk,box in enumerate(result[0]):
                uuid=result[2][kk]
                tvo=tracking_history.get(uuid)

                if tvo is None:
                   tvo=TrackingHistoryVo(uuid)
                current_center_position=((((box[1]+box[3])/2)),(((box[0]+box[2])/2)))

                is_cross_line=False
                if self.IS_DEBUG :
                    trace_color=self.colors[uuid]
                # if tvo.is_crossline() ==False:  ## 한번 통과한 객체는 체크 안함

                for k in range(len(tvo.boxes)-1,0,-1): # 옛날것 부터 확인
                    p1=tvo.boxes[k]
                    center_position=((((p1[1]+p1[3])/2)),(((p1[0]+p1[2])/2))) # history 내 박스의 중심점

                    cross_point=get_crosspt(cross_line[0][0],cross_line[0][1],cross_line[1][0],cross_line[1][1]
                                     ,current_center_position[0],current_center_position[1]
                                     ,center_position[0],center_position[1]
                                     ) # cross line 과의 교차점

                    if self.IS_DEBUG :
                        cv2.circle(image,(int(center_position[0]*width),int(center_position[1]*height) ),2, trace_color,2)

                    if cross_point is not None:
                        direction1=direction_in_line(cross_line[0],cross_line[1],current_center_position)
                        print('direction1 >>>>>>>>>........' ,direction1)

                        if direction1==direction:
                            is_cross_line=True
                            if self.IS_DEBUG :
                                cv2.circle(image,transform_point(cross_point,width,height),15,(255,255,255),2)
                                angle = get_angle(cross_point,current_center_position)
                                print('angle >> ' , angle)
                                cv2.putText(image, str(angle), (int(p1[0]*width), int(p1[1]+20*height)),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                            break


                if  (is_cross_line or tvo.is_crossline()):
                    scores.append(1)
                    classes.append(uuid) # tracking uuid
                    boxes.append(box)
                    tvo.set_crossline()

                    if self.IS_DEBUG :
                        cv2.rectangle(image, (int(box[0]), int(box[1])),
                                      (int(box[0] + box[2]), int(box[1] + box[3])), (0,0,255),
                                      10)

                tvo.add(box)
                inf_new_result.append((boxes, scores, classes))
                tracking_history[uuid]=tvo

            self.tracking_history_dic[ch_id]=tracking_history

            if tracelogger.isEnabledFor(10):
                tracelogger.debug('ch {}   has {} trace object'.format(ch_id,len(tracking_history.keys() )) )

        #clear old track object
        if self.frameCount%500==0:
            for row in  (image_by_ch):
                ch_id = str(row[2])
                tracking_history=self.tracking_history_dic.get(ch_id)
                if self.frameCount %100==0:
                    if tracking_history is not None:
                        for key in tracking_history.keys():
                            if not tracking_history[key].is_valid():
                                del tracking_history[key]

        if self.frameCount > 1000000000:
            self.frameCount = -1

        for (ch_id, _, ch_uuid, cfg_json), inference  in zip(image_by_ch, inf_new_result ):
            sc.set_out_by_ch(self.va_type, ch_id, inference)

        if tracelogger.isEnabledFor(10):
            self.elapseTimeCheckQueue.append((time.time() - start) * 1000)
            tracelogger.debug('elapsed time avg [%.4f]', np.mean(self.elapseTimeCheckQueue))
        tracelogger.debug('clossline elapsed time [%.4f]', time.time() - start)

        return sc;


