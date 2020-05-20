

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
from meteocalc import Temp, dew_point
import sys
import os
from configparser import ConfigParser
import subprocess
import re
import json

parser = ConfigParser()
parser.read('/home/pi/configAir.ini')

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
            _log.info("Didn't find BME680")
            blynk.virtual_write(250, "no BME680")
            bmeI2C = None      
        else:
            _log.info("Found BME680 on I2C-0")
    else:
         _log.info("Found BME680 on I2C-1")
except:
    _log.critical("Can't find I2C device 77 should be the BME280/680 sensor")
    bmeI2C = None

try:
    # Initialize the sensor.
    if (bmeI2C is not None):
       try:
           if (parser.get('droneAir', 'BME680', fallback=False) == "True"):
              bmex80 = adafruit_bme680.Adafruit_BME680_I2C(bmeI2C)            
           else:
              bmex80 = adafruit_bme280.Adafruit_BME280_I2C(bmeI2C)
       except:
           bmex80 = None
           _log.info("Unexpected error: bme680")
    else:
       bme680 = None
except:
    _log.critical("Failed to create object for the BME280/680 sensor")
    bmeI2C = None

try:
    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'))
    timer = blynktimer.Timer()
except:
    _log.critical("Failed to create object for the blynk")
    bmeI2C = None
    
@blynk.handle_event('write V255')
def rebooter(pin, value):
    _log.info("User Reboot")
    blynk.virtual_write(250, "User Reboot")
    blynk.set_property(systemLED, 'color', colours['OFFLINE'])
    os.system('sh /home/pi/updateDroneponics.sh')
    os.system('sudo reboot')

    @blynk.handle_event("connect")
    def connect_handler():
        _log.info("Connected")
        blynk.virtual_write(250, "Connected")
    

    @blynk.handle_event("disconnect")
    def disconnect_handler():
        _log.info("Disconnected")
        blynk.virtual_write(250, "Disconnected")
  
    
    @timer.register(interval=30, run_once=False)
    def blynk_data():
         _log.info("Start of timer.register fx")
         blynk.set_property(systemLED, 'color', colours[1])
         blynk.virtual_write(250, "Updating")
         _log.debug("Going to get timestamp")
         now = datetime.now()
         blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
         if(bmex80 is not None):            
            _log.debug("bmex80 is not None so going to get openweather")
            openWeather.blynkOpenWeather(blynk)
            _log.info("Going to update BME sensor with openWeather sea level pressure")
            bme680.sea_level_pressure = openWeather.getPressure()
            

            _log.debug("Update blynk with BME data")
     #       for alarm in alarmList:
     #          alarm.test(blynk, "temperature", 1, bme680.temperature) 
            blynk.virtual_write(1, bmex80.temperature)
            if (parser.get('droneAir', 'BME680', fallback=False)=="True"): 
               blynk.virtual_write(2, bmex80.gas)
            else:
               blynk.virtual_write(2, None)
               blynk.set_property(2, 'color', colours['OFFLINE'])
            blynk.virtual_write(3, bmex80.humidity)
            blynk.virtual_write(4, bmex80.pressure)
            blynk.virtual_write(5, bmex80.altitude)
        
            _log.debug("find dew point")
            t = Temp(bmex80.temperature, 'c')
            blynk.virtual_write(11, dew_point(temperature=t, humidity=bmex80.humidity))

            _log.debug("set BME form display")
            drone.setBMEFormOnline(blynkObj=blynk, loggerObj=_log)     
         else:
            drone.setBMEFormOffline(blynkObj=blynk, loggerObj=_log)

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
            drone.setTSLFormOnline(blynkObj=blynk, loggerObj=_log)
         else:
            drone.setTSLFormOnline(blynkObj=blynk, loggerObj=_log)

         _log.debug("Now work on mhz19b sensor")
         mhz19b = mh_z19.read()  
         if mhz19b is not None:
             blynk.virtual_write(10, '{0:d}'.format(mhz19b['co2']))
             _log.info('CO2: {0:d}'.format(mhz19b['co2']))
             drone.setMHZFormOnline(blynkObj=blynk, loggerObj=_log)
             _log.info("blynkBridge BLYNK_AUTH = " + parser.get('blynkBridge', 'BLYNK_AUTH', fallback="Fallback"))
             if (parser.get('blynkBridge', 'BLYNK_AUTH', fallback=None) is not None):
                 _log.info("Send CO2 data via blynkBridge")
                 blynkBridge = blynklib.Blynk(parser.get('blynkBridge', 'BLYNK_AUTH'))
                 blynkBridge.run()
                 blynkBridge.virtual_write(parser.get('blynkBridge', 'CO2_VPIN', fallback=10), '{0:d}'.format(mhz19b['co2']))
                 _log.info("blynkBridge CO2 data sent")
         else:
             blynk.virtual_write(98, 'Unexpected error: mhz19b' + '\n')
             _log.error('Unexpected error: mhz19b')
             drone.setMHZFormOffline(blynkObj=blynk, loggerObj=_log)
         blynk.virtual_write(250, "Running")
         blynk.set_property(systemLED, 'color', colours[0])
         _log.debug("End of timer.register fx")
        
        
    blynk.run() #need to call here so you can update app outside main while loop    
    blynk.virtual_write(250, "Start-up")
    blynk.virtual_write(251, drone.gethostname())
    blynk.virtual_write(252, drone.get_ip())        
    blynk.virtual_write(98, "clr")
    if (parser.get('droneAir', 'I2C-0') == "True"):                
        _log.info("Posting I2C 0 devices to app")
        p = subprocess.Popen(['i2cdetect', '-y','0'],stdout=subprocess.PIPE,)
        #cmdout = str(p.communicate())        
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
    _log.debug("Just about to complete Booting")
    now = datetime.now()
    blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(systemLED, 255)
    drone.setFormOnline(blynkObj=blynk, loggerObj=_log, Msg="System now updated and restarted")
    blynk.virtual_write(255, 0)
    _log.info('Completed Boot')

try:        
    while True:
        blynk.run()
        timer.run()
        _log.debug("End of main while loop")
except: 
   _log.error("in main loop except")
   blynk.virtual_write(250, "Crashed")
   drone.setFormOffline(blynkObj=blynk, loggerObj=_log)
   if (parser.get('logging', 'logLevel', fallback=logging.DEBUG) =="CRITICAL"):
        os.system('sh /home/pi/updateDroneponics.sh')
        os.system('sudo reboot')
   else:
        _log.critical("Main Loop exception :- Set log evel to CRITICAL to auto reboot")
