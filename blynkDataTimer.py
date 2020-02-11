#!/usr/bin/python
# -*- coding: utf-8 -*-
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import time 
import smbus
import sys
import time
import BlynkLib
from BlynkTimer import BlynkTimer
from python_tsl2591 import tsl2591
import board
import busio
from ctypes import *

#BLYNK_AUTH = 'g9MjyM6-6erTomtN9OFUXqS5dafRHz0D' # black
BLYNK_AUTH = '5ixcYmoewpFZC5UT-GH5bSMKCSA0eDoF' #black Gloss
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/gmail.send']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1iXetyC5Tqg4kvSs-bFt5BiAsYL5_0O3R-XNEmSUJsLs'
RANGE_NAME = 'cBME280!A:E'


# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()

DEVICE = 0x77 # Default device I2C address


bus = smbus.SMBus(0) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
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


class Chirp(object):
    """Chirp soil moisture sensor with temperature and light sensors.
    Attributes:
        address (int): I2C address
        busy_sleep (float): Sleep time in seconds while waiting for a new
                            measurement. Default: 0.01 second
        light (int): Light measurement. False if no measurement taken.
        light_timestamp (datetime): Timestamp for light measurement.
        max_moist (int): Calibrated maximum value for moisture, required for moist_percent
        min_moist (int): Calibrated Minimum value for moisture, required for moist_percent
        moist (int): Moisture measurement. False if no measurement taken.
        moist_timestamp (datetime): Timestamp for moist measurement
        read_light (bool): Set to True to enable light measurement, else False.
        read_moist (bool): Set to True to enable moisture measurement, else False.
        read_temp (bool): Set to True to enable temp measurement, else False.
        temp (float): Temperature measurement. False if no measurement taken.
        temp_offset (float): Offset for calibrating temperature.
        temp_scale (str): Temperature scale to return. Valid: 'celsius', 'farenheit' or 'kelvin'
        temp_timestamp (datetime): Timestamp for temp measurement.
    """
    def __init__(self, bus=1, address=0x20, min_moist=False, max_moist=False,
                 temp_scale='celsius', temp_offset=0, read_temp=True,
                 read_moist=True, read_light=True):
        """Chir soil moisture sensor.
        Args:
            bus (int, optional): I2C bus. Default: 1
            address (int, optional): I2C address. Default: 0x20
            min_moist (bool, optional): Set to calibrated value to enable moist_percent
            max_moist (bool, optional): Set to calibrated value to enable moist_percent
            temp_scale (str, optional): Temperature scale to use. Default: 'celsius'
                                        Options: 'celsius', 'farenheit', 'kelvin'
            temp_offset (int, optional): Offset for calibrating temperature.
            read_temp (bool, optional): Enable or disable temp measurements.
                                        Default: True
            read_moist (bool, optional): Enable or disable moisture measurements.
                                         Default: True
            read_light (bool, optional): Enable or disable light measurements.
                                         Default: True
        """
        self.bus_num = bus
        self.bus = smbus.SMBus(bus)
#        self.busy_sleep = 0.01
        self.busy_sleep = 3
        self.address = address
        self.min_moist = min_moist
        self.max_moist = max_moist
        self.temp_scale = temp_scale
        self.temp_offset = temp_offset
        self.read_temp = read_temp
        self.read_moist = read_moist
        self.read_light = read_light
        self.temp = False
        self.moist = False
        self.light = False
        self.temp_timestamp = datetime
        self.moist_timestamp = datetime
        self.light_timestamp = datetime

        # Register values
        self._GET_CAPACITANCE = 0x00  # (r) 2 bytes
        self._SET_ADDRESS = 0x01      # (w) 1
        self._GET_ADDRESS = 0x02      # (r) 1
        self._MEASURE_LIGHT = 0x03    # (w) 0
        self._GET_LIGHT = 0x04        # (r) 2
        self._GET_TEMPERATURE = 0x05  # (r) 2
        self._RESET = 0x06            # (w) 0
        self._GET_VERSION = 0x07      # (r) 1
        self._SLEEP = 0x08            # (w) 0
        self._GET_BUSY = 0x09         # (r) 1

    def trigger(self):
        """Triggers measurements on the activated sensors
        """
        if self.read_temp is True:
            self.temp = self._read_temp()
        if self.read_moist is True:
            self.moist = self._read_moist()
        if self.read_light is True:
            self.light = self._read_light()

    def get_reg(self, reg):
        """Read 2 bytes from register
        Args:
            reg (int): Register number
        Returns:
            TYPE: 2 bytes
        """
        val = self.bus.read_word_data(self.address, reg)
        # return swapped bytes (they come in wrong order)
        return (val >> 8) + ((val & 0xFF) << 8)

    @property
    def version(self):
        """Get firmware version for the sensor.
        Returns:
            int: sensor firmware version
        """
        return self.bus.read_byte_data(self.address, self._GET_VERSION)

    @property
    def busy(self):
        """Check if sensor is busy, returns True if busy, else False
        Returns:
            bool: true if busy taking measurements, else False
        """
        busy = self.bus.read_byte_data(self.address, self._GET_BUSY)

        if busy == 1:
            return True
        else:
            return False

    def reset(self):
        """Reset sensor
        """
        self.bus.write_byte(self.address, self._RESET)

    def sleep(self):
        """Enter deep sleep mode
        """
        self.bus.write_byte(self.address, self._SLEEP)

    def wake_up(self, wake_time=1):
        """Wakes up the sensor from deep sleep mode
        Sends a command (get firmware version) to the sensor in deep sleep mode
        to wake it up. The command fails, but it triggers the sensor to wake up
        We then wait for one second for the sensor to wake up. Wake up time can
        be adjusted. Below one second is not recommended, since it usually
        fails to retrieve the first measurement(s) if it's lower than that.
        Args:
            wake_time (int, float, optional): Time in seconds for sensor to wake up.
        """
        self.wake_time = wake_time

        try:
            self.bus.read_byte_data(self.address, self._GET_VERSION)
        except OSError:
            pass
        finally:
            time.sleep(self.wake_time)

    @property
    def sensor_address(self):
        """Read I2C address from the sensor
        Returns:
            int: I2C address
        """
        return self.bus.read_byte_data(self.address, self._GET_ADDRESS)

    @sensor_address.setter
    def sensor_address(self, new_addr):
        """Set a new I2C address for the sensor
        Args:
            new_addr (int): New I2C address. 3-119 or 0x03-0x77
        Raises:
            ValueError: If new_addr is not within required range.
        """
        if isinstance(new_addr, int) and (new_addr >= 3 and new_addr <= 119):
            self.bus.write_byte_data(self.address, 1, new_addr)
            self.reset()
            self.address = new_addr
        else:
            raise ValueError('I2C address must be between 3-119 or 0x03-0x77.')

    @property
    def moist_percent(self):
        """Get moisture in percent.
        Requires calibrated min_moist and max_moist values.
        Returns:
            int: Moisture in percent
        Raises:
            ValueError: If min_moist and max_moist are not defined.
        """
        moisture = self.moist
        return self.moist_to_percent(moisture)

    def moist_to_percent(self, moisture):
        """ Convert a moisture capacitance value to percent using a calibrated
        range for the sensor. Requires calibrated min_moist and max_moist
        values. Useful when converting values not directly from the sensor,
        ie from a database.
        Args:
            moisture (int): The capitance/moisture value recieved from the sensor.
        Returns:
            int: Moisture in percent
        Raises:
            ValueError: If min_moist and max_moist are not defined.
        """
        if (self.min_moist or self.max_moist) is False:
            raise ValueError('min_moist and max_moist must be defined.')
        else:
            return round((((moisture - self.min_moist) /
                           (self.max_moist - self.min_moist)) * 100), 1)

    def _read_moist(self):
        """Read soil moisture (capacitance) from the sensor
        Returns:
            int: Soil moisture
        """
        # This returns last reading, and triggers a new. Discard old value.
        measurement = self.get_reg(self._GET_CAPACITANCE)

        # Wait for sensor to finish measurement
        while self.busy:
            time.sleep(self.busy_sleep)
        self.moist_timestamp = datetime.now()

        # Retrieve the measurement just triggered.
        measurement = self.get_reg(self._GET_CAPACITANCE)
        return measurement

    def _read_temp(self):
        """To read temperature, read 2 bytes from register 5. Returns degrees
        in celsius with one decimal. Adjusted for temperature offset
        Returns:
            float: Temperature in selected scale (temp_scale)
        Raises:
            ValueError: If temp_scale is not properly defined.
        """
        # This returns last reading, and triggers a new. Discard old value.
        measurement = self.get_reg(self._GET_TEMPERATURE)

        # Wait for sensor to finish measurement
        while self.busy:
            time.sleep(self.busy_sleep)
        self.temp_timestamp = datetime.now()

        # Retrieve the measurement just triggered.
        measurement = self.get_reg(self._GET_TEMPERATURE)

        # The chirp sensor returns an integer. But the return measurement is
        # actually a float with one decimal. Needs to be converted to float by
        # dividing by ten. And adjusted for temperature offset (if used).
        celsius = round(((measurement / 10) + self.temp_offset), 1)

        # Check which temperature scale to return the measurement in.
        if self.temp_scale == 'celsius':
            return celsius
        elif self.temp_scale == 'farenheit':
            # °F = (°C × 9/5) + 32
            farenheit = (celsius * 9 / 5) + 32
            return farenheit
        elif self.temp_scale == 'kelvin':
            # K = °C + 273.15
            kelvin = celsius + 273.15
            return kelvin
        else:
            raise ValueError(
                '{} is not a valid temperature scale. Only celsius, farenheit \
                and kelvin are supported.'.format(self.temp_scale))

    def _read_light(self):
        """ Measure light
        Returns:
            int: Light measurement, 0 - 65535 (0 is bright, 65535 is dark)
        """
        # Trigger a measurement
        self.bus.write_byte(self.address, self._MEASURE_LIGHT)

        # Wait for sensor to finish measurement. Takes longer in low light.
        while self.busy:
            time.sleep(self.busy_sleep)
        self.light_timestamp = datetime.now()
        measurement = self.get_reg(self._GET_LIGHT)
        return measurement

    def __repr__(self):
        """Summary
        Returns:
            str: repr
        """
        return '<Chirp sensor on bus {:d}, i2c addres {:d}>'.format(
            self.bus_num, self.address)


def updateGoogle(Temperature, Pressure, Humidity, full, lux, ir):
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    values = [[str(datetime.now()), Temperature, Pressure, Humidity, full, lux, ir]]
    body = {'values' : values }
    result = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                                 valueInputOption='USER_ENTERED', body=body).execute() 
    

addr=0x20
min_moist = 157
max_moist = 527
highest_measurement = False
lowest_measurement = False
# Initialize the sensor.
chirp = Chirp(address=addr,
            read_moist=True,
            read_temp=True,
            read_light=True,
            min_moist=min_moist,
            max_moist=max_moist,
            temp_scale='celsius',
            temp_offset=0)    
scale_sign = '°C'

tsl = tsl2591(0)  # initialize
    # full, ir = tsl.get_full_luminosity()  # Read raw values (full spectrum and infared spectrum).
    # lux = tsl.calculate_lux(full, ir)  # Convert raw values to Lux.

    
# Will Print Every 5 Seconds
def blynk_data():
    chirp.trigger()
    temperature,pressure,humidity = readBME280All()
    tslData = tsl.get_current()
    blynk.virtual_write(0, chirp.moist)
    blynk.virtual_write(1, chirp.moist_percent)
    blynk.virtual_write(2, chirp.temp)
    blynk.virtual_write(3, chirp.light)
    blynk.virtual_write(4, temperature)
    blynk.virtual_write(5, pressure)
    blynk.virtual_write(6, humidity)
    blynk.virtual_write(7, tslData['full'])
    blynk.virtual_write(8, tslData['lux'])
    blynk.virtual_write(9, tslData['ir'])
  

    #updateGoogle(str("{0:.2f}".format(temperature)),
    #    str("{0:.2f}".format(pressure)),
    #    str("{0:.2f}".format(humidity)),
      #  str("{0:.2f}".format(tslData['full'])),
        #str("{0:.2f}".format(tslData['lux'])),           
        #str("{0:.2f}".format(tslData['ir'])))

# Add Timers
timer.set_interval(10, blynk_data)


while True:
    blynk.run()
    timer.run()