#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Class to interact with ir proximity sensors
"""

import logging
import platform
if platform.machine() == "armv6l" or platform.machine() == "armv7l":
    import RPi.GPIO as GPIO
else:
    import GPIOStub as GPIO

MODULE_LOGGER = logging.getLogger("__main__.IRSensor")


class IRSensor(object):  # pylint: disable=too-few-public-methods
    """
    Defines the interaction with the ir proximity sensors
    """

    def __init__(self, gpio_id):
        """
        Initialise the parameters required for the IR Sensor
        """
        self.gpio_id = gpio_id
        MODULE_LOGGER.info("Setting up IRSensor Module")

        # Use physical pin numbering
        GPIO.setmode(GPIO.BCM)

        # Disable warnings
        GPIO.setwarnings(False)

        # set up digital line detectors as inputs
        GPIO.setup(self.gpio_id, GPIO.IN)

    def ir_active(self):
        """
        Returns state of Left IR Obstacle sensor
        """
        return bool(GPIO.input(self.gpio_id) == 0)

    @staticmethod
    def cleanup():
        """
        Cleans up the GPIO port
        """
        GPIO.cleanup()
