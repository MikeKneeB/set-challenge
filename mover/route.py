from api import (
    UltrasonicSensorThread,
    MotorController,
    ServoController,
    GPIOLayout,
    SpeedSettings
)
import time
import threading

class RoutePoint:

    def __init__(self, distance, rotate):
        self.distance = distance
        self.rotate = rotate

class RouteControl:

    def __init__(self):
        self.route = []
        self._sensor_thread = UltrasonicSensorThread.UltrasonicSensorThread(
            0.5,
            self.ultrasonic_callback,
            GPIOLayout.SONAR_FRONT_TX_GPIO,
            GPIOLayout.SONAR_FRONT_RX_GPIO,
            1
        )
        self._motor_controller = MotorController.MotorController(
            GPIOLayout.MOTOR_LEFT_FORWARD_GPIO,
            GPIOLayout.MOTOR_LEFT_BACKWARD_GPIO,
            GPIOLayout.MOTOR_RIGHT_FORWARD_GPIO,
            GPIOLayout.MOTOR_RIGHT_BACKWARD_GPIO
        )
        self._servo_controller = ServoController.ServoController()
        self._servo_controller.start_servos()
        self._initial_distance = 0
        self._speed = SpeedSettings.SPEED_SLOW
        self._distance_difference = 0
        self._dist_lock = threading.Lock()
        self._stop_event = threading.Event()

    def ultrasonic_callback(self, distance):
        with self._dist_lock:
            self._distance_difference = self._initial_distance - distance

    def start(self):
        self._servo_controller.set_pan_servo(0)
        self._servo_controller.set_tilt_servo(0)
        self._sensor_thread.start()
        time.sleep(0.5)
        self._initial_distance = self._sensor_thread.read_data()
        self.run()

    def stop(self):
        self._sensor_thread.exit_now()
        self._sensor_thread.join()

    def run(self):
        while self.route:
            self._motor_controller.forward(SpeedSettings.SPEED_VERYSLOW)
            at_target = False
            while not at_target:
                if not self._stop_event.wait(0.5):
                    with self._dist_lock:
                        print(self._distance_difference)
                        close = self.route[0].distance - self._distance_difference
                        if close < 5 or close > -5:
                            at_target = True
            self._motor_controller.stop()
            self.route.pop()

    def add_point(self, point):
        self.route.append(point)

    def add_point(self, dist, rot):
        self.route.append(RoutePoint(dist, rot))

    def rotate(self):
        pass
