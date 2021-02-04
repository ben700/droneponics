from atlas_i2c import sensors
from atlas_i2c import commands
from atlas_i2c.commands import Command
from atlas_i2c import atlas_i2c
from typing import Any
import sys
import os
sys.path.append('/home/pi/droneponics')
import drone
from configparser import ConfigParser
import logging
import json
import connect
import csv
import datetime
import time

deviceName ={102: "Temperature", 97: "Dissolved Oxygen", 98: "Oxidation Reduction Potential", 99: "pH", 100:"Conductivity", 105:"Gaseous CO2", 111:"Humidity", 103:"Dose Pump", 11:"Dose Pump 1", 12:"Dose Pump 2", 13:"Dose Pump 3", 14:"Dose Pump 4", 15:"Dose Pump 5", 16:"Dose Pump 6", 17:"Dose Pump 7"}
restartCodes={"P":"Powered Off","S":"Software Reset","B":"Brown Out","W":"Watchdog","U":"Unknown"}
ledStatus={"1":"On","0":"Off"}
responseCodes={"1":"Successful Request", "2":"syntax error", "254":"still processing, not ready", "255":"no data to send"}

parser = ConfigParser()
parser.read("/home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")

_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))
    
class CalAction(Command):
    arguments: Any
    name: str 
    processing_delay: int = 300

    @classmethod
    def format_command(cls, arg) -> str:
        return f"{arg}"
    
class Cal(Command):
    """Get info about a device."""

    arguments: None = None
    name: str = "cal,?"
    processing_delay: int = 300

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"
    
    
class PumpVoltage(Command):
    """Get info about a device."""

    arguments: None = None
    name: str = "PV,?"
    processing_delay: int = 300

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"
    
class TotalVolume(Command):
    """Get info about a device."""

    arguments: None = None
    name: str = "TV,?"
    processing_delay: int = 300

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"
    
class AbsoluteTotalVolume(Command):
    """Get info about a device."""

    arguments: None = None
    name: str = "ATV,?"
    processing_delay: int = 300

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"
    
class Parameters(Command):
    """Get info about a device."""

    arguments: None = None
    name: str = "O,?"
    processing_delay: int = 300

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"
    


for device in list_i2c_devices():
    sensor = sensors.Sensor(deviceName[device], device)
    sensor.connect()
    
    response = sensor.query(commands.INFO)
    print(response.data.decode("utf-8"))
    
    
