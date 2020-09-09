

# The ID and range of a sample spreadsheet.
colours = {1: '#FF0000', 0: '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101
import socket
import drone
import datetime
import time
import shlex, requests
import board
import busio
import smbus 
import mh_z19
import blynklib
import blynktimer
import logging
from datetime import datetime
import adafruit_tsl2591
import adafruit_bme680
import adafruit_bme280
from meteocalc import Temp, dew_point
import sys
import os
from configparser import ConfigParser
import subprocess
import re
import json

parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configSoil/"+drone.gethostname()+".ini")

bootup = True


# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.CRITICAL))
_log.critical("critical")
_log.error("error")
_log.warning("warning")
_log.info("info")
_log.debug("debug")
_log.info("/home/pi/droneponics/config/configSoil/"+drone.gethostname()+".ini")

# Initialize Blynk
_log.debug("Creating blynk object for BLYNK_AUTH " + parser.get('blynk', 'BLYNK_AUTH')) 
blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'))
timer = blynktimer.Timer()
_log.debug("Created blynk object and timer for BLYNK_AUTH " + parser.get('blynk', 'BLYNK_AUTH')) 
#except:
#    _log.critical("Failed to create object for the blynk")
#    _log.critical("Set log level to CRITICAL to auto reboot")
#    if (parser.get('logging', 'logLevel', fallback=logging.DEBUG) =="CRITICAL"):
#        os.system('sh /home/pi/updateDroneponics.sh')
#        os.system('sudo reboot')
    
try:    
  	chirp = drone.Chirp(1, addr)
except:
    _log.critical("Can't find I2C device should be the soil sensor")
    tslI2C = None
    
@blynk.handle_event('write V255')
def rebooter(pin, value):
    _log.info("User Reboot")
    blynk.virtual_write(250, "User Reboot")
    blynk.set_property(systemLED, 'color', colours['OFFLINE'])
    os.system('sh /home/pi/updateDroneponics.sh')
    os.system('sudo reboot')

@blynk.handle_event("connect")
def connect_handler():
    _log.warning("Connected")
    blynk.virtual_write(250, "Connected")
    for pin in range(1):
         _log.info('Syncing virtual buttons {}'.format(pin))
         blynk.virtual_sync(pin)
         blynk.read_response(timeout=0.5)
        

@blynk.handle_event("disconnect")
def disconnect_handler():
    _log.warning("Disconnected")
    blynk.virtual_write(250, "Disconnected")
  
    
@timer.register(interval=30, run_once=False)
def blynk_data():
    _log.info("Start of timer.register fx")
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.set_property(0, 'color', colours['ONLINE'])
    blynk.virtual_write(1, chirp.moist())
    blynk.virtual_write(2, chirp.temp()/10) 
    blynk.virtual_write(3, chirp.light())
    _log.debug("End of timer.register fx")
        
_log.info("Created all the objects. Now starting the drone")        
blynk.run() #need to call here so you can update app outside main while loop    
blynk.virtual_write(250, "Start-up")
blynk.virtual_write(251, drone.gethostname())
blynk.virtual_write(252, drone.get_ip())        
blynk.virtual_write(98, "clr")
_log.debug("Just about to get boot timestamp and change system LED")
now = datetime.now()
blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
blynk.virtual_write(systemLED, 255)
blynk.virtual_write(255, 0)
_log.info("--------------------------Completed Boot--------------------------")

while True:
    try:
        blynk.run()
        timer.run()
except: 
       _log.error("in main loop except")
       blynk.virtual_write(250, "Crashed")
       drone.setFormOfflineColours(blynkObj=blynk, loggerObj=_log)
       if (parser.get('logging', 'logLevel', fallback=logging.DEBUG) =="CRITICAL"):
            blynk.notify("Production blynk crashed and is auto-restarting; hostname " +  drone.gethostname() + " at: " + now.strftime("%d/%m/%Y %H:%M:%S"))
            blynk.email(drone.TARGET_EMAIL, 'Production Blynk Crash', "Production blynk crashed and is auto-restarting; hostname " +  drone.gethostname() + " at: " + now.strftime("%d/%m/%Y %H:%M:%S"))            
            os.system('sh /home/pi/updateDroneponics.sh')
            os.system('sudo reboot')
       elif (parser.get('logging', 'logLevel', fallback=logging.DEBUG) is not "DEBUG"):
            blynk.notify("non-Production blynk crashed and is not-restarting; hostname " +  drone.gethostname() + " at: " + now.strftime("%d/%m/%Y %H:%M:%S"))
            _log.critical("Main Loop exception :- Set log evel to CRITICAL to auto reboot")
       else:
            _log.critical("Main Loop exception :- Set log evel to CRITICAL to auto reboot")
        
