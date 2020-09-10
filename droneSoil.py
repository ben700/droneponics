

# The ID and range of a sample spreadsheet.
colours = {1: '#FF0000', 0: '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101
import socket
import drone
import datetime
import time
import shlex, requests
import board
import busio
import smbus 
import mh_z19
import blynklib
import blynktimer
import logging
from datetime import datetime
import adafruit_tsl2591
import adafruit_bme680
import adafruit_bme280
from meteocalc import Temp, dew_point
import sys
import os
from configparser import ConfigParser
import subprocess
import re
import json
from adafruit_seesaw.seesaw import Seesaw
from colour import Color

parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configSoil/"+drone.gethostname()+".ini")

bootup = True


# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.CRITICAL))
_log.critical("critical")
_log.error("error")
_log.warning("warning")
_log.info("info")
_log.debug("debug")
_log.info("/home/pi/droneponics/config/configSoil/"+drone.gethostname()+".ini")


moistureMin=parser.getint('whiteboxes', 'min', fallback=350)
moistureMax=parser.getint('whiteboxes', 'max', fallback=1000)
ssMoistureMin=parser.getint('seesaw', 'min', fallback=350)
ssMoistureMax=parser.getint('seesaw', 'max', fallback=1000)
moistureRange = moistureMax - moistureMin
ssMoistureRange = ssMoistureMax - ssMoistureMin

red = Color("red")
blue = Color("blue")
yellow = Color("yellow")
black = Color("black")

moistureColors = list(red.range_to(blue,moistureRange))
ssMoistureColors = list(red.range_to(blue,ssMoistureRange))

tempColors = list(blue.range_to(red,40))
lightColors = list(yellow.range_to(black,66))




# Initialize Blynk
_log.debug("Creating blynk object for BLYNK_AUTH " + parser.get('blynk', 'BLYNK_AUTH')) 
blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'))
timer = blynktimer.Timer()
_log.debug("Created blynk object and timer for BLYNK_AUTH " + parser.get('blynk', 'BLYNK_AUTH')) 
#except:
#    _log.critical("Failed to create object for the blynk")
#    _log.critical("Set log level to CRITICAL to auto reboot")
#    if (parser.get('logging', 'logLevel', fallback=logging.DEBUG) =="CRITICAL"):
#        os.system('sh /home/pi/updateDroneponics.sh')
#        os.system('sudo reboot')
    
try:    
  	chirp = drone.Chirp(1, 0x20)
except:
    _log.critical("Can't find I2C1 device should be the soil sensor")
    chirp = None

try:        
    i2c_bus = busio.I2C(board.D1, board.D0) 
    ss = Seesaw(i2c_bus, addr=0x38)
except:
    _log.critical("Can't find I2C0 device should be the soil sensor")
    ss = None
    
    
def updateConfig(moistureMin, moistureMax, ssMoistureMin, ssMoistureMax):
    _log.warning("updateConfig")

    red = Color("red")
    
    moistureRange = moistureMax - moistureMin
    ssMoistureRange = ssMoistureMax - ssMoistureMin

    moistureColors = list(red.range_to(Color("blue"),moistureRange))
    ssMoistureColors = list(red.range_to(Color("blue"),ssMoistureRange))
    
    parser.set("whiteboxes","min",str(moistureMin))
    parser.set("whiteboxes","max",str(moistureMax))
    parser.set("seesaw","min",str(ssMoistureMin))
    parser.set("seesaw","max",str(ssMoistureMax))
    cfgfile = open("/home/pi/droneponics/config/configSoil/"+drone.gethostname()+".ini",'w')
    parser.write(cfgfile)
    cfgfile.close()    
    
@blynk.handle_event('write V255')
def rebooter(pin, value):
    _log.info("User Reboot")
    blynk.virtual_write(250, "User Reboot")
    blynk.set_property(systemLED, 'color', colours['OFFLINE'])
    os.system('sh /home/pi/updateDroneponics.sh')
    os.system('sudo reboot')

@blynk.handle_event("connect")
def connect_handler():
    global moistureMin
    global moistureMax
    global ssMoistureMin
    global ssMoistureMax
    _log.warning("Connected")
    blynk.virtual_write(250, "Connected")
    blynk.set_property(1,"min", moistureMin)
    blynk.set_property(1,"max", moistureMax)
    blynk.set_property(5,"min", ssMoistureMin)
    blynk.set_property(5,"max", ssMoistureMax)


@blynk.handle_event("disconnect")
def disconnect_handler():
    _log.warning("Disconnected")
    blynk.virtual_write(250, "Disconnected")
  
    
@timer.register(interval=30, run_once=False)
def blynk_data():
    global moistureMin
    global moistureMax
    global ssMoistureMin
    global ssMoistureMax
    
    _log.info("Start of timer.register fx")
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.set_property(0, 'color', colours['ONLINE'])
    
    moistureRead=chirp.moist()
    blynk.virtual_write(1, moistureRead)
    tempRead = chirp.temp()/10
    blynk.virtual_write(2, tempRead) 
    lightRead = chirp.light()
    blynk.virtual_write(3, lightRead/10)
    blynk.set_property(1, 'color', moistureColors[int(moistureRead-moistureMin)])
    blynk.set_property(2, 'color', tempColors[int(tempRead)])
    blynk.set_property(3, 'color', lightColors[int(lightRead/1000)])
    
    ssMoistureRead = ss.moisture_read()
    blynk.virtual_write(5, ssMoistureRead) 
    ssTempRead = ss.get_temp()
    blynk.virtual_write(6, ssTempRead)
    blynk.set_property(5, 'color', ssMoistureColors[int(ssMoistureRead-ssMoistureMin)])
    blynk.set_property(6, 'color', tempColors[int(ssTempRead)])
    _log.info("Finished reading Sensors")
    
    _log.info("moistureMin =" + str(moistureMin))
    _log.info("moistureMax =" + str(moistureMax))
    _log.info("ssMoistureMin =" + str(ssMoistureMin))
    _log.info("ssMoistureMax =" + str(ssMoistureMax))


    if (moistureRead<moistureMin):
        moistureMin = moistureRead
        blynk.set_property(1,"min", moistureMin)
        updateConfig(moistureMin, moistureMax, ssMoistureMin, ssMoistureMax)
    if (moistureRead>moistureMax):
        moistureMax = moistureRead
        blynk.set_property(1,"max", moistureMax)
        updateConfig(moistureMin, moistureMax, ssMoistureMin, ssMoistureMax)
    
    if (ssMoistureRead<ssMoistureMin):
        ssMoistureMin = ssMoistureRead
        blynk.set_property(5,"min", ssMoistureMin)
        updateConfig(moistureMin, moistureMax, ssMoistureMin, ssMoistureMax)
    if (ssMoistureRead>ssMoistureMax):
        ssMoistureMax = ssMoistureRead
        blynk.set_property(5,"max", ssMoistureMax)
        updateConfig(moistureMin, moistureMax, ssMoistureMin, ssMoistureMax)
    
    _log.debug("End of timer.register fx")
        
_log.info("Created all the objects. Now starting the drone")        
blynk.run() #need to call here so you can update app outside main while loop    
blynk.virtual_write(250, "Start-up")
blynk.virtual_write(251, drone.gethostname())
blynk.virtual_write(252, drone.get_ip())        
blynk.virtual_write(98, "clr")
_log.debug("Just about to get boot timestamp and change system LED")
now = datetime.now()
blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
blynk.virtual_write(systemLED, 255)
blynk.virtual_write(255, 0)


_log.info("--------------------------Completed Boot--------------------------")

while True:
    try:
        blynk.run()
        timer.run()
    except: 
       _log.error("in main loop except")
       blynk.virtual_write(250, "Crashed")
       blynk.notify("non-Production blynk crashed and is not-restarting; hostname " +  drone.gethostname() + " at: " + now.strftime("%d/%m/%Y %H:%M:%S"))
       _log.critical("Main Loop exception :- Set log evel to CRITICAL to auto reboot")
        