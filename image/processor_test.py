#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provides the test functionality for the Camera Thread
"""

import logging
import time
import cv2
from api import (
    SetupConsoleLogger
    CameraThread
)
from processor import Processor

LOGGER = logging.getLogger(__name__)
SetupConsoleLogger.setup_console_logger(LOGGER, logging.DEBUG)

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
