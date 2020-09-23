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
parser.read("/home/pi/droneponics/config/configFeed/"+drone.gethostname()+".ini")

bootup = True


# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))
_log.info("/home/pi/droneponics/config/configRelay/"+drone.gethostname()+".ini")

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    relays=[]
    relays.append(drone.Relay(_log, 20, parser.get('droneFeed', 'Relay1')))
    relays.append(drone.Relay(_log, 21, parser.get('droneFeed', 'Relay=2')))
 

    relays[0].setInfoPin(21)
    relays[1].setInfoPin(22)
    
           
    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'), log=_log.info) 
    timer = blynktimer.Timer()
   
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        blynk.virtual_write(98, "User update and reboot button v255"+ '\n')       
        blynk.virtual_write(250, "User Reboot")
        blynk.set_property(systemLED, 'color', colours['OFFLINE'])
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "Updated and now restarting drone")
        os.system('sudo reboot')
        
        
       
          
    @blynk.handle_event('write V1')
    def write_handler(pin, value):
        staus = value[0]
        relay = 0       
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing off relay " + relays[relay].name)
                 relays[relay].turnOff(_log)
                 relays[relay].setManual("Off")
                 _log.debug(relays[relay].name + " in now off : v1write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
                
           blynk.virtual_write(250, "Stopped")
        elif (staus is "2" ):
           try:
                 _log.debug("in v1write_handler turing on relay")
                 relays[relay].turnOn(_log)
                 relays[relay].setManual("On")
                 _log.debug(relays[relay].name + " in now on : v1write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning on")
           blynk.virtual_write(250, "Feeding")
        else:
           try:
                 _log.debug("in v1write_handler turing on relay")
                 relays[relay].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning auto")
           blynk.virtual_write(250, "Auto")
           relays[relay].cycleOnReset()
           relays[relay].setOffCycleReset() 
        blynk.virtual_write(relays[relay].getInfoPin(), relays[relay].info())       
       
          
    @blynk.handle_event('write V2')
    def write_handler(pin, value):
        staus = value[0]
        relay = 1       
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing off relay " + relays[relay].name)
                 relays[relay].turnOff(_log)
                 relays[relay].setManual("Off")
                 _log.debug(relays[relay].name + " in now off : v1write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
                
           blynk.virtual_write(250, "Stopped")
        elif (staus is "2" ):
           try:
                 _log.debug("in v1write_handler turing on relay")
                 relays[relay].turnOn(_log)
                 relays[relay].setManual("On")
                 _log.debug(relays[relay].name + " in now on : v1write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning on")
           blynk.virtual_write(250, "Feeding")
        else:
           try:
                 _log.debug("in v1write_handler turing on relay")
                 relays[relay].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning auto")
           blynk.virtual_write(250, "Auto")
           relays[relay].cycleOnReset()
           relays[relay].setOffCycleReset() 
        blynk.virtual_write(relays[relay].getInfoPin(), relays[relay].info())
  
  
    @blynk.handle_event('write V11')
    def v25write_handler(pin, value):
        relays[0].cycleResetSet(value[0])
        blynk.virtual_write(relays[0].getInfoPin(), relays[0].info())
        
    @blynk.handle_event('write V12')
    def v26write_handler(pin, value):
        relays[0].cycleOffResetSet(value[0])
        blynk.virtual_write(relays[0].getInfoPin(), relays[0].info())
        
    @blynk.handle_event('write V13')
    def v25write_handler(pin, value):
        relays[1].cycleResetSet(value[0])
        blynk.virtual_write(relays[1].getInfoPin(), relays[1].info())
        
    @blynk.handle_event('write V14')
    def v26write_handler(pin, value):
        relays[1].cycleOffResetSet(value[1])
        blynk.virtual_write(relays[1].getInfoPin(), relays[1].info())
        
        
    @timer.register(interval=60, run_once=False)
    def blynk_data(): 
           _log.info("Update Timer Run")
           text = ""
           now = datetime.now()
           blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))

           for relay in relays:
                _log.debug("Seeing if relay " + relay.name + " is automatic")
                if(relay.isAutomatic()):
                    _log.debug("relay " + relay.name + " is automatic so test cycle")
                    if(relay.whatCycle() == "On"):
                        relay.turnOn(_log)
                    else:
                        relay.turnOff(_log)
                    relay.incCycle()
           if(relay.hasInfoPin()):
                blynk.virtual_write(relay.getInfoPin(), relay.info())
           else:
                text = text + self.name + " is " + relay.whatCycle() + " "
           blynk.virtual_write(28,text)
           _log.debug("The End")
     
    while True:
        blynk.run()
        if bootup :
           blynk.virtual_write(98, "clr")
           blynk.virtual_write(98, "Rebooted"+ '\n')
           blynk.virtual_write(250, "Start-up")
           blynk.set_property(251, "label",drone.gethostname())
           blynk.virtual_write(251, drone.get_ip())
 
           
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
   blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'))
   blynk.run()
   blynk.virtual_write(98,"in main loop except"+ '\n')
   blynk.virtual_write(250, "Crashed")
   now = datetime.now()
 
   drone.turnLEDsOffline(blynk)
   drone.turnButtonsOffline(blynk)
   GPIO.cleanup()

   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')