#!/usr/bin/python3
BLYNK_AUTH = '00vIt07mIauITIq4q_quTOakFvcvpgGb' #atlasMonitor

import blynklib
import blynktimer

from datetime import datetime
import time

import logging
import sys
import os
import RPi.GPIO as GPIO

from AtlasI2C import (
   AtlasI2C
)
import math  
import subprocess
import re
import drone

bootup = True
colours = {0: '#FF0000', 1: '#00FF00', '0': '#FF0000', '1': '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101
sensors = []

try:

    # tune console logging
    _log = logging.getLogger('BlynkLog')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _log.addHandler(consoleHandler)
    _log.setLevel(logging.DEBUG)

    sensors = drone.buildSensors(sensors, _log)
    
    # Initialize Blynk
    blynk = blynklib.Blynk(BLYNK_AUTH)        
    timer = blynktimer.Timer()

    blynk.run()
    blynk.set_property(systemLED, 'color', colours['ONLINE'])
    
    # Initialize the sensor.
    try:
       # Create the I2C bus
       for sensor in sensors:
           sensor.sensor = AtlasI2C(sensor.sensorId)
           blynk.set_property(sensor.displayPin, 'color', colours['ONLINE'])
           blynk.set_property(sensor.displayPin, 'label', sensor.name)
       blynk.virtual_write(98, "Sensors created" + '\n') 
    except:
        blynk.virtual_write(98, "Unexpected error: atlas" + '\n') 
        _log.info("Unexpected error: Atlas")
    			
  
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        _log.info( "User reboot")	
        blynk.virtual_write(98, "User Reboot " + '\n')
        for sensor in sensors:
            blynk.set_property(sensor.displayPin, 'color', colours['OFFLINE'])
        blynk.set_property(systemLED, 'color', colours['OFFLINE'])	
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')

	
    @timer.register(interval=60, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))

        cTemp = sensors[0].sensor.query("R").split(":")[1].strip().rstrip('\x00')
        sensors[0].value = cTemp #Temp
        sensors[1].value = sensors[1].sensor.query("RT,"+cTemp).split(":")[1].strip().rstrip('\x00') #EC
        sensors[2].value = sensors[2].sensor.query("RT,"+sensors[0].value).split(":")[1].strip().rstrip('\x00')  #pH
        for sensor in sensors:
             if sensor is not None:
                  _log.info("Going to update " + str(sensor.name) + "using pin " + str(sensor.displayPin) + " with value " + str(sensor.value))                  
                  blynk.virtual_write(98, "Current " + str(sensor.name) + " reading =[" + str(sensor.value) + "]" + '\n')
                  blynk.virtual_write(sensor.displayPin, sensor.value)
        _log.info("Completed Timer Function") 

    while True:
        try:
           blynk.run()
           if bootup :
              p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
              #cmdout = str(p.communicate())
              for i in range(0,9):
                   blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
              bootup = False
              now = datetime.now()
              blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
              for sensor in sensors:
                  blynk.virtual_write(sensor.displayPin, 255)
              blynk.virtual_write(systemLED, 255)
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')
           timer.run()
        except:
           _log.info('Unexpected error')
           blynk.virtual_write(98, "System has main loop error" + '\n')
           for sensor in sensors:
                 blynk.virtual_write(sensor.displayPin, 255)
           blynk.set_property(systemLED, 'color', colours['OFFLINE'])
           os.system('sh /home/pi/updateDroneponics.sh')
           os.system('sudo reboot') 
  
  
except KeyboardInterrupt:
   _log.info('Keyboard Interrupt')
   blynkErr = blynklib.Blynk(BLYNK_AUTH)
   for sensor in sensors:
        blynkErr.set_property(sensor.displayPin, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')

except:
   _log.info('Unexpected error')
   blynkErr = blynklib.Blynk(BLYNK_AUTH)
   for sensor in sensors:
        blynkErr.set_property(sensor.displayPin, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
