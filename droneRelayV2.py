

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
rowIndex=1
droneCounter = drone.DroneCounter()

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))
_log.info("/home/pi/droneponics/config/configRelay_"+drone.gethostname()+".ini")

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    relays=[]
    relays.append(drone.Relay(_log, 18, parser.get('droneRelay', 'Relay1')))
    relays.append(drone.Relay(_log, 23, parser.get('droneRelay', 'Relay2')))
    relays.append(drone.Relay(_log, 24, parser.get('droneRelay', 'Relay3')))
    relays.append(drone.Relay(_log, 25, parser.get('droneRelay', 'Relay4')))
    relays.append(drone.Relay(_log, 12, parser.get('droneRelay', 'Relay5')))
    relays.append(drone.Relay(_log, 16, parser.get('droneRelay', 'Relay6')))
    relays.append(drone.Relay(_log, 20, parser.get('droneRelay', 'Relay7')))
    relays.append(drone.Relay(_log, 21, parser.get('droneRelay', 'Relay8')))
 

    relays[0].setInfoPin(24)
    relays[6].setInfoPin(23)
    relays[7].setInfoPin(20)
        
        
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
        for pin in range(24,30):
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
        _log.debug("in v2write_handler and the staus = " + str(value[0]))
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing on relay " + relays[relay].name)
                 relays[relay].turnOn(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning On")
        else:
           try:
                 _log.debug("in v2write_handler turing off relay")
                 relays[relay].turnOff(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
                
    @blynk.handle_event('write V3')
    def write_handler(pin, value):  
        staus = value[0]
        relay = 2
        _log.debug("in v2write_handler and the staus = " + str(value[0]))
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing on relay " + relays[relay].name)
                 relays[relay].turnOn(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning On")
        else:
           try:
                 _log.debug("in v2write_handler turing off relay")
                 relays[relay].turnOff(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
 

    @blynk.handle_event('write V4')
    def write_handler(pin, value):  
        staus = value[0]
        relay = 3
        _log.debug("in v2write_handler and the staus = " + str(value[0]))
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing on relay " + relays[relay].name)
                 relays[relay].turnOn(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning On")
        else:
           try:
                 _log.debug("in v2write_handler turing off relay")
                 relays[relay].turnOff(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
                
 
    @blynk.handle_event('write V5')
    def write_handler(pin, value):  
        staus = value[0]
        relay = 4
        _log.debug("in v2write_handler and the staus = " + str(value[0]))
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing on relay " + relays[relay].name)
                 relays[relay].turnOn(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning On")
        else:
           try:
                 _log.debug("in v2write_handler turing off relay")
                 relays[relay].turnOff(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
                
 
    @blynk.handle_event('write V6')
    def write_handler(pin, value):  
        staus = value[0]
        relay = 5
        _log.debug("in v2write_handler and the staus = " + str(value[0]))
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing on relay " + relays[relay].name)
                 relays[relay].turnOn(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning On")
        else:
           try:
                 _log.debug("in v2write_handler turing off relay")
                 relays[relay].turnOff(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")

                
    @blynk.handle_event('write V7')
    def v7write_handler(pin, value):
        staus = value[0]
        relay = 6
        if (staus is "1" ):
            try:
                 _log.debug("in v7write_handler and turning off relay " + relays[relay].name + " on pin " + str(relays[relay].gpioPin))
                 relays[relay].turnOff(_log)
                 _log.debug("waste turnOff() completed")
                 relays[relay].setManual("Off")
                 _log.debug("waste setManual() completed")
                 blynk.virtual_write(relays[relay].getInfoPin(), relays[relay].info())
                 _log.debug("in v7write_handler and turning off relay completed")
            except:
                 _log.error("Except handle_event V7 Turning Off waste")
                 blynk.virtual_write(28, "Except handle_event V7 Turning Off waste")           
        elif (staus is "2" ):
            try:
                 _log.debug("in v7write_handler and turning on relay " + relays[relay].name + " on pin " + str(relays[relay].gpioPin))
                 relays[relay].turnOn(_log)
                 relays[relay].setManual("On")
                 blynk.virtual_write(relays[relay].getInfoPin(), relays[relay].info())
                 _log.debug("in v7write_handler and turning on relay completed")
            except:
                 _log.error("Except handle_event V7 Turning on waste")
                 blynk.virtual_write(relays[relay].getInfoPin(), "Except handle_event V7 Turning on waste")
        else : 
            try:
                 _log.debug("in v7write_handler and turning relay " + relays[relay].name + " auto on pin " + str(relays[relay].gpioPin))
                 relays[relay].setAutomatic() 
                 _log.debug("waste setAutomatic()")
                 relays[relay].cycleOnReset()
                 _log.debug("waste cycleReset()")
                 relays[relay].cycleOffResetClear()
                 blynk.virtual_write(relays[relay].getInfoPin(), relays[relay].info())
                 _log.debug("waste cycleOffResetClear()")
            except:
                 _log.error("Except handle_event V7 Turning waste auto")
                 blynk.virtual_write(relays[relay].getInfoPin(), "Except handle_event V7 Turning waste auto")
                 
                
    @blynk.handle_event('write V8')
    def write_handler(pin, value):
        relay = 7
        relays[relay].setTimer(int(value[0]), int(value[1]))

    @blynk.handle_event('write V25')
    def v25write_handler(pin, value):
        relays[0].cycleResetSet(value[0])
        blynk.virtual_write(relays[0].getInfoPin(), relays[0].info())
        
    @blynk.handle_event('write V26')
    def v26write_handler(pin, value):
        relays[0].cycleOffResetSet(value[0])
        blynk.virtual_write(relays[0].getInfoPin(), relays[0].info())
         
    @blynk.handle_event('write V27')
    def v27write_handler(pin, value):
        relays[6].cycleResetSet(value[0])
        relays[6].cycleOffResetClear()
        blynk.virtual_write(relays[0].getInfoPin(), relays[0].info())
    
    @blynk.handle_event('write V29')
    def v29write_handler(pin, value):
        _log.debug("v29write_handler rowIndex =" + str(value[0]))
        global rowIndex
        rowIndex = int(value[0])
          
    @blynk.handle_event('write V96')
    def v96write_handler(pin, value):
        _log.debug("v96write_handler")
        blynk.virtual_write(97,"clr")
        
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
           x = 1 
           for relay in relays:
                 relay.setBlynkLabel(blynk, x, 10+x)
                 x = x +1 
           
           bootup = False
           _log.debug("Just about to complete Booting")
           now = datetime.now()
           blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
           blynk.virtual_write(97, "add", rowIndex, "Reboot", now.strftime("%d/%m/%Y %H:%M:%S"))
           blynk.virtual_write(29,rowIndex+1)
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

   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
