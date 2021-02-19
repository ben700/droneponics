##!/usr/bin/env python3 
import sys
import os
sys.path.append('/home/pi/droneponics/droneAtlas')
from AtlasI2C import (AtlasI2C)

complete = False
while (complete is not True):
    complete = True
    try:
        co2 = AtlasI2C(105)
        print("Processing CO2")
        print(co2.query("O,t,1"))
        print(co2.query("O,?")) 
        print("Success CO2")
        complete = True
    except:
        print("Fail CO2")
        complete = False

    try:
        hum = AtlasI2C(111)
        print("Processing Humidity")
        print(hum.query("O,HUM,1"))
        print(hum.query("O,Dew,1"))
        print(hum.query("O,T,1"))
        print(hum.query("O,?")) 
        print("Success HUM")
    except:
        print("Failed hum")
        complete = False
    
    if(complete is not True):
        print("Something Failed will retry")
 
