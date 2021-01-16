from atlas_i2c import sensors
from atlas_i2c import commands
from atlas_i2c import atlas_i2c


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
print(AtlasI2C.list_i2c_devices())

