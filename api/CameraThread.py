#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sets up and generates images from a camera within two threads.
The first thread grabs images and the second process the received
images, which are then passed to the callback configured during
initialisation.
"""

from __future__ import division
import logging
import time
import threading
import cv2
import picamera
import picamera.array

# Create a logger to both file and stdout
MODULE_LOGGER = logging.getLogger("__main__.CameraThread")


class ImageCapture(threading.Thread):
    """
    Thread created from the stream processing thread to generate a
    series of images which are then passed back via an event.
    """

    def __init__(self, width, height, stream_processor):
        """
        Initialise the parameters required for the Image Capture thread
        """
        super(ImageCapture, self).__init__()
        MODULE_LOGGER.debug("ImageCapture constructor called")

        self._stream_processor = stream_processor
        self._exit_now = False

        self.camera = picamera.PiCamera()
        # Camera resolution defaults to the monitors resolution,
        # but needs to be lower for speed of processing
        self.camera.resolution = (width, height)
        self.camera.framerate = 10  # If not set then defaults to 30fps
        self.camera.vflip = True  # Needed for mounting of camera on pan/tilt
        self.camera.hflip = True  # Needed for mounting of camera on pan/tilt
        MODULE_LOGGER.info('Waiting for the camera to wake up ...')
        # Allow the camera time to warm-up
        time.sleep(2)  # This is the value/line used in the PiBorg example

        self.start()  # starts the thread by calling the run method.

    def __del__(self):
        """
        Destructor
        """
        MODULE_LOGGER.debug("ImageCapture destructor called")
        del self.camera  # Is this needed?

    def run(self):
        """
        The run() method is the entry point for a thread
        This method runs in a separate thread
        """
        MODULE_LOGGER.info("Starting the ImageCapture thread")

        self.camera.capture_sequence(
            self.trigger_stream(), format='bgr', use_video_port=True)

        MODULE_LOGGER.info("Finshed the ImageCapture thread")

    def exit_now(self):
        """
        Request the thread to exit
        """
        MODULE_LOGGER.info("Request to stop Image Capture thread")
        self._exit_now = True

    def trigger_stream(self):
        """
        Stream delegation loop
        """

        while not self._exit_now:
            if self._stream_processor.event.is_set():
                time.sleep(0.01)
            else:
                yield self._stream_processor.stream
                self._stream_processor.event.set()


# pylint: disable=too-many-instance-attributes
class StreamProcessor(threading.Thread):
    """
    Image stream processing thread, which also starts the
    image capture thread.
    """

    def __init__(self, width, height, processing_cb=None, show_input=False):
        """
        Initialise the parameters required for StreamProcessor thread
        """
        super(StreamProcessor, self).__init__()
        MODULE_LOGGER.debug("StreamProcessor constructor called")

        self.event = threading.Event()
        self._exit_now = False
        self.max_processing_delay = 0.0  # Initialsed for delay calculations
        self.min_processing_delay = 100.0  # Initialsed for delay calculations
        self._frames_processed = 0
        self.width = width
        self.height = height
        self._processing_cb = processing_cb
        self._show_input = show_input

        # Start the capture thread to generate images
        self.capture_thread = ImageCapture(self.width, self.height, self)
        self.stream = picamera.array.PiRGBArray(self.capture_thread.camera)
        self.start()  # starts the thread by calling the run method.

    def __del__(self):
        """
        Destructor
        """

    def exit_now(self):
        """
        Blocking call to request the thread to exit.
        Works by calling the subthread and when this is complete
        joins and closes down this stream processor before returning
        """
        MODULE_LOGGER.info("Request to stop Stream Processor thread")
        self.capture_thread.exit_now()
        self.capture_thread.join()
        self._exit_now = True
        MODULE_LOGGER.info(
            "Image processing delays min: %.2f ms and max: %.2f ms",
            self.min_processing_delay * 1000, self.max_processing_delay * 1000)
        MODULE_LOGGER.info("Frames processed: %.2f", self._frames_processed)

    def run(self):
        """
        The run() method is the entry point for a thread
        This method runs in a separate thread
        """
        MODULE_LOGGER.info("Starting the Stream Processing thread")

        while not self._exit_now:
            # Wait for an image to be written to the stream
            # The wait() method takes an argument representing the
            # number of seconds to wait for the event before timing out.
            if self.event.wait(1):
                try:
                    # Read the image and do some processing on it
                    self.stream.seek(0)
                    self.process_image(self.stream.array)
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()

        MODULE_LOGGER.info("Finshed the Stream Processing thread")

    def process_image(self, image):
        """
        The main image processing function
        """
        # View the original image seen by the camera.
        if self._show_input:
            cv2.imshow('Original', image)

            # Capture a key press. The function waits argument in ms
            # for any keyboard event
            # For some reason image does not show without this!
            # pylint: disable=expression-not-assigned
            cv2.waitKey(1) & 0xFF

        start_time = cv2.getTickCount()

        if self._processing_cb is not None:
            self._processing_cb(image, self.width, self.height)

        # Calculate image processing overhead
        # https://docs.opencv.org/3.0.0/dc/d71/tutorial_py_optimization.html
        end_time = cv2.getTickCount()
        time_taken = (end_time - start_time) / cv2.getTickFrequency()
        if time_taken > self.max_processing_delay:
            self.max_processing_delay = time_taken
        elif time_taken < self.min_processing_delay:
            self.min_processing_delay = time_taken

        self._frames_processed += 1
