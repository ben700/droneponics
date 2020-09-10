import time

import board
import busio

from adafruit_seesaw.seesaw import Seesaw

#i2c_bus = busio.I2C(SCL, SDA)
i2c_bus = busio.I2C(board.D1, board.D0) 

ss = Seesaw(i2c_bus, addr=0x38)

while True:
    # read moisture level through capacitive touch pad
    touch = ss.moisture_read()

    # read temperature from the temperature sensor
    temp = ss.get_temp()

    print("temp: " + str(temp) + "  moisture: " + str(touch))
    time.sleep(1)
