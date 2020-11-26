import datetime
import time
from datetime import datetime
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)


CO2 = AtlasI2C(105)

while True:
    try:
        f = open("/home/pi/co2Data.txt", "a")
        now = datetime.now()
        f.write( now.strftime("%d/%m/%Y %H:%M:%S") + "     "+ CO2.query("R").rstrip('\x00') + '\n')
        f.close()
        time.sleep(5)
    except:
        f = open("/home/pi/co2Data.txt", "a")
        now = datetime.now()
        f.write( now.strftime("%d/%m/%Y %H:%M:%S") + "     except" + '\n')
        f.close()
