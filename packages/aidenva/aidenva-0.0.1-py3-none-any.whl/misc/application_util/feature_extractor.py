from __future__ import absolute_import, division, print_function

import pathlib

import tensorflow as tf
import cv2
import os
import numpy as np
import matplotlib.pylab as plt
import glob
import time
import random
import PIL
from PIL import Image






import numpy

from tensorflow.python.ops.image_ops_impl import ResizeMethod

tf.enable_eager_execution()
AUTOTUNE = tf.data.experimental.AUTOTUNE
os.environ["CUDA_VISIBLE_DEVICES"] = '10'
os.environ['TF_ENABLE_AUTO_MIXED_PRECISION'] = '1'
data_root = '/home/ocrusr/service/tensorflow/object_detection/she/data/classification/val_merged'
BATCH_SIZE = 1
RESULT_IMAGE_COUNT = 24
SHOW_RESULT = False

IMAGE_SIZE = (224, 224)
PB_FILE_PATH = '/home/ocrusr/IdeaProjects/ml/she/intrusion/classification/models/NAS-Mobile-1/saved_models/1576658992/optimized_frozen_inference_graph.pb'
INPUT_TENSOR_NAME = 'NASNet_input'
OUTPUT_TENSOR_NAME = 'dense/Softmax'
FEATURE_TENSOR_NAME='global_average_pooling2d/Mean:0'

def loadGraph(_path):
    _detection_graph = tf.Graph()
    with _detection_graph.as_default():
        _od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(_path, 'rb') as fid:
            _serialized_graph = fid.read()
            _od_graph_def.ParseFromString(_serialized_graph)
            tf.import_graph_def(_od_graph_def, name='')
        return tf.Session(graph=_detection_graph)


def show(result_images, result_labels, image_batch, result_orgin_labels):
    plt.figure(figsize=(128, 128))
    for n, img in enumerate(result_images):
        plt.subplot(6, 4, n + 1)
        plt.imshow(image_batch[n])
        plt.title("result :" + result_labels[n] + " == origin: " + result_orgin_labels[n])
        plt.axis('off')
        _ = plt.suptitle("Model predictions")
    plt.show()

def preprocess_image2(image, imgSize):
    image = cv2.resize(cv2.cvtColor(image, cv2.COLOR_RGB2BGR), imgSize, interpolation=cv2.INTER_LINEAR) #0.94526
    return image / 255.0

def execute(imageBatch):
    image_ds = np.array([preprocess_image2(image, IMAGE_SIZE) for image in imageBatch])
    ttt = time.time()
    result_batch = sess.run([out,feature], feed_dict={lambda_input: image_ds})
    elapseTime = (time.time() - ttt)
    return result_batch, elapseTime


sess = loadGraph(PB_FILE_PATH)
out = sess.graph.get_tensor_by_name(OUTPUT_TENSOR_NAME + ':0')
feature = sess.graph.get_tensor_by_name(FEATURE_TENSOR_NAME )

lambda_input = sess.graph.get_tensor_by_name(INPUT_TENSOR_NAME + ':0')


image_generator = tf.keras.preprocessing.image.ImageDataGenerator( rescale=1 / 255,     vertical_flip=False, horizontal_flip=False)
val_data = image_generator.flow_from_directory(str(data_root), batch_size=BATCH_SIZE, target_size=IMAGE_SIZE, shuffle=True ,color_mode='rgb' ,interpolation='bicubic' )

op = sess.graph.get_operations()

for nn in [m.values() for m in op]:
    print('>>> nn' , nn)


for i,(image_batch, label_batch) in enumerate(val_data) :

    t=time.time()
    result_batch = execute(image_batch)

    for result in result_batch:
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print('result>>' ,len(result) )
        print('result 0 >>' ,result[0] )
        print('result 1 >>' ,result[1] )
        print('result>>' , (result[1].shape) )
        print('result>>' , (result[0].shape) )
        print('result>>' , type(result[1].shape) )
    elapseTime=time.time()-t
    if i==0:
        break



