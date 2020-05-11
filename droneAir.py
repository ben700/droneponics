

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
parser.read('/home/pi/config.ini')

bootup = True

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)

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

    # Initialize the sensor.
    if (tslI2C is not None):
       try:
          tsl = adafruit_tsl2591.TSL2591(tslI2C)
          # You can optionally change the gain and integration time:
          tsl.gain = adafruit_tsl2591.GAIN_LOW
          tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS
       except:
           tsl = None
           print("Unexpected error: TSL2591. Paser was " + str(parser.get('droneAir', 'TSLI2C0', fallback=True)))
    else:
           tsl = None
     
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
            
    # Initialize the sensor.
    if (bmeI2C is not None):
       try:
           bme680 = adafruit_bme680.Adafruit_BME680_I2C(bmeI2C)
       except:
           bme680 = None
           _log.info("Unexpected error: bme680")
    else:
       bme680 = None
        
    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
    timer = blynktimer.Timer()
    
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        blynk.virtual_write(250, "User Reboot")
        drone.setFormOffline(blynkObj=blynk, loggerObj=_log, Msg="User Reboot")
        blynk.set_property(systemLED, 'color', colours['OFFLINE'])
        os.system('sh /home/pi/updateDroneponics.sh')
        os.system('sudo reboot')

    @timer.register(interval=10, run_once=False)
    def blynk_data():
        blynk.virtual_write(250, drone.gethostname())
        _log.info("Update Timer Run")
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
          
        if(bme680 is not None):
           _log.debug("going to update Blynk")
           openWeather.blynkOpenWeather(blynk)
           _log.debug("Going to read pressure")
           bme680.sea_level_pressure = openWeather.getPressure()
            

           _log.debug("update blynk BME")
     #      for alarm in alarmList:
     #         alarm.test(blynk, "temperature", 1, bme680.temperature) 
           blynk.virtual_write(1, bme680.temperature)
           blynk.virtual_write(2, bme680.gas)
           blynk.virtual_write(3, bme680.humidity)
           blynk.virtual_write(4, bme680.pressure)
           blynk.virtual_write(5, bme680.altitude)
        
           _log.debug("find dew point")
           t = Temp(bme680.temperature, 'c')
           blynk.virtual_write(11, dew_point(temperature=t, humidity=bme680.humidity))

           _log.debug("set BME form display")
           drone.setBMEFormOnline(blynkObj=blynk, loggerObj=_log)     
        else:
           drone.setBMEFormOffline(blynkObj=blynk, loggerObj=_log)

        _log.debug("Now work on TSL2591 sensor")
        if (tsl is not None):
           _log.info('Total light: {0:.2f}lux'.format(tsl.lux))
           _log.info('Infrared light: {0:d}'.format(tsl.infrared))
           _log.info('Visible light: {0:d}'.format(tsl.visible))
           _log.info('Full spectrum (IR + visible) light: {0:d}'.format(tsl.full_spectrum))
           blynk.virtual_write(6, str("{0:.2f}".format(tsl.lux))) 
           blynk.virtual_write(7, str("{0:d}".format(tsl.infrared)))
           blynk.virtual_write(8, ("{0:d}".format(tsl.visible)))
           blynk.virtual_write(9, ("{0:d}".format(tsl.full_spectrum)))
           drone.setTSLFormOnline(blynkObj=blynk, loggerObj=_log)
        else:
           drone.setTSLFormOnline(blynkObj=blynk, loggerObj=_log)

        mhz19b = mh_z19.read()  
        if mhz19b is not None:
            blynk.virtual_write(10, '{0:d}'.format(mhz19b['co2']))
            _log.info('CO2: {0:d}'.format(mhz19b['co2']))
            drone.setMHZFormOnline(blynkObj=blynk, loggerObj=_log)
        else:
            blynk.virtual_write(98, 'Unexpected error: mhz19b' + '\n')
            _log.info('Unexpected error: mhz19b')
            drone.setMHZFormOffline(blynkObj=blynk, loggerObj=_log)


    while True:
        blynk.run()
        if bootup :
           blynk.virtual_write(250, "Start-up")
           blynk.virtual_write(98, "clr")
           _log.info("Posting I2C 0 devices to app")
           p = subprocess.Popen(['i2cdetect', '-y','0'],stdout=subprocess.PIPE,)
           #cmdout = str(p.communicate())
           blynk.virtual_write(98, "I2C 0 devices"+'\n')
           for i in range(0,9):
                blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
           x=1
           for alarm in alarmList:
                alarm.display(blynk,x)
                x=x+1
           _log.info("Posting I2C 1 devices to app")
           blynk.virtual_write(98, "I2C 1 devices"+'\n')
           q = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
           #cmdout = str(p.communicate())
           for i in range(0,9):
               blynk.virtual_write(98, str(q.stdout.readline()) + '\n')
           bootup = False
           _log.debug("Just about to complete Booting")
           now = datetime.now()
           blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
           blynk.virtual_write(systemLED, 255)
           drone.setFormOnline(blynkObj=blynk, loggerObj=_log, Msg="System now updated and restarted")
           blynk.virtual_write(255, 0)
           blynk.virtual_write(251, drone.get_ip())
           _log.info('Just Booted')

        timer.run()
except: 
   _log.info("in main loop except")
   blynk.virtual_write(250, "Offline")
   drone.setFormOffline(blynkObj=blynk, loggerObj=_log)
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
