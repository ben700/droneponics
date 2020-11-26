# The ID and range of a sample spreadsheet.
colours = {1: '#00FF00', 0: '#FFFFFF', '0': '#FFFFFF', '1': '#00FF00', 2: '#FF0000', '2': '#FF0000', 3: '#00FFFF', '3': '#00FFFF','OFFLINE': '#0000FF', 'ONLINE': '#00FF00', 'UNAVILABLE': '#002700'}
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
counter=0

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))
_log.info("/home/pi/droneponics/config/configFeed/"+drone.gethostname()+".ini")

lcdDisplay= None
try:
    lcdDisplay=drone.LCD(_log, Product="droneFeed", productTagLine="Smart Feed Solution", ip=drone.get_ip())
except:
    lcdDisplay=None
	
        
try:
    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'), log=_log.info) 
    timer = blynktimer.Timer()
    _log.debug("start blynk")
    blynk.run()
    _log.info("Blynk Created")  
    

    relays=[]
    relays.append(drone.RelayI2C(_log, 5, parser.get('droneFeed', 'Relay1')))
    relays.append(drone.RelayI2C(_log, 6, parser.get('droneFeed', 'Relay2')))
    relays.append(drone.RelayI2C(_log, 7, parser.get('droneFeed', 'Relay3')))
    relays.append(drone.RelayI2C(_log, 8, parser.get('droneFeed', 'Relay4')))
 
    relays[0].setBlynk(blynk) 
    relays[1].setBlynk(blynk)
    relays[2].setBlynk(blynk) 
    relays[3].setBlynk(blynk) 
    
    _log.info("Set info pins")
    relays[0].setInfoPin(21)
    relays[1].setInfoPin(22)
    relays[2].setInfoPin(23)
    relays[3].setInfoPin(24)
    
    relays[0].setLEDPin(85)
    relays[1].setLEDPin(86)
    relays[2].setLEDPin(87)
    relays[3].setLEDPin(88)
           

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
                
        elif (staus is "2" ):
           try:
                 _log.debug("in v1write_handler turing on relay")
                 relays[relay].turnOn(_log)
                 relays[relay].setManual("On")
                 _log.debug(relays[relay].name + " in now on : v1write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning on")
        else:
           try:
                 _log.debug("in v1write_handler turing on relay")
                 relays[relay].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning auto")
           relays[relay].cycleOnReset()
           relays[relay].setOffCycleReset() 
        blynk.virtual_write(relays[relay].getInfoPin(), relays[relay].info())   
        blynk.set_property(relay+1, 'color', colours[staus])
        try:			
           if lcdDisplay is not None: 
                 lcdDisplay.updateLCDPumps (relays[0].state, relays[1].state, relays[2].state, relays[3].state, relays[0].isManual(), relays[1].isManual(), relays[2].isManual(), relays[3].isManual() )
                 displayOn()			
        except:
           _log.critical("updating LCD crashed v1")
       
          
    @blynk.handle_event('write V2')
    def write_handler(pin, value):
        staus = value[0]
        relay = 1       
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing off relay " + relays[relay].name)
                 relays[relay].turnOff(_log)
                 relays[relay].setManual("Off")
                 _log.debug(relays[relay].name + " in now off : v2write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
                
        elif (staus is "2" ):
           try:
                 _log.debug("in v1write_handler turing on relay")
                 relays[relay].turnOn(_log)
                 relays[relay].setManual("On")
                 _log.debug(relays[relay].name + " in now on : v2write_handler completed")                    
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning on")
        else:
           try:
                 _log.debug("in v1write_handler turing on relay")
                 relays[relay].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning auto")
           relays[relay].cycleOnReset()
           relays[relay].setOffCycleReset() 
        blynk.virtual_write(relays[relay].getInfoPin(), relays[relay].info())
        blynk.set_property(relay+1, 'color', colours[staus])
        try:			
           if lcdDisplay is not None: 
                 lcdDisplay.updateLCDPumps (relays[0].state, relays[1].state, relays[2].state, relays[3].state, relays[0].isManual(), relays[1].isManual(), relays[2].isManual(), relays[3].isManual() )
                 displayOn()
        except:
           _log.critical("relays[0].state = " + str(relays[0].state))
           _log.critical("relays[1].state = " + str(relays[1].state))
           _log.critical("relays[2].state = " + str(relays[2].state))
           _log.critical("relays[3].state = " + str(relays[3].state))

           _log.critical("relays[0].isManual() = " + str(relays[0].isManual()))
           _log.critical("relays[1].isManual() = " + str(relays[1].isManual()))
           _log.critical("relays[2].isManual() = " + str(relays[2].isManual()))
           _log.critical("relays[3].isManual() = " + str(relays[3].isManual()))
		
           _log.critical("updating LCD crashed v2")
  

    @blynk.handle_event('write V3')
    def write_handler(pin, value):
        staus = value[0]
        relay = 2
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing off relay " + relays[relay].name)
                 relays[relay].turnOff(_log)
                 relays[relay].setManual("Off")
                 _log.debug(relays[relay].name + " in now off : v3write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
        elif (staus is "2" ):
           try:
                 _log.debug("in v3write_handler turing on relay")
                 relays[relay].turnOn(_log)
                 relays[relay].setManual("On")
                 _log.debug(relays[relay].name + " in now on : v3write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning on")
        else:
           try:
                 _log.debug("in v3write_handler turing on relay")
                 relays[relay].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning auto")
           relays[relay].cycleOnReset()
           relays[relay].setOffCycleReset() 
        blynk.virtual_write(relays[relay].getInfoPin(), relays[relay].info())       
        blynk.set_property(relay+1, 'color', colours[staus])
        try:			
           if lcdDisplay is not None: 
                 lcdDisplay.updateLCDPumps (relays[0].state, relays[1].state, relays[2].state, relays[3].state, relays[0].isManual(), relays[1].isManual(), relays[2].isManual(), relays[3].isManual() )
                 displayOn()
        except:
           _log.critical("updating LCD crashed v3")
       
          
    @blynk.handle_event('write V4')
    def write_handler(pin, value):
        staus = value[0]
        relay = 3      
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing off relay " + relays[relay].name)
                 relays[relay].turnOff(_log)
                 relays[relay].setManual("Off")
                 _log.debug(relays[relay].name + " in now off : v4write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
        elif (staus is "2" ):
           try:
                 _log.debug("in v4write_handler turing on relay")
                 relays[relay].turnOn(_log)
                 relays[relay].setManual("On")
                 _log.debug(relays[relay].name + " in now on : v4write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning on")
        else:
           try:
                 _log.debug("in v4write_handler turing on relay")
                 relays[relay].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning auto")
           relays[relay].cycleOnReset()
           relays[relay].setOffCycleReset() 
        blynk.virtual_write(relays[relay].getInfoPin(), relays[relay].info())
        blynk.set_property(relay+1, 'color', colours[staus])
        try:			
           if lcdDisplay is not None: 
                 lcdDisplay.updateLCDPumps (relays[0].state, relays[1].state, relays[2].state, relays[3].state, relays[0].isManual(), relays[1].isManual(), relays[2].isManual(), relays[3].isManual() )
                 displayOn()
        except:
           _log.critical("updating LCD crashed v4")
  
  
    @blynk.handle_event('write V11')
    def v11write_handler(pin, value):
        relays[0].cycleResetSet(value[0])
        blynk.virtual_write(relays[0].getInfoPin(), relays[0].info())
        displayOn()
        
    @blynk.handle_event('write V12')
    def v12write_handler(pin, value):
        relays[0].cycleOffResetSet(value[0])
        blynk.virtual_write(relays[0].getInfoPin(), relays[0].info())
        displayOn()
        
    @blynk.handle_event('write V13')
    def v13write_handler(pin, value):
        relays[1].cycleResetSet(value[0])
        blynk.virtual_write(relays[1].getInfoPin(), relays[1].info())
        displayOn()
        
    @blynk.handle_event('write V14')
    def v14write_handler(pin, value):
        relays[1].cycleOffResetSet(value[0])
        blynk.virtual_write(relays[1].getInfoPin(), relays[1].info())        
        displayOn()
  
    @blynk.handle_event('write V15')
    def v15write_handler(pin, value):
        relays[2].cycleResetSet(value[0])
        blynk.virtual_write(relays[2].getInfoPin(), relays[2].info())
        displayOn()
        
    @blynk.handle_event('write V16')
    def v16write_handler(pin, value):
        relays[2].cycleOffResetSet(value[0])
        blynk.virtual_write(relays[2].getInfoPin(), relays[2].info())
        displayOn()
        
    @blynk.handle_event('write V17')
    def v17write_handler(pin, value):
        relays[3].cycleResetSet(value[0])
        blynk.virtual_write(relays[3].getInfoPin(), relays[3].info())
        displayOn()
        
    @blynk.handle_event('write V18')
    def v18write_handler(pin, value):
        relays[3].cycleOffResetSet(value[0])
        blynk.virtual_write(relays[3].getInfoPin(), relays[3].info())
        displayOn()
    
    def displayOn():
        counter = 0 
        lcdDisplay.displayOn()
        blynk.virtual_write(50, 1)
	
    def displayOff():
        lcdDisplay.displayOff()
        blynk.virtual_write(50, 1)

    @blynk.handle_event('write V50')
    def v50write_handler(pin, value):
        if(value[0] == '1'):
            _log.debug("Turn ON LCD display")
            displayOn()            
        else:
            _log.debug("Turn OFF LCD display")
            displayOff()            
     
    @blynk.handle_event("connect")
    def connect_handler():
        _log.warning("Connected")
        blynk.virtual_write(250, "Connected")
        pins = [1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17, 18, 50, 1]
        for pin in pins:
           _log.info('Syncing virtual buttons {}'.format(pin))
           blynk.virtual_sync(pin)
           blynk.read_response(timeout=0.5)
        
    
    @timer.register(interval=60, run_once=False)
    def blynk_data(): 
           _log.info("Update Timer Run")
           text = ""
           now = datetime.now()
           blynk.virtual_write(0, now.strftime("%H:%M:%S"))

           for relay in relays:
                _log.debug("Seeing if relay " + relay.name + " is automatic")
                if(relay.isAutomatic()):
                    _log.debug("relay " + relay.name + " is automatic so test cycle")
                    if(relay.whatCycle() == "On"):
                        relay.turnOn(_log)
                    else:
                        relay.turnOff(_log)
                    relay.incCycle()
      #     if(relay.hasInfoPin()):
      #          blynk.virtual_write(relay.getInfoPin(), relay.info())
      #     else:
      #          text = text + self.name + " is " + relay.whatCycle() + " "
           
           try:			
                if lcdDisplay is not None: 
                    lcdDisplay.updateLCDPumps (relays[0].state, relays[1].state, relays[2].state, relays[3].state, relays[0].isManual(), relays[1].isManual(), relays[2].isManual(), relays[3].isManual() )
           except:
              _log.critical("updating LCD crashed loop")
                
           counter = counter + 1
           if (counter > 10):
                displayOff()		
           _log.debug("The End")
     
    while True:
        blynk.run()
        if bootup :
           _log.debug("The Start of boot")
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
           blynk.set_property(systemLED, 'color', colours['ONLINE'])
           blynk.set_property(0, 'color', colours['ONLINE'])
           blynk.set_property(11, 'color', colours['ONLINE'])
           blynk.set_property(12, 'color', colours['ONLINE'])
           blynk.set_property(13, 'color', colours['ONLINE'])
           blynk.set_property(14, 'color', colours['ONLINE'])
           blynk.set_property(15, 'color', colours['ONLINE'])
           blynk.set_property(16, 'color', colours['ONLINE'])
           blynk.set_property(17, 'color', colours['ONLINE'])
           blynk.set_property(18, 'color', colours['ONLINE'])
            
            
           pins = [1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17, 18, 50, 1]
           for pin in pins:
                _log.info('Syncing virtual buttons {}'.format(pin))
                blynk.virtual_sync(pin)
                blynk.read_response(timeout=0.5)
           _log.debug("Completed Booting")
        timer.run()
except: 
   blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'))
   blynk.run()
   blynk.virtual_write(98,"in main loop except"+ '\n')
   blynk.virtual_write(250, "Crashed")
   drone.turnLEDsOffline(blynk)
   drone.turnButtonsOffline(blynk)
   GPIO.cleanup()
   os.system('sh /home/pi/updateDroneponics.sh')
 #  os.system('sudo reboot')
finally:
   blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'))
   blynk.run()
   blynk.virtual_write(250, "Shutdown")
   blynk.set_property(85, 'color', colours['OFFLINE'])
   blynk.set_property(86, 'color', colours['OFFLINE'])
   blynk.set_property(87, 'color', colours['OFFLINE'])
   blynk.set_property(88, 'color', colours['OFFLINE'])
          
   
