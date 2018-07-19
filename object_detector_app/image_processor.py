import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import time
import io

import threading

from time import sleep

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt

from PIL import Image

import cv2
from api import CameraThread

from picamera.array import PiRGBArray
from picamera import PiCamera

# ## Object detection imports
# Here are the imports from the object detection module.

# In[3]:

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

class ImageProcessor(object):

    # Defines class to apply additional processing to the image returned by callback.

    def __init__(self, im_disp = True):

      self.width = 480
      self.height = 360
      self.confidence_threshold = 0.5
      self.bounding_boxes = []
      self.detected_classes = []
      self.confidences = []
      self.im_disp = im_disp
      self._thread = threading.Thread(target = self._run, name = "Imaging Thread")
      self.go_sig = threading.Semaphore(1)
      self.sem = threading.Semaphore(0)
      self._running = True

    def __del__(self):
      self.cleanup()

    def start(self):
        self._thread.start()

    def _run(self):
        self.model_preparation()

    def stop(self):
        self._running = False
        self._thread.join()
        print("Deathed")

    def cleanup(self):
      ##Cleanup
      print('Shutting down Object Detection App...')

    def model_preparation(self):

        camera = PiCamera()
        camera.resolution = (self.width, self.height)
        camera.framerate = 25
        rawCapture = PiRGBArray(camera, size=(self.width, self.height))

        # # Model preparation

        # ## Variables
        #
        # Any model exported using the `export_inference_graph.py` tool can be loaded here simply by changing `PATH_TO_CKPT` to point to a new .pb file.
        #
        # By default we use an "SSD with Mobilenet" model here. See the [detection model zoo](https://github.com/tensorflow/models/blob/master/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.

        # In[4]:

        # What model to download.
        MODEL_NAME = 'ssd_mobilenet_v2_pibot_16_07_2018_v7'

        # Path to frozen detection graph. This is the actual model that is used for the object detection.
        ABS_PATH = os.path.dirname(os.path.abspath(__file__))
        PATH_TO_CKPT = ABS_PATH + '/models/' + MODEL_NAME + '/frozen_inference_graph.pb'

        # List of the strings that is used to add correct label for each box.
        PATH_TO_LABELS = os.path.join(ABS_PATH, 'data', 'pibot_label_map.pbtxt')

        NUM_CLASSES = 3

        # ## Load a (frozen) Tensorflow model into memory.

        # In[6]:
        bounding_box_temp = []
        detected_classes_temp = []
    	confidences_temp = []

        detection_graph = tf.Graph()
        with detection_graph.as_default():
          od_graph_def = tf.GraphDef()
          with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')


        # ## Loading label map
        # Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

        # In[7]:

        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        category_index = label_map_util.create_category_index(categories)

        # # Detection

        # In[9]:

        # For the sake of simplicity we will use only 2 images:
        # image1.jpg
        # image2.jpg
        # If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
        #PATH_TO_TEST_IMAGES_DIR = 'test_images'
        #TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 3) ]

        # Size, in inches, of the output images.
        IMAGE_SIZE = (12, 8)

         # In[10]:

        config = tf.ConfigProto()
        NUM_THREADS = 4
        config.intra_op_parallelism_threads=NUM_THREADS
        config.inter_op_parallelism_threads=NUM_THREADS

        with detection_graph.as_default():
          with tf.Session(graph=detection_graph, config=config) as self.sess:
            #while True:
            count = 0
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
              count += 1

              bounding_boxes_temp = []
              detected_classes_temp = []
              confidences_temp = []

              bgr_image = frame.array
              cv2.imwrite('image_{}.png'.format(count), bgr_image)
              image_np = np.rot90(np.array(bgr_image), 2)
              # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
              image_np_expanded = np.expand_dims(image_np, axis=0)
              image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
              # Each box represents a part of the image where a particular object was detected.
              boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
              # Each score represent how level of confidence for each of the objects.
              # Score is shown on the result image, together with the class label.
              scores = detection_graph.get_tensor_by_name('detection_scores:0')
              classes = detection_graph.get_tensor_by_name('detection_classes:0')
              num_detections = detection_graph.get_tensor_by_name('num_detections:0')
              # Actual detection.
              (boxes, scores, classes, num_detections) = self.sess.run(
                  [boxes, scores, classes, num_detections],
                  feed_dict={image_tensor: image_np_expanded})

              # Visualization of the results of a detection. Only do this if asked!!
              if self.im_disp:
                  vis_util.visualize_boxes_and_labels_on_image_array(
                      image_np,
                      np.squeeze(boxes),
                      np.squeeze(classes).astype(np.int32),
                      np.squeeze(scores),
                      category_index,
                      use_normalized_coordinates=True,
                      line_thickness=8)

              for i in range(num_detections[0]):
              	  if np.squeeze(scores)[i] > self.confidence_threshold:
                      ymin = boxes[0][i][0] * self.height
                      xmin = boxes[0][i][1] * self.width
                      ymax = boxes[0][i][2] * self.height
                      xmax = boxes[0][i][3] * self.width
                      bounding_boxes_temp.append([ymin, xmin, ymax, xmax])
                      detected_classes_temp.append(classes[0][i].astype(np.int32))
                      confidences_temp.append(scores[0][i])

	          self.bounding_boxes = bounding_boxes_temp[:]
	          self.detected_classes = detected_classes_temp[:]
              self.confidences = confidences_temp[:]
              self.sem.release()

              if self.im_disp: # Only do this if asked!!
                  cv2.imshow('object detection', cv2.resize(image_np, (self.width*1, self.height*1)))
              rawCapture.truncate(0)

              if cv2.waitKey(25) & 0xFF == ord('q') or not self._running:
                cv2.destroyAllWindows()
                break

              self.go_sig.acquire()
              sleep(0.5)
