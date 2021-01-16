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
restartCodes={"P":"Powered Off","S":"Software Reset","B":"Brown Out","W":"Watchdog","U":"Unknown"}
ledStatus={1:"On",0:"Off"}

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
    
    response = sensor.query(commands.INFO)
    payloadSub.add("Device",response.data.decode("utf-8").split(",")[1])
    payloadSub.add("Firmware",response.data.decode("utf-8").split(",")[2])
    
    response = sensor.query(Cal)
    payloadSub.add("Calibration Points", response.data.decode("utf-8").split("?CAL,")[1])
    
    response = sensor.query(commands.STATUS)
    payloadSub.add("Reason for restart",restartCodes[response.data.decode("utf-8").split(",")[1]])
    payloadSub.add("VoltageatVcc",response.data.decode("utf-8").split(",")[2])
    
    response = sensor.query(commands.LED, arguments="?")
    payloadSub.add("LED",ledStatus[response.data.decode("utf-8").split("L,")[1]])
    
    payload.add(sensor.name, payloadSub.getSub())
    
stateJson = json.loads(payload.getWithSub())
serializedState= json.dumps(stateJson, sort_keys=False, indent=3)
print(serializedState)

