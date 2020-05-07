

# The ID and range of a sample spreadsheet.
colours = {1: '#FF0000', 0: '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101

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
import drone
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
            bmeI2C = None      
        else:
            _log.info("Found BME680 on I2C-0")
    else:
         _log.info("Found BME680 on I2C-1")
    # Initialize the sensor.
    if (bmeI2C is not None):
       try:
           bme680 = adafruit_bme680.Adafruit_BME680_I2C(bmeI2C)
           # change this to match the location's pressure (hPa) at sea level
           openWeatherAPI = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=53.801277&lon=-1.548567&exclude=hourly,daily&units=metric&appid=7ab0c16c9b00854f26df8a57435ad6ce")   
           openWeather = openWeatherAPI.json()
           bme680.sea_level_pressure = openWeather["current"]["pressure"]
       except:
           bme680 = None
           _log.info("Unexpected error: bme680")
    else:
       bme680 = None
        
    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
    timer = blynktimer.Timer()
    #blynk.run()
    #print(blynk.getProperty(98, 'colour'))
   
    def blynkOpenWeather(openWeather):
        openWeatherAPI = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=53.801277&lon=-1.548567&exclude=hourly,daily&units=metric&appid=7ab0c16c9b00854f26df8a57435ad6ce")   
        openWeather = openWeatherAPI.json()
        print("---------------------------------------------------")
        print(openWeather["current"]["weather"][0]["icon"])
        print(openWeather["current"]["dew_point"])
        print(openWeather["current"]["temp"])
        print(openWeather["current"]["pressure"])
        print(openWeather["current"]["humidity"])
        return
#https://api.openweathermap.org/data/2.5/onecall?lat=53.801277&lon=-1.548567&exclude=hourly,daily&units=metric&appid=7ab0c16c9b00854f26df8a57435ad6ce
 #  {"lat":53.8,
 #   "lon":-1.55,
 #   "timezone":"Europe/London",
 #   "current":{"dt":1588830963,
 #              "sunrise":1588825069,
 #              "sunset":1588880857,
#               "temp":278,
#               "feels_like":276.25,
#               "pressure":1023,
#               "humidity":90,
#               "dew_point":276.5,
#               "uvi":4.78,
#               "clouds":0,
#               "wind_speed":0.44,
#               "wind_deg":170,
#               "weather":[{"id":800,
#                           "main":"Clear",
#                           "description":"clear sky",
#                           "icon":"01d"}]}}
 
 
 
   
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        blynk.virtual_write(98, "User Reboot " + '\n')
        blynk.set_property(systemLED, 'color', colours['OFFLINE'])
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')

    @timer.register(interval=10, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
          
        if(bme680 is not None):
           openWeatherAPI = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=53.801277&lon=-1.548567&exclude=hourly,daily&units=metric&appid=7ab0c16c9b00854f26df8a57435ad6ce")   
           openWeather = openWeatherAPI.json()
           bme680.sea_level_pressure = openWeather["current"]["pressure"]
           _log.debug("calling blynkOpenWeather")        
           blynkOpenWeather(openWeather)
           _log.debug("returned from blynkOpenWeather")
            
           _log.info("Temperature: %0.1f C" % bme680.temperature)
           _log.info("Gas: %d ohm" % bme680.gas)
           _log.info("Humidity: %0.1f %%" % bme680.humidity)
           _log.info("Pressure: %0.3f hPa" % bme680.pressure)
           _log.info("Altitude = %0.2f meters" % bme680.altitude)

           blynk.virtual_write(1, bme680.temperature)
           blynk.virtual_write(2, bme680.gas)
           blynk.virtual_write(3, bme680.humidity)
           blynk.virtual_write(4, bme680.pressure)
           blynk.virtual_write(5, bme680.altitude)

           t = Temp(bme680.temperature, 'c')
           blynk.virtual_write(11, dew_point(temperature=t, humidity=bme680.humidity))

           drone.setBMEFormOnline(blynkObj=blynk, loggerObj=_log)     
        else:
           drone.setBMEFormOffline(blynkObj=blynk, loggerObj=_log)

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
           blynk.virtual_write(98, "clr")
           _log.info("Posting I2C 0 devices to app")
           p = subprocess.Popen(['i2cdetect', '-y','0'],stdout=subprocess.PIPE,)
           #cmdout = str(p.communicate())
           blynk.virtual_write(98, "I2C 0 devices"+'\n')
           for i in range(0,9):
                blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
              
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
           _log.info('Just Booted')

        timer.run()
except: 
   _log.info("in main loop except")
   drone.setFormOffline(blynkObj=blynk, loggerObj=_log)
   #os.system('sh /home/pi/updateDroneponics.sh')
   #os.system('sudo reboot')
