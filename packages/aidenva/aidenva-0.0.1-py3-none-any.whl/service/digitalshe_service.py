from service import constants as const
from vaengine.detection_va_v4 import DetectionVA
from vaengine.falldown_va_2 import FalldownVA
from vaengine.helmet_va_2 import HelmetVA
from vaengine.firesmoke_va_6 import FiresmokeVA
from vaengine.harness_va_v2 import HarnessVA
from vaengine.intrusion_va_v8 import IntrusionVA
from vaengine.cctv_exc_va import CCTVExcavatorVA
from vaengine.loitering_va import LoiteringVA
from vaengine.tracking_va import TrackingVA
from vaengine.cluster_va import ClusterVA
from vaengine.crossline_va import CrossLineVA

from misc import debug
import logging
import time
import traceback

systemlogger = logging.getLogger('system')

class DSService:
    def __init__(self, config):
        self.config = config
        self.de = DetectionVA(config, const.DETECT_VA).dependVAType(const.FALLDOWN_VA | const.HELMET_VA | const.HARNESS_VA | const.CLUSTER_VA | const.LOITERING_VA| const.CROSSLINE_VA)
        self.intrusion = IntrusionVA(config, const.INTRUSION_VA)
        self.fd = FalldownVA(config, const.FALLDOWN_VA)
        self.hm = HelmetVA(config, const.HELMET_VA)
        self.fs = FiresmokeVA(config, const.FIRESMOKE_VA)
        self.ha = HarnessVA(config, const.HARNESS_VA)
        self.ccexc = CCTVExcavatorVA(config, const.CCTVEXC_VA)
        self.tracking=TrackingVA(config, const.TRACKING_VA).dependVAType(const.LOITERING_VA)
        self.loiter=LoiteringVA(config, const.LOITERING_VA)
        self.cluster = ClusterVA(config, const.CLUSTER_VA)
        self.crossline = CrossLineVA(config, const.CROSSLINE_VA)

    def execute(self, sc):
        start = time.time()

        threads = []
        try:
            if self.config.getbool('debug'):
                self.de.execute_va(sc, sync=True)
                self.intrusion.execute_va(sc, sync=True)
                self.fd.execute_va(sc, sync=True)
                self.hm.execute_va(sc, sync=True)
                self.fs.execute_va(sc, sync=True)
                self.ha.execute_va(sc, sync=True)
                self.ccexc.execute_va(sc, sync=True)
                self.tracking.execute_va(sc, sync=True)
                self.loiter.execute_va(sc, sync=True)
                self.cluster.execute_va(sc, sync=True)
                self.crossline.execute_va(sc, sync=True)
            else:
                threads.append(self.de.execute_va(sc, sync=True))
                threads.append(self.tracking.execute_va(sc, sync=True))
                threads.append(self.intrusion.execute_va(sc))
                threads.append(self.fd.execute_va(sc))
                threads.append(self.hm.execute_va(sc))
                threads.append(self.fs.execute_va(sc))
                threads.append(self.ha.execute_va(sc))
                threads.append(self.ccexc.execute_va(sc))
                threads.append(self.loiter.execute_va(sc))
                threads.append(self.cluster.execute_va(sc))
                threads.append(self.crossline.execute_va(sc))

                for th in threads:
                    if th is not None:
                        th.join()

            systemlogger.info('total elapsed time [%.3f], ch_id [%d] %s', time.time() - start, len(sc.chid_list), sc.chid_list)

        except Exception as error:
            systemlogger.error(traceback.format_exc())
            sc.output = list([])

        return sc