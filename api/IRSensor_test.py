#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provides the test functionality for the IRSensor
"""

import logging
import SetupConsoleLogger
import GPIOLayout
import IRSensor

MODULE_LOGGER = logging.getLogger("__main__")
SetupConsoleLogger.setup_console_logger(MODULE_LOGGER)


def test_irsensor():
    """
    Test a single IR sensor
    """
    SENSOR = None

    try:
        SENSOR = IRSensor.IRSensor(GPIOLayout.LINE_FOLLOWER_MIDDLE_GPIO)
        MODULE_LOGGER.info("ir_active: " + str(SENSOR.ir_active()))
    except KeyboardInterrupt:
        pass
    finally:
        SENSOR.cleanup()


if __name__ == "__main__":
    test_irsensor()
