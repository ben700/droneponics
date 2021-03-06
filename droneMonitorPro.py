##!/usr/bin/env python3 
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

from drone import OpenWeather

bootup = True
systemLED=101

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

    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('droneMonitor', 'BLYNK_AUTH'))        
    timer = blynktimer.Timer()
    blynk.run()
    #blynk.virtual_write(98, "clr")
    blynk.set_property(systemLED, 'color', drone.colours['ONLINE'])
    _log.info("Blynk created")
	
	
    sensors = []
    sensors = drone.buildMonitorSensors(sensors, _log)
    _log.info("All Monitor Sensors created")
	
	
    try:
        lcdDisplay=drone.Display(_log)
    except:
        lcdDisplay=None
	
    _log.info("all senses created")
		
     

    
    # Initialize the sensor.
 #   try:
 #      for sensor in sensors:
 #          sensor.sensor = AtlasI2C(sensor.sensorId)
 #          blynk.set_property(sensor.displayPin, 'color', colours['ONLINE'])
 #          blynk.set_property(sensor.displayPin, 'label', sensor.name)
 #      blynk.virtual_write(98, "Sensors created" + '\n') 
 #   except:
 #       blynk.virtual_write(98, "Unexpected error: atlas on sensotr " + sensor.name + '\n') 
 #       _log.info("Unexpected error: Atlas")
    def processSensors():   
        for sensor in sensors:
           if sensor is not None:
              sensor.read()

        try:		
           drone.pubSensorReadingsToGoolgeCloud(sensors, _log)
        except:
           _log.critical("except logging readings to Google")	
     

        try:		
           sensors[0].color = drone.getTempColour(_log, int(round(float(sensors[0].value)*10,0)))
        except:
           _log.critical("Working out sensor colour crashed")	

        for sensor in sensors:
           if sensor is not None:
              sensor.display(blynk)
      		
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        _log.info( "User reboot")
        blynk.virtual_write(250, "Reboot")
        blynk.set_property(250, 'color', drone.colours['OFFLINE'])	
        blynk.virtual_write(98, "User Reboot " + '\n')
        blynk.set_property(systemLED, 'color', drone.colours['OFFLINE'])	
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')

        
    @timer.register(interval=30, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        blynk.virtual_write(250, "Running")
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
       # blynk.virtual_write(98, "The weekday is " + str(now.strftime("%w")+1))
        processSensors()
   
        _log.info("Completed Timer Function") 

    while True:
        try:
           blynk.run()
           timer.run()
           if bootup :
              blynk.virtual_write(250, "Boot")
              drone.pubDeviceBootToGoolgeCloud()
              blynk.set_property(250, 'color', drone.colours['ONLINE'])	
              p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
              #cmdout = str(p.communicate())
              for i in range(0,9):
                   blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
              bootup = False
              blynk.set_property(251, "label",drone.gethostname())
              blynk.virtual_write(251, drone.get_ip())
              now = datetime.now()
              blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
              blynk.virtual_write(systemLED, 255)
              #blynk.virtual_write(98, "clr")
              blynk.virtual_write(51,"EC Settings")
              blynk.virtual_write(52,"pH Settings")
              blynk.set_property(38, "label", "EC Trigger Level")
              blynk.set_property(48, "label", "pH Trigger Level")
              blynk.set_property(39, "label", "EC Mode")
              blynk.set_property(49, "label", "pH Mode")
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')
    
              _log.info("Boot Completed")

        except:
           _log.info('Unexpected error')
           blynk.virtual_write(250, "Crash")
           blynk.virtual_write(98, "System has main loop error" + '\n')
           blynk.set_property(systemLED, 'color', drone.colours['OFFLINE'])
           os.system('sh /home/pi/updateDroneponics.sh')
           os.system('sudo reboot') 
  
   
except KeyboardInterrupt:
   _log.info('Keyboard Interrupt')
   blynk.virtual_write(250, "Keyboard Interrupt")
   blynkErr = blynklib.Blynk(parser.get('droneMonitor', 'BLYNK_AUTH'))
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')

except:
   _log.info('Unexpected error')
   blynk.virtual_write(250, "Crash")
   blynkErr = blynklib.Blynk(parser.get('droneMonitor', 'BLYNK_AUTH'))
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
