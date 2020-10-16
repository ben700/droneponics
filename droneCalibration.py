##!/usr/bin/env python3 
from configparser import ConfigParser
from datetime import datetime
import time
import logging
import blynklib
import blynktimer
from configparser import ConfigParser
from datetime import datetime
import time
import logging
import sys
import os

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
_log.info("Blynk created")
    


def displaySensorData():
     _log.debug("-----------displaySensorData")	
     for sensor in sensors:
         _log.debug("Look as Sonsor" + str(sensor.name))
         if sensor is not None:
             _log.debug("Sonsor" + str(sensor.name) +  " was not null" )
             sensor.read()
             sensor.display(blynk)
             sensor.displayCurrenCalibration(blynk)   
	 
	

@blynk.handle_event('write V60')
def v60write_handler(pin, value):
      _log.debug("v60write_handler and value[0] = " + str(value[0]))
      if (value[0] == '1'):
           _log.debug("Clear Caibration")
           sensors[1].query("Cal,clear")

      displaySensorData()
      blynk.virtual_write(60,0)

@blynk.handle_event('write V61')
def v61write_handler(pin, value): 
      _log.critial("v60write_handler and value[0] = " + str(value[0]))
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
    
		
while True:
    try:
        blynk.run()
       # timer.run()
        if bootup :
           blynk.virtual_write(250, "Initializing")
           blynk.set_property(250, 'color', '#ff00dd')	
           p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
           #cmdout = str(p.communicate())
           for i in range(0,9):
              blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
           bootup = False
           blynk.set_property(251, "label",drone.gethostname())
           blynk.virtual_write(251, drone.get_ip())
           now = datetime.now()
           blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
           blynk.virtual_write(drone.systemLED, 255)
           blynk.set_property(drone.systemLED, 'color', drone.colours['ONLINE'])

	
        
    except:
      _log.critical('Unexpected error')
      blynkErr = blynklib.Blynk(parser.get('configCalibration', 'BLYNK_AUTH'))  
      blynkErr.run()
      blynkErr.virtual_write(250, "Crash")
      blynkErr.virtual_write(98, "System has error" + '\n')
      #os.system('sh /home/pi/updateDroneponics.sh')
      #os.system('sudo reboot')
