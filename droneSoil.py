

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
reboots = 0

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


moistureMin=parser.getint('whiteboxes', 'min', fallback=150)
moistureMax=parser.getint('whiteboxes', 'max', fallback=650)
ssMoistureMin=parser.getint('seesaw', 'min', fallback=260)
ssMoistureMax=parser.getint('seesaw', 'max', fallback=360)
moistureRange = moistureMax - moistureMin
ssMoistureRange = ssMoistureMax - ssMoistureMin

red = Color("red")
blue = Color("blue")
yellow = Color("yellow")
black = Color("black")

moistureColors = list(Color("red").range_to(Color("blue"),101))
tempColors = list(Color("blue").range_to(Color("red"),40))
lightColors = list(Color("yellow").range_to(Color("black"),66))


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

    
    
def updateConfig(moistureMin, moistureMax, ssMoistureMin, ssMoistureMax):
    _log.warning("updateConfig")

    global moistureRange
    global ssMoistureRange
    
    moistureRange = moistureMax - moistureMin
    ssMoistureRange = ssMoistureMax - ssMoistureMin

    parser.set("whiteboxes","min",str(moistureMin))
    parser.set("whiteboxes","max",str(moistureMax))
    parser.set("seesaw","min",str(ssMoistureMin))
    parser.set("seesaw","max",str(ssMoistureMax))
    cfgfile = open("/home/pi/droneponics/config/configSoil/"+drone.gethostname()+".ini",'w')
    parser.write(cfgfile)
    cfgfile.close()    
    
@blynk.handle_event('write V254')
def rebootsCounter(pin, value):
    global reboots
    reboots = int(value[0])
    
@blynk.handle_event('write V255')
def rebooter(pin, value):
    _log.info("User Reboot")
    blynk.virtual_write(250, "User Reboot")
    blynk.virtual_write(98, "User Reboot"+ '\n')
    blynk.set_property(systemLED, 'color', colours['OFFLINE'])
    blynk.virtual_write(98, "Update Code"+ '\n')
    os.system('sh /home/pi/updateDroneponics.sh')
    blynk.virtual_write(98, "Now do the Reboot"+ '\n')
    os.system('sudo reboot')

    
@blynk.handle_event("connect")
def connect_handler():
    _log.info("Connected")
    pins = [254]
    for pin in pins:
        _log.info('Syncing virtual buttons {}'.format(pin))
        blynk.virtual_sync(pin)
        blynk.read_response(timeout=0.5)
        
        
@timer.register(interval=30, run_once=False)
def blynk_data():
    global moistureMin
    global moistureMax
    global ssMoistureMin
    global ssMoistureMax
    global moistureRange
    global ssMoistureRange

    
    blynk.virtual_write(250, "Running")
    blynk.set_property(250, 'color', colours['ONLINE'])
    _log.info("Start of timer.register fx")
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.set_property(0, 'color', colours['ONLINE'])

    _log.info("timer.register fx Update Time")
    try:
        chirp1 = drone.Chirp(1, 0x20)
        moistureRead=chirp1.moist()
        tempRead = chirp1.temp()/10
        lightRead = chirp1.light()
            
        moistureReadPer = int(((moistureRead-moistureMin)/moistureRange)*100) 
        blynk.virtual_write(1, moistureReadPer)
        blynk.virtual_write(2, tempRead) 
        blynk.virtual_write(3, int(lightRead/10))
        blynk.set_property(1, 'color', drone.getMoistColour(_log, int(moistureReadPer)))
        blynk.set_property(2, 'color', drone.getTempColour(_log, tempRead))
        blynk.set_property(3, 'color', colours['ONLINE']) # change to per max = 65535
        blynk.virtual_write(4, moistureRead)
        blynk.set_property(4, 'color', drone.getMoistColour(_log, int(moistureReadPer)))    
    except:
        _log.critical("Can't find I2C1 chirp device should be a soil sensor")
        blynk.virtual_write(250, "Sensor 1 Error")
        blynk.set_property(250, 'color', '#ff0000')
        blynk.virtual_write(1, -1)
        blynk.virtual_write(2, -1) 
        blynk.virtual_write(3, -1)
        blynk.virtual_write(4, -1)
        blynk.set_property(1, 'color', colours['OFFLINE'])
        blynk.set_property(2, 'color', colours['OFFLINE'])
        blynk.set_property(3, 'color', colours['OFFLINE'])
        blynk.set_property(4, 'color', colours['OFFLINE'])  
        
        
    try:
        chirp0 = drone.Chirp(0, 0x20)
        moistureRead=chirp0.moist()
        tempRead = chirp0.temp()/10
        lightRead = chirp0.light()
            
        moistureReadPer = int(((moistureRead-moistureMin)/moistureRange)*100) 
        blynk.virtual_write(5, moistureReadPer)
        blynk.virtual_write(6, tempRead) 
        blynk.virtual_write(7, int(lightRead/10))
        blynk.set_property(5, 'color', drone.getMoistColour(_log, int(moistureReadPer)))
        blynk.set_property(6, 'color', drone.getTempColour(_log, tempRead))
        blynk.set_property(7, 'color', colours['ONLINE']) # change to per max = 65535
        blynk.virtual_write(8, moistureRead)
        blynk.set_property(8, 'color', drone.getMoistColour(_log, int(moistureReadPer)))    
    except:
        _log.critical("Can't find I2C0 chirp device should be a soil sensor")
        blynk.virtual_write(250, "Sensor 0 Error")
        blynk.set_property(250, 'color', '#ff0000')
        blynk.virtual_write(5, -1)
        blynk.virtual_write(6, -1) 
        blynk.virtual_write(7, -1)
        blynk.virtual_write(8, -1)
        blynk.set_property(5, 'color', colours['OFFLINE'])
        blynk.set_property(6, 'color', colours['OFFLINE'])
        blynk.set_property(7, 'color', colours['OFFLINE'])
        blynk.set_property(8, 'color', colours['OFFLINE'])  
        
        
       

#        if (moistureRead<moistureMin):
#            moistureMin = moistureRead
#            updateConfig(moistureMin, moistureMax, ssMoistureMin, ssMoistureMax)
#        if (moistureRead>moistureMax):
#            moistureMax = moistureRead
#            updateConfig(moistureMin, moistureMax, ssMoistureMin, ssMoistureMax)

#        if (ssMoistureRead<ssMoistureMin):
#            ssMoistureMin = ssMoistureRead
#            updateConfig(moistureMin, moistureMax, ssMoistureMin, ssMoistureMax)
#        if (ssMoistureRead>ssMoistureMax):
#            ssMoistureMax = ssMoistureRead
#            updateConfig(moistureMin, moistureMax, ssMoistureMin, ssMoistureMax)

    _log.info("Now work on second sensor")

    try:
        i2c_bus = busio.I2C(board.SCL, board.SDA) 
        ss = Seesaw(i2c_bus, addr=0x36)
        ssMoistureRead = ss.moisture_read()
        ssTempRead = round(ss.get_temp(),1)
        ssMoistureReadPer = int(((ssMoistureRead-ssMoistureMin)/ssMoistureRange)*100)
        blynk.virtual_write(10, ssMoistureReadPer) 
        blynk.virtual_write(11, ssTempRead)
        blynk.virtual_write(12, ssMoistureRead)
        blynk.set_property(10, 'color', drone.getMoistColour(_log, int(ssMoistureReadPer)))
        blynk.set_property(11, 'color', drone.getTempColour(_log, int(ssTempRead*10)))
        blynk.set_property(12, 'color', drone.getMoistColour(_log, int(ssMoistureReadPer)))
            
    except:
        _log.critical("Can't find I2C1 device 36 a soil sensor")
        blynk.virtual_write(250, "Sensor 2 Error")
        blynk.set_property(250, 'color', '#ff0000')
        blynk.set_property(10, 'color', colours['OFFLINE'])
        blynk.set_property(11, 'color', colours['OFFLINE'])
        blynk.set_property(12, 'color', colours['OFFLINE'])

        
    try:
        i2c_bus = busio.I2C(board.SCL, board.SDA) 
        ss = Seesaw(i2c_bus, addr=0x37)
        ssMoistureRead = ss.moisture_read()
        ssTempRead = round(ss.get_temp(),1)
        ssMoistureReadPer = int(((ssMoistureRead-ssMoistureMin)/ssMoistureRange)*100)
        blynk.virtual_write(13, ssMoistureReadPer) 
        blynk.virtual_write(14, ssTempRead)
        blynk.virtual_write(15, ssMoistureRead)
        blynk.set_property(13, 'color', drone.getMoistColour(_log, int(ssMoistureReadPer)))
        blynk.set_property(14, 'color', drone.getTempColour(_log, int(ssTempRead*10)))
        blynk.set_property(15, 'color', drone.getMoistColour(_log, int(ssMoistureReadPer)))
            
    except:
        _log.critical("Can't find I2C1 device 37 a soil sensor")
        blynk.virtual_write(250, "Sensor 3 Error")
        blynk.set_property(250, 'color', '#ff0000')
        blynk.set_property(13, 'color', colours['OFFLINE'])
        blynk.set_property(14, 'color', colours['OFFLINE'])
        blynk.set_property(15, 'color', colours['OFFLINE'])
        
    try:
        i2c_bus = busio.I2C(board.D1, board.D0) 
        ss = Seesaw(i2c_bus, addr=0x36)
        ssMoistureRead = ss.moisture_read()
        ssTempRead = round(ss.get_temp(),1)
        ssMoistureReadPer = int(((ssMoistureRead-ssMoistureMin)/ssMoistureRange)*100)
        blynk.virtual_write(16, ssMoistureReadPer) 
        blynk.virtual_write(17, ssTempRead)
        blynk.virtual_write(18, ssMoistureRead)
        blynk.set_property(16, 'color', drone.getMoistColour(_log, int(ssMoistureReadPer)))
        blynk.set_property(17, 'color', drone.getTempColour(_log, int(ssTempRead*10)))
        blynk.set_property(18, 'color', drone.getMoistColour(_log, int(ssMoistureReadPer)))
            
    except:
        _log.critical("Can't find I2C0 device 36 a soil sensor")
        blynk.virtual_write(250, "Sensor 4 Error")
        blynk.set_property(250, 'color', '#ff0000')
        blynk.set_property(16, 'color', colours['OFFLINE'])
        blynk.set_property(17, 'color', colours['OFFLINE'])
        blynk.set_property(18, 'color', colours['OFFLINE'])
        
        
    try:
        i2c_bus = busio.I2C(board.D1, board.D0) 
        ss = Seesaw(i2c_bus, addr=0x38)
        ssMoistureRead = ss.moisture_read()
        ssTempRead = round(ss.get_temp(),1)
        ssMoistureReadPer = int(((ssMoistureRead-ssMoistureMin)/ssMoistureRange)*100)
        blynk.virtual_write(19, ssMoistureReadPer) 
        blynk.virtual_write(20, ssTempRead)
        blynk.virtual_write(21, ssMoistureRead)
        blynk.set_property(19, 'color', drone.getMoistColour(_log, int(ssMoistureReadPer)))
        blynk.set_property(20, 'color', drone.getTempColour(_log, int(ssTempRead*10)))
        blynk.set_property(21, 'color', drone.getMoistColour(_log, int(ssMoistureReadPer)))
            
    except:
        _log.critical("Can't find I2C0 device 38 a soil sensor")
        blynk.virtual_write(250, "Sensor 5 Error")
        blynk.set_property(250, 'color', '#ff0000')
        blynk.set_property(19, 'color', colours['OFFLINE'])
        blynk.set_property(20, 'color', colours['OFFLINE'])
        blynk.set_property(21, 'color', colours['OFFLINE'])
        
        
    _log.info("Finished reading Sensors")
    
    _log.debug("End of timer.register fx")
        
_log.info("Created all the objects. Now starting the drone")        
blynk.run() #need to call here so you can update app outside main while loop    
blynk.virtual_write(250, "Start-up")
blynk.set_property(250, 'label', "Status")
blynk.virtual_write(251, drone.gethostname())
blynk.set_property(251, 'label', "hostname")
blynk.virtual_write(252, drone.get_ip())
blynk.set_property(251, 'label', "IP Address")
blynk.virtual_write(98, "clr")


_log.debug("Posting I2C 0 devices to app")
p = subprocess.Popen(['i2cdetect', '-y','0'],stdout=subprocess.PIPE,)
blynk.virtual_write(98, "I2C 0 devices"+'\n')
for i in range(0,9):
     blynk.virtual_write(98, str(p.stdout.readline()) + '\n')    
    
_log.info("Posting I2C 1 devices to app")
blynk.virtual_write(98, "I2C 1 devices"+'\n')
q = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
for i in range(0,9):
     blynk.virtual_write(98, str(q.stdout.readline()) + '\n')

_log.debug("Just about to get boot timestamp and change system LED")
now = datetime.now()
blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
blynk.virtual_write(systemLED, 255)
blynk.set_property(systemLED, 'color', colours['ONLINE'])
blynk.set_property(0, 'color', colours['ONLINE'])
blynk.set_property(250, 'color', colours['ONLINE'])
blynk.virtual_write(255, 0)
blynk.virtual_sync(254)
blynk.read_response(timeout=0.5)
reboots = reboots + 1
blynk.virtual_write(254, reboots)

blynk.virtual_write(98, "Completed Boot" + '\n')
_log.info("--------------------------Completed Boot--------------------------")

while True:
    try:
        blynk.run()
        timer.run()
    except: 
       _log.critical("Main Loop exception :- Auto reboot")
       blynk.virtual_write(250, "Crashed")
       blynk.set_property(systemLED, 'color', colours['OFFLINE'])
       blynk.notify("Moisture Sensors have crashed and are restarting; hostname " +  drone.gethostname() + " at: " + now.strftime("%d/%m/%Y %H:%M:%S"))
       os.system('sh /home/pi/updateDroneponics.sh')
       os.system('sudo reboot')
        
