import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)

# Create the I2C bus
device = AtlasI2C(102)
device.query("i")
