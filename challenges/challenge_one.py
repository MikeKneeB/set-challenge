from object_detector_app import image_processor

from time import sleep

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
            GPIOLayout.MOTOR_RIGHT_BACKWARD_GPIO
        )
        self.imager = image_processor.ImageProcessor(im_disp = True)
        self.imager.start()

    def stop(self):
        self.motor.stop()
        self.imager.stop()

    def turn(self, time, rev = False):
        if rev:
            self.motor.spin_right(SpeedSettings.SPEED_FASTEST)
        else:
            self.motor.spin_left(SpeedSettings.SPEED_FASTEST)
        sleep(time)
        self.motor.stop()

    def forward(self, time):
        self.motor.forward(SpeedSettings.SPEED_FASTEST)
        sleep(time)
        self.motor.stop()

    def backward(self, time):
        self.motor.reverse(SpeedSettings.SPEED_FASTEST)
        sleep(time)
        self.motor.stop()

    def find_target(self, attempts = 20, turn_amt = 0.3, rev = False):
        print("Start find")
        total_spins = 0
        while total_spins != attempts: # Sevenish gets a full circle or so
            self.turn(turn_amt, rev)
            self.imager.go_sig.release()
            # Classes are:
            #   1 = obstacle
            #   2 = taret
            #   3 = decoy
            self.imager.sem.acquire()
            print("Got signal from imager that an image is ready")
            if 2 in self.imager.detected_classes:
                return True
            total_spins += 1
        return False

    def find_obstacle(self, attempts = 20, turn_amt = 0.3, rev = False):
        print("Start obst find")
        total_spins = 0
        while total_spins != attempts:
            self.turn(turn_amt, rev)
            self.imager.go_sig.release()
            self.imager.sem.acquire()
            print("Got signal from imager that an image is ready")
            if 1 in self.imager.detected_classes:
                return True
            total_spins += 1
        return False

    def pass_obstacle(self):
        print("Start obst. pass")
        while True:
            self.imager.go_sig.release()
            self.imager.sem.acquire()
            ind = self.imager.detected_classes.index(1)
            box = self.imager.bounding_boxes[ind]
            box_edge = box[3] + 10
            box_sz = abs(box[1] - box[3])
            print("Box edge: {} Box sz: {} Box coords: {},{}".format(box_edge, box_sz, box[1], box[3]))
            if box_edge < 410 and box_edge > 300:
                self.forward(0.3)
            elif box_edge > 410:
                self.turn(0.05, True)
            else:
                self.turn(0.05, False)

    def centre_target(self):
        print("Start centring")
        while True:
            self.imager.go_sig.release()
            self.imager.sem.acquire()
            try:
                ind = self.imager.detected_classes.index(2)
                box = self.imager.bounding_boxes[ind]
                box_mid = (box[1] + box[3]) / 2
                box_sz = abs(box[1] - box[3])
                print("Box mid: {} Box sz: {}".format(box_mid, box_sz))
                if box_mid < 260 and box_mid > 220:
                    return True
                elif box_mid > 260:
                    self.turn(0.05, True)
                else:
                    self.turn(0.05, False)
            except ValueError:
                print("Couldn't see")
                return False

    def charge(self):
        print("Start Charge")
        while True:
            self.forward(0.5)
            self.imager.go_sig.release()
            self.imager.sem.acquire()
            try:
                ind = self.imager.detected_classes.index(2)
                box = self.imager.bounding_boxes[ind]
                box_mid = (box[1] + box[3]) / 2
                box_sz = abs(box[1] - box[3])
                print("Box mid: {} Box sz: {}".format(box_mid, box_sz))
                if box_mid < 260 and box_mid > 220:
                    if box_sz > 300:
                        self.forward(0.4)
                        self.backward(0.4)
                        return True
                    pass
                else:
                    print("Freakout")
                    self.centre_target()
            except ValueError:
                return False

    def challenge(self):
        self.imager.sem.acquire()
        print('Got imager flag - good to go')
        rev = False
        while True:
            if self.find_target(rev = rev):
                print("'U'")
                print("Centring")
                # if target to left spin_left
                # if target to the right spin_right
                ind = self.imager.detected_classes.index(2)
                box = self.imager.bounding_boxes[ind]
                box_mid = (box[1] + box[3]) / 2
                box_sz = abs(box[1] - box[3])
                print("Box sz: {}".format(box_sz))
                print("Box mid: {}".format(box_mid))
                if self.centre_target():
                    self.charge()
                else:
                    self.forward(1)
                    if box_mid < 240:
                        rev = False
                    else:
                        rev = True
                    pass
            else:
                print("@ @")
                print(" ^")

    def challenge_two(self):
        self.imager.sem.acquire()
        print('Got imager flag - good to go')
        rev = False
        while True:
            if self.find_obstacle(rev = rev):
                print("Got a box")
                self.pass_obstacle()
            else:
                print("@ @")
                print(" ^")

if __name__ == '__main__':
    overlord = Overlord()
    try:
        overlord.challenge_two()
    except KeyboardInterrupt:
        print("Death")
        pass
    finally:
        print("Stopping...")
        overlord.stop()
