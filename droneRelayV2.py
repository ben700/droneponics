# The ID and range of a sample spreadsheet.
systemLED=101

import socket
import drone
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
parser.read("/home/pi/droneponics/config/configRelay/"+drone.gethostname()+".ini")

bootup = True
counter=0

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))
_log.info("/home/pi/droneponics/config/configRelay/"+drone.gethostname()+".ini")

lcdDisplay= None
try:
    lcdDisplay=drone.LCD(_log, Product="droneRelay", productTagLine="Smart Control Solution", ip=drone.get_ip())
except:
    lcdDisplay=None
	
        
try:
    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'), log=_log.info) 
    timer = blynktimer.Timer()
    _log.debug("start blynk")
    blynk.run()
    _log.info("Blynk Created")  
except:
    _log.info("except : Creating Blynk") 

try:
    relayBus=drone.RelaysI2C(_log, blynk)
    _log.debug("-------------------------------------build Relay")
    relayBus.addRelay(1, parser.get('droneFeed', 'Relay1'), 21, 85)
    _log.debug("-------------------------------------Relay1 completed going to do relay 2")
    relayBus.addRelay(2, parser.get('droneFeed', 'Relay2'), 22, 86)
    relayBus.addRelay(3, parser.get('droneFeed', 'Relay3'), 23, 87)
    relayBus.addRelay(4, parser.get('droneFeed', 'Relay4'), 24, 88)
    relayBus.addRelay(5, parser.get('droneFeed', 'Relay5'), 25, 89)
    relayBus.addRelay(6, parser.get('droneFeed', 'Relay6'), 26, 90)
    relayBus.addRelay(7, parser.get('droneFeed', 'Relay7'), 27, 91)
    relayBus.addRelay(8, parser.get('droneFeed', 'Relay8'), 28, 92)
    _log.debug("------------------------------------- 4 Relays have been setup")
except:
    _log.info("except : Creating Relays") 

try:
           

    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        blynk.virtual_write(98, "User update and reboot button v255"+ '\n')       
        blynk.virtual_write(250, "User Reboot")
        blynk.set_property(systemLED, 'color', drone.colours['OFFLINE'])
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "Updated and now restarting drone")
        os.system('sudo reboot')
              

    @blynk.handle_event('write V1')
    def v1write_handler(pin, value):
        global relays
        status = value[0]
        index = 0       
        _log.debug("in v1write_handler staus =" + str(status))       
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing off relay " + relays.relays[index].name)
                 relays.relays[index].turnOff(_log)
                 relays.relays[index].setManual("Off")
                 _log.debug(relays.relays[index].name + " in now off : v"+str(index+1)+"write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning Off")
                
        elif (staus is "2" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].turnOn(_log)
                 relays.relays[index].setManual("On")
                 _log.debug(relays.relays[index].name + " in now on : v"+str(index+1)+"write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning on")
        else:
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning auto")
           relays.relays[index].cycleOnReset()
           relays.relays[index].setOffCycleReset() 
        blynk.virtual_write(relays.relays[index].getInfoPin(), relays.relays[index].info())   
        blynk.set_property(index+1, 'color', drone.colours[status])
        try:			
           if lcdDisplay is not None: 
                 lcdDisplay.updateLCDPumps (relays.relays[0].state, relays.relays[1].state, relays.relays[2].state, relays.relays[3].state, relays.relays[4].state, relays.relays[5].state, relays.relays[6].state, relays.relays[7].state,  relays.relays[0].isManual(), relays.relays[1].isManual(), relays.relays[2].isManual(), relays.relays[3].isManual(),  relays.relays[4].isManual(), relays.relays[5].isManual(), relays.relays[6].isManual(), relays.relays[7].isManual() )
                 turnDisplayOn()			
        except:
           _log.critical("updating LCD crashed v"+str(index+1)+"")

    @blynk.handle_event('write V2')
    def v2write_handler(pin, value):
        global relays
        status = value[0]
        index = 1       
        _log.debug("in v1write_handler staus =" + str(status))       
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing off relay " + relays.relays[index].name)
                 relays.relays[index].turnOff(_log)
                 relays.relays[index].setManual("Off")
                 _log.debug(relays.relays[index].name + " in now off : v"+str(index+1)+"write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning Off")
                
        elif (staus is "2" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].turnOn(_log)
                 relays.relays[index].setManual("On")
                 _log.debug(relays.relays[index].name + " in now on : v"+str(index+1)+"write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning on")
        else:
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning auto")
           relays.relays[index].cycleOnReset()
           relays.relays[index].setOffCycleReset() 
        blynk.virtual_write(relays.relays[index].getInfoPin(), relays.relays[index].info())   
        blynk.set_property(index+1, 'color', drone.colours[status])
        try:			
           if lcdDisplay is not None: 
                 lcdDisplay.updateLCDPumps (relays.relays[0].state, relays.relays[1].state, relays.relays[2].state, relays.relays[3].state, relays.relays[4].state, relays.relays[5].state, relays.relays[6].state, relays.relays[7].state,  relays.relays[0].isManual(), relays.relays[1].isManual(), relays.relays[2].isManual(), relays.relays[3].isManual(),  relays.relays[4].isManual(), relays.relays[5].isManual(), relays.relays[6].isManual(), relays.relays[7].isManual() )
                 turnDisplayOn()			
        except:
           _log.critical("updating LCD crashed v"+str(index+1)+"")

    @blynk.handle_event('write V3')
    def v3write_handler(pin, value):
        global relays
        status = value[0]
        index = 2       
        _log.debug("in v1write_handler staus =" + str(status))       
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing off relay " + relays.relays[index].name)
                 relays.relays[index].turnOff(_log)
                 relays.relays[index].setManual("Off")
                 _log.debug(relays.relays[index].name + " in now off : v"+str(index+1)+"write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning Off")
                
        elif (staus is "2" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].turnOn(_log)
                 relays.relays[index].setManual("On")
                 _log.debug(relays.relays[index].name + " in now on : v"+str(index+1)+"write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning on")
        else:
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning auto")
           relays.relays[index].cycleOnReset()
           relays.relays[index].setOffCycleReset() 
        blynk.virtual_write(relays.relays[index].getInfoPin(), relays.relays[index].info())   
        blynk.set_property(index+1, 'color', drone.colours[status])
        try:			
           if lcdDisplay is not None: 
                 lcdDisplay.updateLCDPumps (relays.relays[0].state, relays.relays[1].state, relays.relays[2].state, relays.relays[3].state, relays.relays[4].state, relays.relays[5].state, relays.relays[6].state, relays.relays[7].state,  relays.relays[0].isManual(), relays.relays[1].isManual(), relays.relays[2].isManual(), relays.relays[3].isManual(),  relays.relays[4].isManual(), relays.relays[5].isManual(), relays.relays[6].isManual(), relays.relays[7].isManual() )
                 turnDisplayOn()			
        except:
           _log.critical("updating LCD crashed v"+str(index+1)+"")

    @blynk.handle_event('write V4')
    def v4write_handler(pin, value):
        global relays
        status = value[0]
        index = 3      
        _log.debug("in v1write_handler staus =" + str(status))       
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing off relay " + relays.relays[index].name)
                 relays.relays[index].turnOff(_log)
                 relays.relays[index].setManual("Off")
                 _log.debug(relays.relays[index].name + " in now off : v"+str(index+1)+"write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning Off")
                
        elif (staus is "2" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].turnOn(_log)
                 relays.relays[index].setManual("On")
                 _log.debug(relays.relays[index].name + " in now on : v"+str(index+1)+"write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning on")
        else:
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning auto")
           relays.relays[index].cycleOnReset()
           relays.relays[index].setOffCycleReset() 
        blynk.virtual_write(relays.relays[index].getInfoPin(), relays.relays[index].info())   
        blynk.set_property(index+1, 'color', drone.colours[status])
        try:			
           if lcdDisplay is not None: 
                 lcdDisplay.updateLCDPumps (relays.relays[0].state, relays.relays[1].state, relays.relays[2].state, relays.relays[3].state, relays.relays[4].state, relays.relays[5].state, relays.relays[6].state, relays.relays[7].state,  relays.relays[0].isManual(), relays.relays[1].isManual(), relays.relays[2].isManual(), relays.relays[3].isManual(),  relays.relays[4].isManual(), relays.relays[5].isManual(), relays.relays[6].isManual(), relays.relays[7].isManual() )
                 turnDisplayOn()			
        except:
           _log.critical("updating LCD crashed v"+str(index+1)+"")

    @blynk.handle_event('write V5')
    def v5write_handler(pin, value):
        global relays
        status = value[0]
        index = 4      
        _log.debug("in v1write_handler staus =" + str(status))       
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing off relay " + relays.relays[index].name)
                 relays.relays[index].turnOff(_log)
                 relays.relays[index].setManual("Off")
                 _log.debug(relays.relays[index].name + " in now off : v"+str(index+1)+"write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning Off")
                
        elif (staus is "2" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].turnOn(_log)
                 relays.relays[index].setManual("On")
                 _log.debug(relays.relays[index].name + " in now on : v"+str(index+1)+"write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning on")
        else:
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning auto")
           relays.relays[index].cycleOnReset()
           relays.relays[index].setOffCycleReset() 
        blynk.virtual_write(relays.relays[index].getInfoPin(), relays.relays[index].info())   
        blynk.set_property(index+1, 'color', drone.colours[status])
        try:			
           if lcdDisplay is not None: 
                 lcdDisplay.updateLCDPumps (relays.relays[0].state, relays.relays[1].state, relays.relays[2].state, relays.relays[3].state, relays.relays[4].state, relays.relays[5].state, relays.relays[6].state, relays.relays[7].state,  relays.relays[0].isManual(), relays.relays[1].isManual(), relays.relays[2].isManual(), relays.relays[3].isManual(),  relays.relays[4].isManual(), relays.relays[5].isManual(), relays.relays[6].isManual(), relays.relays[7].isManual() )
                 turnDisplayOn()			
        except:
           _log.critical("updating LCD crashed v"+str(index+1)+"")

    @blynk.handle_event('write V6')
    def v6write_handler(pin, value):
        global relays
        status = value[0]
        index = 5    
        _log.debug("in v1write_handler staus =" + str(status))       
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing off relay " + relays.relays[index].name)
                 relays.relays[index].turnOff(_log)
                 relays.relays[index].setManual("Off")
                 _log.debug(relays.relays[index].name + " in now off : v"+str(index+1)+"write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning Off")
                
        elif (staus is "2" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].turnOn(_log)
                 relays.relays[index].setManual("On")
                 _log.debug(relays.relays[index].name + " in now on : v"+str(index+1)+"write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning on")
        else:
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning auto")
           relays.relays[index].cycleOnReset()
           relays.relays[index].setOffCycleReset() 
        blynk.virtual_write(relays.relays[index].getInfoPin(), relays.relays[index].info())   
        blynk.set_property(index+1, 'color', drone.colours[status])
        try:			
           if lcdDisplay is not None: 
                 lcdDisplay.updateLCDPumps (relays.relays[0].state, relays.relays[1].state, relays.relays[2].state, relays.relays[3].state, relays.relays[4].state, relays.relays[5].state, relays.relays[6].state, relays.relays[7].state,  relays.relays[0].isManual(), relays.relays[1].isManual(), relays.relays[2].isManual(), relays.relays[3].isManual(),  relays.relays[4].isManual(), relays.relays[5].isManual(), relays.relays[6].isManual(), relays.relays[7].isManual() )
                 turnDisplayOn()			
        except:
           _log.critical("updating LCD crashed v"+str(index+1)+"")

    @blynk.handle_event('write V7')
    def v7write_handler(pin, value):
        global relays
        status = value[0]
        index = 6      
        _log.debug("in v1write_handler staus =" + str(status))       
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing off relay " + relays.relays[index].name)
                 relays.relays[index].turnOff(_log)
                 relays.relays[index].setManual("Off")
                 _log.debug(relays.relays[index].name + " in now off : v"+str(index+1)+"write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning Off")
                
        elif (staus is "2" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].turnOn(_log)
                 relays.relays[index].setManual("On")
                 _log.debug(relays.relays[index].name + " in now on : v"+str(index+1)+"write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning on")
        else:
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning auto")
           relays.relays[index].cycleOnReset()
           relays.relays[index].setOffCycleReset() 
        blynk.virtual_write(relays.relays[index].getInfoPin(), relays.relays[index].info())   
        blynk.set_property(index+1, 'color', drone.colours[status])
        try:			
           if lcdDisplay is not None: 
                 lcdDisplay.updateLCDPumps (relays.relays[0].state, relays.relays[1].state, relays.relays[2].state, relays.relays[3].state, relays.relays[4].state, relays.relays[5].state, relays.relays[6].state, relays.relays[7].state,  relays.relays[0].isManual(), relays.relays[1].isManual(), relays.relays[2].isManual(), relays.relays[3].isManual(),  relays.relays[4].isManual(), relays.relays[5].isManual(), relays.relays[6].isManual(), relays.relays[7].isManual() )
                 turnDisplayOn()			
        except:
           _log.critical("updating LCD crashed v"+str(index+1)+"")

    @blynk.handle_event('write V8')
    def v8write_handler(pin, value):
        global relays
        status = value[0]
        index = 7      
        _log.debug("in v1write_handler staus =" + str(status))       
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing off relay " + relays.relays[index].name)
                 relays.relays[index].turnOff(_log)
                 relays.relays[index].setManual("Off")
                 _log.debug(relays.relays[index].name + " in now off : v"+str(index+1)+"write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning Off")
                
        elif (staus is "2" ):
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].turnOn(_log)
                 relays.relays[index].setManual("On")
                 _log.debug(relays.relays[index].name + " in now on : v"+str(index+1)+"write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning on")
        else:
           try:
                 _log.debug("in v"+str(index+1)+"write_handler turing on relay")
                 relays.relays[index].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(index+1)+" Turning auto")
           relays.relays[index].cycleOnReset()
           relays.relays[index].setOffCycleReset() 
        blynk.virtual_write(relays.relays[index].getInfoPin(), relays.relays[index].info())   
        blynk.set_property(index+1, 'color', drone.colours[status])
        try:			
           if lcdDisplay is not None: 
                 lcdDisplay.updateLCDPumps (relays.relays[0].state, relays.relays[1].state, relays.relays[2].state, relays.relays[3].state, relays.relays[4].state, relays.relays[5].state, relays.relays[6].state, relays.relays[7].state,  relays.relays[0].isManual(), relays.relays[1].isManual(), relays.relays[2].isManual(), relays.relays[3].isManual(),  relays.relays[4].isManual(), relays.relays[5].isManual(), relays.relays[6].isManual(), relays.relays[7].isManual() )
                 turnDisplayOn()			
        except:
           _log.critical("updating LCD crashed v"+str(index+1)+"")
	
    @blynk.handle_event('write V11')
    def v11write_handler(pin, value):
        relays[0].cycleResetSet(value[0])
        blynk.virtual_write(relays[0].getInfoPin(), relays[0].info())
        turnDisplayOn()
        
    @blynk.handle_event('write V12')
    def v12write_handler(pin, value):
        relays[0].cycleOffResetSet(value[0])
        blynk.virtual_write(relays[0].getInfoPin(), relays[0].info())
        turnDisplayOn()
        
    @blynk.handle_event('write V13')
    def v13write_handler(pin, value):
        relays[1].cycleResetSet(value[0])
        blynk.virtual_write(relays[1].getInfoPin(), relays[1].info())
        turnDisplayOn()
        
    @blynk.handle_event('write V14')
    def v14write_handler(pin, value):
        relays[1].cycleOffResetSet(value[0])
        blynk.virtual_write(relays[1].getInfoPin(), relays[1].info())        
        turnDisplayOn()
  
    @blynk.handle_event('write V15')
    def v15write_handler(pin, value):
        relays[2].cycleResetSet(value[0])
        blynk.virtual_write(relays[2].getInfoPin(), relays[2].info())
        turnDisplayOn()
        
    @blynk.handle_event('write V16')
    def v16write_handler(pin, value):
        relays[2].cycleOffResetSet(value[0])
        blynk.virtual_write(relays[2].getInfoPin(), relays[2].info())
        turnDisplayOn()
        
    @blynk.handle_event('write V17')
    def v17write_handler(pin, value):
        relays[3].cycleResetSet(value[0])
        blynk.virtual_write(relays[3].getInfoPin(), relays[3].info())
        turnDisplayOn()
        
    @blynk.handle_event('write V18')
    def v18write_handler(pin, value):
        relays[3].cycleOffResetSet(value[0])
        blynk.virtual_write(relays[3].getInfoPin(), relays[3].info())
        turnDisplayOn()
    
    def turnDisplayOn():
        global counter
        _log.info("Turn display on")
        if(counter is not 0):		
                counter = 0 
                lcdDisplay.displayOn()
                blynk.virtual_write(50, 1)
	
    def turnDisplayOff():
        _log.info("Turn display off")
        lcdDisplay.displayOff()
        blynk.virtual_write(50, 0)

    @blynk.handle_event('write V50')
    def v50write_handler(pin, value):
        if(value[0] == '1'):
            _log.debug("Turn ON LCD display")
            turnDisplayOn()            
        else:
            _log.debug("Turn OFF LCD display")
            turnDisplayOff()            
     
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
           global counter
           counter = counter + 1
           
           _log.info("Update Timer Run. Counter = " + str(counter))
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
                
           if (counter > 5):
                turnDisplayOff()		
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
           blynk.set_property(systemLED, 'color', drone.colours['ONLINE'])
           blynk.set_property(0, 'color', drone.colours['ONLINE'])
           blynk.set_property(11, 'color', drone.colours['ONLINE'])
           blynk.set_property(12, 'color', drone.colours['ONLINE'])
           blynk.set_property(13, 'color', drone.colours['ONLINE'])
           blynk.set_property(14, 'color', drone.colours['ONLINE'])
           blynk.set_property(15, 'color', drone.colours['ONLINE'])
           blynk.set_property(16, 'color', drone.colours['ONLINE'])
           blynk.set_property(17, 'color', drone.colours['ONLINE'])
           blynk.set_property(18, 'color', drone.colours['ONLINE'])
            
            
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
   blynk.set_property(85, 'color', drone.colours['OFFLINE'])
   blynk.set_property(86, 'color', drone.colours['OFFLINE'])
   blynk.set_property(87, 'color', drone.colours['OFFLINE'])
   blynk.set_property(88, 'color', drone.colours['OFFLINE'])
   blynk.set_property(89, 'color', drone.colours['OFFLINE'])
   blynk.set_property(90, 'color', drone.colours['OFFLINE'])
   blynk.set_property(91, 'color', drone.colours['OFFLINE'])
   blynk.set_property(92, 'color', drone.colours['OFFLINE'])          
   
