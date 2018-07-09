#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provides the test functionality for the Camera Thread
"""

import logging
import time
import cv2
from api import (
    SetupConsoleLogger,
    CameraThread,
    MotorController,
    ServoController,
    GPIOLayout
)
from processor import Processor

LOGGER = logging.getLogger(__name__)
SetupConsoleLogger.setup_console_logger(LOGGER, logging.DEBUG)

motor_controller = MotorController.MotorController(
    GPIOLayout.MOTOR_LEFT_FORWARD_GPIO,
    GPIOLayout.MOTOR_LEFT_BACKWARD_GPIO,
    GPIOLayout.MOTOR_RIGHT_FORWARD_GPIO,
    GPIOLayout.MOTOR_RIGHT_BACKWARD_GPIO
)

servo_controller = ServoController.ServoController()

def cb(position):
    print(position)
    if position and position[0] > 300 and position[0] < 340:
        motor_controller.stop()
        motor_controller.forward(SpeedSettings.SPEED_FAST)

def main():
    """
    Performs the "Camera Capture and stream mechanism" test
    """
    LOGGER.info("'Camera Capture and stream mechanism' Starting.")
    LOGGER.info("CTRL^C to terminate program")

    image_processor = None
    stream_processor = None
    motor_controller.stop()

    try:
        servo_controller.start_servos()
        sleep(0.5)
        servo_controller.set_pan_servo(0)
        servo_controller.set_tilt_servo(0)
        # Create the object that will process the images
        # passed in to the image_process_entry function
        image_processor = Processor(cb)

        # Start stream process to handle images and
        # pass then to the callback function
        stream_processor = CameraThread.StreamProcessor(
            640, 480, image_processor.image_process_entry, False)

        sleep(1)
        motor_controller.spin_left(SpeedSettings.SPEED_FASTEST)

    except KeyboardInterrupt:
        LOGGER.info("Stopping 'Camera Capture and stream mechanism'.")

    finally:
        motor_controller.stop()
        if stream_processor is not None:
            stream_processor.exit_now()
            stream_processor.join()
        if image_processor is not None:
            image_processor.cleanup()
        cv2.destroyAllWindows()

    LOGGER.info("'Camera Capture and stream mechanism' Finished.")


if __name__ == "__main__":
    main()
