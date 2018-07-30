from time import sleep
from random import random
import argparse
import sys
from object_detector_app import image_processor
from utility.ir_monitor import careful_sleep
from api import (
    MotorController,
    SpeedSettings,
    GPIOLayout,
    IRSensor
)

parser = argparse.ArgumentParser()
parser.add_argument("challenge", type = int, help = "Which challenge to run.")

class Overlord(object):

    def __init__(self):
        self.motor = MotorController.MotorController(
            GPIOLayout.MOTOR_LEFT_FORWARD_GPIO,
            GPIOLayout.MOTOR_LEFT_BACKWARD_GPIO,
            GPIOLayout.MOTOR_RIGHT_FORWARD_GPIO,
            GPIOLayout.MOTOR_RIGHT_BACKWARD_GPIO
        )
        self.long_ir = IRSensor.IRSensor(GPIOLayout.IR_LEFT_GPIO)
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

    def explore(self):
        self.motor.forward(SpeedSettings.SPEED_FAST)
        for i in range(50):
            sleep(0.1)
            if self.long_ir.ir_active():
                self.motor.stop()
                ran_turn = random() * 0.8
                self.turn(0.2 + ran_turn)
                self.motor.forward(SpeedSettings.SPEED_FAST)

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
            #if 2 in self.imager.detected_classes:
            if self.check_for_target():
                return True
            total_spins += 1
        return False

    def find_obstacle(self, attempts = 20, turn_amt = 0.3, rev = False, thing = 1):
        print("Start obst find")
        total_spins = 0
        while total_spins != attempts:
            self.turn(turn_amt, rev)
            self.imager.go_sig.release()
            self.imager.sem.acquire()
            print("Got signal from imager that an image is ready")
            print(self.imager.detected_classes)
            if thing in self.imager.detected_classes:
                return True
            total_spins += 1
        return False

    def check_obstacle(self, rev, thing = 1):
        print("Start obst. check - going {}".format(rev))
        spins = 0
        while True:
            self.imager.go_sig.release()
            self.imager.sem.acquire()
            if self.check_for_target():
                return True
            if thing in self.imager.detected_classes:
                print("Check found obst.")
                self.turn(0.15 * spins, not rev)
                return False
            elif spins != 1:
                print("Keep checking")
                self.turn(0.15, rev)
            else:
                print("Saw nothing, go back")
                self.turn(0.15 * spins, not rev)
                return True
            spins += 1

    def check_for_target(self):
        if 2 in self.imager.detected_class:
            print("There is a target")
            obscured = 0
            target_ind = self.imager.detected_classes.index(2)
            obst_indices = [i for i, x in enumerate(self.imager.detected_classes) if x == 1 or x == 3]
            target_box = self.imager.bounding_boxes[target_ind]
            for i in obst_indices:
                if (self.imager.bounding_boxes[i][1] < target_box[3] + 10
                 or self.imager.bounding_boxes[i][1] > target_box[3] - 10
                 or self.imager.bounding_boxes[i][3] < target_box[1] + 10
                 or self.imager.bounding_boxes[i][3] > target_box[1] - 10):
                    print("An obstacle or decoy is close...")
                    obstacle_sz = abs(self.imager.bounding_boxes[i][1] - self.imager.bounding_boxes[i][3])
                    target_sz = abs(target_box[1] - target_box[3])
                    if target_sz > obstacle_sz:
                        print("But it looks like the target is in front of the obstacle.")
                    else:
                        print("Looks like obstacle is in front of target.")
                        obscured += 1
                else:
                    print("That obstacle is far from the target.")
            if obscured == 0:
                print("We saw an obstacle and we don't think it is obscured")
                return True
            else:
                print("We saw an obstacle but it looks like something is in front of it")
                return False
        else:
            print("No target in sight")
            return False

    def pass_obstacle(self, thing = 1):
        passing = None
        print("Start obst. pass")
        while True:
            self.imager.go_sig.release()
            self.imager.sem.acquire()
            try:
                ind = self.imager.detected_classes.index(thing)
                box = self.imager.bounding_boxes[ind]
                box_mid = (box[1] + box[3]) / 2
                box_sz = abs(box[1] - box[3])
                if box_mid > 240:
                    passing = 'right'
                    print("@@@@ Box mid > 240")
                    box_edge = box[1]
                    print("Box edge: {} Box mid: {} Box sz: {} Box coords: {},{}".format(box_edge, box_mid, box_sz, box[1], box[3]))
                    if box_edge < 410 and box_edge > 340:
                        print("Obst pass going forward.")
                        self.forward(0.3)
                    elif box_edge > 410:
                        print("Obst pass turning right")
                        self.turn(0.07, True)
                    else:
                        print("Obst pass turning left")
                        self.turn(0.07, False)
                else:
                    passing = 'left'
                    print("@@@@ Box mid < 240")
                    box_edge = box[3]
                    print("Box edge: {} Box mid: {} Box sz: {} Box coords: {},{}".format(box_edge, box_mid, box_sz, box[1], box[3]))
                    if box_edge > 70 and box_edge < 140:
                        print("Obst pass going forward")
                        self.forward(0.3)
                    elif box_edge < 70:
                        print("Obst pass turning left")
                        self.turn(0.07, False)
                    else:
                        print("Obst pass turning right")
                        self.turn(0.07, True)
            except ValueError:
                print("No longer seeing obst. Let's go")
                self.forward(1.5)
                return passing

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
                if 3 in self.imager.detected_classes:
                    print("check decoy")
                    dec_box = self.imager.detected_classes.index(3)
                    dec_box_sz = abs(box[1] - box[3])
                    if dec_box_sz > box_sz:
                        pass_obstacle(thing = 3)
                print("Box mid: {} Box sz: {} Box coords: {},{}".format(
                  box_mid, box_sz, box[1], box[3]))
                if box[1] < 240 and box[3] > 240:
                    return True
                elif box[1] > 240:
                    self.turn(0.05, True)
                else:
                    self.turn(0.05, False)
            except ValueError:
                print("Couldn't see")
                return False

    def charge(self):
        print("Start Charge")
        while True:
            self.forward(1)
            self.imager.go_sig.release()
            self.imager.sem.acquire()
            try:
                ind = self.imager.detected_classes.index(2)
                box = self.imager.bounding_boxes[ind]
                box_mid = (box[1] + box[3]) / 2
                box_sz = abs(box[1] - box[3])
                print("Box mid: {} Box sz: {}".format(box_mid, box_sz))
                if box_mid < 260 and box_mid > 220: # Change this to use edges
                    if box_sz > 250:
                        print("Clooooose")
                        self.forward(1)
                        self.backward(0.4)
                        return True
                    pass
                else:
                    print("Freakout")
                    self.centre_target() # Check return value here.
            except ValueError:
                return False

    def challenge(self):
        self.imager.sem.acquire()
        self.backward(4)
        # Maybe ask for a new image?
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
            else:
                print("@ @")
                print(" ^")

    def challenge_two(self):
        self.imager.sem.acquire()
        print('Got imager flag - good to go')
        rev = False
        while True:
            if self.find_target(attempts = 10, turn_amt = 0.2, rev = rev):
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
            elif self.find_obstacle(rev = rev):
                print("Got a box")
                side = self.pass_obstacle()
                print("Side: {}".format(side))
                if side == 'left':
                   if self.check_obstacle(False):
                       self.pass_obstacle()
                elif side == 'right':
                   if self.check_obstacle(True):
                       self.pass_obstacle()
                else:
                    print("Freakout")
            elif self.find_obstacle(rev = rev, thing = 3):
                print("It's a trap.")
                side = self.pass_obstacle()
                print("Side: {}".format(side))
                if side == 'left':
                    if self.check_obstacle(False):
                        self.pass_obstacle()
                    elif side == 'right':
                        if self.check_obstacle(True):
                            self.pass_obstacle()
                        else:
                            print("Freakout")
            else:
                self.explore()
                print("@ @")
                print(" ^")

    def obst_test(self):
        self.imager.sem.acquire()
        print("Lets go")
        rev = False
        if self.find_obstacle(attempts = 6, rev = rev):
            print("Got a box")
            side = self.pass_obstacle()
            print("Side: {}".format(side))
            if side == 'right':
                while not self.check_obstacle(False):
                    self.pass_obstacle()
            elif side == 'left':
                while not self.check_obstacle(True):
                    self.pass_obstacle()
            else:
                print("Freakout")
        else:
            print("@ @")
            print(" ^")

    def im_test(self):
        self.imager.sem.acquire()
        print("Lets go")
        while True:
            self.imager.go_sig.release()
            self.imager.sem.acquire()

    def explore_test(self):
        while True:
            print("Exploring")
            self.explore()

    def careful_test(self):
        self.forward(2)

if __name__ == '__main__':
    args = parser.parse_args()
    overlord = Overlord()
    try:
        if args.challenge == 1:
            overlord.challenge()
        elif args.challenge == 2:
            overlord.challenge_two()
        elif args.challenge == 10:
            overlord.im_test()
        elif args.challenge == 11:
            overlord.obst_test()
        elif args.challenge == 12:
            overlord.careful_test()
        elif args.challenge == 13:
            overlord.explore_test()
        else:
            print("I'm afraid I can't do that.")
    except KeyboardInterrupt:
        print("Death")
        pass
    finally:
        print("Stopping...")
        overlord.stop()
