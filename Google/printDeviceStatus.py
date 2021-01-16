from atlas_i2c import sensors
from atlas_i2c import commands
from atlas_i2c import atlas_i2c

class Cal(Command):
    """Get info about a device."""

    arguments: None = None
    name: str = "cal,?"
    processing_delay: int = 300

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"
    
    
    
sensor = sensors.Sensor("Temperature", 102)
sensor.connect()
response = sensor.query(Cal)

RTD = atlas_i2c.AtlasI2C(102)
DO =  atlas_i2c.AtlasI2C(97)
ORP = atlas_i2c.AtlasI2C(102)

device_list = [RTD,DO,ORP]


for device in device_list:
    response = dev.query("cal,?", processing_delay=1500)
    print("returned status_code = " + str(response.status_code))
    print(" data = " + str(response.data.decode("utf-8")))
    
    
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)

deviceName ={102: "Temp", 97: "DO", 98: "ORP"}
b =AtlasI2C()
devicesAttached = b.list_i2c_devices()
             
print("devicesAttached =" +str(devicesAttached))
for device in devicesAttached:
    d = AtlasI2C(device)
    calStatus = d.query("cal,?")         
    print(deviceName[device] + " returned " + calStatus)
    
