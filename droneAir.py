


# The ID and range of a sample spreadsheet.
colours = {1: '#FF0000', 0: '#00FF00', 'OFFLINE': '#0000FF'}
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
import sys
import os
from configparser import ConfigParser

parser = ConfigParser()
parser.read('/home/pi/config.ini')

class Counter:
     cycle = 0

bootup = True
T_CRI_VALUE = 10.5  # 16.5°C
T_CRI_MSG = 'Low TEMP!!!'
T_CRI_COLOR = '#c0392b'

T_COLOR = '#f5b041'
H_COLOR = '#85c1e9'
P_COLOR = '#a2d9ce'

TL_COLOR = '#cea2d9'
IR_COLOR = '#a2add9'
VL_COLOR = '#d9cea2'
FS_COLOR = '#add9a2'

CO2_COLOR = '#d9b3a2'

ERR_COLOR = '#444444'

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)


try:


    # Initialize the I2C bus.
    if (parser.get('droneAir', 'TSLI2C0', fallback=True) == True):
        i2c0 = busio.I2C(board.SCL, board.SDA)
    else:
        print("i2c-0")    
        i2c0 = busio.I2C(board.D1, board.D0)

    # Initialize the sensor.
    try:
       tsl = adafruit_tsl2591.TSL2591(i2c0)
       # You can optionally change the gain and integration time:
       tsl.gain = adafruit_tsl2591.GAIN_LOW
       tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS
    except:
        tsl = None
        print("Unexpected error: TSL2591. Paser was " + str(parser.get('droneAir', 'TSLI2C0', fallback=True)))


    # Initialize the sensor.
    try:
       i2c1 = busio.I2C(board.SCL, board.SDA)
       bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
       # change this to match the location's pressure (hPa) at sea level
       bme680.sea_level_pressure = 1013.25
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


    @blynk.handle_event("write V255")
    def buttonV255Pressed(value):
        blynk.virtual_write(98, "User Reboot " + '\n')
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')




    @timer.register(interval=10, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        Counter.cycle += 1
        
        mhz19b = mh_z19.read()    
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))

        _log.info("\nTemperature: %0.1f C" % bme680.temperature)
        _log.info("Gas: %d ohm" % bme680.gas)
        _log.info("Humidity: %0.1f %%" % bme680.humidity)
        _log.info("Pressure: %0.3f hPa" % bme680.pressure)
        _log.info("Altitude = %0.2f meters" % bme680.altitude)

        
        blynk.virtual_write(1, str("{0.1f}".format(bme680.temperature)))
        blynk.virtual_write(2, str("{d}".format(bme680.gas)))
        blynk.virtual_write(3, str("{0.1f}".format(bme680.humidity)))
        blynk.virtual_write(4, str("{0.3f}".format(bme680.pressure)))
        blynk.virtual_write(5, str("{0.2f}".format( bme680.altitude)))


        if (tsl is not None):
           lux = tsl.lux
           _log.info('Total light: {0:.2f}lux'.format(lux))
           blynk.virtual_write(4, str("{0:.2f}".format(lux))) 
           blynk.set_property(4, 'color', TL_COLOR)


           infrared = tsl.infrared
           _log.info('Infrared light: {0:d}'.format(infrared))
           blynk.virtual_write(5, str("{0:d}".format(infrared)))
           blynk.set_property(4, 'color', IR_COLOR)

           visible = tsl.visible
           _log.info('Visible light: {0:d}'.format(visible))
           blynk.virtual_write(6, ("{0:d}".format(visible)))
           blynk.set_property(4, 'color', VL_COLOR)

           full_spectrum = tsl.full_spectrum
           _log.info('Full spectrum (IR + visible) light: {0:d}'.format(full_spectrum))
           blynk.virtual_write(7, ("{0:d}".format(full_spectrum)))
           blynk.set_property(4, 'color', FS_COLOR)
        else:
           blynk.set_property(4, 'color', ERR_COLOR)
           blynk.set_property(5, 'color', ERR_COLOR)
           blynk.set_property(6, 'color', ERR_COLOR)
           blynk.set_property(7, 'color', ERR_COLOR)


        if mhz19b is not None:
            blynk.virtual_write(10, '{0:d}'.format(mhz19b['co2']))
            blynk.set_property(10, 'color', CO2_COLOR)
            _log.info('CO2: {0:d}'.format(mhz19b['co2']))

        else:
            blynk.virtual_write(98, 'Unexpected error: mhz19b' + '\n')
            _log.info('Unexpected error: mhz19b')
            blynk.set_property(10, 'color', ERR_COLOR)

        blynk.virtual_write(98, "Completed Timer Function" + '\n') 



    while True:
        try:
           blynk.run()
           if bootup :
              bootup = False
              now = datetime.now()
              blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
              blynk.virtual_write(98, "clr")
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')

           timer.run()
        except:
           _log.info('Unexpected error')
           blynk.virtual_write(98, "System has main loop error" + '\n')
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
