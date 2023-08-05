import cv2
import numpy as np

def _boxesIntersect(boxA, boxB):
    if boxA[0] > boxB[2]:
        return False  # boxA is right of boxB
    if boxB[0] > boxA[2]:
        return False  # boxA is left of boxB
    if boxA[3] < boxB[1]:
        return False  # boxA is above boxB
    if boxA[1] > boxB[3]:
        return False  # boxA is below boxB
    return True


def _getArea(box):
    return (box[2] - box[0] + 1) * (box[3] - box[1] + 1)


def _getUnionAreas(boxA, boxB, interArea=None):
    area_A = _getArea(boxA)
    area_B = _getArea(boxB)
    if interArea is None:
        interArea = _getIntersectionArea(boxA, boxB)
    return float(area_A + area_B - interArea)


def getIou(boxA, boxB):
    if _boxesIntersect(boxA, boxB) is False:
        return 0
    interArea = _getIntersectionArea(boxA, boxB)
    union = _getUnionAreas(boxA, boxB, interArea=interArea)
    # intersection over union
    iou = interArea / union
    assert iou >= 0
    return iou


def _getIntersectionArea(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # intersection area
    return (xB - xA + 1) * (yB - yA + 1)

def drawResult(image,ch_id,_boxes, _score, score_threthold=0.5):
    # clone=image.copy()
    height, width = image.shape[:2]
    _heightMargin=int(height/20)
    for idx in range(len(_boxes)):
        box_t = tuple(_boxes[idx])
        tlx = int(box_t[1] * width)
        tly = int(box_t[0] * height)
        brx = int(box_t[3] * width)
        bry = int(box_t[2] * height)
        if _score[idx]> score_threthold:
            cv2.rectangle(image, (tlx, tly), (brx, bry), (0, 0, 255),2)
        else:
            cv2.rectangle(image, (tlx, tly), (brx, bry), (255, 0, 0),2)
        cv2.putText(image, str(_score[idx])[0:4], (tlx,tly-_heightMargin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.imshow('Object detector:'+str(ch_id), image)



def enhanceContrast(org):
    '''
    contras
    :param org:
    :return:
    '''
    clahe =cv2.createCLAHE(2,(8,8))
    l_channel, a_channel, b_channel = cv2.split(org)
    l_channel=clahe.apply(l_channel)
    a_channel=clahe.apply(a_channel)
    b_channel=clahe.apply(b_channel)
    return cv2.merge((l_channel, a_channel, b_channel))


# mat=cv2.imread('/media/ocrusr/raid11/she/validations/20190715/images/2614361443144767699_92.jpg')
#
# print('mean ', cv2.mean(mat))
# print('np mean ', np.mean(cv2.mean(mat)[0:2]))
# cv2.imshow('org',mat)
#
# cv2.imshow('rr',enhanceContrast(mat))
#
# cv2.waitKey()