#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provides ability to control the motors on the robot.
"""

from config_motors import (
    LEFT_MOTOR_OFFSET,
    RIGHT_MOTOR_OFFSET
)

import logging
import platform
if platform.machine() == "armv6l" or platform.machine() == "armv7l":
    import RPi.GPIO as GPIO
else:
    import GPIOStub as GPIO

MODULE_LOGGER = logging.getLogger("__main__.MotorController")


# pylint: disable=too-many-instance-attributes
class MotorController(object):
    """
    Provides ability to control the motors on the robot.
    """
    START_FREQ = 100

    def __init__(self, left_forward, left_backward, right_forward,
                 right_backward):
        """
        Initialises GPIO pins
        """
        self.left_forward = left_forward
        self.left_backward = left_backward
        self.right_forward = right_forward
        self.right_backward = right_backward

        log_string = "Setting up MotorController Module (lf:" + \
            str(self.left_forward) + \
            ", lb:" + \
            str(self.left_backward) + \
            ", rf:" + \
            str(self.right_forward) + \
            ", rb:" + \
            str(self.right_backward) + \
            ")"
        MODULE_LOGGER.info(log_string)

        # Use board pin numbering
        GPIO.setmode(GPIO.BCM)

        # Disable warnings
        GPIO.setwarnings(False)

        # use pwm on inputs so motors don't go too fast
        GPIO.setup(self.left_forward, GPIO.OUT)
        self.motor_left_forward = GPIO.PWM(self.left_forward, self.START_FREQ)
        self.motor_left_forward.start(0)

        GPIO.setup(self.left_backward, GPIO.OUT)
        self.motor_left_backward = GPIO.PWM(self.left_backward,
                                            self.START_FREQ)
        self.motor_left_backward.start(0)

        GPIO.setup(self.right_forward, GPIO.OUT)
        self.motor_right_forward = GPIO.PWM(self.right_forward,
                                            self.START_FREQ)
        self.motor_right_forward.start(0)

        GPIO.setup(self.right_backward, GPIO.OUT)
        self.motor_right_backward = GPIO.PWM(self.right_backward,
                                             self.START_FREQ)
        self.motor_right_backward.start(0)

    def cleanup(self):
        """
        Sets all motors off and sets GPIO to standard values
        """
        self.stop()
        log_string = "Cleaned up MotorController (lf:" + \
            str(self.left_forward) + \
            ", lb:" + \
            str(self.left_backward) + \
            ", rf:" + \
            str(self.right_forward) + \
            ", rb:" + \
            str(self.right_backward) + \
            ")"
        MODULE_LOGGER.info(log_string)

    def stop(self):
        """
        Causes the Robot to stop all motors
        """
        self.motor_left_forward.ChangeDutyCycle(0)
        self.motor_left_backward.ChangeDutyCycle(0)
        self.motor_right_forward.ChangeDutyCycle(0)
        self.motor_right_backward.ChangeDutyCycle(0)

    def forward(self, speed):
        """
        Move each wheel forward
        Sets both motors to move forward at speed. 0 <= speed <= 100
        """
        self.motor_left_forward.ChangeDutyCycle(speed + LEFT_MOTOR_OFFSET)
        self.motor_left_backward.ChangeDutyCycle(0)
        self.motor_right_forward.ChangeDutyCycle(speed + RIGHT_MOTOR_OFFSET)
        self.motor_right_backward.ChangeDutyCycle(0)

    def reverse(self, speed):
        """
        Move each wheel forward
        Sets both motors to reverse at speed. 0 <= speed <= 100
        """
        self.motor_left_forward.ChangeDutyCycle(0)
        self.motor_left_backward.ChangeDutyCycle(speed + LEFT_MOTOR_OFFSET)
        self.motor_right_forward.ChangeDutyCycle(0)
        self.motor_right_backward.ChangeDutyCycle(speed + RIGHT_MOTOR_OFFSET)

    def spin_left(self, speed):
        """
        Causes the Robot to rotate left as fast as possible
        Sets motors to turn opposite directions at speed. 0 <= speed <= 100
        """
        self.motor_left_forward.ChangeDutyCycle(0)
        self.motor_left_backward.ChangeDutyCycle(speed + LEFT_MOTOR_OFFSET)
        self.motor_right_forward.ChangeDutyCycle(speed + RIGHT_MOTOR_OFFSET)
        self.motor_right_backward.ChangeDutyCycle(0)

    def spin_right(self, speed):
        """
        Causes the Robot to rotate right as fast as possible
        Sets motors to turn opposite directions at speed. 0 <= speed <= 100
        """
        self.motor_left_forward.ChangeDutyCycle(speed + LEFT_MOTOR_OFFSET)
        self.motor_left_backward.ChangeDutyCycle(0)
        self.motor_right_forward.ChangeDutyCycle(0)
        self.motor_right_backward.ChangeDutyCycle(speed + RIGHT_MOTOR_OFFSET)

    def left_forwards(self, speed):
        """
        Causes the Robot to turn right using just one wheel
        Sets just one side to turn. 0 <= speed <= 100
        """
        self.motor_left_forward.ChangeDutyCycle(speed + LEFT_MOTOR_OFFSET)
        self.motor_left_backward.ChangeDutyCycle(0)

    def left_backwards(self, speed):
        """
        Causes the Robot to turn right using just one wheel
        Sets just one side to turn. 0 <= speed <= 100
        """
        self.motor_left_forward.ChangeDutyCycle(0)
        self.motor_left_backward.ChangeDutyCycle(speed + RIGHT_MOTOR_OFFSET)

    def right_forwards(self, speed):
        """
        Causes the Robot to turn right using just one wheel
        Sets just one side to turn. 0 <= speed <= 100
        """
        self.motor_right_forward.ChangeDutyCycle(speed + RIGHT_MOTOR_OFFSET)
        self.motor_right_backward.ChangeDutyCycle(0)

    def right_backwards(self, speed):
        """
        Causes the Robot to turn right using just one wheel
        Sets just one side to turn. 0 <= speed <= 100
        """
        self.motor_right_forward.ChangeDutyCycle(0)
        self.motor_right_backward.ChangeDutyCycle(speed + RIGHT_MOTOR_OFFSET)

    def turn_forward(self, left_speed, right_speed):
        """
        Moves forwards in an arc by setting different speeds.
        0 <= left_speed,right_speed <= 100
        """
        self.motor_left_forward.ChangeDutyCycle(left_speed + LEFT_MOTOR_OFFSET)
        self.motor_left_backward.ChangeDutyCycle(0)
        self.motor_right_forward.ChangeDutyCycle(right_speed + RIGHT_MOTOR_OFFSET)
        self.motor_right_backward.ChangeDutyCycle(0)

    def turn_reverse(self, left_speed, right_speed):
        """
        Moves backwards in an arc by setting different speeds.
        0 <= left_speed,right_speed <= 100
        """
        self.motor_left_forward.ChangeDutyCycle(0)
        self.motor_left_backward.ChangeDutyCycle(left_speed + LEFT_MOTOR_OFFSET)
        self.motor_right_forward.ChangeDutyCycle(0)
        self.motor_right_backward.ChangeDutyCycle(right_speed + RIGHT_MOTOR_OFFSET)
