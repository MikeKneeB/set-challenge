from time import sleep
from api import (
    IRSensor,
    GPIOLayout
)

LEFT_SENSOR = IRSensor.IRSensor(GPIOLayout.IR_LEFT_GPIO)
RIGHT_SENSOR = IRSensor.IRSensor(GPIOLayout.IR_RIGHT_GPIO)

def careful_sleep(time):
    elapsed = 0
    while elapsed < time:
        sleep(0.001)
        if LEFT_SENSOR.ir_active() or RIGHT_SENSOR.ir_active():
            print("Sensor trigger")
            return False
        print("No sensor trigger")
        elapsed += 0.001
    return True
