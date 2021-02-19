##!/usr/bin/env python3 
import sys
import os
import time
sys.path.append('/home/pi/droneponics/droneAtlas/drone')
from AtlasI2C import (AtlasI2C)

complete = False
while (complete is not True):
    complete = True
    try:
        co2 = AtlasI2C(105)
        print(co2.query("O,?"))     
    except:
        complete = False
        co2 = None
        print("Failed : No CO2 sensor")
    try:
        if(co is not None):
            print(co2.query("O,t,1"))
            print(co2.query("O,?")) 
            print("Success CO2")
            complete = True
    except:
        print("Fail CO2")
        complete = False

    try:
        hum = AtlasI2C(111)
        print(hum.query("O,?")) 
    except:
        complete = False
        hum = None
        print("Failed : No Humidity sensor")
        
        
    try:
        if(hum is not None):
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
    time.sleep(5) #give time to read
