from models import basemodel
from service import constants as const

import numpy as np

from models.inference_manager import InferenceManager

class ObjectDetect(basemodel.BaseModel):
    def __init__(self, enabled, config, va_name, in_shape=(299, 299)):
        super(ObjectDetect, self).__init__(enabled, config, va_name)
        self.in_shape = in_shape
        self.inf_manager = InferenceManager()  # singleton

        if self.enabled:
            self.__warmup()

    # override
    def get_inf_method(self):
        return const.INF_METHOD_DETECTION

    def __warmup(self):
        self.inf_manager.inferece(
            (self.va_name, [np.ndarray(shape=(self.in_shape[1], self.in_shape[0], 3), dtype=np.float32)]))

    def _inference(self, image_np_list):
        if not self.enabled:
            raise Exception ('VA engine [%s] not enabled' % self.get_va_name())

        return self.inf_manager.inferece((self.va_name, image_np_list))