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

class SensorList:
  def __init__(self, deviceType="BME280"): #deviceType BME280 or BME680
    self.sensorlist = []
    self.deviceType = deviceType
    try:
        RTD = Sensor(102, "Temperature", "temperature")
        EC = Sensor(100, "EC", "conductivity", "totalDissolvedSolids", "salinity", "specificGravity")
        PH = Sensor(99, "pH", "PH")
        DO = Sensor(97, "Dissolved Oxygen", "DO", "saturation")
        ORP = Sensor(98, "Oxidation Reduction Potential", "oxidationReductionPotential")
        CO2 = Sensor(105, "CO2", "CO2", "temperature")
        HUM = Sensor(111, "Humitity", "humidity", "temperature", "dewPoint")
    except:   
        print("Except creating list")
    devList = [RTD,  EC, PH, DO, ORP, CO2, HUM]
    i=0
    for device in devList:
      try:
        print("Testing : Is the sensor "+device.name+" connected!")
        if (device.connected()):
          self.sensorlist.append(device)
          print("Success : " + device.name + " is connected")          
      except:
          print("No : Sensor" + device.name + " not connected")
        
    if(len(self.sensorlist) == 0):
      print("Failed : No sensors not connected!")
    else:  
      print("Success : " + str(len(self.sensorlist)) + " sensors connected.")
    
  def payload(self, _payload):
    for sensor in self.sensorlist:
      sensor.payload(_payload);
    return _payload
    
    
    

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
       tsl = adafruit_tsl2591.TSL2591(tslI2C)
       # You can optionally change the gain and integration time:
       tsl.gain = adafruit_tsl2591.GAIN_LOW
       tsl.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS
    else:
       tsl = None
except:
    print("Failed to create object for Light sensor")
    tsl = None


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

bme680 = None
bme280 = None














try:
    # Initialize the sensor.
    if (bmeI2C is not None):
        if (deviceType == "BME680"):
            print("Creating BME680 object for device 77 should be the BME680 sensor") 
     #      bmex80 = adafruit_bme680.Adafruit_BME680_I2C(bmeI2C)     
            bme680 = adafruit_bme680.Adafruit_BME680_I2C(bmeI2C)
            print("Created BME680 object for device 77 should be the BME680 sensor") 
            try:
                test = bme680.temperature
                print("BME680 object for device 77 tested and working OK") 
            except:
                bme680 = None
                bme280 = None
                print("Failed to test object for device 77 should be the BME680 sensor")
        else:
            print("Creating BME280 object for device 77 should be the BME280 sensor") 
            bme280 = adafruit_bme280.Adafruit_BME280_I2C(bmeI2C)
            print("Created BME280 object for device 77 should be the BME280 sensor")
            test = bme280.temperature
            print("BME280 object for device 77 tested and working OK") 
    else:
       bme680 = None
       bme280 = None
except:
    print("Failed to create and test object for device 77 should be the BME280/680 sensor")
    bme680 = None
    bme280 = None

    
    payload = {}
    payload["devicetime"] = time.time()
    if(bme680 is not None):            
        payload["sensorType"] = "bme680"
        payload["voc"] = "{0:.4f}".format(bme680.gas)
        payload["temperature"] = "{0:.4f}".format(bme680.temperature)
        payload["humidity"] = "{0:.4f}".format(bme680.gas)
        payload["pressure"] = "{0:.4f}".format(bme680.pressure)
        payload["altitude"] = "{0:.4f}".format(bme680.altitude)
        t = Temp(bme680.temperature, 'c')
        dewPoint = dew_point(temperature=t, humidity=bme680.humidity)
        payload["dewPoint"] = dewPoint
    elif(bme280 is not None):           
        payload["sensorType"] = "bme280"
        payload["temperature"] = "{0:.4f}".format(bme280.temperature)
        payload["humidity"] = "{0:.4f}".format(bme280.gas)
        payload["pressure"] = "{0:.4f}".format(bme280.pressure)
        payload["altitude"] = "{0:.4f}".format(bme280.altitude)
        t = Temp(bme280.temperature, 'c')
        dewPoint = dew_point(temperature=t, humidity=bme280.humidity)
        payload["dewPoint"] = dewPoint
   
    payload = drone.dronePayload(_log)
    if (tsl is not None):
        payload["lux"] = "{0:.0f}".format(tsl.lux)
        payload["infrared"] = "{0:d}".format(tsl.infrared)
        payload["visible"] = "{0:d}".format(tsl.visible)
        payload["full_spectrum"] = "{0:d}".format(tsl.full_spectrum)
  
    mhz19b = mh_z19.read()  
    if mhz19b is not None:
        payload["CO2"] = '{0:d}'.format(mhz19b['co2'])
  
