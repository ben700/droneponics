


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
              
    # Initialize the I2C bus.
    #if (parser.get('droneAir', 'TSLI2C0', fallback=True) == True):
        

    # Initialize the sensor.
    if (tslI2C is not None):
       try:
          tsl = adafruit_tsl2591.TSL2591(i2c0)
          # You can optionally change the gain and integration time:
          tsl.gain = adafruit_tsl2591.GAIN_LOW
          tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS
       except:
           tsl = None
           print("Unexpected error: TSL2591. Paser was " + str(parser.get('droneAir', 'TSLI2C0', fallback=True)))
    else:
           tsl = None
              
    # Initialize the sensor.
    try:
       i2c1 = busio.I2C(board.SCL, board.SDA)
       bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c1)
       # change this to match the location's pressure (hPa) at sea level
       bme680.sea_level_pressure = 1026
    except:
        bme680 = None
        print("Unexpected error: bme680")

    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
    timer = blynktimer.Timer()
    #blynk.run()
    APP_CONNECT_PRINT_MSG = '[APP_CONNECT_EVENT]'
    APP_DISCONNECT_PRINT_MSG = '[APP_DISCONNECT_EVENT]'
    CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
    DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'
    WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
    READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
    ALLOWED_COMMANDS_LIST = ['ls', 'lsusb', 'ip a', 'ip abc']
    TWEET_MSG = "New value='{}' on VPIN({})"


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
        
        mhz19b = mh_z19.read()    
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
          

        if(bme680 is not None):
                _log.info("\nTemperature: %0.1f C" % bme680.temperature)
                _log.info("Gas: %d ohm" % bme680.gas)
                _log.info("Humidity: %0.1f %%" % bme680.humidity)
                _log.info("Pressure: %0.3f hPa" % bme680.pressure)
                _log.info("Altitude = %0.2f meters" % bme680.altitude)
                blynk.virtual_write(1, bme680.temperature)
                blynk.virtual_write(2, bme680.gas)
                blynk.virtual_write(3, bme680.humidity)
                blynk.virtual_write(4, bme680.pressure)
                blynk.virtual_write(5, bme680.altitude)
 #               blynk.virtual_write(1, str("{0.1f}".format(bme680.temperature)))
#                blynk.virtual_write(2, str("{d}".format(bme680.gas)))
#                blynk.virtual_write(3, str("{0.1f}".format(bme680.humidity)))
#                blynk.virtual_write(4, str("{0.3f}".format(bme680.pressure)))
#                blynk.virtual_write(5, str("{0.2f}".format( bme680.altitude)))
                t = Temp(bme680.temperature, 'c')
                blynk.virtual_write(11, dew_point(temperature=t, humidity=bme680.humidity))
#                blynk.virtual_write(11, dew_point(temperature=t, humidity=bme680.humidity))
                blynk.set_property(1, 'color', colours['ONLINE'])
                blynk.set_property(2, 'color', colours['ONLINE'])
                blynk.set_property(3, 'color', colours['ONLINE'])
                blynk.set_property(4, 'color', colours['ONLINE'])
                blynk.set_property(5, 'color', colours['ONLINE'])
                blynk.set_property(11, 'color', colours['ONLINE'])
               
        else:
                blynk.set_property(1, 'color', colours['OFFLINE'])
                blynk.set_property(2, 'color', colours['OFFLINE'])
                blynk.set_property(3, 'color', colours['OFFLINE'])
                blynk.set_property(4, 'color', colours['OFFLINE'])
                blynk.set_property(5, 'color', colours['OFFLINE'])
                blynk.set_property(11, 'color', colours['OFFLINE'])

        if (tsl is not None):
           lux = tsl.lux
           _log.info('Total light: {0:.2f}lux'.format(lux))
           blynk.virtual_write(6, str("{0:.2f}".format(lux))) 
           blynk.set_property(6, 'color', colours['ONLINE'])#

           infrared = tsl.infrared
           _log.info('Infrared light: {0:d}'.format(infrared))
           blynk.virtual_write(7, str("{0:d}".format(infrared)))
           blynk.set_property(7, 'color', colours['ONLINE'])

           visible = tsl.visible
           _log.info('Visible light: {0:d}'.format(visible))
           blynk.virtual_write(8, ("{0:d}".format(visible)))
           blynk.set_property(8, 'color', colours['ONLINE'])

           full_spectrum = tsl.full_spectrum
           _log.info('Full spectrum (IR + visible) light: {0:d}'.format(full_spectrum))
           blynk.virtual_write(9, ("{0:d}".format(full_spectrum)))
           blynk.set_property(9, 'color', colours['ONLINE'])
        else:
           blynk.set_property(6, 'color', colours['OFFLINE'])
           blynk.set_property(7, 'color', colours['OFFLINE'])
           blynk.set_property(8, 'color', colours['OFFLINE'])
           blynk.set_property(9, 'color', colours['OFFLINE'])


        if mhz19b is not None:
            blynk.virtual_write(10, '{0:d}'.format(mhz19b['co2']))
            blynk.set_property(10, 'color', colours['ONLINE'])
            _log.info('CO2: {0:d}'.format(mhz19b['co2']))

        else:
            blynk.virtual_write(98, 'Unexpected error: mhz19b' + '\n')
            _log.info('Unexpected error: mhz19b')
            blynk.set_property(10, 'color', colours['OFFLINE'])

        blynk.virtual_write(98, "Completed Timer Function" + '\n') 



    while True:
        try:
           blynk.run()
           if bootup :
              p = subprocess.Popen(['i2cdetect', '-y','0'],stdout=subprocess.PIPE,)
              #cmdout = str(p.communicate())
              for i in range(0,9):
                   blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
              p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
              #cmdout = str(p.communicate())
              for i in range(0,9):
                   blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
              bootup = False
              now = datetime.now()
              blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
              blynk.virtual_write(98, "clr")
              blynk.virtual_write(systemLED, 255)
              blynk.set_property(systemLED, 'color', colours['ONLINE'])
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')

           timer.run()
        except:
           _log.info('Unexpected error')
           blynk.virtual_write(98, "System has main loop error" + '\n')
           blynk.set_property(systemLED, 'color', colours['OFFLINE'])
           blynk.set_property(1, 'color', colours['OFFLINE'])
           blynk.set_property(2, 'color', colours['OFFLINE'])
           blynk.set_property(3, 'color', colours['OFFLINE'])
           blynk.set_property(4, 'color', colours['OFFLINE'])
           blynk.set_property(5, 'color', colours['OFFLINE'])
           blynk.set_property(6, 'color', colours['OFFLINE'])
           blynk.set_property(7, 'color', colours['OFFLINE'])
           blynk.set_property(10, 'color', colours['OFFLINE'])
           os.system('sh /home/pi/updateDroneponics.sh')
           os.system('sudo reboot') 
  
  
except:
   _log.info('Unexpected error')
   blynkErr = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
   blynkErr.run()
   blynkErr.virtual_write(98, "System has error" + '\n')
   blynkErr.set_property(systemLED, 'color', colours['OFFLINE'])
   blynkErr.set_property(1, 'color', colours['OFFLINE'])
   blynkErr.set_property(2, 'color', colours['OFFLINE'])
   blynkErr.set_property(3, 'color', colours['OFFLINE'])
   blynkErr.set_property(4, 'color', colours['OFFLINE'])
   blynkErr.set_property(5, 'color', colours['OFFLINE'])
   blynkErr.set_property(6, 'color', colours['OFFLINE'])
   blynkErr.set_property(7, 'color', colours['OFFLINE'])
   blynkErr.set_property(10, 'color', colours['OFFLINE'])
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
