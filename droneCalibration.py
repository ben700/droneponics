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


def displayState():
     for sensor in sensors:
          if sensor is not None:
                sensor.currenCalibration()
		
	
@blynk.handle_event('write V1')
def write_handler(pin, value): 
      staus = value[0]
      BLYNK_LOG("Button is pressed");
      Blynk.notify("D0 is pressed");
      answer = input("Are you sure you want to calibrate PH (y/n)")
      if (answer == 'y'):
         answer = input("Going to calibrate ph to mid 7.00. Enter y when you are ready(y/n)")
		
@blynk.handle_event('write V60')
def v60write_handler(pin, value):
      _log.debug("v60write_handler and value[0] = " + str(value[0]))
      if (value[0] == '1'):
           _log.debug("Clear Caibration")
           displaySensorData[1].query("Cal,clear")
           displayState()  
      blynk.virtual_write(60,0)

@blynk.handle_event('write V61')
def v61write_handler(pin, value): 
      if (value[0] == '1'):
           _log.debug("Clear Caibration")
           sensors[2].query("Cal,clear")
           sensors[3].query("Cal,clear")
           displaySensorData()             
      blynk.virtual_write(61,0)
	  
	  
@blynk.handle_event('write V255')
def reBooter(pin, value):
    _log.critical( "User reboot")        
    drone.rebooter(pin, value, blynk)
    _log.debug("Look as Sonsors")
    
@timer.register(interval=10, run_once=False)
def blynk_data():
    _log.info("Update Timer Run")
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))

def displaySensorData():
     for sensor in sensors:
     _log.debug("Look as Sonsor" + str(sensor.name) )
     if sensor is not None:
         _log.debug("Sonsor" + str(sensor.name) +  " was not null" )
         sensor.read()
         sensor.display(blynk)
         sensor.displayCurrenCalibration(blynk)   
	 
    
for sensor in sensors:
    _log.debug("Look as Sonsor" + str(sensor.name) )
    displaySensorData()
		
while True:
        try:
           blynk.run()
           timer.run()
        
        except:
           _log.critical('Unexpected error')
           blynkErr = blynklib.Blynk(parser.get('configCalibration', 'BLYNK_AUTH'))  
           blynkErr.run()
           blynkErr.virtual_write(250, "Crash")
           blynkErr.virtual_write(98, "System has error" + '\n')
           os.system('sh /home/pi/updateDroneponics.sh')
           os.system('sudo reboot')
