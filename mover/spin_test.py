from api import (
    MotorController,
    GPIOLayout,
    SpeedSettings
)

import time

if __name__ == '__main__':
    try:
        motor = MotorController.MotorController(GPIOLayout.MOTOR_LEFT_FORWARD_GPIO,
                                                GPIOLayout.MOTOR_LEFT_BACKWARD_GPIO,
                                                GPIOLayout.MOTOR_RIGHT_FORWARD_GPIO,
                                                GPIOLayout.MOTOR_RIGHT_BACKWARD_GPIO)
        start = time.time()
        motor.spin_left(SpeedSettings.SPEED_MEDIUM)
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        end = time.time()
        print(end - start)
