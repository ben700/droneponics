# The ID and range of a sample spreadsheet.
systemLED=101

import socket
import drone
from drone import OpenWeather
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
from i2crelay import I2CRelayBoard  

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
    _log.critical("except setting LCD to default")

	
        
try:
    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'), log=_log.info) 
    timer = blynktimer.Timer()
    _log.debug("start blynk")
    blynk.run()
    _log.info("Blynk Created")
except:
    _log.critical("except setting up blynk")

relayBus=None
try:
    relayBus=drone.RelaysI2C(_log, blynk)
except:
    relayBus=None
    _log.critical("except setting up relay bus")

try:
    relayBus.addRelay(drone.RelayI2C(5, parser.get('droneFeed', 'Relay1'), 21, 85))
    _log.debug("Relay 1 setup")
    relayBus.addRelay(drone.RelayI2C(6, parser.get('droneFeed', 'Relay2'), 22, 86))
    _log.debug("Relay 2 setup")
    relayBus.addRelay(drone.RelayI2C(7, parser.get('droneFeed', 'Relay3'), 23, 87))
    _log.debug("Relay 3 setup")
    relayBus.addRelay(drone.RelayI2C(8, parser.get('droneFeed', 'Relay4'), 24, 88))
    _log.debug("Relay 4 setup")
except:
    _log.critical("except setting up relays")
       
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
        staus = value[0]
        relay = 0       
        _log.debug("in v1write_handler staus =" + str(staus))       
        if (staus is "1" ):
           #relays[relay].turnOff(_log)     
           relayBus.i2CRelayBoard.switch_on(5)
        elif (staus is "2" ):
           #relays[relay].turnOn(_log)
           relayBus.i2CRelayBoard.switch_on(5)

    @blynk.handle_event('write V2')
    def v2write_handler(pin, value):
        global relays
        staus = value[0]
        relay = 1       
        _log.debug("in v2write_handler staus =" + str(staus))       
        if (staus is "1" ):
           #relays[relay].turnOff(_log)
           relayBus.i2CRelayBoard.switch_on(6)
        elif (staus is "2" ):
           #relays[relay].turnOn(_log)
           relayBus.i2CRelayBoard.switch_off(6)
           

    @blynk.handle_event('write V3')
    def v3write_handler(pin, value):
        global relays
        staus = value[0]
        relay = 2
        if (staus is "1" ):
           #relays[relay].turnOff(_log)
           relayBus.i2CRelayBoard.switch_on(7)
        elif (staus is "2" ):
           _log.debug("in v3write_handler turing on relay")
           #relays[relay].turnOn(_log)
           relayBus.i2CRelayBoard.switch_off(7)
        
          
    @blynk.handle_event('write V4')
    def v4write_handler(pin, value):
        global relays		
        staus = value[0]
        relay = 3      
        if (staus is "1" ):
           relayBus.i2CRelayBoard.switch_on(8)
          # relays[relay].turnOff(_log)
        elif (staus is "2" ):
           #relays[relay].turnOn(_log)
           relayBus.i2CRelayBoard.switch_off(8)
        
  
    @blynk.handle_event('write V11')
    def v11write_handler(pin, value):
        relayBus.relays[0].cycleResetSet(value[0])
        blynk.virtual_write(relayBus.relays[0].getInfoPin(), relayBus.relays[0].info())
        turnDisplayOn()
        
    @blynk.handle_event('write V12')
    def v12write_handler(pin, value):
        relayBus.relays[0].cycleOffResetSet(value[0])
        blynk.virtual_write(relayBus.relays[0].getInfoPin(), relayBus.relays[0].info())
        turnDisplayOn()
        
    @blynk.handle_event('write V13')
    def v13write_handler(pin, value):
        relayBus.relays[1].cycleResetSet(value[0])
        blynk.virtual_write(relayBus.relays[1].getInfoPin(), relayBus.relays[1].info())
        turnDisplayOn()
        
    @blynk.handle_event('write V14')
    def v14write_handler(pin, value):
        relayBus.relays[1].cycleOffResetSet(value[0])
        blynk.virtual_write(relayBus.relays[1].getInfoPin(), relayBus.relays[1].info())        
        turnDisplayOn()
  
    @blynk.handle_event('write V15')
    def v15write_handler(pin, value):
        relayBus.relays[2].cycleResetSet(value[0])
        blynk.virtual_write(relayBus.relays[2].getInfoPin(), relayBus.relays[2].info())
        turnDisplayOn()
        
    @blynk.handle_event('write V16')
    def v16write_handler(pin, value):
        relayBus.relays[2].cycleOffResetSet(value[0])
        blynk.virtual_write(relayBus.relays[2].getInfoPin(), relayBus.relays[2].info())
        turnDisplayOn()
        
    @blynk.handle_event('write V17')
    def v17write_handler(pin, value):
        relayBus.relays[3].cycleResetSet(value[0])
        blynk.virtual_write(relayBus.relays[3].getInfoPin(), relayBus.relays[3].info())
        turnDisplayOn()
        
    @blynk.handle_event('write V18')
    def v18write_handler(pin, value):
        relayBus.relays[3].cycleOffResetSet(value[0])
        blynk.virtual_write(relayBus.relays[3].getInfoPin(), relayBus.relays[3].info())
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

           for relay in relayBus.relays:
                _log.debug("Seeing if relay " + relay.name + " is automatic")
                if(relay.isAutomatic()):
                    _log.debug("relay " + relay.name + " is automatic so test cycle")
                    if(relay.whatCycle() == "On"):
                        #relay.turnOn(_log)
                        i2CRelayBoard.switch_off(relay.relayNum)

                    else:
                        #relay.turnOff(_log)
                        i2CRelayBoard.switch_on(relay.relayNum)

                    relay.incCycle()
      #     if(relay.hasInfoPin()):
      #          blynk.virtual_write(relay.getInfoPin(), relay.info())
      #     else:
      #          text = text + self.name + " is " + relay.whatCycle() + " "
           
           try:			
                if lcdDisplay is not None: 
                    lcdDisplay.updateLCDPumps (relayBus.relays[0].state, relayBus.relays[1].state, relayBus.relays[2].state, relayBus.relays[3].state, relayBus.relays[0].isManual(), relayBus.relays[1].isManual(), relayBus.relays[2].isManual(), relayBus.relays[3].isManual() )
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
          
   
