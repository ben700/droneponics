import datetime
import time
from datetime import datetime
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)


CO2 = AtlasI2C(105)

f = open("/home/pi/co2Data.txt", "a")
f.write(CO2.query("R"))
f.write(CO2.query("R").strip().rstrip('\x00'))
f.close()
