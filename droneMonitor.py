##!/usr/bin/env python3 

LED = [10,11,12,13,14,15]
VolumePin = [26,21,22,23,24,25] 
import blynklib
import blynktimer
from configparser import ConfigParser
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

from drone import Alarm, OpenWeather

bootup = True
colours = {0: '#FF0000', 1: '#00FF00', '0': '#FF0000', '1': '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101
rowIndex=1

parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configMonitor/"+drone.gethostname()+".ini")


try:

    # tune console logging
    _log = logging.getLogger('BlynkLog')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _log.addHandler(consoleHandler)
    _log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))

    _log.critical("critical")
    _log.error("error")
    _log.warning("warning")
    _log.info("info")
    _log.debug("debug")

    _log.info("/home/pi/droneponics/config/configMonitor/"+drone.gethostname()+".ini")

    pH=0
    eC=9999	
    sensors = []
    _log.info("drone.buildSensors(sensors")
    
    try:
        sensors.append( Sensor(102, "Temprature", 30, Target=20, LowAlarm=10, HighAlarm=25))
    except
        _log,info("No Temp")
    
    sensors = drone.buildSensors(sensors, _log)
    _log.info("all senses created")
	
	
    try:
        lcdDisplay=drone.Display(_log)
    except:
        lcdDisplay=None
	
    _log.info("all senses created")
		
     
    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('droneDoser', 'BLYNK_AUTH'))        
    timer = blynktimer.Timer()
    blynk.run()
    #blynk.virtual_write(98, "clr")
    blynk.set_property(systemLED, 'color', colours['ONLINE'])
    _log.info("Blynk created")
    
    # Initialize the sensor.
    try:
       for sensor in sensors:
           sensor.sensor = AtlasI2C(sensor.sensorId)
           blynk.set_property(sensor.displayPin, 'color', colours['ONLINE'])
           blynk.set_property(sensor.displayPin, 'label', sensor.name)
       blynk.virtual_write(98, "Sensors created" + '\n') 
    except:

        blynk.virtual_write(98, "Unexpected error: atlas" + '\n') 
        _log.info("Unexpected error: Atlas")
    
    @blynk.handle_event('write V29')
    def v29write_handler(pin, value):
        _log.debug("v29write_handler rowIndex =" + str(value[0]))
        global rowIndex
        rowIndex = int(value[0])
   	

    @blynk.handle_event('write V96')
    def v96write_handler(pin, value):
        _log.debug("v96write_handler")
        blynk.virtual_write(97,"clr")
        blynk.virtual_write(96,0)
        blynk.virtual_write(29,0)
      
   
			
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        _log.info( "User reboot")
        blynk.virtual_write(250, "Reboot")
        blynk.set_property(250, 'color', colours['OFFLINE'])	
        blynk.virtual_write(98, "User Reboot " + '\n')
        blynk.set_property(systemLED, 'color', colours['OFFLINE'])	
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')
	
    @blynk.handle_event("connect")
    def connect_handler():
        _log.warning("Connected")
        blynk.virtual_write(250, "Connected")
        pins = [1, 2, 3, 4, 8, 29,30,31,32,35,36,38,39,41,42,43,44,45,46,47,48,49, 60, 61, 62, 63, 64, 65, 66]
        for pin in pins:
           _log.info('Syncing virtual buttons {}'.format(pin))
           blynk.virtual_sync(pin)
           blynk.read_response(timeout=0.5)
        
    @timer.register(interval=60, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        blynk.virtual_write(250, "Running")
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
       # blynk.virtual_write(98, "The weekday is " + str(now.strftime("%w")+1))

        cTemp = sensors[0].sensor.query("R").split(":")[1].strip().rstrip('\x00')
        if (float(cTemp) < 0) :
             _log.critical("cTemp = " + str(cTemp))
        else :
             _log.critical("cTemp -ve = " + str(cTemp))
    
        sensors[0].oldValue = sensors[0].value
        sensors[1].oldValue = sensors[1].value
        sensors[2].oldValue = sensors[2].value

        sensors[0].value = cTemp #Temp
        sensors[1].value = sensors[1].sensor.query("RT,"+cTemp).split(":")[1].strip().rstrip('\x00') #EC
        sensors[2].value = sensors[2].sensor.query("RT,"+sensors[0].value).split(":")[1].strip().rstrip('\x00')  #pH
	
        try:
             sensors[0].color = drone.getTempColour(_log, round(float(sensors[0].value)*10,0))
             sensors[1].color = drone.getECColour(_log, round(float(sensors[1].value),0))
             sensors[2].color = drone.getPHColour(_log, round(float(sensors[2].value)*10,0))
        except:
             _log.critical("Working out sensor colour crashed")
		
		    
        for sensor in sensors:
             if sensor is not None:
                  _log.info("Going to update " + str(sensor.name) + " using pin " + str(sensor.displayPin) + " with value " + str(sensor.value))                  
                  blynk.virtual_write(98,"Going to update " + str(sensor.name) + " using pin " + str(sensor.displayPin) + " with value " + str(sensor.value) +'\n')
                  _log.info("going to update pin = " + str(sensor.displayPin))
                  blynk.set_property(sensor.displayPin, "label", sensor.name)
                  _log.info("updated label =" + sensor.name)
                  blynk.set_property(sensor.displayPin, 'color', sensor.color)
                  _log.info("updated color =" + str(sensor.color))
                  blynk.virtual_write(sensor.displayPin, sensor.value)
                  _log.info("updated value =" + str(sensor.value))
                  	
                  
        _log.info( "Sensors displays updated")  
        _log.info("sensors[1].target = " + str(sensors[1].target))
        _log.info("sensors[2].target = " + str(sensors[2].target))
        blynk.virtual_write(98,"sensors[1].target = " + str(sensors[1].target)+ '\n')
        blynk.virtual_write(98,"sensors[2].target = " + str(sensors[2].target)+ '\n')
        blynk.virtual_write(98,"sensors[1].mode = " + str(sensors[1].mode)+ '\n')
        blynk.virtual_write(98,"sensors[2].mode = " + str(sensors[2].mode)+ '\n')
       
  
        _log.info("Completed Timer Function") 

    while True:
        try:
           blynk.run()
           timer.run()
           if bootup :
              blynk.virtual_write(250, "Boot")
              blynk.set_property(250, 'color', colours['ONLINE'])	
              p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
              #cmdout = str(p.communicate())
              for i in range(0,9):
                   blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
              bootup = False
              blynk.set_property(251, "label",drone.gethostname())
              blynk.virtual_write(251, drone.get_ip())
              x = 1 
              for relay in relays:
                 relay.setBlynkLabel(blynk, x, 20+x)
                 x = x +1 
              now = datetime.now()
              blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
              blynk.virtual_write(97, "add", rowIndex, "Reboot", now.strftime("%d/%m/%Y %H:%M:%S"))
              blynk.virtual_write(29,rowIndex+1)
              for l in LED:
                  blynk.virtual_write(l, 255)
              blynk.virtual_write(systemLED, 255)
              #blynk.virtual_write(98, "clr")
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')
    
              pins = [1, 2, 3, 4, 8, 29,30,31,32,35,36,38,39,41,42,43,44,45,46,47,48,49, 60, 61, 62, 63, 64, 65, 66]
              for pin in pins:
                   _log.info('Syncing virtual buttons {}'.format(pin))
                   blynk.virtual_sync(pin)
                   blynk.read_response(timeout=0.5)
	
              _log.info("Boot Completed")

        except:
           _log.info('Unexpected error')
           blynk.virtual_write(250, "Crash")
           blynk.virtual_write(98, "System has main loop error" + '\n')
           for l in LED:
                blynk.set_property(l, 'color', colours['OFFLINE'])
           blynk.set_property(systemLED, 'color', colours['OFFLINE'])
           os.system('sh /home/pi/updateDroneponics.sh')
    #       os.system('sudo reboot') 
  
   
except KeyboardInterrupt:
   _log.info('Keyboard Interrupt')
   blynk.virtual_write(250, "Keyboard Interrupt")
   blynkErr = blynklib.Blynk(parser.get('droneDoser', 'BLYNK_AUTH'))
   for l in LED:
        blynkErr.set_property(l, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
#   os.system('sudo reboot')

except:
   _log.info('Unexpected error')
   blynk.virtual_write(250, "Crash")
   blynkErr = blynklib.Blynk(parser.get('droneDoser', 'BLYNK_AUTH'))
   for l in LED:
        blynkErr.set_property(l, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
 #  os.system('sudo reboot')
