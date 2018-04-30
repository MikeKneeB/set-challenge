#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This code is used on startup to initialise the various devices
used on the robot.
"""

import logging
import time
import GPIOLayout
import MotorController
import UltrasonicSensor
import SetupConsoleLogger
import ServoController

# Create a logger to both file and stdout
LOGGER = logging.getLogger(__name__)
SetupConsoleLogger.setup_console_logger(LOGGER)


def initialise_servos():
    """
    Initialise the three servos to their 0 degree position
    """
    LOGGER.info("  Initialising Servos")

    servo_controller = ServoController.ServoController()
    servo_controller.start_servos()
    time.sleep(1)
    servo_controller.set_pan_servo(0)
    servo_controller.set_tilt_servo(0)
    time.sleep(1)
    servo_controller.stop_servos()


def initialise_motor_controllers():
    """
    Initialise the motor controllers to outputs and all "off"
    """
    LOGGER.info("  Initialising Motor Controllers")

    motor_controller = MotorController.MotorController(
        GPIOLayout.MOTOR_LEFT_FORWARD_PIN, GPIOLayout.MOTOR_LEFT_BACKWARD_PIN,
        GPIOLayout.MOTOR_RIGHT_FORWARD_PIN,
        GPIOLayout.MOTOR_RIGHT_BACKWARD_PIN)
    motor_controller.stop()
    motor_controller.cleanup()


def initialise_ultrasonics():
    """
    Initialise the ultrasonics to inputs and outputs and off if required
    """
    LOGGER.info("  Initialising Ultrasonics")

    prox_front = UltrasonicSensor.UltrasonicSensor(
        GPIOLayout.SONAR_FRONT_TX_GPIO)
    prox_left = UltrasonicSensor.UltrasonicSensor(
        GPIOLayout.SONAR_LEFT_RX_GPIO, GPIOLayout.SONAR_LEFT_TX_GPIO)
    prox_right = UltrasonicSensor.UltrasonicSensor(
        GPIOLayout.SONAR_RIGHT_RX_GPIO, GPIOLayout.SONAR_RIGHT_TX_GPIO)
    prox_front.cleanup()
    prox_left.cleanup()
    prox_right.cleanup()


def main():
    """
    Main function to call each of the initialisation routines
    """
    initialise_servos()
    initialise_motor_controllers()
    initialise_ultrasonics()


if __name__ == "__main__":
    try:
        LOGGER.info("Starting the robot intialisation routine")
        main()
    except KeyboardInterrupt:
        LOGGER.info("Stopping the robot intialisation routine")
    finally:
        LOGGER.info("Completed the robot intialisation routine")
