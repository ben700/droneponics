import sys
import os
sys.path.append('/home/pi/droneponics/droneAtlas/drone')
import datetime
import time
import drone
import board
import busio
import smbus 
import mh_z19
import adafruit_tsl2591
import adafruit_bme680
import adafruit_bme280
from meteocalc import Temp, dew_point

class SensorList:
  def __init__(self, deviceType="BME280"): #deviceType BME280 or BME680
    self.deviceType = deviceType
    
    tslI2C = None
    try:    
      tslI2C = busio.I2C(board.SCL, board.SDA)
      if not 0x29 in tslI2C.scan():
        tslI2C = busio.I2C(board.D1, board.D0)   
        if not 0x29 in tslI2C.scan():
          print("Didn't find TSL2591")
          tslI2C = None  
        else:
          print("Found TSL2591 on I2C-0")
      else:
        print("Found TSL2591 on I2C-1")
    except:
        print("Can't find I2C device 29 should be the Light sensor")
        tslI2C = None
        
    try:     
        # Initialize the sensor.
        if (tslI2C is not None):
            self.tsl = adafruit_tsl2591.TSL2591(tslI2C)
            # You can optionally change the gain and integration time:
            self.tsl.gain = adafruit_tsl2591.GAIN_LOW
            self.tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS
        else:
            self.tsl = None
    except:
        print("Failed to create object for Light sensor")
        self.tsl = None


    try:
        bmeI2C = busio.I2C(board.SCL, board.SDA)
        if not 0x77 in bmeI2C.scan():
            bmeI2C = busio.I2C(board.D1, board.D0)   
            if not 0x77 in bmeI2C.scan():
                print("Can't find I2C device 77 should be the BME280/680 sensor")
                blynk.virtual_write(250, "no BMEx80")
                bmeI2C = None      
            else:
                print("Found I2C device 77 should be the BME280/680 sensor on I2C-0")
        else:
            print("Found I2C device 77 should be the BME280/680 sensor on I2C-1")
    except:
        print("Can't find I2C device 77 should be the BME280/680 sensor")
        bmeI2C = None

    self.bme680 = None
    self.bme280 = None

    try:
        # Initialize the sensor.
        if (bmeI2C is not None):
            if (self.deviceType == "BME680"):
                print("Creating BME680 object for device 77 should be the BME680 sensor") 
         #      self.bmex80 = adafruit_bme680.Adafruit_BME680_I2C(bmeI2C)     
                self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(bmeI2C)
                print("Created BME680 object for device 77 should be the BME680 sensor") 
                try:
                    test = self.bme680.temperature
                    print("BME680 object for device 77 tested and working OK") 
                except:
                    self.bme680 = None
                    self.bme280 = None
                    print("Failed to test object for device 77 should be the BME680 sensor")
            else:
                print("Creating BME280 object for device 77 should be the BME280 sensor") 
                self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(bmeI2C)
                print("Created BME280 object for device 77 should be the BME280 sensor")
                test = self.bme280.temperature
                print("BME280 object for device 77 tested and working OK") 
        else:
            self.bme680 = None
            self.bme280 = None
    except:
        print("Failed to create and test object for device 77 should be the BME280/680 sensor")
        self.bme680 = None
        self.bme280 = None

  def payload(self, __payload):
    try:
      __payload["devicetime"] = time.time()
      if(self.bme680 is not None):
        __payload["sensorType"] = "bme680"
        __payload["voc"] = "{0:.2f}".format(self.bme680.gas)
        __payload["temperature"] = "{0:.1f}".format(self.bme680.temperature)
        __payload["humidity"] = "{0:.0f}".format(self.bme680.gas)
        __payload["pressure"] = "{0:.0f}".format(self.bme680.pressure)
        __payload["altitude"] = "{0:.0f}".format(self.bme680.altitude)
        t = Temp(self.bme680.temperature, 'c')
        dewPoint = dew_point(temperature=t, humidity=self.bme680.humidity)
        __payload["dewPoint"] = dewPoint
      elif(bme280 is not None):           
        print("payload for BME280")
        __payload["sensorType"] = "bme280"
        __payload["temperature"] = "{0:.4f}".format(self.bme280.temperature)
        __payload["humidity"] = "{0:.4f}".format(self.bme280.gas)
        __payload["pressure"] = "{0:.4f}".format(self.bme280.pressure)
        __payload["altitude"] = "{0:.4f}".format(self.bme280.altitude)
        t = Temp(self.bme280.temperature, 'c')
        dewPoint = dew_point(temperature=t, humidity=self.bme280.humidity)
        __payload["dewPoint"] = dewPoint
    except:
      pass
 
    try:
      if (self.tsl is not None):
        print("payload for tsl")
        __payload["lux"] = "{0:.0f}".format(self.tsl.lux)
        __payload["infrared"] = "{0:d}".format(self.tsl.infrared)
        __payload["visible"] = "{0:d}".format(self.tsl.visible)
        __payload["full_spectrum"] = "{0:d}".format(self.tsl.full_spectrum)
    except:
      pass

    try:
      mhz19b = mh_z19.read()  
      if mhz19b is not None:
        __payload["CO2"] = '{0:d}'.format(mhz19b['co2'])
    except:
      pass
    print("Completed payload")
