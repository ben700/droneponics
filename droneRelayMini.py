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

parser = ConfigParser()
parser.read('/home/pi/configDroneRelayMini.ini')
       
bootup = True
CO2=0
# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)

#if True:
try:

    relays=drone.Relays()
    relays.add( drone.SwitchRelay(15, parser.get('droneRelayMini', 'Relay1'), 1))
    relays.add( drone.SwitchRelay(18, parser.get('droneRelayMini', 'Relay2'), 2))
    relays.add( drone.SwitchRelay(23, parser.get('droneRelayMini', 'Relay3'), 3))
    relays.add( drone.SwitchRelay(24, parser.get('droneRelayMini', 'Relay4'), 4))
    
    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'))
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
        for pin in range(1,5):
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
        _log.debug("Write_handler for " + str(pin) + " the value is " + str(value[0]))
        relays.relays[pin-1].blynkWriteHandler(blynk, value[0])
    
    @blynk.handle_event('write V2')
    def write_handler(pin, value):
        _log.debug("Write_handler for " + str(pin) + " the value is " + str(value[0]))
        relays.relays[pin-1].blynkWriteHandler(blynk, value[0])
    
    @blynk.handle_event('write V3')
    def write_handler(pin, value):
        _log.debug("Write_handler for " + str(pin) + " the value is " + str(value[0]))
        relays.relays[pin-1].blynkWriteHandler(blynk, value[0])
    
    @blynk.handle_event('write V4')
    def write_handler(pin, value):
        _log.debug("Write_handler for " + str(pin) + " the value is " + str(value[0]))
        relays.relays[pin-1].blynkWriteHandler(blynk, value[0])
    
    @blynk.handle_event('write V10')
    def write_handler(pin, value):
        global CO2
        CO2 = value[0]
        _log.info("!!!!!!!!!!!!!!!!!!!!!!!   CO2=" + str(CO2))
              
    @timer.register(interval=10, run_once=False)
    def blynk_data():
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        for switchRelay in relays.relays:
           # _log.debug("TimerHandler for relay " + switchRelay.name)
            switchRelay.blynkTimerHandler(blynk)
        _log.debug("Update Timer Run completed")
        
    while True:
        blynk.run()
        if bootup :
           blynk.virtual_write(98, "clr")
           blynk.virtual_write(98, "Rebooted"+ '\n')
           blynk.virtual_write(250, "Start-up")
           blynk.set_property(251, "label",drone.gethostname())
           blynk.virtual_write(251, drone.get_ip())
           for relay in relays.relays:
              relay.setDisplay(blynk)  
           bootup = False
           _log.debug("Just about to complete Booting")
           now = datetime.now()
           blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
           blynk.virtual_write(drone.systemLED, 255)
           blynk.set_property(drone.systemLED, 'color', drone.colours[0])
           blynk.virtual_write(255, 0)
           blynk.virtual_write(98, "Running"+ '\n')
           _log.info('Just Booted')
           blynk.virtual_write(250, "Running")
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
   os.system('sudo reboot')
