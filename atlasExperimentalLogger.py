##!/usr/bin/env python3 
BLYNK_AUTH = 'YmB7l_ho4gRcEzxN-fQZtGml_ocWpwU7' #atlasExperimentalLogger 

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
    
import subprocess
import re
import drone

bootup = True
colours = {0: '#FF0000', 1: '#00FF00', '0': '#FF0000', '1': '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101


try:

    # tune console logging
    _log = logging.getLogger('BlynkLog')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _log.addHandler(consoleHandler)
    _log.setLevel(logging.DEBUG)

    DO=None
    sensors = drone.buildExperimentalSensors(sensors, _log)
    
    # Initialize Blynk
    blynk = blynklib.Blynk(BLYNK_AUTH)        
    timer = blynktimer.Timer()
    blynk.run()
    blynk.virtual_write(98, "clr")
    blynk.set_property(systemLED, 'color', colours['ONLINE'])

    
    
    # Initialize the sensor.
    try:
       # Create the I2C bus
       for sensor in sensors:
           sensor.sensor = AtlasI2C(sensor.sensorId)
       blynk.virtual_write(98, "Sensors created" + '\n') 
    except:

        blynk.virtual_write(98, "Unexpected error: atlas" + '\n') 
        _log.info("Unexpected error: Atlas")
    else:
        try:	
            for sensor in sensors:
                sensor.sensor = AtlasI2C(sensor.sensorId)
        except:
            _log.info("Expected error: Use Atlas Error")
            blynk.virtual_write(98, "Expected error: Atlas Error" + '\n') 
            
            
    APP_CONNECT_PRINT_MSG = '[APP_CONNECT_EVENT]'
    APP_DISCONNECT_PRINT_MSG = '[APP_DISCONNECT_EVENT]'
    CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
    DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'
    WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
    READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
    ALLOWED_COMMANDS_LIST = ['ls', 'lsusb', 'ip a', 'ip abc']
    TWEET_MSG = "New value='{}' on VPIN({})"
	
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        _log.info( "User reboot")	
        blynk.virtual_write(98, "User Reboot " + '\n')
        for l in LED:
            blynk.set_property(l, 'color', colours['OFFLINE'])
        blynk.set_property(systemLED, 'color', colours['OFFLINE'])	
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')

	
    @timer.register(interval=60, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        #Counter.cycle += 1
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        cDO = 
        sensors[0].value = sensors[0].sensor.query("R").split(":")[1].strip().rstrip('\x00') #DO
        _log.info( "Sensors have been read")  
        for sensor in sensors:
             if sensor is not None:
                  _log.info("Going to update pin " + str(sensor.displayPin) + " with value " + str(sensor.value))                  
                  #unhash to continue
                  #sensor.blynk()
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
              blynk.virtual_write(systemLED, 255)
              #blynk.virtual_write(98, "clr")
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')
           timer.run()
        except:
           _log.info('Unexpected error')
           blynk.virtual_write(98, "System has main loop error" + '\n')
           blynk.set_property(systemLED, 'color', colours['OFFLINE'])
           os.system('sh /home/pi/updateDroneponics.sh')
           os.system('sudo reboot') 
  
  
except KeyboardInterrupt:
   _log.info('Keyboard Interrupt')
   blynkErr = blynklib.Blynk(BLYNK_AUTH)
   blynkErr.set_property(systemLED, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')

except:
   _log.info('Unexpected error')
   blynkErr = blynklib.Blynk(BLYNK_AUTH)
   blynkErr.set_property(systemLED, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
