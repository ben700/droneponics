##!/usr/bin/env python3 
from configparser import ConfigParser
from datetime import datetime
import time
import logging
import sys
import os
import blynklib
import blynktimer
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (
    AtlasI2C
)
import math  
import subprocess
import re
import drone

bootup = True
rowIndex=1

parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configCalibration/"+drone.gethostname()+".ini")


# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)

    
#test to see what log levels are outputted
_log.critical("critical")
_log.error("error")
_log.warning("warning")
_log.info("info")
_log.debug("debug")

_log.info("/home/pi/droneponics/config/configCalibration/"+drone.gethostname()+".ini")
    
# Initialize Blynk
blynk = blynklib.Blynk(parser.get('configCalibration', 'BLYNK_AUTH'))        
timer = blynktimer.Timer()
blynk.run()
#blynk.virtual_write(98, "clr")
blynk.set_property(drone.systemLED, 'color', drone.colours['ONLINE'])
_log.info("Blynk created")
    

sensors = []
nutrientMix = []

# Initialize the sensor.
try:
    _log.info("drone.buildNutrientMix")
    nutrientMix = drone.buildNutrientMix(nutrientMix, _log, scheduleWeek='Grow')
    _log.info("drone.buildSensors(sensors")
    sensors = drone.buildSensors(sensors, _log)
    _log.info("all senses created")
except:
    _log.eror("Error createing atals sensor or pumps ")




    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('configCalibration', 'BLYNK_AUTH'))        
    timer = blynktimer.Timer()
    blynk.run()
    #blynk.virtual_write(98, "clr")
    blynk.set_property(systemLED, 'color', drone.colours['ONLINE'])
    _log.info("Blynk created")

@blynk.handle_event('write V1')
def write_handler(pin, value): 
      staus = value[0]
      BLYNK_LOG("Button is pressed");
      Blynk.notify("D0 is pressed");
      answer = input("Are you sure you want to calibrate PH (y/n)")
      if (answer == 'y'):
         answer = input("Going to calibrate ph to mid 7.00. Enter y when you are ready(y/n)")
        

def main():
    blynk.run()
    for sensor in sensors:
        if sensor is not None:
            sensor.read()
            sensor.display(blynk)                   	
        
