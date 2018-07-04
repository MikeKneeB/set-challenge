from api import (
    ServoController,
    UltrasonicSensor,
    MotorController,
    GPIOLayout,
    SpeedSettings
)

from time import sleep

if __name__ == '__main__':
    #servo = ServoController.ServoController()
    motor = MotorController.MotorController(GPIOLayout.MOTOR_LEFT_FORWARD_GPIO,
                                            GPIOLayout.MOTOR_LEFT_BACKWARD_GPIO,
                                            GPIOLayout.MOTOR_RIGHT_FORWARD_GPIO,
                                            GPIOLayout.MOTOR_RIGHT_BACKWARD_GPIO)
    ultra = UltrasonicSensor.UltrasonicSensor(GPIOLayout.SONAR_FRONT_TX_GPIO,
                                              qsize=10)
    #servo.start_servos()
    #servo.set_tilt_servo(0)
    #servo.set_pan_servo(0)
    initial_distance = ultra.measurement()
    motor.forward(SpeedSettings.SPEED_MEDIUM)
    sleep(5)
    motor.stop()
    final_distance = ultra.measurement()
    print(initial_distance - final_distance)
