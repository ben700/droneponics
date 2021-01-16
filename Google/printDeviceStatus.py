from atlas_i2c import sensors
from atlas_i2c import commands
from atlas_i2c.commands import Command
from atlas_i2c import atlas_i2c
import sys
import os
sys.path.append('/home/pi/droneponics')
import drone
from configparser import ConfigParser
import logging
import json

deviceName ={102: "Temperature", 97: "Dissolved Oxygen", 98: "Oxidation Reduction Potential", 99: "pH", 100:"Conductivity", 105:"Gaseous CO2", 111:"Humidity"}

parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configDoser/"+drone.gethostname()+".ini")

_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))
    
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

payload = drone.dronePayload(_log)
  
for device in list_i2c_devices():
    payloadSub = drone.dronePayload(_log)
    sensor = sensors.Sensor(deviceName[device], device)
    sensor.connect()
    response = sensor.query(Cal)
    print(sensor.name + " returned status_code = " + str(response.status_code))
    print(sensor.name + " data = " + str(response.data.decode("utf-8")))
    print(sensor.name + " Calibration Points = " + str(response.data.decode("utf-8").split("?CAL,")[1]))
    payloadSub.add("Sensor Type",sensor.name)
    payloadSub.add("Calibration Points", response.data.decode("utf-8").split("?CAL,")[1])
    payloadSub.add("Status Code",response.status_code)    
    payload.add(sensor.name, payloadSub.getSub())
    
print(payload.getWithSub())

from io import StringIO
io = StringIO()
outputString = payloadSub.getSub()
json.dump(outputString, io)
serialized= json.dumps(outputString, sort_keys=False, indent=3)

stringer = {"Sensor Type": "Oxidation Reduction Potential","Calibration Points": "0","Status Code": "1"}
serializeds= json.dumps(stringer, sort_keys=False, indent=3)

full = { "ts": "1610770467", "deviceMAC": "dc:a6:32:8a:39:53","Temperature":{"Sensor Type": "Temperature","Calibration Points": "0","Status Code": "1"},"Dissolved Oxygen": {"Sensor Type": "Dissolved Oxygen","Calibration Points": "2","Status Code": "1"},"Oxidation Reduction Potential": {"Sensor Type": "Oxidation Reduction Potential","Calibration Points": "0","Status Code": "1"}}
serializedfull= json.dumps(full, sort_keys=False, indent=3)

print(outputString)
print(io.getvalue())
print(serialized)
print(serializeds)
print(serializedfull)
