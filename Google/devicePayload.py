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
    """Get info about a device."""
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

def getDeviceStatePayload():

    payload = drone.dronePayload(_log)
  
    for device in list_i2c_devices():
        payloadSub = drone.dronePayload(_log)
        sensor = sensors.Sensor(deviceName[device], device)
        sensor.connect()
    
        response = sensor.query(commands.INFO)
        deviceType=response.data.decode("utf-8").split(",")[1]
        payloadSub.add("Device",deviceType)
        payloadSub.add("Firmware",response.data.decode("utf-8").split(",")[2])
    
        response = sensor.query(Cal)
        payloadSub.add("Calibration Points", response.data.decode("utf-8").split("?CAL,")[1])
    
        response = sensor.query(commands.STATUS)
        payloadSub.add("Reason for restart",restartCodes[response.data.decode("utf-8").split(",")[1]])
        payloadSub.add("VoltageatVcc",response.data.decode("utf-8").split(",")[2])
    
        response = sensor.query(commands.LED, arguments="?")
        payloadSub.add("LED",ledStatus[response.data.decode("utf-8").split("L,")[1]])
    
        if (deviceType == "PMP"):
            response = sensor.query(PumpVoltage)
            payloadSub.add("Pump Voltage",response.data.decode("utf-8").split("PV,")[1])
            response = sensor.query(TotalVolume)
            payloadSub.add("Total Volume",response.data.decode("utf-8").split("TV,")[1])
            response = sensor.query(AbsoluteTotalVolume)
            payloadSub.add("Absolute Total Volume",response.data.decode("utf-8").split("ATV,")[1])
            response = sensor.query(Parameters)
            payloadSub.add("Parameters",response.data.decode("utf-8").split("O,")[1])
        else:
            response = sensor.query(commands.READ)
            payloadSub.add("Reading",response.data.decode("utf-8"))
    
        payload.add(sensor.name, payloadSub.getSub())
    
    stateJson = json.loads(payload.getWithSub())
    serializedState= json.dumps(stateJson, sort_keys=False, indent=3)
    return serializedState

def deviceCalibrationCommand(sDevice, sCommand):
    try:
        device_name = deviceName[int(sDevice)]
    except:
        return -1
    if(device_name is None):
        return -1
    try:
        sensor = sensors.Sensor(device_name, int(sDevice))
        sensor.connect()
    except:
        return -1
    try:        
        response = sensor.query(CalAction, sCommand)
        if(response.status_code is None or str(response.status_code) != "1"):    
            print("response.status_code =" + responseCodes[response.status_code])
            return 0
        else:
            return 1
    except:
        return 0
        
    
def calibrationHelpPayload(sError):

    payloadStr = '{"Error":"' + sError + '", "Calibration Commands":{  "Temperature": { \
          "deviceID": "102", \
          "Clear": "Cal,clear", \
          "Set to t": "Cal,t" \
       }, \
       "Dissolved Oxygen": { \
          "deviceID": "97", \
          "Clear": "Cal,clear", \
          "Atmospheric": "Cal", \
          "Solution": "Cal,0" \
       }, \
       "Oxidation Reduction Potential": { \
          "deviceID": "98", \
          "Clear": "Cal,clear", \
          "Set to n" : "Cal,n" \
       }, \
       "Conductivity": { \
          "deviceID": "100", \
          "Clear": "Cal,clear", \
          "Atmospheric": "Cal,dry", \
          "Single Point": "Cal,n", \
          "Low": "Cal,low,n", \
          "High": "Cal,high,n", \
          "probe Type": "K,n"    \
       }, \
       "pH": { \
          "deviceID": "99", \
          "Clear": "Cal,clear", \
          "Mid": "Cal,mid,7", \
          "Low": "Cal,low,4", \
          "High": "Cal,high,10" \
       }, \
       "Dose Pump": { \
          "deviceID": "103" \
       }, \
       "Dose Pump 1": { \
          "deviceID": "11" \
       }, \
       "Dose Pump 2": { \
          "deviceID": "12" \
       }, \
       "Dose Pump 3": { \
          "deviceID": "13" \
       }, \
       "Dose Pump 4": { \
          "deviceID": "14" \
       }, \
       "Dose Pump 5": { \
          "deviceID": "15" \
       }, \
       "Dose Pump 6": { \
          "deviceID": "16" \
       }, \
       "Dose Pump 7": { \
          "deviceID": "17" \
       } \
    }}'
    stateJson = json.loads(payloadStr)
    serializedState= json.dumps(stateJson, sort_keys=False, indent=5)
    print(serializedState)
    return serializedState
