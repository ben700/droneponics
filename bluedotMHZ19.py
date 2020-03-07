##!/usr/bin/env python3 /etc/init.d/getAndLogBMEAndCO2Data.py
### BEGIN INIT INFO
# Provides:          getAndLogBMEAndCO2Data.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO


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
import BlynkLib
from BlynkTimer import BlynkTimer
from datetime import datetime
import adafruit_tsl2591
import sys
import os
        

# Initialize the I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the sensor.
try:
   tsl = adafruit_tsl2591.TSL2591(i2c)
   # You can optionally change the gain and integration time:
   tsl.gain = adafruit_tsl2591.GAIN_LOW
   tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS
except:
    blynk.virtual_write(100, "Unexpected error: TSL2591")
    tsl = None
    print("Unexpected error: TSL2591")
    
    
# The ID and range of a sample spreadsheet.
#BLYNK_AUTH = '4IfX_hzDREonPi_PIDQrETikxc0-XpqI' #envLogger4
#BLYNK_AUTH = 'Hd6GWt2tJ2Gzun2VA-NxsTL_umv1wPWm' #envLogger3
#BLYNK_AUTH = 'FnSZls3WUdCbWmDJvfnjz3f83Sm70HqI' #envLogger2
#BLYNK_AUTH = 'ZDy8p4aFPCKGwQhafv4jwUT6TpCY9CyP' #envLogger1

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()

now = datetime.now()
blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
    
@blynk.on("V255")
def buttonV255Pressed(value):
    os.system('sudo reboot')

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
        
# Will Print Every 10 Seconds
def blynk_data():
    temperature,pressure,humidity = readBME280All()
    mhz19b = mh_z19.read()    
    now = datetime.now()
 
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    print('Temperature: {0:.2f} C'.format(temperature))
    blynk.virtual_write(1, str("{0:.2f}".format(temperature)))
    print('Pressure: {0:.0f}'.format(pressure))
    blynk.virtual_write(2, str("{0:.2f}".format(pressure)))
    print('Humidity: {0:.2f}'.format(humidity))
    blynk.virtual_write(3, str("{0:.2f}".format(humidity)))
    
    if (tsl is not null):
       lux = tsl.lux
       print('Total light: {0:.2f}lux'.format(lux))
       blynk.virtual_write(4, str("{0:.2f}".format(lux)))           
 
       infrared = tsl.infrared
       print('Infrared light: {0:d}'.format(infrared))
       blynk.virtual_write(5, str("{0:d}".format(infrared)))

       visible = tsl.visible
       print('Visible light: {0:d}'.format(visible))
       blynk.virtual_write(6, ("{0:d}".format(visible)))
     
       full_spectrum = tsl.full_spectrum
       print('Full spectrum (IR + visible) light: {0:d}'.format(full_spectrum))
       blynk.virtual_write(7, ("{0:d}".format(full_spectrum)))
    
    if mhz19b is not None:
        blynk.virtual_write(10, '{0:d}'.format(mhz19b['co2']))
        print('CO2: {0:d}'.format(mhz19b['co2']))
        
    else:
        blynk.virtual_write(100, 'Unexpected error: mhz19b')
        print('Unexpected error: mhz19b')
    

# Add Timers
timer.set_interval(10, blynk_data)


while True:
    try:
       blynk.run()
       timer.run()
    except:
        os.system('sudo reboot')

