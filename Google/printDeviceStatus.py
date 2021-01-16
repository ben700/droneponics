from atlas_i2c import sensors
from atlas_i2c import commands
from atlas_i2c.commands import Command
from atlas_i2c import atlas_i2c

deviceName ={102: "Temp", 97: "DO", 98: "ORP", 99: "pH", 100:"Conductivity"}

class Cal(Command):
    """Get info about a device."""

    arguments: None = None
    name: str = "cal,?"
    processing_delay: int = 300

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"
    
def list_i2c_devices():
    i2c_devices_attached = []
    dev = atlas_i2c.AtlasI2C()
    for device in deviceName.keys():
        try:
            dev.set_i2c_address(device)
            dev.read("R")
            i2c_devices_attached.append(device)
        except IOError:
            pass
    return i2c_devices_attached
    
  
for device in list_i2c_devices():
    sensor = device.Sensor(deviceName[device], device)
    response = sensor.query(Cal)
    print("returned status_code = " + str(response.status_code))
    print(" data = " + str(response.data.decode("utf-8")))
    
