##!/usr/bin/env python3 
BLYNK_AUTH = 'iipK7r0pSz68i8ZDo4sVdtkhbCzXM_ns' #relay

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
from drone.droneObj import LED

bootup = True
colours = {0: '#FF0000', 1: '#00FF00', '0': '#FF0000', '1': '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101


if True:

    # tune console logging
    _log = logging.getLogger('BlynkLog')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _log.addHandler(consoleHandler)
    _log.setLevel(logging.DEBUG)


    relays = []
    relays = drone.buildRelay(relays, _log)
    
    # Initialize Blynk
    blynk = blynklib.Blynk(BLYNK_AUTH)        
    timer = blynktimer.Timer()
    blynk.run()
    #blynk.virtual_write(98, "clr")
    blynk.set_property(systemLED, 'color', colours['ONLINE'])
   
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for relay in relays:
         GPIO.setup(relay.pinId, GPIO.OUT)
    
            
    APP_CONNECT_PRINT_MSG = '[APP_CONNECT_EVENT]'
    APP_DISCONNECT_PRINT_MSG = '[APP_DISCONNECT_EVENT]'
    CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
    DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'
    WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
    READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
    ALLOWED_COMMANDS_LIST = ['ls', 'lsusb', 'ip a', 'ip abc']
    TWEET_MSG = "New value='{}' on VPIN({})"
      
   @blynk.handle_event('write V1')
    def button1(pin, value):
        _log,info("button1")	
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))   
        if(value[0]==1):
            relayOn(0)
        else:
            relayOff(0)
	
    @blynk.handle_event('write V2')
    def button2(pin, value):
        _log,info("button2")	
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))   
        if(value[0]==1):
            relayOn(1)
        else:
            relayOff(1)

    @blynk.handle_event('write V3')
    def button3(pin, value):
        _log,info("button3")	
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))   
        if(value[0]==1):
            relayOn(2)
        else:
            relayOff(2)
	
    @blynk.handle_event('write V4')
    def button4(pin, value):
        _log,info("button4")		
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))   
        if(value[0]==1):
            relayOn(3)
        else:
            relayOff(3)
	
    def relayOn(i):
        blynk.set_property(relays[i].LED, 'color', colours[1])
        GPIO.output(relays[i].pinId,GPIO.HIGH)
	
    def relayOn(i):
        blynk.set_property(relays[i].LED, 'color', colours[0])
        GPIO.output(relays[i].pinId,GPIO.LOW)
 		

    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        print( "User reboot")	

    @blynk.handle_event("connect")
    def connect_handler():
        print('SCRIPT_START')
        
    @timer.register(interval=30, run_once=False)
    def blynk_data():
        print("Completed Timer Function") 

    while True:
        if True:
           blynk.run()
           timer.run()
