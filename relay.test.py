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
 
    # Initialize Blynk
    blynk = blynklib.Blynk(BLYNK_AUTH)        
    timer = blynktimer.Timer()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for relay in relays:
         GPIO.setup(relay.pinId, GPIO.OUT)
    
    @blynk.handle_event('write V1')
    def button1(pin, value):
        _log,info("button1")	
    
    @blynk.handle_event('write V2')
    def button2(pin, value):
        _log,info("button2")	
    
    @blynk.handle_event('write V3')
    def button3(pin, value):
        _log,info("button3")	
    
    @blynk.handle_event('write V4')
    def button4(pin, value):
        _log,info("button4")		

    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        _log.info( "User reboot")	

    @blynk.handle_event("connect")
    def connect_handler():
        _log.info('SCRIPT_START')
        
    @timer.register(interval=30, run_once=False)
    def blynk_data():
        _log.info("Completed Timer Function") 

    while True:
        if True:
           blynk.run()
           timer.run()
