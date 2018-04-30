#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Class for enabling a gpio port to be switched on and off
"""

import logging
import platform
if platform.machine() == "armv6l" or platform.machine() == "armv7l":
    import RPi.GPIO as GPIO
    try:
        from gpiozero import OutputDevice
    except ImportError:
        print "ERROR importing OutputDevice from gpiozero"
else:
    from GPIOZeroStub import OutputDevice as OutputDevice
    import GPIOStub as GPIO

MODULE_LOGGER = logging.getLogger("__main__.SwitchingGPIO")


class SwitchingGPIO(object):
    """
    Defines the interaction with a GPIO socket
    """

    def __init__(self, bcm_num, active_high=True):
        """
        Initialise the parameters required for the switching base class
        """
        MODULE_LOGGER.info("GPIO Class init on socket " + str(bcm_num) +
                           " active high " + str(active_high))

        # Use board pin numbering
        GPIO.setmode(GPIO.BCM)

        self.bcm_num = bcm_num
        self.active_high = active_high
        self.socket = OutputDevice(bcm_num)
        self.switch_off()

    def __del__(self):
        """
        Destructor
        """
        MODULE_LOGGER.info("GPIO Switch closed on socket " + str(self.bcm_num))
        self.socket.close()

    def switch_on(self):
        """
        Switches socket on
        """
        MODULE_LOGGER.debug("Switching on " + str(self.bcm_num))
        if self.active_high:
            self.socket.on()
        else:
            self.socket.off()

    def switch_off(self):
        """
        Switches socket off
        """
        MODULE_LOGGER.debug("Switching off " + str(self.bcm_num))
        if self.active_high:
            self.socket.off()
        else:
            self.socket.on()

    def is_on(self):
        """
        Gets the state of the gpio line
        """
        if self.socket.is_active:
            if self.active_high:
                MODULE_LOGGER.debug("State is True")
                return True
            else:
                MODULE_LOGGER.debug("State is False")
                return False
        else:
            if self.active_high:
                MODULE_LOGGER.debug("State is False")
                return False
            else:
                MODULE_LOGGER.debug("State is True")
                return True
