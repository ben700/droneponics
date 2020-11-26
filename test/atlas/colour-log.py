import datetime
import time
from datetime import datetime
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)


colour = AtlasI2C(112)

while True:
    try:
        f = open("/home/pi/colourData.txt", "a")
        now = datetime.now()
        f.write( now.strftime("%d/%m/%Y %H:%M:%S") + "     "+ colour.query("R").rstrip('\x00') + '\n')
        f.close()
        time.sleep(5)
    except:
        f = open("/home/pi/colourData.txt", "a")
        now = datetime.now()
        f.write( now.strftime("%d/%m/%Y %H:%M:%S") + "     except" + '\n')
        f.close()
