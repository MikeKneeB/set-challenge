#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provides the test functionality for the Ultrasonic Sensor
"""

import logging
import SetupConsoleLogger
import GPIOLayout
import UltrasonicSensor

MODULE_LOGGER = logging.getLogger("__main__")
SetupConsoleLogger.setup_console_logger(MODULE_LOGGER, logging.DEBUG)


def test_ultrasonic():
    """
    Tests the simple ultrasonic sensor
    """
    try:
        PROXITY_TWO_IO_LEFT = UltrasonicSensor.UltrasonicSensor(
            GPIOLayout.SONAR_LEFT_RX_GPIO, GPIOLayout.SONAR_LEFT_TX_GPIO)
        MODULE_LOGGER.info("Left: " + format(PROXITY_TWO_IO_LEFT.measurement(),
                                             '.2f') + " cm")
        PROXITY_TWO_IO_LEFT.cleanup()

        PROXITY_TWO_IO_RIGHT = UltrasonicSensor.UltrasonicSensor(
            GPIOLayout.SONAR_RIGHT_RX_GPIO, GPIOLayout.SONAR_RIGHT_TX_GPIO)
        MODULE_LOGGER.info("Right: " + format(
            PROXITY_TWO_IO_RIGHT.measurement(), '.2f') + " cm")
        PROXITY_TWO_IO_RIGHT.cleanup()

        PROXITY_ONE_IO = UltrasonicSensor.UltrasonicSensor(
            GPIOLayout.SONAR_FRONT_TX_GPIO)
        MODULE_LOGGER.info(
            "Front: " + format(PROXITY_ONE_IO.measurement(), '.2f') + " cm")
        PROXITY_ONE_IO.cleanup()

        PROXITY_HIGH_Q = UltrasonicSensor.UltrasonicSensor(
            GPIOLayout.SONAR_FRONT_TX_GPIO, qsize=20)
        MODULE_LOGGER.info("Front - Large Queue Average: " +
                           format(PROXITY_HIGH_Q.measurement(), '.2f') + " cm")
        PROXITY_HIGH_Q.cleanup()

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    test_ultrasonic()
