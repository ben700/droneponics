

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

parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configRelay_"+drone.gethostname()+".ini")

bootup = True
button_state=0
CO2=0
CO2Target=0
startTime =None
stopTime=None
waterTemp=99
droneCounter = drone.DroneCounter()

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))
_log.info("/home/pi/droneponics/config/configRelay_"+drone.gethostname()+".ini")

if (True):
#try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    relays=[]
    relays.append(drone.Relay(18, parser.get('droneRelay', 'Relay1')))
    relays.append(drone.Relay(23, parser.get('droneRelay', 'Relay2')))
    relays.append(drone.Relay(24, parser.get('droneRelay', 'Relay3')))
    relays.append(drone.Relay(25, parser.get('droneRelay', 'Relay4')))
    relays.append(drone.Relay(12, parser.get('droneRelay', 'Relay5')))
    relays.append(drone.Relay(16, parser.get('droneRelay', 'Relay6')))
    relays.append(drone.Relay(10, parser.get('droneRelay', 'Relay7')))
    relays.append(drone.Relay(21, parser.get('droneRelay', 'Relay8')))
    
    
    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'), log=_log.info) 
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
        _log.warning("Connected")
        for pin in range(0,11):
           _log.info('Syncing virtual buttons {}'.format(pin))
           blynk.virtual_sync(pin)
           blynk.read_response(timeout=0.5)
        for pin in range(24,28):
           _log.info('Syncing virtual buttons {}'.format(pin))
           blynk.virtual_sync(pin)
           blynk.read_response(timeout=0.5)
        blynk.virtual_write(250, "Connected")
    

    @blynk.handle_event("disconnect")
    def disconnect_handler():
        _log.warning("Disconnected")
        blynk.virtual_write(250, "Disconnected")

    @blynk.handle_event('write V2')
    def v2write_handler(pin, value):  
        staus = value[0]
        _log.debug("in v2write_handler and the staus = " + str(value[0]))
        if (staus is "1" ):
           try:
                 _log.debug("in v2write_handler turing on relay")
                 relays[1].turnOn(_log)
           except:
                 _log.error("Except handle_event V2 Turning Off")
        else:
           try:
                 _log.debug("in v2write_handler turing off relay")
                 relays[1].turnOff(_log)
           except:
                 _log.error("Except handle_event V2 Turning Off")
        
    @blynk.handle_event('write V7')
    def v7write_handler(pin, value):
        staus = value[0]
        _log.debug("in v7write_handler and the staus = " + str(value[0]))
        _log.debug("Waste relay is "+ str(relays[7].name))
        if (staus is "1" ):
            try:
                 relays[6].turnOff(_log)
                 droneCounter.wasteAutomatic = False
                 droneCounter.wasteCycleState = "Off"
                 blynk.virtual_write(28, "Waste is Off")
            except:
                 _log.error("Except handle_event V7 Turning Off waste")
                 blynk.virtual_write(28, "Except handle_event V7 Turning Off waste")           
        elif (staus is "2" ):
            try:
                 relays[6].turnOn(_log)
                 blynk.virtual_write(28, "Waste is On")
                 droneCounter.wasteAutomatic = False
                 droneCounter.wasteCycleState = "On"
            except:
                 _log.error("Except handle_event V7 Turning on waste")
                 blynk.virtual_write(28, "Except handle_event V7 Turning on waste")
        else : 
            try:
                 blynk.virtual_write(28, "Waste is set to run for " + str(droneCounter.wasteCycleReset) + " mins.")
                 droneCounter.wasteAutomatic = True
                 droneCounter.wasteCycleState = "Auto"
                 droneCounter.wasteCycle = 0
            except:
                 _log.error("Except handle_event V7 Turning waste auto")
                 blynk.virtual_write(28, "Except handle_event V7 Turning waste auto")
                 
  
         
    @blynk.handle_event('write V27')
    def v27write_handler(pin, value):
        if(int(value[0]) > 0 ):
             droneCounter.setWasteCycle(_log, value[0])
        else:    
             blynk.virtual_write(27, 1)
             droneCounter.setWasteCycle(_log, 1)
        blynk.virtual_write(28, "Waste is set to run for " + str(droneCounter.wasteCycleReset) + " mins.")  
        
    @timer.register(interval=60, run_once=False)
    def blynk_data(): 
          _log.info("Update Timer Run")
          _log.debug("The End")
     
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
