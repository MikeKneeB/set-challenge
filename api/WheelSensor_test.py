
import logging
import SetupConsoleLogger
import GPIOLayout
import WheelSensor
import MotorController
import SpeedSettings

MODULE_LOGGER = logging.getLogger("__main__")
SetupConsoleLogger.setup_console_logger(MODULE_LOGGER)

def test_sensors():
    try:
        left_sensor = WheelSensor.WheelSensor(GPIOLayout.WHEEL_SENSOR_LEFT_GPIO)
        right_sensor = WheelSensor.WheelSensor(GPIOLayout.WHEEL_SENSOR_RIGHT_GPIO)
        motor_controller = MotorController.MotorController(
            GPIOLayout.MOTOR_LEFT_FORWARD_GPIO,
            GPIOLayout.MOTOR_LEFT_BACKWARD_GPIO,
            GPIOLayout.MOTOR_RIGHT_FORWARD_GPIO,
            GPIOLayout.MOTOR_RIGHT_BACKWARD_GPIO)
        motor_controller.stop()
        motor_controller.forward(SpeedSettings.SPEED_MEDIUM)
        for i in range(20):
            left_sensor.print_val()
            right_sensor.print_val()
            sleep(0.2)
        motor_controller.stop()
        for i in range(10):
            left_sensor.print_val()
            right_sensor.print_val()
            sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        left_sensor.cleanup()
        right_sensor.cleanup()
