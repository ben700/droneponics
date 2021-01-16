from atlas_i2c import sensors
from atlas_i2c import commands
from atlas_i2c import atlas_i2c


RTD = sensors.Sensor("Temperature", 102)
DO =  sensors.Sensor("dissolvedOxygen", 97)
ORP =  sensors.Sensor("oxidationReductionPotential", 102)

device_list = [RTD,DO,ORP]


for device in device_list:
    device.connect()
    response = device.query(commands.Command("cal,?")) 
    print(device.name + " returned status_code = " + str(response.status_code))
    print(device.name + " data = " + str(response.data.decode("utf-8")))
    
    
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)
print(AtlasI2C.list_i2c_devices())

