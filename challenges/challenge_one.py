from object_detector_app import image_processor

from api import (
    MotorController,
    SpeedSettings,
    GPIOLayout,
    IRSensor
)

class Overlord(object):

    def __init__(self):
        self.motor = MotorController.MotorController(
            GPIOLayout.MOTOR_LEFT_FORWARD_GPIO,
            GPIOLayout.MOTOR_LEFT_BACKWARD_GPIO,
            GPIOLayout.MOTOR_RIGHT_FORWARD_GPIO,
            GPIOLayout.MOTOR_RIGHT_BACKWARD_GPIO)
        )
        self.servo = ServoController.ServoController()
        self.servo.start_servos()
        self.imager = image_processor.ImageProcessor(im_disp = False)
        self.imager.start()
        print("Waiting for imager thread to init......")
        sleep(5)
        print("Imager thread is probably init by now and if its not who cares lets go")

    def stop(self):
        self.motor.stop()

    def norm_servo(self):
        sleep(0.5)
        self.servo.set_pan_servo(0)
        self.servo.set_tilt_servo(0)

    def turn(self, time, rev = False):
        if rev:
            self.motor.spin_right(SpeedSettings.SPEED_FASTEST)
        else:
            self.motor.spin_left(SpeedSettings.SPEED_FASTEST)
        sleep(time)
        self.motor.stop()

    def find_target(self, attempts = 6):
        total_spins = 0
        while total_spins != attempts: # Sevenish gets a full circle or so
            self.turn(0.5)
            sleep(1)
            # Classes are:
            #   1 = obstacle
            #   2 = taret
            #   3 = decoy
            if imager.detected_classes.contains(2):
                return True
        return False

    def centre_target(self):
        pass

    def charge(self):
        pass

    def challenge(self):
        if self.find_target():
            print("'U'")
            self.centre_target()
            self.charge()
        else:
            print("@ @")
            print(" ^")

if __name__ == '__main__':
    overlord = Overlord()
    try:
        overlord.challenge()
    except KeyboardInterrupt:
        pass
    finally:
        overlord.stop()
