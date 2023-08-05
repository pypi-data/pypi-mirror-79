
import tensorflow as tf
import os
import sys
import logging
import urllib.request
import traceback

from tqdm import tqdm
from service import constants as const
from abc import ABCMeta, abstractmethod
from models.inference_manager import InferenceManager

logger = logging.getLogger('system')
trace = logging.getLogger('trace')

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def check_exist_model(path, url, root_path=''):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(os.path.join(root_path, path)):
        download_url = os.path.join(url, path)
        try:
            with DownloadProgressBar(file=sys.stdout, unit='B', unit_scale=True, mininterval=10,
                                     desc=download_url.split('/')[-1]) as t:
                urllib.request.urlretrieve(download_url, filename=path, reporthook=t.update_to)
        except:
           raise Exception('cannot download model(pb) from repository or not exist [%s]' % path)


class BaseModel(metaclass=ABCMeta):
    def __init__(self, enabled, config, va_name, batch_size=20):
        self.va_name = va_name

        self.conf_prefix = 'va_engines.models.%s.' % self.va_name
        self.enabled = enabled
        self.batch_size = batch_size

        if self.enabled:
            frozen_pb = config.getvalue(self.conf_prefix + 'model_dir')
            if not os.path.isfile(frozen_pb):
                check_exist_model(frozen_pb, config.getvalue('model_repository_url'))

            self.in_tensor_name = config.getvalue(self.conf_prefix + 'in_tensor_name')
            self.out_tensor_name =  config.getvalue(self.conf_prefix + 'out_tensor_name') \
                if len(config.getlist(self.conf_prefix + 'out_tensor_name')) == 1 \
                else config.getlist(self.conf_prefix + 'out_tensor_name')

            self.gpu_config = const.get_gpu_options(config)

            self.graph = tf.Graph()
            with self.graph.as_default():
                graph_def = tf.compat.v1.GraphDef()
                with tf.io.gfile.GFile(frozen_pb, 'rb') as f:
                    graph_def.ParseFromString(f.read())
                tf.import_graph_def(graph_def, name='')

            logger.info('[%s] sucessfully loaded [%s] file.', self.va_name, frozen_pb)

            self.persistent_sess = tf.compat.v1.Session(graph=self.graph, config=self.gpu_config)

            instance = InferenceManager()   # singleton
            instance.regist_va(va_name, self.get_inf_method(), self.graph, self.persistent_sess, self.in_tensor_name,
                               self.out_tensor_name, self.batch_size)

    def get_va_name(self):
        return self.va_name

    @property
    def graph(self):
        return self.__model_graph;

    @graph.setter
    def graph(self, model_graph):
        self.__model_graph = model_graph

    @abstractmethod
    def _inference(self, input):
        pass

    @abstractmethod
    def get_inf_method(self):
        pass
