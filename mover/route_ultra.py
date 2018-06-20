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
    '''
    Point on a route - distance followed by a rotation. This may not stay
    necessary depending on how we continue to do routing...
    '''
    def __init__(self, distance, rotate):
        '''
        Awh jeez, it's a struct...
        '''
        self.distance = distance
        self.rotate = rotate

class RouteControl:
    '''
    Does route control jobs. Who knows how stable this class will be, but for
    now it should do the trick? We might need to think about how the ultrasonic
    thread is going to work as well. If threads need to access the ultrasonic
    we'll need a rethink on that one...
    '''

    def __init__(self):
        '''
        Inits the route controller. Creates an ultrasonic sensor thread, a motor
        controller and servo controller.
        '''
        self.route = []
        self._sensor_thread = UltrasonicSensorThread.UltrasonicSensorThread(
            0.01,
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
        self._motor_controller.stop()
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
        t = threading.Thread(target = self.run)
        t.start()

    def stop(self):
        self._sensor_thread.exit_now()
        self._sensor_thread.join()
        self._stop_event.set()

    def run(self):
        while self.route:
            self._motor_controller.forward(SpeedSettings.SPEED_MEDIUM)
            at_target = False
            while not at_target:
                if not self._stop_event.wait(0.01):
                    with self._dist_lock:
                        print(self._distance_difference)
                        close = self.route[0].distance - self._distance_difference
                        print(close)
                        if close < 5:
                            at_target = True
                else:
                    self._motor_controller.stop()
                    return
            self._motor_controller.stop()
            self.route.pop()

    def add_point(self, point):
        self.route.append(point)

    def add_point(self, dist, rot):
        self.route.append(RoutePoint(dist, rot))

    def rotate(self):
        self._motor_controller.spin_left(SpeedSettings.SPEED_MEDIUM)
        for i in range(200):
            print('{},{}'.format(i,
                 self._sensor_thread.read_data())
            time.sleep(0.01)
