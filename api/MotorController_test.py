#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provides the test functionality for the MotorController
"""

import time
import logging
import SetupConsoleLogger
import GPIOLayout
import SpeedSettings
import MotorController

MODULE_LOGGER = logging.getLogger("__main__")
SetupConsoleLogger.setup_console_logger(MODULE_LOGGER)


def test_motorcontroller(sleep_len=0):
    """
    Tests the motor controller
    """
    MCONTROLLER = None

    try:
        SetupConsoleLogger.setup_console_logger(MODULE_LOGGER)
        MCONTROLLER = MotorController.MotorController(
            GPIOLayout.MOTOR_LEFT_FORWARD_GPIO,
            GPIOLayout.MOTOR_LEFT_BACKWARD_GPIO,
            GPIOLayout.MOTOR_RIGHT_FORWARD_GPIO,
            GPIOLayout.MOTOR_RIGHT_BACKWARD_GPIO)

        MCONTROLLER.stop()
        time.sleep(sleep_len)
        MODULE_LOGGER.info("forward 50%")
        MCONTROLLER.forward(SpeedSettings.SPEED_MEDIUM)
        time.sleep(sleep_len)
        MODULE_LOGGER.info("reverse 50%")
        MCONTROLLER.reverse(SpeedSettings.SPEED_MEDIUM)
        time.sleep(sleep_len)
        MODULE_LOGGER.info("spin_left 50%")
        MCONTROLLER.spin_left(SpeedSettings.SPEED_MEDIUM)
        time.sleep(sleep_len)
        MODULE_LOGGER.info("spin_right 50%")
        MCONTROLLER.spin_right(SpeedSettings.SPEED_MEDIUM)
        time.sleep(sleep_len)
        MODULE_LOGGER.info("turn_forward (left) 50%")
        MCONTROLLER.turn_forward(0, SpeedSettings.SPEED_MEDIUM)
        time.sleep(sleep_len)
        MODULE_LOGGER.info("turn_forward (right) 50%")
        MCONTROLLER.turn_forward(SpeedSettings.SPEED_MEDIUM, 0)
        time.sleep(sleep_len)
        MODULE_LOGGER.info("turn_reverse (right) 50%")
        MCONTROLLER.turn_reverse(0, SpeedSettings.SPEED_MEDIUM)
        time.sleep(sleep_len)
        MODULE_LOGGER.info("turn_reverse (left) 50%")
        MCONTROLLER.turn_reverse(SpeedSettings.SPEED_MEDIUM, 0)
        time.sleep(sleep_len)
        MODULE_LOGGER.info("left_forwards 50%")
        MCONTROLLER.left_forwards(SpeedSettings.SPEED_MEDIUM)
        time.sleep(sleep_len)
        MODULE_LOGGER.info("left_backwards 50%")
        MCONTROLLER.left_backwards(SpeedSettings.SPEED_MEDIUM)
        time.sleep(sleep_len)
        MODULE_LOGGER.info("right_forwards 50%")
        MCONTROLLER.right_forwards(SpeedSettings.SPEED_MEDIUM)
        time.sleep(sleep_len)
        MODULE_LOGGER.info("right_backwards 50%")
        MCONTROLLER.right_backwards(SpeedSettings.SPEED_MEDIUM)

    except KeyboardInterrupt:
        pass
    finally:
        MCONTROLLER.cleanup()


if __name__ == "__main__":
    test_motorcontroller(5)
