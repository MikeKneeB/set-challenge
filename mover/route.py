from api import (
    UltrasonicSensorThread,
    MotorController,
    ServoController,
    GPIOLayout,
    SpeedSettings
)
from ave_speed import (
    AVE_SPEED
)
import time
import threading
import Queue

class RoutePoint:

    def __init__(self, distance, rotate):
        self.distance = distance
        self.rotate = rotate

class RouteControl:

    def __init__(self):
        self.route = Queue.Queue()
        self._motor_controller = MotorController.MotorController(
            GPIOLayout.MOTOR_LEFT_FORWARD_GPIO,
            GPIOLayout.MOTOR_LEFT_BACKWARD_GPIO,
            GPIOLayout.MOTOR_RIGHT_FORWARD_GPIO,
            GPIOLayout.MOTOR_RIGHT_BACKWARD_GPIO
        )
        self._motor_controller.stop()
        self._stop_event = threading.Event()

    def start(self):
        t = threading.Thread(target = self.run)
        t.start()

    def stop(self):
        self._stop_event.set()

    def run(self):
        running = True
        while running:
            next_point = self.route.get()
            # Hmmm...
            on_time = next_point.distance / AVE_SPEED 
            self._motor_controller.forward(SpeedSettings.SPEED_MEDIUM)
            stopped = self._stop_event.wait(on_time):
            self._motor_controller.stop()
            if not stopped:
                # Do rotation!
                rotate_time, direction = self.get_rotation(angle)
                if direction == 'left':
                    self._motor_controller.spin_left(SpeedSettings.SPEED_MEDIUM)
                    sleep(rotate_time)
                    self._motor_controller.stop()
                elif direction == 'right':
                    self._motor_controller.spin_right(SpeedSettings.SPEED_MEDIUM)
                    sleep(rotate_time)
                    self._motor_controller.stop()
            else:
                running = False

    def add_point(self, point):
        self.route.put(point)

    def add_point(self, dist, rot):
        self.route.put(RoutePoint(dist, rot))

    def rotate(self):
        pass
