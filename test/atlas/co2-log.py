import datetime
import time
from datetime import datetime
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)


CO2 = AtlasI2C(105)

f = open("/home/pi/co2Data.txt", "a")
f.write('\n')
f.write(CO2.query("R"))
f.write('\n')
f.write(CO2.query("R").strip().rstrip('\x00'))
f.write('\n')
f.write(CO2.query("R").strip())
f.write('\n')
f.write(CO2.query("R").rstrip('\x00'))
f.write('\n')
f.write("End")
now = datetime.now()
f.write("%d/%m/%Y %H:%M:%S")
    
f.close()
