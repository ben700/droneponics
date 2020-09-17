

# The ID and range of a sample spreadsheet.
colours = {1: '#FF0000', 0: '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101
import socket
import drone
from drone import Alarm, OpenWeather
alarmList=[]
#load Temperature alarms
alarmList.append(Alarm('temperature', "low", "low",18.0, Notify=False,  Message = 'Low TEMP!!!', Colour = '#c0392b'))
alarmList.append(Alarm('temperature', "High", "high", 26.0, Notify=False, Message = 'High TEMP!!!', Colour = '#c0392b'))
alarmList.append(Alarm('temperature', "low", "lowlow", 15.0, Notify=True,  Message = 'Low Low TEMP!!!', Colour = '#c0392b'))
alarmList.append(Alarm('temperature', "High", "highhigh", 30.0,Notify=True, Message = 'High High TEMP!!!', Colour = '#c0392b'))

openWeather = OpenWeather() 

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

parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configAir/"+drone.gethostname()+".ini")

bootup = True
rowIndex=1

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
_log.info("/home/pi/droneponics/config/configAir/"+drone.gethostname()+".ini")

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
    tslI2C = busio.I2C(board.SCL, board.SDA)
    if not 0x29 in tslI2C.scan():
        tslI2C = busio.I2C(board.D1, board.D0)   
        if not 0x29 in tslI2C.scan():
            _log.info("Didn't find TSL2591")
            tslI2C = None  
        else:
            _log.info("Found TSL2591 on I2C-0")
    else:
         _log.info("Found TSL2591 on I2C-1")
except:
    _log.critical("Can't find I2C device 29 should be the Light sensor")
    tslI2C = None
try:     
    # Initialize the sensor.
    if (tslI2C is not None):
       tsl = adafruit_tsl2591.TSL2591(tslI2C)
       # You can optionally change the gain and integration time:
       tsl.gain = adafruit_tsl2591.GAIN_LOW
       tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS
    else:
       tsl = None
except:
    _log.critical("Failed to create object for Light sensor")
    tsl = None

try:
    bmeI2C = busio.I2C(board.SCL, board.SDA)
    if not 0x77 in bmeI2C.scan():
        bmeI2C = busio.I2C(board.D1, board.D0)   
        if not 0x77 in bmeI2C.scan():
            _log.error("Can't find I2C device 77 should be the BME280/680 sensor")
            blynk.virtual_write(250, "no BMEx80")
            bmeI2C = None      
        else:
            _log.info("Found I2C device 77 should be the BME280/680 sensor on I2C-0")
    else:
         _log.info("Found I2C device 77 should be the BME280/680 sensor on I2C-1")
except:
    _log.critical("Can't find I2C device 77 should be the BME280/680 sensor")
    bmeI2C = None

bme680 = None
bme280 = None

try:
    # Initialize the sensor.
    if (bmeI2C is not None):
        if (parser.get('droneAir', 'BME680', fallback=False) == "True"):
            _log.debug("Creating BME680 object for device 77 should be the BME680 sensor") 
     #      bmex80 = adafruit_bme680.Adafruit_BME680_I2C(bmeI2C)     
            bme680 = adafruit_bme680.Adafruit_BME680_I2C(bmeI2C)
            _log.info("Created BME680 object for device 77 should be the BME680 sensor") 
            try:
                test = bme680.temperature
                _log.info("BME680 object for device 77 tested and working OK") 
            except:
                bme680 = None
                bme280 = None
                _log.critical("Failed to test object for device 77 should be the BME680 sensor")
                blynklib.Blynk.notify_msg("BME680 sensor fail on " + drone.gethostname())
                blynklib.Blynk.email("{DEVICE_OWNER_EMAIL}", "{DEVICE_NAME} : Alarm", "Your {DEVICE_NAME} has critical BME680 error!") 
        else:
            _log.debug("Creating BME280 object for device 77 should be the BME280 sensor") 
       #     bmex80 = adafruit_bme280.Adafruit_BME280_I2C(bmeI2C)
            bme280 = adafruit_bme280.Adafruit_BME280_I2C(bmeI2C)
            _log.info("Created BME280 object for device 77 should be the BME280 sensor")
            test = bme280.temperature
            _log.info("BME280 object for device 77 tested and working OK") 
    else:
       bme680 = None
       bme280 = None
except:
    _log.critical("Failed to create and test object for device 77 should be the BME280/680 sensor")
    bme680 = None
    bme280 = None

@blynk.handle_event('write V29')
def v29write_handler(pin, value):
    _log.debug("v29write_handler rowIndex =" + str(value[0]))
    global rowIndex
    rowIndex = int(value[0])
                 
    
@blynk.handle_event('write V255')
def rebooter(pin, value):
    _log.info("User Reboot")
    blynk.virtual_write(250, "User Reboot")
    blynk.set_property(systemLED, 'color', colours['OFFLINE'])
    os.system('sh /home/pi/updateDroneponics.sh')
    os.system('sudo reboot')

@blynk.handle_event("connect")
def connect_handler():
    _log.warning("Connected")
    blynk.virtual_write(250, "Connected")
    for pin in range(24,30):
         _log.info('Syncing virtual buttons {}'.format(pin))
         blynk.virtual_sync(pin)
         blynk.read_response(timeout=0.5)
        

@blynk.handle_event("disconnect")
def disconnect_handler():
    _log.warning("Disconnected")
    blynk.virtual_write(250, "Disconnected")
  
    
@timer.register(interval=30, run_once=False)
def blynk_data():
  #  try:
  #      _log.debug(bme680.gas)
  #  except:
  #      bme680 = None
    _log.debug("bme680 = " + str(bme680))
    _log.debug("bme280 = " + str(bme280))
    
    
    _log.info("Start of timer.register fx")
    blynk.set_property(systemLED, 'color', colours[1])
    blynk.virtual_write(250, "Updating")
    _log.debug("Going to get timestamp")
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.set_property(0, 'color', colours['ONLINE'])
    _log.debug("Going to get openweather")
    openWeather.blynkOpenWeather(blynk, _log)
    _log.debug("Completed openweather")
    if(bme280 is  None and bme680 is None):            
        drone.setBMEFormOfflineColours(blynkObj=blynk, loggerObj=_log)   
     
    
    _log.debug("bme680 = " + str(bme680))
    _log.debug("bme280 = " + str(bme280))      
    if(bme680 is not None):            
        _log.debug("bme680 is not None so going to set pressure")
        bme680.sea_level_pressure = openWeather.getPressure()
        _log.debug("Going to send bme680 data to blynk app")
        blynk.virtual_write(2, bme680.gas)
        _log.info("bme680.gas =" + str(bme680.gas))
        blynk.virtual_write(1, bme680.temperature)
        _log.info("bme680.temperature =" + str(bme680.temperature))
        blynk.virtual_write(3, bme680.humidity)
        _log.info("bme680.humidity =" + str(bme680.humidity))
        blynk.virtual_write(4, bme680.pressure)
        _log.info("bme680.pressure =" + str(bme680.pressure))
        blynk.virtual_write(5, bme680.altitude)
        _log.info("bme680.altitude =" + str(bme680.altitude))
        _log.debug("Going to get dew point from bme680 data")
        t = Temp(bme680.temperature, 'c')
        dewPoint = dew_point(temperature=t, humidity=bme680.humidity)
        blynk.virtual_write(11, dewPoint)
        _log.info("bme680.dew_point =" + str(dewPoint))
        drone.setBME680FormColours(bme680, blynkObj=blynk, loggerObj=_log)     
    elif(bme280 is not None):           
        _log.debug("Going to send bme280 data to blynk app")
        blynk.virtual_write(2, "BME280")
        blynk.set_property(2, 'color', colours['OFFLINE'])
        blynk.virtual_write(1, bme280.temperature)
        _log.info("bme280.temperature" + str(bme280.temperature))  
        blynk.virtual_write(3, bme280.humidity)
        _log.info("bme280.humidity" + str(bme280.humidity))  
        blynk.virtual_write(4, bme280.pressure)
        _log.info("bme280.pressure" + str(bme280.pressure))  
        blynk.virtual_write(5, bme280.altitude)
        _log.info("bme280.altitude" + str(bme280.altitude))  
        _log.debug("Going to get dew point from bme280 data")
        t = Temp(bme280.temperature, 'c')
        blynk.virtual_write(11, dew_point(temperature=t, humidity=bme280.humidity))
        _log.debug("set BME form display")
        drone.setBME280FormColours(bme280, blynkObj=blynk, loggerObj=_log)          

    _log.debug("Now work on TSL2591 sensor")
    if (tsl is not None):
        _log.debug('Total light: {0:.2f}lux'.format(tsl.lux))
        _log.debug('Infrared light: {0:d}'.format(tsl.infrared))
        _log.debug('Visible light: {0:d}'.format(tsl.visible))
        _log.debug('Full spectrum (IR + visible) light: {0:d}'.format(tsl.full_spectrum))
        blynk.virtual_write(6, str("{0:.2f}".format(tsl.lux))) 
        blynk.virtual_write(7, str("{0:d}".format(tsl.infrared)))
        blynk.virtual_write(8, ("{0:d}".format(tsl.visible)))
        blynk.virtual_write(9, ("{0:d}".format(tsl.full_spectrum)))
        _log.debug("Now drone.setTSLFormOnline") 
        drone.setTSLFormOnlineColours(blynkObj=blynk, loggerObj=_log)
    else:
        drone.setTSLFormOfflineColours(blynkObj=blynk, loggerObj=_log)

    _log.debug("Now work on mhz19b sensor")
    mhz19b = mh_z19.read()  
    if mhz19b is not None:
        blynk.virtual_write(10, '{0:d}'.format(mhz19b['co2']))
        _log.info('CO2: {0:d}'.format(mhz19b['co2']))
        drone.setMHZFormOnlineColours(blynkObj=blynk, loggerObj=_log)
        _log.info("blynkBridge BLYNK_AUTH = " + parser.get('blynkBridge', 'BLYNK_AUTH', fallback="Fallback"))
        if (parser.get('blynkBridge', 'BLYNK_AUTH', fallback=None) is not None):
            _log.warning("Send CO2 data via blynkBridge")
            blynkBridge = blynklib.Blynk(parser.get('blynkBridge', 'BLYNK_AUTH'))
            blynkBridge.run()
            CO2_VPIN = parser.get('blynkBridge', 'CO2_VPIN', fallback=10)
            blynkBridge.virtual_write(CO2_VPIN, '{0:d}'.format(mhz19b['co2']))
            blynkBridge.set_property(CO2_VPIN, 'label', "from " + drone.gethostname())
            blynkBridge.virtual_sync(10)
        #    blynkBridge.virtual_write(CO2_VPIN+1, now)
            _log.info("blynkBridge CO2 data sent")
    else:
        blynk.virtual_write(98, 'Unexpected error: mhz19b' + '\n')
        _log.error('Unexpected error: mhz19b')
        drone.setMHZFormOfflineColours(blynkObj=blynk, loggerObj=_log)
    blynk.virtual_write(250, "Running")
    blynk.set_property(systemLED, 'color', colours[0])
    _log.debug("End of timer.register fx")
        
_log.info("Created all the objects. Now starting the drone")        
blynk.run() #need to call here so you can update app outside main while loop    
blynk.virtual_write(250, "Start-up")
blynk.virtual_write(251, drone.gethostname())
blynk.virtual_write(252, drone.get_ip())        
blynk.virtual_write(98, "clr")
if (parser.get('logging', 'logLevel', fallback=logging.CRITICAL) =="DEBUG"):
    if (parser.get('droneAir', 'I2C-0', fallback=False) == "True"):
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
x=1
for alarm in alarmList:
    alarm.display(blynk,x)
    x=x+1
_log.debug("Just about to get boot timestamp and change system LED")
now = datetime.now()
blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
blynk.virtual_write(97, "add", rowIndex, "Reboot", now.strftime("%d/%m/%Y %H:%M:%S"))
blynk.virtual_write(29,rowIndex+1)          
blynk.virtual_write(systemLED, 255)
_log.debug("Main fx:- calling drone.setFormOnline to remove blue")
drone.setFormOnlineColours(blynkObj=blynk, loggerObj=_log)
blynk.virtual_write(255, 0)
_log.info("--------------------------Completed Boot--------------------------")
_log.debug("droneAir : drone.getTempColour(_log,int(10)) = " + str(drone.getTempColour(_log,100)))
    
while True:
    try:
        blynk.run()
        timer.run()
    except: 
       _log.error("in main loop except")
       blynk.virtual_write(250, "Crashed")
       drone.setFormOfflineColours(blynkObj=blynk, loggerObj=_log)
       if (parser.get('logging', 'logLevel', fallback=logging.DEBUG) =="CRITICAL"):
            blynk.notify("Production blynk crashed and is auto-restarting; hostname " +  drone.gethostname() + " at: " + now.strftime("%d/%m/%Y %H:%M:%S"))
            blynk.email(drone.TARGET_EMAIL, 'Production Blynk Crash', "Production blynk crashed and is auto-restarting; hostname " +  drone.gethostname() + " at: " + now.strftime("%d/%m/%Y %H:%M:%S"))            
            os.system('sh /home/pi/updateDroneponics.sh')
            os.system('sudo reboot')
       elif (parser.get('logging', 'logLevel', fallback=logging.DEBUG) is not "DEBUG"):
            blynk.notify("non-Production blynk crashed and is not-restarting; hostname " +  drone.gethostname() + " at: " + now.strftime("%d/%m/%Y %H:%M:%S"))
            _log.critical("Main Loop exception :- Set log evel to CRITICAL to auto reboot")
       else:
            _log.critical("Main Loop exception :- Set log evel to CRITICAL to auto reboot")
        
