

# The ID and range of a sample spreadsheet.
colours = {1: '#FF0000', 0: '#00FF00', '1': '#FF0000', '0': '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
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
    if(parser.get('droneRelay', 'RelaySize') == "8"):
       GPIO.setup(Relay5,GPIO.OUT)
       GPIO.setup(Relay6,GPIO.OUT)
       GPIO.setup(Relay7,GPIO.OUT)
       GPIO.setup(Relay8,GPIO.OUT)
    
    
    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('droneRelay', 'BLYNK_AUTH'))
    timer = blynktimer.Timer()
    
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        blynk.set_property(255, 'onlabel', "Updating")
        blynk.virtual_write(250, "User Reboot")
        drone.turnLEDsOffline(blynk)
        drone.turnButtonsOffline(blynk)
        blynk.set_property(systemLED, 'color', colours['OFFLINE'])
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.set_property(255, 'onlabel', "Rebooting")
        os.system('sudo reboot')

    @blynk.handle_event("connect")
    def connect_handler():
        print("Connected")
        for pin in range(1,9):
           _log.info('Syncing virtual buttons {}'.format(pin))
           blynk.virtual_sync(pin)
        blynk.virtual_write(250, "Connected")
    

    @blynk.handle_event("disconnect")
    def disconnect_handler():
        print("Connected")
        blynk.virtual_write(250, "Disconnected")
  
    @blynk.handle_event('write V1')
    def buttonV1Pressed(pin, value):
        _log.info("-------------------Button code 1----------------------" +str(value[0]))
        _log.info(str(value[0]))
        drone.processButtonPressed(blynk, 11, 1, GPIO, Relay1,value[0])
  
    
    @blynk.handle_event('write V2')
    def buttonV2Pressed(pin, value):
        _log.info("-------------------Button code 2----------------------" +str(value[0]))
        drone.processButtonPressed(blynk, 12, 2, GPIO, Relay2,value[0])
        
    @blynk.handle_event('write V3')
    def buttonV3Pressed(pin, value):
        _log.info("-------------------Button code 3----------------------" +str(value[0]))
        drone.processButtonPressed(blynk, 13, 3, GPIO, Relay3,value[0])
    
    @blynk.handle_event('write V4')        
    def buttonV4Pressed(pin, value):
        _log.info("-------------------Button code 4----------------------" +str(value[0]))
        drone.processButtonPressed(blynk, 14, 4, GPIO, Relay4,value[0])
                          
    @blynk.handle_event('write V5')
    def buttonV5Pressed(pin, value):
        _log.info("-------------------Button code 5----------------------" +str(value[0]))
        drone.processButtonPressed(blynk, 15, 5, GPIO, Relay5,value[0])
    
    @blynk.handle_event('write V6')
    def buttonV6Pressed(pin, value):
        _log.info("-------------------Button code 6----------------------" +str(value[0]))
        drone.processButtonPressed(blynk, 16, 6, GPIO, Relay6,value[0])
        
    @blynk.handle_event('write V7')
    def buttonV7Pressed(pin, value):
        _log.info("-------------------Button code 7----------------------" +str(value[0]))
        drone.processButtonPressed(blynk, 17, 7, GPIO, Relay7,value[0])
        
    @blynk.handle_event('write V8')        
    def buttonV8Pressed(pin, value):
        _log.info("-------------------Button code 8----------------------" +str(value[0]))
        drone.processButtonPressed(blynk, 18, 8, GPIO, Relay8,value[0])
                          
   
    @timer.register(interval=180, run_once=False)
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
           blynk.set_property(251, "label",drone.gethostname())
           blynk.virtual_write(251, drone.get_ip())
        
        
           drone.turnLEDsOnline(blynk)
           drone.turnButtonsOnline(blynk)
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
          # blynk.virtual_write(98, "clr")
          # _log.info("Posting I2C 0 devices to app")
          # p = subprocess.Popen(['i2cdetect', '-y','0'],stdout=subprocess.PIPE,)
           #cmdout = str(p.communicate())
          # blynk.virtual_write(98, "I2C 0 devices"+'\n')
          # for i in range(0,9):
          #      blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
          # _log.info("Posting I2C 1 devices to app")
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

#   drone.turnLEDsOffline(blynk)
#   drone.turnButtonsOffline(blynk)
#   GPIO.cleanup()

  # os.system('sh /home/pi/updateDroneponics.sh')
  # os.system('sudo reboot')
