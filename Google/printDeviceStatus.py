from atlas_i2c import sensors
from atlas_i2c import commands
from atlas_i2c import atlas_i2c


RTD = sensors.Sensor("Temperature", 102)
DO =  sensors.Sensor("dissolvedOxygen", 97)
ORP =  sensors.Sensor("oxidationReductionPotential", 102)

device_list = [RTD,DO,ORP]


for device in device_list:
    device.connect()
    response = device.query("cal,?") 
    print(device.name + " returned status_code = " + str(response.status_code))
    print(device.name + " data = " + str(response.data.decode("utf-8")))
    

