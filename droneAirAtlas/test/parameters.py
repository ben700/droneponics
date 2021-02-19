
##!/usr/bin/env python3 
import time
import sys
import os
sys.path.append('/home/pi/droneponics/droneAirAtlas')
from AtlasI2C import (AtlasI2C)
    
CO2 = AtlasI2C(105)
HUM = AtlasI2C(111)

CO2.write("R")
print(CO2.read())
