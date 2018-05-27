#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provides the test functionality for the Camera Thread
"""

import logging
import time
import cv2
import SetupConsoleLogger
import CameraThread

LOGGER = logging.getLogger(__name__)
SetupConsoleLogger.setup_console_logger(LOGGER, logging.DEBUG)


class Processor(object):
    """
    Defines a class to apply additional processing to the image
    returned by the callback
    """

    def __init__(self):
        """
        Constructor
        """
        LOGGER.debug("Processor constructor called")

        self.width = 320
        self.height = 240

    def __del__(self):
        """
        Destructor
        """
        self.cleanup()

    def cleanup(self):
        """
        Cleanup
        """

    def image_process_entry(self, bgr_image, width, height):
        """
        Called each time an image can be processed
        """
        # Blur the image
        MED_FILTER_APRTRE_SIZE = 5  # Must be odd number
        bgr_blur_image = cv2.medianBlur(bgr_image, MED_FILTER_APRTRE_SIZE)

        # Convert the image from 'BGR' to HSV colour space
        hsv_image = cv2.cvtColor(bgr_blur_image, cv2.COLOR_BGR2HSV)

        cv2.imshow('Blured HSV Image', hsv_image)
        cv2.imwrite('orig.jpg', bgr_image)
        cv2.imwrite('blur.jpg', hsv_image)

        raise KeyboardInterrupt

        # Capture a key press. The function waits argument in ms
        # for any keyboard event
        # For some reason image does not show without this!
        cv2.waitKey(1) & 0xFF


def main():
    """
    Performs the "Camera Capture and stream mechanism" test
    """
    LOGGER.info("'Camera Capture and stream mechanism' Starting.")
    LOGGER.info("CTRL^C to terminate program")

    try:
        # Create the object that will process the images
        # passed in to the image_process_entry function
        image_processor = Processor()

        # Start stream process to handle images and
        # pass then to the callback function
        stream_processor = CameraThread.StreamProcessor(
            640, 480, image_processor.image_process_entry, True)

        # Wait for the interval period for finishing
        time.sleep(300)

    except KeyboardInterrupt:
        LOGGER.info("Stopping 'Camera Capture and stream mechanism'.")

    finally:
        stream_processor.exit_now()
        stream_processor.join()
        image_processor.cleanup()
        cv2.destroyAllWindows()

    LOGGER.info("'Camera Capture and stream mechanism' Finished.")


if __name__ == "__main__":
    main()
