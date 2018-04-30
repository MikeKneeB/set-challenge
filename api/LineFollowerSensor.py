#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provides ability to read the three sensors of the line
follower module
"""

import logging
import IRSensor

MODULE_LOGGER = logging.getLogger("__main__.LineFollowerSensor")


class LineFollowerSensor(object):
    """
    Provides ability to read the three sensors of the line
    follower module
    """

    def __init__(self, left_sensor_id, middle_sensor_id, right_sensor_id):
        """
        Initialises the class
        """
        MODULE_LOGGER.info("Setting up LineFollowerSensor Module")

        self.sensor_l = IRSensor.IRSensor(left_sensor_id)
        self.sensor_m = IRSensor.IRSensor(middle_sensor_id)
        self.sensor_r = IRSensor.IRSensor(right_sensor_id)

    def get_l_state(self):
        """
        Get the state of the left sensor
        """
        return self.sensor_l.ir_active()

    def get_m_state(self):
        """
        Get the state of the middle sensor
        """
        return self.sensor_m.ir_active()

    def get_r_state(self):
        """
        Get the state of the right sensor
        """
        return self.sensor_r.ir_active()

    def cleanup(self):
        """
        Cleans up the GPIO port
        """
        self.sensor_l.cleanup()
