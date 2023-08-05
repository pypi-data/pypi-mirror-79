from service import constants as const

import threading
import tensorflow as tf
import time
import logging
import numpy as np
import os

tracelogger = logging.getLogger('trace')
systemlogger = logging.getLogger('system')


BATCH_SIZE = 20


# singleton class
class InferenceManager(object):
    _instance = None
    _lock = threading.Lock()
    va_engine = dict()

    def __new__(cls):
        if InferenceManager._instance is None:
            with InferenceManager._lock:
                if InferenceManager._instance is None:
                    InferenceManager._instance = super(InferenceManager, cls).__new__(cls)
        return InferenceManager._instance

    def regist_va(self, name, inf_method, graph, persistent_sess, in_tensor_name, out_tensor_name, batch_size):
        InferenceManager.va_engine[name] = ( inf_method, graph, persistent_sess, in_tensor_name, out_tensor_name, batch_size)

    def inferece(self, inputs):

        va_name, input = inputs

        inf_method, graph, persistent_sess, in_tensor_name, out_tensor_name, batch_size = InferenceManager.va_engine[va_name]

        def run(images):
            with graph.as_default():
                if inf_method == const.INF_METHOD_CLASSIFICATION:
                    input_tensor = tf.compat.v1.get_default_graph().get_tensor_by_name(in_tensor_name)
                    # output_tensor = tf.compat.v1.get_default_graph().get_tensor_by_name(out_tensor_name)
                    output_tensor = []

                    if isinstance(out_tensor_name, list):
                        for key in out_tensor_name:
                            # output_tensor[key] = tf.compat.v1.get_default_graph().get_tensor_by_name(key)
                            output_tensor.append(tf.compat.v1.get_default_graph().get_tensor_by_name(key))
                    else:
                        output_tensor = tf.compat.v1.get_default_graph().get_tensor_by_name(out_tensor_name)

                    # Run inference
                    start = time.time()
                    logits = persistent_sess.run(output_tensor, feed_dict={input_tensor: images})

                    tracelogger.debug('[%-10s] classification inference elapesed time: [%.3f], images [%d]', va_name, (time.time() - start), len(images))

                    return logits
                elif inf_method == const.INF_METHOD_DETECTION:
                    input_tensor = tf.compat.v1.get_default_graph().get_tensor_by_name(in_tensor_name)
                    output_tensor = {}

                    for key in out_tensor_name:
                        output_tensor[key] = tf.compat.v1.get_default_graph().get_tensor_by_name(key)

                    output_list = list()
                    # Run inference
                    start = time.time()
                    inference_dict = persistent_sess.run(output_tensor, feed_dict={input_tensor: images})
                    tracelogger.debug('[%-10s] detection inference elapesed time: [%.3f], images [%d]', va_name, (time.time() - start), len(images))

                    for idx in range(len(images)):
                        output_list.append([inference_dict[tensor_name][idx] for tensor_name in out_tensor_name])

                    return output_list
                else:
                    raise NotImplementedError

        inf_results = []

        if len(input) > 0:
            if len(input) < batch_size:
                inf_results.extend(run(input))
            else:
                for i in range(0, len(input), batch_size):
                    c = input[i: i + batch_size]
                    inf_results.extend(run(c))
        return inf_results

if __name__ == '__main__':
    i = InferenceManager()
    a = InferenceManager()

    print(i)
    print(a)
    print( i == a)




