import numpy as np
import json

# test only
import glob
import os
import cv2
from service import constants as const

class ServiceContext:
    def __init__(self, input):
        self.input = input
        # channel id list
        self.chid_list = sorted([row[3] for row in input])

        # input channl 수 만큼 dict로 초기화
        # self.output : ch order list -> dict { person : , falldown : ...}
        self.output = [dict() for i in range(len(self.input))]

        #extra value by channel
        self.extvalue = [dict() for i in range(len(self.input))]

    def get_in_by_vatype_gen(self, func):
        for ch_idx, (image_np, width_height, va, ch_id) in enumerate(self.input):
            yield ch_idx, image_np, width_height, va, ch_id

    '''
        입력된 image 중 service_flag에 맞는 channel의 사진만 추출
        self.input : [ image, width/height, va_type, ch_uudi ]

        return list[ idx, img_np, ch_uuid ]
    '''

    def get_in_by_vatype(self, func):
        arr = np.array(self.input)
        extract = list()
        # arr[0] : image
        # arr[1] : width/heigth
        # arr[2] : service type ( ref: models/constants.py )
        # arr[3] : channel id ( cctv UUID )
        # arr[4] : VA config JSON object
        for idx, f in enumerate(arr[:, 2]):
            if func(f):
                extract.append([idx, arr[idx][0], arr[idx][3], json.loads(arr[idx][4])])  # idx, image_np, ch_uuid, config json

        return np.array(extract)

    '''
        channel별 결과 setting
        va_type : const 정의된 va type
        ch_idx  : channel index
        inf_result : [ boxes, scores, classnames ]
        
    '''

    def set_out_by_ch(self, va_type, ch_idx, inf_result, extvalue = None):
        self.output[ch_idx][const.VA_TYPES[va_type]] = inf_result

        if extvalue is not None :
            self.extvalue[ch_idx][const.VA_TYPES[va_type]] = extvalue

    '''
        get_out은 channel순서로 service flag에 맞는 결과 값을 return
    '''

    def get_out_by_vatype(self, va_type):
        out_result = list()

        for out in self.output:
            if const.VA_TYPES[va_type] in out:
                out_result.append(out[const.VA_TYPES[va_type]])
            else:
                out_result.append(None)

        return out_result

    '''
        channel 별 설정된 추가 정보 return
    '''
    def get_out_ext_by_vatype(self, va_type):
        ext_result = list()

        for ext in self.extvalue:
            if const.VA_TYPES[va_type] in ext:
                ext_result.append(ext[const.VA_TYPES[va_type]])
            else:
                ext_result.append(None)

        return ext_result


if __name__ == '__main__':

    img_path = '/Users/hojung/1.WORK/tensorflow/git/tensorflow/research/objectdetection/datasets/test'
    image_files = glob.glob(os.path.join(img_path, '*.jpg'))

    images = list()

    idx = 0
    for image in image_files:
        print(image)
        img = cv2.imread(image)
        if idx % 2 == 0:
            images.append([cv2.cvtColor(img, cv2.COLOR_RGB2BGR), None, const.DETECT_VA])  # 침탐
        else:
            images.append([cv2.cvtColor(img, cv2.COLOR_RGB2BGR), None, const.DETECT_VA | const.FALLDOWN_VA])  # 쓰러짐
        idx = idx + 1


    def is_support_fc(flags):
        def check_fc(flags):
            return const.check_va_type(const.FALLDOWN_VA, flags)

        return check_fc(flags)


    sc = ServiceContext(images)

    result = sc.get_in_by_vatype(is_support_fc)
    print(result)