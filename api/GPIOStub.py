#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provides a test version of the GPIO class for platforms where
it doesn't exist.
"""

import random

BOARD = 1
BCM = 2
OUT = 3
IN = 4


class PWMObject(object):
    """
    Provides a stub for the PWM class defined in Rpi
    """

    def __init__(self):
        """
        Stub function
        """

    @staticmethod
    def start(param):
        """
        Stub function
        """
        del param

    @staticmethod
    # pylint: disable=C0103
    def ChangeDutyCycle(param1):
        """
        Stub function
        """
        del param1


def setmode(param):
    """
    Stub function
    """
    del param


def setwarnings(param):
    """
    Stub function
    """
    del param


def setup(param1, param2):
    """
    Stub function
    """
    del param1, param2


def output(param1, param2):
    """
    Stub function
    """
    del param1, param2


# pylint: disable=W0622
def input(param1):
    """
    Stub function
    """
    del param1
    return random.randint(0, 1)


# pylint: disable=C0103
def PWM(param1, param2):
    """
    Stub function
    """
    del param1, param2
    return PWMObject()


def cleanup():
    """
    Stub function
    """
