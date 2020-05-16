

# The ID and range of a sample spreadsheet.
colours = {1: '#FF0000', 0: '#00FF00', '0': '#00FF00', '1': '#FF0000', 2: '#00FF00', 3: '#80FF00',4: '#00FF80', 5: '#80FF80','OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101

import socket
import drone
from drone import Alarm, OpenWeather
import datetime
import time
import shlex, requests
import blynklib
import blynktimer
import logging
from datetime import datetime 
import RPi.GPIO as GPIO   
import sys
import os
from configparser import ConfigParser
import subprocess
import re
import json

parser = ConfigParser()
parser.read('/home/pi/config.ini')

class Counter:
    cycle = 0
        
bootup = True
button_state=0

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    #relays=[0,21,20,16,12,25,24,23,18]
    #Relay1 = 21 #heater
    #Relay2 = 20 #Feed
    #Relay3 = 16 #Air
    #Relay4 = 12 #heater
    #Relay5 = 25 #Feed
    #Relay6 = 24 #Air
    #Relay7 = 23 #Mixer - turned off with low water 
    #Relay8 = 18  #Mixer - turned off with low water 

    relays=[0,18,23,24,25,12,16,20,21]
    Relay1 = 18 #heater
    Relay2 = 23 #Feed
    Relay3 = 24 #Air
    Relay4 = 25 #heater
    Relay5 = 12 #Feed
    Relay6 = 16 #Air
    Relay7 = 20 #Mixer - turned off with low water 
    Relay8 = 21  #Mixer - turned off with low water 

    GPIO.setup(Relay1,GPIO.OUT, initial=1)
    GPIO.setup(Relay2,GPIO.OUT, initial=1)
    GPIO.setup(Relay3,GPIO.OUT, initial=1)
    GPIO.setup(Relay4,GPIO.OUT, initial=1)
    if(parser.get('droneRelay', 'RelaySize') == "8"):
       GPIO.setup(Relay5,GPIO.OUT, initial=1)
       GPIO.setup(Relay6,GPIO.OUT, initial=1)
       GPIO.setup(Relay7,GPIO.OUT, initial=1)
       GPIO.setup(Relay8,GPIO.OUT, initial=1)
    
    
    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('droneRelay', 'BLYNK_AUTH'))
    timer = blynktimer.Timer()
    
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
        print("Connected")
        for pin in range(1,9):
           _log.info('Syncing virtual buttons {}'.format(pin))
           blynk.virtual_sync(pin)
           blynk.read_response(timeout=0.5)
        blynk.virtual_write(250, "Connected")
    

    @blynk.handle_event("disconnect")
    def disconnect_handler():
        print("Connected")
        blynk.virtual_write(250, "Disconnected")
  
    @blynk.handle_event('write V1')
    def write_handler(pin, value):
        global button_state
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        
        button_state = int(value[0])-1
        blynk.set_property(10+pin, 'color', colours[button_state])
        blynk.set_property(pin, 'onBackColor', colours[button_state])
        blynk.set_property(pin, 'color', colours[button_state])
        
        if (button_state==0 ):
            GPIO.output(relays[1],0)
            blynk.virtual_write(250, "Feeding")
            blynk.virtual_write(98, "Feeding"+ '\n')
        if (button_state==1 ):
            GPIO.output(relays[1],1)
            blynk.virtual_write(250, "Running")
            blynk.virtual_write(98, "Running"+ '\n')
        elif (button_state==2):
            GPIO.output(relays[1],0)
            blynk.virtual_write(250, "50-50")
            blynk.virtual_write(98, "50-50"+ '\n')
        elif (button_state==3):
            GPIO.output(relays[1],0)
            blynk.virtual_write(250, "Just-on")
            blynk.virtual_write(98, "Just-on"+ '\n')
        elif (button_state==4):
            GPIO.output(relays[1],0)
            blynk.virtual_write(250, "Dry")
            blynk.virtual_write(98, "Dry"+ '\n')
            
        blynk.set_property(systemLED, 'color', colours[0])
        
    @blynk.handle_event('write V2')
    def write_handler(pin, value):
        drone.droneRelayWriteHandler(pin, value[0], blynk, relays)
        
    @blynk.handle_event('write V3')
    def write_handler(pin, value):
        drone.droneRelayWriteHandler(pin, value[0], blynk, relays)
        
    @blynk.handle_event('write V4')
    def write_handler(pin, value):
        drone.droneRelayWriteHandler(pin, value[0], blynk, relays)
        
    @blynk.handle_event('write V5')
    def write_handler(pin, value):
        drone.droneRelayWriteHandler(pin, value[0],blynk, relays)
        
    @blynk.handle_event('write V6')
    def write_handler(pin, value):
        drone.droneRelayWriteHandler(pin, value[0],blynk, relays)
        
    @blynk.handle_event('write V7')
    def write_handler(pin, value):
        drone.droneRelayWriteHandler(pin, value[0], blynk, relays)
        
    @blynk.handle_event('write V8')
    def write_handler(pin, value):
        startTime  = time.localtime(int(value[0]))
        stopTime = time.localtime(int(value[1]))
        localtime = time.localtime()
        
        if( startTime < localtime and localtime < stopTime):
            print("run")
            iValue = 1
        else:
            print("stop")
            iValue = 0
        
        now = datetime.now()
        blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
        drone.droneRelayWriteHandler(pin, iValue, blynk, relays)
        
    @timer.register(interval=60, run_once=False)
    def blynk_data():
        global button_state
        _log.info("Update Timer Run")
        Counter.cycle += 1
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        if(button_state == 2):
            if Counter.cycle % 2 == 0:
              Counter.cycle = 0
        if(button_state ==3):
             if Counter.cycle % 4 == 0:
              Counter.cycle = 0
        if(button_state ==4):
             if Counter.cycle % 10 == 0:
              Counter.cycle = 0
        if (Counter.cycle == 0):
            
           GPIO.output(relays[1],0)
        else:
           GPIO.output(relays[1],1)

    while True:
        blynk.run()
        if bootup :
           blynk.virtual_write(98, "clr")
           blynk.virtual_write(98, "Rebooted"+ '\n')
           blynk.virtual_write(250, "Start-up")
           blynk.set_property(251, "label",drone.gethostname())
           blynk.virtual_write(251, drone.get_ip())
        
           blynk.set_property(1, "label", parser.get('droneRelay', 'Relay1'))
           blynk.set_property(11, "label", parser.get('droneRelay', 'Relay1'))
           blynk.virtual_write(11, 255)
           blynk.set_property(2, "label", parser.get('droneRelay', 'Relay2'))
           blynk.set_property(12, "label", parser.get('droneRelay', 'Relay2'))
           blynk.virtual_write(12, 255)
           blynk.set_property(3, "label", parser.get('droneRelay', 'Relay3'))
           blynk.set_property(13, "label", parser.get('droneRelay', 'Relay3'))
           blynk.virtual_write(13, 255)
           blynk.set_property(4, "label", parser.get('droneRelay', 'Relay4'))
           blynk.set_property(14, "label", parser.get('droneRelay', 'Relay4'))
           blynk.virtual_write(14, 255)
           if(parser.get('droneRelay', 'RelaySize') == "8"):
              blynk.set_property(5, "label", parser.get('droneRelay', 'Relay5'))
              blynk.set_property(15, "label", parser.get('droneRelay', 'Relay5'))
              blynk.virtual_write(15, 255)
              blynk.set_property(6, "label", parser.get('droneRelay', 'Relay6'))
              blynk.set_property(16, "label", parser.get('droneRelay', 'Relay6'))
              blynk.virtual_write(16, 255)
              blynk.set_property(7, "label", parser.get('droneRelay', 'Relay7'))
              blynk.set_property(17, "label", parser.get('droneRelay', 'Relay7'))
              blynk.virtual_write(17, 255)
              blynk.set_property(8, "label", parser.get('droneRelay', 'Relay8'))
              blynk.set_property(18, "label", parser.get('droneRelay', 'Relay8'))
              blynk.virtual_write(18, 255)
          
           bootup = False
           _log.debug("Just about to complete Booting")
           now = datetime.now()
           blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
           blynk.virtual_write(systemLED, 255)
           blynk.virtual_write(255, 0)
           blynk.virtual_write(98, "Running"+ '\n')
           _log.info('Just Booted')
           blynk.virtual_write(250, "Running")
           blynk.set_property(systemLED, 'color', colours[0])
        timer.run()
except: 
   blynk = blynklib.Blynk(parser.get('droneRelay', 'BLYNK_AUTH'))
   blynk.run()
   blynk.virtual_write(98,"in main loop except"+ '\n')
   blynk.virtual_write(250, "Crashed")

   drone.turnLEDsOffline(blynk)
   drone.turnButtonsOffline(blynk)
   GPIO.cleanup()

   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
