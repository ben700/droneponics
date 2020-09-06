

# The ID and range of a sample spreadsheet.
colours = {1: '#FF0000', 0: '#00FF00', '0': '#00FF00', 1: '#FF0000', '1': '#FF0000', 2: '#FF8000', 3: '#FF00FF',4: '#00FFFF', 5: '#00FFFF','OFFLINE': '#0000FF', 'ONLINE': '#00FF00', 'UNAVILABLE': '#002700'}
systemLED=101

import socket
import drone
from drone import Alarm, OpenWeather
from datetime import datetime, date
#import date
import time
import shlex, requests
import blynklib
import blynktimer
import logging
import RPi.GPIO as GPIO   
import sys
import os
from configparser import ConfigParser
import subprocess
import re
import json
import numbers
import liquidcrystal_i2c
import time

from board import SCL, SDA
import busio

from adafruit_seesaw.seesaw import Seesaw


parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configAutoWater/"+drone.gethostname()+".ini")

bootup = True
button_state=0
rowIndex=1

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))
_log.info("/home/pi/droneponics/config/configButt/"+drone.gethostname()+".ini")
_log.info("Done hostname")


    
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
GPIO.setup(17, GPIO.OUT)           # set GPIO17 as an output   
        
# Initialize Blynk
_log.warning(parser.get('blynk', 'BLYNK_AUTH'))
blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'), log=_log.info) 
timer = blynktimer.Timer()
   
_log.info("Done blynk")

i2c_bus = busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, addr=0x39)

@blynk.handle_event('write V255')
def rebooter(pin, value):
        blynk.virtual_write(98, "User update and reboot button v255"+ '\n')       
        blynk.set_property(255, 'onlabel', "Updating")
        blynk.virtual_write(250, "User Reboot")
        drone.turnLEDsOffline(blynk)
        drone.turnButtonsOffline(blynk)
        blynk.set_property(systemLED, 'color', colours['OFFLINE'])
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.set_property(255, 'onlabel', "Rebooting")
        blynk.virtual_write(98, "Updated and now restarting drone")
        os.system('sudo reboot')

@blynk.handle_event("connect")
def connect_handler():
        _log.warning("Connected")
        for pin in range(28,30):
           _log.info('Syncing virtual buttons {}'.format(pin))
           blynk.virtual_sync(pin)
           blynk.read_response(timeout=0.5)
        blynk.virtual_write(250, "Connected")
    
@blynk.handle_event("disconnect")
def disconnect_handler():
        _log.warning("Disconnected")
        blynk.virtual_write(250, "Disconnected")
        
        
@blynk.handle_event('write V1')
def write_handler(pin, value):
        staus = value[0]
        if (staus is "1" ):
           try:
                 _log.debug("in v1 write_handler turing off pump ")
                 GPIO.output(17, 0)
                 _log.debug("Pump in now off : v1write_handler completed")
           except:
                 _log.error("Except handle_event V1 Turning Off")
                
           blynk.virtual_write(250, "Stopped")
        elif (staus is "2" ):
           try:
                 _log.debug("in v1write_handler turing on pump")
                 GPIO.output(17, 0)
                 _log.debug("Pump in now on : v1write_handler completed")
                 
           except:
                 _log.error("Except handle_event V1 Turning on")
           blynk.virtual_write(250, "Feeding")
        else:
           try:
                 _log.debug("in v1write_handler turing Pump Auto")
                 
           except:
                 _log.error("Except handle_event V1 Turning auto")
           blynk.virtual_write(250, "Auto")
                 
        
@blynk.handle_event('write V29')
def v29write_handler(pin, value):
        _log.debug("v29write_handler rowIndex =" + str(value[0]))
        global rowIndex
        rowIndex = int(value[0])
        
@timer.register(interval=60, run_once=False)
def blynk_data(): 
    _log.info("Update Timer Run")
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))

    blynk.virtual_write(10, ss.moisture_read())
    blynk.virtual_write(11, ss.get_temp())

    _log.debug("The End")

try:     
    while True:
        blynk.run()
        if bootup :
          # blynk.virtual_write(98, "clr")
           _log.info("Start of boot sequence")
           now = datetime.now()
           _log.info("Update Blynk in boot sequence") 
           blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
          
           blynk.virtual_write(98, "Rebooted"+ '\n')
           blynk.virtual_write(250, "Start-up")
           blynk.set_property(251, "label",drone.gethostname())
           blynk.virtual_write(251, drone.get_ip())
           _log.info("Access seesaw in boot sequence")
           blynk.virtual_write(10, ss.moisture_read())
           blynk.virtual_write(11, ss.get_temp())
       
           bootup = False
           _log.debug("Just about to complete Booting")

          ## blynk.virtual_write(97, "add", rowIndex, "Reboot", now.strftime("%d/%m/%Y %H:%M:%S"))
           #blynk.virtual_write(29,rowIndex+1)
           blynk.virtual_write(systemLED, 255)
           blynk.virtual_write(255, 0)
           blynk.virtual_write(98, "Running"+ '\n')
           _log.info('Just Booted')
           blynk.virtual_write(250, "Running")
           blynk.set_property(systemLED, 'color', colours[0])
        timer.run()
except: 
   blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'))
   blynk.run()
   blynk.virtual_write(98,"in main loop except"+ '\n')
   blynk.virtual_write(250, "Crashed")
   now = datetime.now()
   blynk.notify(drone.gethostname() + " just crashed at " + now.strftime("%d/%m/%Y %H:%M:%S"))

   drone.turnLEDsOffline(blynk)
   drone.turnButtonsOffline(blynk)
   GPIO.cleanup()

#   os.system('sh /home/pi/updateDroneponics.sh')
#   os.system('sudo reboot')
