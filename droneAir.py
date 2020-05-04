


# The ID and range of a sample spreadsheet.
colours = {1: '#FF0000', 0: '#00FF00', 'OFFLINE': '#0000FF'}



from python_tsl2591 import tsl2591
import datetime
import time
import shlex, requests
import board
import busio
import smbus 
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte
import mh_z19
import blynklib
import blynktimer
import logging
from datetime import datetime
import adafruit_tsl2591
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
        i2c = busio.I2C(board.SCL, board.SDA)
    else:
        print("i2c-0")    
        i2c = busio.I2C(board.P1, board.P0)

    # Initialize the sensor.
    try:
       tsl = adafruit_tsl2591.TSL2591(i2c)
       # You can optionally change the gain and integration time:
       tsl.gain = adafruit_tsl2591.GAIN_LOW
       tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS
    except:
        tsl = None
        print("Unexpected error: TSL2591. Paser was " + str(parser.get('droneAir', 'TSLI2C0', fallback=True)))



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


    DEVICE = 0x77 # Default device I2C address

    bus = smbus.SMBus(1) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
                         # Rev 1 Pi uses bus 0

    def getShort(data, index):
      # return two bytes from data as a signed 16-bit value
      return c_short((data[index+1] << 8) + data[index]).value

    def getUShort(data, index):
      # return two bytes from data as an unsigned 16-bit value
      return (data[index+1] << 8) + data[index]

    def getChar(data,index):
      # return one byte from data as a signed char
      result = data[index]
      if result > 127:
        result -= 256
      return result

    def getUChar(data,index):
      # return one byte from data as an unsigned char
      result =  data[index] & 0xFF
      return result

    def readBME280ID(addr=DEVICE):
      # Chip ID Register Address
      REG_ID     = 0xD0
      (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
      return (chip_id, chip_version)

    def readBME280All(addr=DEVICE):
      # Register Addresses
      REG_DATA = 0xF7
      REG_CONTROL = 0xF4
      REG_CONFIG  = 0xF5

      REG_CONTROL_HUM = 0xF2
      REG_HUM_MSB = 0xFD
      REG_HUM_LSB = 0xFE

      # Oversample setting - page 27
      OVERSAMPLE_TEMP = 2
      OVERSAMPLE_PRES = 2
      MODE = 1

      # Oversample setting for humidity register - page 26
      OVERSAMPLE_HUM = 2
      bus.write_byte_data(addr, REG_CONTROL_HUM, OVERSAMPLE_HUM)

      control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
      bus.write_byte_data(addr, REG_CONTROL, control)

      # Read blocks of calibration data from EEPROM
      # See Page 22 data sheet
      cal1 = bus.read_i2c_block_data(addr, 0x88, 24)
      cal2 = bus.read_i2c_block_data(addr, 0xA1, 1)
      cal3 = bus.read_i2c_block_data(addr, 0xE1, 7)

      # Convert byte data to word values
      dig_T1 = getUShort(cal1, 0)
      dig_T2 = getShort(cal1, 2)
      dig_T3 = getShort(cal1, 4)

      dig_P1 = getUShort(cal1, 6)
      dig_P2 = getShort(cal1, 8)
      dig_P3 = getShort(cal1, 10)
      dig_P4 = getShort(cal1, 12)
      dig_P5 = getShort(cal1, 14)
      dig_P6 = getShort(cal1, 16)
      dig_P7 = getShort(cal1, 18)
      dig_P8 = getShort(cal1, 20)
      dig_P9 = getShort(cal1, 22)

      dig_H1 = getUChar(cal2, 0)
      dig_H2 = getShort(cal3, 0)
      dig_H3 = getUChar(cal3, 2)

      dig_H4 = getChar(cal3, 3)
      dig_H4 = (dig_H4 << 24) >> 20
      dig_H4 = dig_H4 | (getChar(cal3, 4) & 0x0F)

      dig_H5 = getChar(cal3, 5)
      dig_H5 = (dig_H5 << 24) >> 20
      dig_H5 = dig_H5 | (getUChar(cal3, 4) >> 4 & 0x0F)

      dig_H6 = getChar(cal3, 6)

      # Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
      wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM)+0.575)
      time.sleep(wait_time/1000)  # Wait the required time  

      # Read temperature/pressure/humidity
      data = bus.read_i2c_block_data(addr, REG_DATA, 8)
      pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
      temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
      hum_raw = (data[6] << 8) | data[7]

      #Refine temperature
      var1 = ((((temp_raw>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
      var2 = (((((temp_raw>>4) - (dig_T1)) * ((temp_raw>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
      t_fine = var1+var2
      temperature = float(((t_fine * 5) + 128) >> 8);

      # Refine pressure and adjust for temperature
      var1 = t_fine / 2.0 - 64000.0
      var2 = var1 * var1 * dig_P6 / 32768.0
      var2 = var2 + var1 * dig_P5 * 2.0
      var2 = var2 / 4.0 + dig_P4 * 65536.0
      var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
      var1 = (1.0 + var1 / 32768.0) * dig_P1
      if var1 == 0:
        pressure=0
      else:
        pressure = 1048576.0 - pres_raw
        pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
        var1 = dig_P9 * pressure * pressure / 2147483648.0
        var2 = pressure * dig_P8 / 32768.0
        pressure = pressure + (var1 + var2 + dig_P7) / 16.0

      # Refine humidity
      humidity = t_fine - 76800.0
      humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
      humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
      if humidity > 100:
        humidity = 100
      elif humidity < 0:
        humidity = 0

      return temperature/100.0,pressure/100.0,humidity

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
        temperature,pressure,humidity = readBME280All()
        mhz19b = mh_z19.read()    
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))

        if not all([temperature,pressure,humidity]):
           blynk.set_property(1, 'color', ERR_COLOR)
           blynk.set_property(2, 'color', ERR_COLOR)
           blynk.set_property(3, 'color', ERR_COLOR)



        _log.info('Temperature: {0:.2f} C'.format(temperature))
        blynk.virtual_write(1, str("{0:.2f}".format(temperature)))

        if temperature <= T_CRI_VALUE:
           blynk.set_property(1, 'color', T_CRI_COLOR)
           # send notifications not each time but once a minute (6*10 sec)
           if Counter.cycle % 6 == 0:
              blynk.notify(T_CRI_MSG)
              Counter.cycle = 0
        else:
           blynk.set_property(1, 'color', T_COLOR)


        _log.info('Pressure: {0:.0f}'.format(pressure))
        blynk.virtual_write(2, str("{0:.2f}".format(pressure)))
        blynk.set_property(2, 'color', P_COLOR)

        _log.info('Humidity: {0:.2f}'.format(humidity))
        blynk.virtual_write(3, str("{0:.2f}".format(humidity)))
        blynk.set_property(3, 'color', H_COLOR)

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
