from api import (
    MotorController,
    SpeedSettings,
    GPIOLayout
)
from time import sleep
import precision_time as pt

def slight_move(m):
    m.spin_left(SpeedSettings.SPEED_FASTEST)
    sleep(0.2)
    m.stop()

if __name__ == '__main__':
    m = MotorController.MotorController(
        GPIOLayout.MOTOR_LEFT_FORWARD_GPIO,
        GPIOLayout.MOTOR_LEFT_BACKWARD_GPIO,
        GPIOLayout.MOTOR_RIGHT_FORWARD_GPIO,
        GPIOLayout.MOTOR_RIGHT_BACKWARD_GPIO)
    try:
        for i in range(10):
            slight_move(m)
            sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        m.stop()
        #end = pt.monotonic_time()
        #print()
        #print(end - start)
