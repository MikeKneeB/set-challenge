#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provides a test version of the GPIOZero.GPIODevice class for platforms where
it doesn't exist.
"""


class OutputDevice(object):
    """
    Provides a stub for the GPIODevice class defined in GPIOZero
    """

    def __init__(self, param1):
        """
        Stub function
        """
        del param1
        self.active = False

    # pylint: disable=C0103
    def on(self):
        """
        Stub function
        """

    def off(self):
        """
        Stub function
        """

    def close(self):
        """
        Stub function
        """

    def is_active(self):
        """
        Stub function
        """
        return self.active

    def set_active(self, active):
        """
        Used to set whether the port is active, so as many branches as possible
        can be exercised
        """
        self.active = active
