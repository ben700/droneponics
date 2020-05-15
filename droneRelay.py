

# The ID and range of a sample spreadsheet.
colours = {1: '#FF0000', 0: '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
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

bootup = True

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)

if True:
#try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    
    Relay1 = 21 #heater
    Relay2 = 20 #Feed
    Relay3 = 16 #Air
    Relay4 = 12 #heater
    Relay5 = 25 #Feed
    Relay6 = 24 #Air
    Relay7 = 23 #Mixer - turned off with low water 
    Relay8 = 18  #Mixer - turned off with low water 


    GPIO.setup(Relay1,GPIO.OUT)
    GPIO.setup(Relay2,GPIO.OUT)
    GPIO.setup(Relay3,GPIO.OUT)
    GPIO.setup(Relay4,GPIO.OUT)
    if(parser.get('droneRelay', 'BLYNK_AUTH') == 8):
       GPIO.setup(Relay5,GPIO.OUT)
       GPIO.setup(Relay6,GPIO.OUT)
       GPIO.setup(Relay7,GPIO.OUT)
       GPIO.setup(Relay8,GPIO.OUT)
    
    
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
  
    @blynk.handle_event('write V1')
    def buttonV1Pressed(pin, value):
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        blynk.set_property(1, 'color', colours[value[0]])
        if(value[0] == '1'):
            blynk.virtual_write(98,"Relay 1 turned off" + '\n')
            GPIO.output(Relay1,GPIO.HIGH)
        else:
            blynk.virtual_write(98,"Relay 1 turned on" + '\n')
            GPIO.output(Relay1,GPIO.LOW)
        blynk.virtual_write(250, "Running")
        blynk.set_property(systemLED, 'color', colours[0])
    
    @blynk.handle_event('write V2')
    def buttonV2Pressed(pin, value):
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        blynk.set_property(2, 'color', colours[value[0]])
        if(value[0] == '1'):
            blynk.virtual_write(98,"Relay 1 turned off" + '\n')
            GPIO.output(Relay2,GPIO.HIGH)
        else:
            blynk.virtual_write(98,"Relay 1 turned on" + '\n')
            GPIO.output(Relay2,GPIO.LOW)
        blynk.virtual_write(250, "Running")
        blynk.set_property(systemLED, 'color', colours[0])
        
    @blynk.handle_event('write V3')
    def buttonV3Pressed(pin, value):
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        blynk.set_property(3, 'color', colours[value[0]])
        if(value[0] == '1'):
            blynk.virtual_write(98,"Relay 1 turned off" + '\n')
            GPIO.output(Relay3,GPIO.HIGH)
        else:
            blynk.virtual_write(98,"Relay 1 turned on" + '\n')
            GPIO.output(Relay3,GPIO.LOW)
        blynk.virtual_write(250, "Running")
        blynk.set_property(systemLED, 'color', colours[0])
        
    @blynk.handle_event('write V4')        
    def buttonV4Pressed(pin, value):
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        blynk.set_property(4, 'color', colours[value[0]])
        if(value[0] == '1'):
            blynk.virtual_write(98,"Relay 1 turned off" + '\n')
            GPIO.output(Relay4,GPIO.HIGH)
        else:
            blynk.virtual_write(98,"Relay 1 turned on" + '\n')
            GPIO.output(Relay4,GPIO.LOW)
        blynk.virtual_write(250, "Running")
        blynk.set_property(systemLED, 'color', colours[0])
                          
    @blynk.handle_event('write V5')
    def buttonV5Pressed(pin, value):
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        blynk.set_property(5, 'color', colours[value[0]])
        if(value[0] == '1'):
            blynk.virtual_write(98,"Relay 1 turned off" + '\n')
            GPIO.output(Relay5,GPIO.HIGH)
        else:
            blynk.virtual_write(98,"Relay 1 turned on" + '\n')
            GPIO.output(Relay5,GPIO.LOW)
        blynk.virtual_write(250, "Running")
        blynk.set_property(systemLED, 'color', colours[0])
    
    @blynk.handle_event('write V6')
    def buttonV6Pressed(pin, value):
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        blynk.set_property(6, 'color', colours[value[0]])
        if(value[0] == '1'):
            blynk.virtual_write(98,"Relay 1 turned off" + '\n')
            GPIO.output(Relay6,GPIO.HIGH)
        else:
            blynk.virtual_write(98,"Relay 1 turned on" + '\n')
            GPIO.output(Relay6,GPIO.LOW)
        blynk.virtual_write(250, "Running")
        blynk.set_property(systemLED, 'color', colours[0])
        
    @blynk.handle_event('write V7')
    def buttonV7Pressed(pin, value):
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        blynk.set_property(7, 'color', colours[value[0]])
        if(value[0] == '1'):
            blynk.virtual_write(98,"Relay 1 turned off" + '\n')
            GPIO.output(Relay7,GPIO.HIGH)
        else:
            blynk.virtual_write(98,"Relay 1 turned on" + '\n')
            GPIO.output(Relay7,GPIO.LOW)
        blynk.virtual_write(250, "Running")
        blynk.set_property(systemLED, 'color', colours[0])
        
    @blynk.handle_event('write V8')        
    def buttonV8Pressed(pin, value):
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        blynk.set_property(8, 'color', colours[value[0]])
        if(value[0] == '1'):
            blynk.virtual_write(98,"Relay 1 turned off" + '\n')
            GPIO.output(Relay8,GPIO.HIGH)
        else:
            blynk.virtual_write(98,"Relay 1 turned on" + '\n')
            GPIO.output(Relay8,GPIO.LOW)
        blynk.virtual_write(250, "Running")
        blynk.set_property(systemLED, 'color', colours[0])
                          
   
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
        
           blynk.set_property(1, "label", parser.get('droneRelay', 'Relay1'))
           blynk.set_property(2, "label", parser.get('droneRelay', 'Relay2'))
           blynk.set_property(3, "label", parser.get('droneRelay', 'Relay3'))
           blynk.set_property(4, "label", parser.get('droneRelay', 'Relay4'))
           if(parser.get('droneRelay', 'BLYNK_AUTH') == 8):
              blynk.set_property(5, "label", parser.get('droneRelay', 'Relay5'))
              blynk.set_property(6, "label", parser.get('droneRelay', 'Relay6'))
              blynk.set_property(7, "label", parser.get('droneRelay', 'Relay7'))
              blynk.set_property(8, "label", parser.get('droneRelay', 'Relay8'))
    
           #blynk.virtual_write(98, "clr")
           #_log.info("Posting I2C 0 devices to app")
           #p = subprocess.Popen(['i2cdetect', '-y','0'],stdout=subprocess.PIPE,)
           #cmdout = str(p.communicate())
           #blynk.virtual_write(98, "I2C 0 devices"+'\n')
           #for i in range(0,9):
           #     blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
           #_log.info("Posting I2C 1 devices to app")
           #blynk.virtual_write(98, "I2C 1 devices"+'\n')
           #q = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
           #cmdout = str(p.communicate())
          # for i in range(0,9):
          #     blynk.virtual_write(98, str(q.stdout.readline()) + '\n')
           bootup = False
           _log.debug("Just about to complete Booting")
           now = datetime.now()
           blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
           blynk.virtual_write(systemLED, 255)
           blynk.virtual_write(255, 0)
           _log.info('Just Booted')

        timer.run()
#except: 
#   blynk = blynklib.Blynk(parser.get('droneRelay', 'BLYNK_AUTH'))
#   blynk.run()
#   _log.info("in main loop except")
#   blynk.virtual_write(250, "Crashed")
  # os.system('sh /home/pi/updateDroneponics.sh')
  # os.system('sudo reboot')
