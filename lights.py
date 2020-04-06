##!/usr/bin/env python3 
BLYNK_AUTH = 'jX8rstxGafpXQU9ChKVCliPHRlmgjHHp' #lights

from python_tsl2591 import tsl2591
import datetime
import time
from time import strftime
from time import gmtime
import shlex, requests
import board
import busio
import smbus 
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte
import mh_z19
import blynklib
import blynktimer
import logging
from datetime import datetime
import adafruit_tsl2591
import sys
import os
import RPi.GPIO as GPIO
    
import subprocess
import re

import drone

class Counter:
    cycle = 0

bootup = True
colours = {1: '#00FF00', 0: '#FF0000', 'OFFLINE': '#0000FF'}

startTime = 0 
stopTime = 0
overRdTime = 3
#try:
if True:
    # tune console logging
    _log = logging.getLogger('BlynkLog')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _log.addHandler(consoleHandler)
    _log.setLevel(logging.DEBUG)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(drone.lightPin(), GPIO.OUT)
    
    
    # Initialize Blynk
    blynk = blynklib.Blynk(BLYNK_AUTH)        
    timer = blynktimer.Timer()

        
    APP_CONNECT_PRINT_MSG = '[APP_CONNECT_EVENT]'
    APP_DISCONNECT_PRINT_MSG = '[APP_DISCONNECT_EVENT]'
    CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
    DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'
    WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
    READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
    ALLOWED_COMMANDS_LIST = ['ls', 'lsusb', 'ip a', 'ip abc']
    TWEET_MSG = "New value='{}' on VPIN({})"
    
    @blynk.handle_event("connect")
    def connect_handler():
        _log.info('SCRIPT_START')
        blynk.virtual_sync(1)       
        blynk.read_response(timeout=0.5)
            
    @blynk.handle_event('write V1')
    def lightTimer(pin, value):
        global startTime
        global stopTime
        startTime  = value[0]
        stopTime = value[1]
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))   
       if(overRdTime==1):
            lightOn()
        elif(overRdTime==2):
            lightOff()
        else:
             midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
             currTime = (now - midnight).seconds
             lightShouldBeOn = float(startTime) <= float(currTime) <= float(stopTime)
             if(lightShouldBeOn):
                 lightOn()
             else :
                 lightOff()
        

    @blynk.handle_event('write V2')
    def lightTimer(pin, value):
        global overRdTime
        overRdTime = value[0]
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))   
        if(overRdTime==1):
            lightOn()
        elif(overRdTime==2):
            lightOff()
        else:
             midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
             currTime = (now - midnight).seconds
             lightShouldBeOn = float(startTime) <= float(currTime) <= float(stopTime)
             if(lightShouldBeOn):
                 lightOn()
             else :
                 lightOff()
            
        
    def lightOn():
        _log.info("light on")
        blynk.set_property(9, 'color', colours[1])
        GPIO.output(drone.lightPin(),GPIO.HIGH)

    def lightOff():
        _log.info("light off")
        blynk.set_property(9, 'color', colours[0])
        GPIO.output(drone.lightPin(),GPIO.LOW)
        
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        blynk.virtual_write(98, "User Reboot " + '\n')
        blynk.set_property(10, 'color', colours['OFFLINE'])
        blynk.set_property(9, 'color', colours['OFFLINE'])   
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')


    @timer.register(interval=10, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        global startTime
        global stopTime
        global overRdTime
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    

        
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        currTime = (now - midnight).seconds
        lightShouldBeOn = float(startTime) <= float(currTime) <= float(stopTime)
        if(lightShouldBeOn is True and overRdTime == 3):
            lightOn()
        else :
            lightOff()
        #blynk.virtual_write(98, "Completed Timer Function" + '\n') 

    while True:
 #       try:
        if True:
           blynk.run()
        
              
 
           if bootup :
              p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
              #cmdout = str(p.communicate())
              for i in range(0,9):
                   blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
              bootup = False
              now = datetime.now()
              blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
              blynk.virtual_write(10,255)
              blynk.set_property(10, 'color', colours[1])  
              blynk.virtual_write(9,255)
              blynk.virtual_write(2,3)  
              #blynk.virtual_write(98, "clr")
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')

           timer.run()
       # except:
       #    _log.info('Unexpected error')
       #    blynk.virtual_write(98, "System has main loop error" + '\n')
       #    blynk.set_property(10, 'color', colours['OFFLINE'])
       #    blynk.set_property(9, 'color', colours['OFFLINE']) 
       #    os.system('sh /home/pi/updateDroneponics.sh')
       #    os.system('sudo reboot') 
  
  
#except:
#   _log.info('Unexpected error')
#   blynkErr = blynklib.Blynk(BLYNK_AUTH)
#   blynkErr.set_property(10, 'color', colours['OFFLINE'])
#   blynkErr.set_property(9, 'color', colours['OFFLINE'])   
#   blynkErr.virtual_write(98, "System has error" + '\n')
#   os.system('sh /home/pi/updateDroneponics.sh')
#   os.system('sudo reboot')
#finally:
#   blynk.set_property(10, 'color', colours['OFFLINE'])
#   blynk.set_property(9, 'color', colours['OFFLINE'])    
#   GPIO.cleanup()
