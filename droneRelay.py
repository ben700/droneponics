

# The ID and range of a sample spreadsheet.
colours = {1: '#FF0000', 0: '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101

import socket
import drone
from drone import Alarm, OpenWeather
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
from meteocalc import Temp, dew_point
import sys
import os
from configparser import ConfigParser
import subprocess
import re
import json

parser = ConfigParser()
parser.read('/home/pi/config.ini')

bootup = True

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)

try:

    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('droneRelay', 'BLYNK_AUTH'))
    timer = blynktimer.Timer()
    
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        blynk.virtual_write(250, "User Reboot")
        #drone.setFormOffline(blynkObj=blynk, loggerObj=_log, Msg="User Reboot")
        blynk.set_property(systemLED, 'color', colours['OFFLINE'])
        os.system('sh /home/pi/updateDroneponics.sh')
        os.system('sudo reboot')

    @blynk.handle_event("connect")
    def connect_handler():
        print("Connected")
        blynk.virtual_write(250, "Connected")
    

    @blynk.handle_event("disconnect")
    def disconnect_handler():
        print("Connected")
        blynk.virtual_write(250, "Disconnected")
  
    
    @timer.register(interval=30, run_once=False)
    def blynk_data():
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        _log.info("Update Timer Run")
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
          
        blynk.virtual_write(250, "Running")
        blynk.set_property(systemLED, 'color', colours[0])

    while True:
        blynk.run()
        if bootup :
           blynk.virtual_write(250, "Start-up")
           blynk.virtual_write(251, drone.gethostname())
           blynk.virtual_write(252, drone.get_ip())        
           blynk.virtual_write(98, "clr")
           _log.info("Posting I2C 0 devices to app")
           p = subprocess.Popen(['i2cdetect', '-y','0'],stdout=subprocess.PIPE,)
           #cmdout = str(p.communicate())
           blynk.virtual_write(98, "I2C 0 devices"+'\n')
           for i in range(0,9):
                blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
           x=1
           for alarm in alarmList:
                alarm.display(blynk,x)
                x=x+1
           _log.info("Posting I2C 1 devices to app")
           blynk.virtual_write(98, "I2C 1 devices"+'\n')
           q = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
           #cmdout = str(p.communicate())
           for i in range(0,9):
               blynk.virtual_write(98, str(q.stdout.readline()) + '\n')
           bootup = False
           _log.debug("Just about to complete Booting")
           now = datetime.now()
           blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
           blynk.virtual_write(systemLED, 255)
           drone.setFormOnline(blynkObj=blynk, loggerObj=_log, Msg="System now updated and restarted")
           blynk.virtual_write(255, 0)
           _log.info('Just Booted')

        timer.run()
except: 
   _log.info("in main loop except")
   blynk.virtual_write(250, "Crashed")
   drone.setFormOffline(blynkObj=blynk, loggerObj=_log)
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
