

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
parser.read('/home/pi/configRelay.ini')

class Counter:
    cycle = 0
        
bootup = True
button_state=0
CO2=0
CO2Target=0
startTime =None
stopTime=None
waterTemp=99

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    relays=[0,18,23,24,25,12,16,20,21]
    Relay1 = relays[1] #feed
    Relay2 = relays[2] #fan
    Relay3 = relays[3] #Air
    Relay4 = relays[4] #heater
    Relay5 = relays[5] #Feed
    Relay6 = relays[6] #Air
    Relay7 = relays[7] #Mixer - turned off with low water 
    Relay8 = relays[8]  #Mixer - turned off with low water 

    GPIO.setup(Relay1,GPIO.OUT, initial=1)
    GPIO.setup(Relay2,GPIO.OUT, initial=1)
    GPIO.setup(Relay3,GPIO.OUT, initial=1)
    GPIO.setup(Relay4,GPIO.OUT, initial=1)
    GPIO.setup(Relay5,GPIO.OUT, initial=1)
    GPIO.setup(Relay6,GPIO.OUT, initial=1)
    GPIO.setup(Relay7,GPIO.OUT, initial=1)
    GPIO.setup(Relay8,GPIO.OUT, initial=1)
    
    
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
        for pin in range(1,11):
           _log.info('Syncing virtual buttons {}'.format(pin))
           blynk.virtual_sync(pin)
           blynk.read_response(timeout=0.5)
        blynk.virtual_sync(30)
        blynk.virtual_write(250, "Connected")
    

    @blynk.handle_event("disconnect")
    def disconnect_handler():
        _log.warning("Disconnected")
        blynk.virtual_write(250, "Disconnected")
  
    @blynk.handle_event('write V1')
    def write_handler(pin, value):
        _log.debug("droneRelayWriteHandler on pin " + str(pin) + " value is " + str(value[0]))
        global button_state
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        
        button_state = int(value[0])-1
        blynk.set_property(10+pin, 'color', colours[button_state])
        blynk.set_property(pin, 'color', colours[button_state])
            
        blynk.virtual_write(98, "droneRelayWriteHandler on pin " + str(pin) + " value is " + str(button_state) + " colour : " + str(colours[button_state]) + '\n')
            
        if (button_state==0 ):
            GPIO.output(relays[1],0)
            blynk.virtual_write(250, "Stopped")
            blynk.virtual_write(98, "Stopped"+ '\n')
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
        _log.debug("droneRelayWriteHandler on pin " + str(pin) + " value is " + str(value[0]))
        drone.droneRelayWriteHandler(pin, value[0], blynk, relays)
        
    @blynk.handle_event('write V3')
    def write_handler(pin, value):
        _log.debug("write_handler for V3")
        drone.droneRelayWriteHandler(pin, value[0], blynk, relays)
        
    @blynk.handle_event('write V4')
    def write_handler(pin, value):
        if (str(value[0]) == "0.0"):
            value[0] = 0
        _log.debug("droneRelayWriteHandler on pin " + str(pin) + " value is " + str(value[0]))            
        drone.droneRelayWriteHandler(pin, value[0], blynk, relays)
        
    @blynk.handle_event('write V5')
    def write_handler(pin, value):
        if (str(value[0]) == "0.0"):
            value[0] = 0
        _log.debug("droneRelayWriteHandler on pin " + str(pin) + " value is " + str(value[0]))            
        drone.droneRelayWriteHandler(pin, value[0],blynk, relays)
        
    @blynk.handle_event('write V6')
    def write_handler(pin, value):
        _log.debug("droneRelayWriteHandler on pin " + str(pin) + " value is " + str(value[0]))
        if (str(value[0]) == "0.0"):
            value[0] = 0
        drone.droneRelayWriteHandler(pin, value[0],blynk, relays)
        
        
    def v7_Temp_write_handler(pin, VALUE, waterTemp):
        if (waterTemp>15 and VALUE == 1):
            drone.droneRelayWriteHandler(pin, 1, blynk, relays)
        else:
            drone.droneRelayWriteHandler(pin, 0, blynk, relays)
       
        
    @blynk.handle_event('write V7')
    def write_handler(pin, value):
      #  global waterTemp
      #  _log.debug("droneRelayWriteHandler on pin " + str(pin) + " value is " + str(value[0]))
      #  if (str(value[0]) == "0.0"):
      #     value[0] = 0
     #   v7_Temp_write_handler(pin, value[0], waterTemp)
        _log.debug("droneRelayWriteHandler on pin " + str(pin) + " value is " + str(value[0]))
        if (str(value[0]) == "0.0"):
            value[0] = 0
        drone.droneRelayWriteHandler(pin, value[0],blynk, relays)
  
    
    
    def v8_CO2_write_handler(pin, CO2, CO2Target, startTime, stopTime):         
        _log.debug("droneRelayWriteHandler on pin " + str(pin) + " startTime is " + str(startTime))
        _log.debug("droneRelayWriteHandler on pin " + str(pin) + " stopTime is " + str(stopTime))            
        
        today = date.today()
        seconds_since_midnight = int(time.time() - time.mktime(today.timetuple()))
        
        if( startTime < seconds_since_midnight and stopTime > seconds_since_midnight):
            if all([CO2, CO2Target]):
                blynk.virtual_write(98,"CO2Target : "+ str(CO2Target) + " and co2 level : " +str(CO2)+ '\n')    
                if (CO2 <CO2Target):
                    _log.info("CO2 is less than target")
                    blynk.virtual_write(20,"CO2 On")
                    blynk.virtual_write(98,"CO2 Relay is on"+ '\n')    
                    iValue = "1"
                else:
                    _log.info("CO2 is above target")
                    iValue = "0"
                    blynk.virtual_write(20,"CO2 Off : Level")
                    blynk.virtual_write(98,"Co2 Relay is off due to level"+ '\n')
            else:
                _log.info("Co2 Relay is on due to time and not being overwritten by current co2 reading " +str(CO2) + " with target " + str(CO2Target))
                iValue = "1"
                blynk.virtual_write(20,"CO2 On : Default")
                blynk.virtual_write(98,"Co2 Relay is on due to time and not being overwritten by current co2 reading " +str(CO2) + " with target " + str(CO2Target) + '\n')
                    
        else:
            iValue = "0"
            blynk.virtual_write(20,"CO2 Off : Time")
            blynk.virtual_write(98,"Co2 Relay is off due to time"+ '\n')    
        now = datetime.now()
        blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
        drone.droneRelayWriteHandler(pin, iValue, blynk, relays)

    
    @blynk.handle_event('write V8')
    def write_handler(pin, value):
        global CO2Target
        global CO2
        global startTime 
        global stopTime
        startTime  =int(value[0])
        stopTime = int(value[1])
        v8_CO2_write_handler(8, CO2, CO2Target, startTime, stopTime)
            
    @blynk.handle_event('write V9')
    def write_handler(pin, value):
        global CO2Target
        global CO2
        global startTime 
        global stopTime
        CO2Target = value[0]        
        blynk.virtual_write(98,"Current CO2Target :" + str(CO2Target) +'\n')
        _log.info("CO2Target updated to :" + str(CO2Target))
        v8_CO2_write_handler(8, CO2, CO2Target, startTime, stopTime)
        
    @blynk.handle_event('write V10')
    def write_handler(pin, value):
        global CO2Target
        global CO2
        global startTime 
        global stopTime
        CO2 = value[0]
        blynk.virtual_write(98,"Current CO2 :" + str(CO2) +'\n')
        _log.info("CO2 updated to :" + str(CO2))
        v8_CO2_write_handler(8, CO2, CO2Target, startTime, stopTime)
        
    @blynk.handle_event('write V30')
    def write_handler(pin, value):
        global waterTemp
        waterTemp = value[0]
        v7_Temp_write_handler(7, waterTemp)
        
    @timer.register(interval=60, run_once=False)
    def blynk_data():
        global button_state
        _log.info("Update Timer Run")
        blynk.virtual_sync(10)
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
