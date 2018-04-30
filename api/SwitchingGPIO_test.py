#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provides the test functionality for the SwitchingGPIO class
"""

import logging
import SetupConsoleLogger
import SwitchingGPIO

MODULE_LOGGER = logging.getLogger("__main__")
SetupConsoleLogger.setup_console_logger(MODULE_LOGGER)


def run_test(gpio_if):
    """
    Performs on/ off and state check tests
    """
    gpio_if.switch_on()
    gpio_if.socket.set_active(False)
    gpio_if.is_on()
    gpio_if.socket.set_active(True)
    gpio_if.is_on()

    gpio_if.switch_off()
    gpio_if.socket.set_active(False)
    gpio_if.is_on()
    gpio_if.socket.set_active(True)
    gpio_if.is_on()


def test_switchinggpio():
    """
    Tests the switching gpio using both active low and active high modes
    """
    try:
        active_high = SwitchingGPIO.SwitchingGPIO(1)
        run_test(active_high)
        active_low = SwitchingGPIO.SwitchingGPIO(1, False)
        run_test(active_low)

    except KeyboardInterrupt:
        pass
    finally:
        pass


if __name__ == "__main__":
    test_switchinggpio()
