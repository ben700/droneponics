##!/usr/bin/env python3 
BLYNK_AUTH = 'iipK7r0pSz68i8ZDo4sVdtkhbCzXM_ns' #relay
BLYNK_AUTH_Sensor = '4IfX_hzDREonPi_PIDQrETikxc0-XpqI' #i2cLogger

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
    blynkSensor = blynklib.Blynk(BLYNK_AUTH_Sensor)   	
    timer = blynktimer.Timer()

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for relay in relays:
         GPIO.setup(relay.pinId, GPIO.OUT)
   		
    @blynk.handle_event('connect')
    def connect_handler():
        _log.info('SCRIPT_START')
        for pin in range(5):
            _log.info('Syncing virtual pin {}'.format(pin))
            blynk.virtual_sync(pin)

            # within connect handler after each server send operation forced socket reading is required cause:
            #  - we are not in script listening state yet
            #  - without forced reading some portion of blynk server messages can be not delivered to HW
            blynk.read_response(timeout=0.5)
    
    blynk.run()
    blynkSensor.run()	
    blynk.virtual_write(98, "clr")
    blynk.set_property(systemLED, 'color', colours['ONLINE'])
   
    @blynk.handle_event('write V1')
    def button1(pin, value):
        _log.info("button1")	
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))   
        if(value[0]=='1'):
            relayOn(0)
        else:
            relayOff(0)
	
    @blynk.handle_event('write V2')
    def button2(pin, value):
        _log.info("button2")	
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))   
        if(value[0]=='1'):
            relayOn(1)
        else:
            relayOff(1)

    @blynk.handle_event('write V3')
    def button3(pin, value):
        _log.info("button3")	
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))   
        if(value[0]=='1'):
            relayOn(2)
        else:
            relayOff(2)
	
    @blynk.handle_event('write V4')
    def button4(pin, value):
        _log.info("button4")		
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))   
        if(value[0]=='1'):
            relayOn(3)
        else:
            relayOff(3)
	
    def relayOn(i):
        blynk.set_property(relays[i].LED, 'color', colours[1])
        GPIO.output(relays[i].pinId,GPIO.HIGH)
	
    def relayOff(i):
        blynk.set_property(relays[i].LED, 'color', colours[0])
        GPIO.output(relays[i].pinId,GPIO.LOW)
 
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        _log.info( "User reboot")	
        blynk.virtual_write(98, "User Reboot " + '\n')
	blynkSensor.virtual_write(255,1)
        for l in LED:
            blynk.set_property(l, 'color', colours['OFFLINE'])
        blynk.set_property(systemLED, 'color', colours['OFFLINE'])	
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')	
				
    @timer.register(interval=30, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        _log.info("Completed Timer Function") 

    while True:
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
              for relay in relays:
                  blynk.virtual_write(relay.LED, 255)
                  blynk.set_property(relay.LED, 'label', relay.name)
                  blynk.set_property(relay.button, 'label', relay.name )
                  blynk.set_property(relay.LED, 'color', colours[GPIO.input(relay.pinId)])		
                  _log.info("setup relay " + relay.name + " using LED " + str(relay.LED) + " and pin " + str(relay.pinId) + '\n')
         

              blynk.virtual_write(systemLED, 255)
              #blynk.virtual_write(98, "clr")
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')
           timer.run()
