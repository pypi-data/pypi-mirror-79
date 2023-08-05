from service import constants as const
from abc import ABCMeta, abstractmethod
import logging
import time
import threading

tracelogger = logging.getLogger('trace')

class VAService( metaclass=ABCMeta):
    def __init__(self, config, va_type):
        self.config = config
        self.va_type = va_type
        self.conf_prefix = 'va_engines.engines.%s.' % const.VA_TYPES[self.va_type]
        self.label_map = self._set_lables(self.config.getvalue(self.conf_prefix + 'path_to_label'))
        self.enabled = self.config.getbool(self.conf_prefix + 'enabled')
        self.__depend = const.NONE

    def execute_va(self, sc, sync=False):
        if self.enabled:
            start = time.time()
            if sync:
                self._execute(sc)
                return None
            else:
                th = threading.Thread(target=self._execute, args=(sc,))
                th.start()
                return th
        else:
            return None

    @abstractmethod
    def _set_lables(self, path_to_labels):
        pass

    @abstractmethod
    def _execute(self, sc):
        pass

    def dependVAType(self, depend):
        self.__depend = depend
        return self

    def is_support_vatype_fc(self, va_type):
        def check_fc(va_type):
            return const.check_va_type(self.va_type | self.__depend, va_type )
        return check_fc(va_type)