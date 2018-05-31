import logging
import platform
if platform.machine() == "armv6l" or platform.machine() == "armv7l":
    import RPi.GPIO as GPIO
else:
    import GPIOStub as GPIO

MODULE_LOGGER = logging.getLogger("__main__.IRSensor")

class WheelSensor(object):

    def __init__(self, gpio_id):
        self.gpio_id = gpio_id
        MODULE_LOGGER.info("Setting up IRSensor Module")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        GPIO.setup(self.gpio_id, GPIO.IN)

    def print_val(self):
        MODULE_LOGGER.info("GPIO Value: {}".format(GPIO.input(self.gpio_id)))

    def cleanup():
        GPIO.cleanup()
