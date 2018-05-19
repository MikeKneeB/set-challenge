import UltrasonicSensorThread
import MotorController
import GPIOLayout
import SpeedSettings

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
        self._initial_distance = 0
        self._speed = SpeedSettings.SPEED_SLOW

    def ultrasonic_callback(self, distance):
        print("{} - {}".format(self._initial_distance - distance,
                               route[0].distance))
        if self._initial_distance - distance == self.route[0].distance:
            self._motor_controller.stop()
            self.rotate()
            self.route.pop()
            self._initial_distance = self._sensor_thread.read_data()
            self._motor_controller.forward(self._speed)

    def start(self):
        self._sensor_thead.start()
        self._initial_distance = self._sensor_thead.read_data()

    def add_point(self, point):
        self.route.append(point)

    def add_point(self, dist, rot):
        self.route.append(RoutePoint(dist, rot))
