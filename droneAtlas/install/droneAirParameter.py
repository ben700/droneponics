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
        time.sleep(1)
        print("CO2 Read starting config :" + co2.query("O,?"))     
    except:
        complete = False
        co2 = None
        print("Failed : No CO2 sensor")
    try:
        if(co2 is not None):
            print("CO2 Turn on temp :" + co2.query("O,t,1"))
            print("CO2 Read ending config :" + co2.query("O,?")) 
            print("Success : Processing CO2 commands")
            complete = True
    except:
        print("Failed : Processing CO2 commands")
        complete = False

    try:
        hum = AtlasI2C(111)
        time.sleep(1)
        print("Humidity Read starting config :" + hum.query("O,?")) 
    except:
        complete = False
        hum = None
        print("Failed : No Humidity sensor")
        
        
    try:
        if(hum is not None):
            print("Humidity Turn on Humidity :" + hum.query("O,HUM,1"))
            print("Humidity Turn on dew :" + hum.query("O,Dew,1"))
            print("Humidity Turn on temp :" + hum.query("O,T,1"))
            print("Humidity Read ending config :" + hum.query("O,?")) 
            print("Success : Processing Humidity commands")
    except:
        print("Failed : Processing Humidity commands")
        complete = False
    
    if(complete is not True):
        print("")
    time.sleep(5) #give time to read
