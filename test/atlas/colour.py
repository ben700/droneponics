import datetime
import time
from datetime import datetime
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)


colour = AtlasI2C(112)

try:
    print(colour.query("R").rstrip('\x00') + '\n'))        
except:
    print("except")
