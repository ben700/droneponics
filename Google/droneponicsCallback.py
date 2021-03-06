import datetime
import time
import jwt
import paho.mqtt.client as mqtt
import re
from devicePayload import  getDeviceStatePayload, deviceCalibrationCommand, calibrationHelpPayload
from droneponicsPostToGoogle import droneponicsSaveDeviceState
import subprocess
import sys
import os
sys.path.append('/home/pi/droneponics')
import drone
from configparser import ConfigParser
import json
import connect
import csv

import base64


parser = ConfigParser()
parser.read("/home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")

service_account_json =parser.get('Google', 'service_account_json')
project_id =parser.get('Google', 'project_id')
cloud_region = parser.get('Google','gcp_location')
registry_id =parser.get('Google', 'registry_id')
device_id = parser.get('Google', 'device_id')
gateway_id =parser.get('Google', 'gateway_id')
num_messages = 1
rsa_private_path = parser.get('Google', 'rsa_private_path')
algorithm = parser.get('Google', 'ssl_algorithm')
ca_certs = parser.get('Google', 'root_cert_filepath')
log_path = parser.get('Google', 'log_path')
mqtt_bridge_hostname = "mqtt.googleapis.com"
mqtt_bridge_port = 8883

def logDroneponicsCallback(client):
    def log_on_message(unused_client, unused_userdata, message):
        if not os.path.exists(log_path):
            with open(log_path, "w") as csvfile:
                logwriter = csv.writer(csvfile, dialect="excel")
                logwriter.writerow(["time", "topic", "data"])

        with open(log_path, "a") as csvfile:
            logwriter = csv.writer(csvfile, dialect="excel")
            logwriter.writerow(
                [
                    datetime.datetime.now().isoformat(),
                    message.topic,
                    message.payload,
                ]
            )
    
        if(message.topic ==  "/devices/{}/commands".format(device_id)):
            command = message.payload.decode("utf-8") 
            if(command[0:3] == "cal"):
                try:
                    calDevice = command.split("#")[1]
                    calCommand = command.split("#")[2]
                except:
                   calDevice = None
                   calCommand = None
                if(calDevice is None or calCommand is None):
                    unused_client.publish("/devices/{}/state".format(device_id), "{} : {}".format(device_id, calibrationHelpPayload("Calibration not formated correctly: should be cal#device#command" )))  
                else:
                    success = deviceCalibrationCommand(calDevice, calCommand)
                    if(success == 1): 
                        unused_client.publish("/devices/{}/state".format(device_id), "{} : {}".format(device_id, "Success :- Calibrated of " + str(calDevice) + " with command " + calCommand))  
                    else:
                        if(success == -1):
                            unused_client.publish("/devices/{}/state".format(device_id), "{} : {}".format(device_id, calibrationHelpPayload("Calibration Device "+ str(calDevice) +" Not Found" )))          
                        else:
                            unused_client.publish("/devices/{}/state".format(device_id), "{} : {}".format(device_id, calibrationHelpPayload("Calibration Command "+ str(calCommand) +" Not Found" )))          
            elif(command == "updateReboot"):
                infot = unused_client.publish("/devices/{}/state".format(device_id), "{} : {}".format(device_id, "Update and reboot" ), qos=1)
                time.sleep(10)
                subprocess.call(['sh', '/home/pi/updateDroneponics.sh'])
                os.system('sudo reboot')
            else: # update Device State
                unused_client.publish("/devices/{}/state".format(device_id), "{} : {}".format(device_id, getDeviceStatePayload()))
                

    client.on_message = log_on_message
                
                
    
