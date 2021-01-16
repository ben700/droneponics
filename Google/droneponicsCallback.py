import datetime
import time
import jwt
import paho.mqtt.client as mqtt
import re
from devicePayload import  getDeviceStatePayload
from droneponicsPostToGoogle import droneponicsSaveDeviceState
import sys
import os
sys.path.append('/home/pi/droneponics')
import drone
from configparser import ConfigParser
import json
import connect
import csv



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
    myClient = client
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
            if(command == "updateState"):
                print("droneponicsSaveDeviceState()")
                droneponicsSaveDeviceState()
                client = connect.get_client(
                                        project_id,
                                        cloud_region,
                                        registry_id,
                                        gateway_id,
                                        rsa_private_path,
                                        algorithm,
                                        ca_certs,
                                        mqtt_bridge_hostname,
                                        mqtt_bridge_port,
                                    )
                print("Waiting for device to attach.")
                device_command_topic = "/devices/{}/command/#".format(device_id)
                client.subscribe(device_command_topic, qos=1)

            elif(command == "state"):
               # client.disconnect()
                print("droneponicsSaveDeviceState()")
                myClient.publish("/devices/{}/state".format(device_id), "{} : {}".format(device_id, getDeviceStatePayload()))
            elif(command == "s"):
                print("droneponicsSaveDeviceState()")
                unused_client.publish("/devices/{}/state".format(device_id), "{} : {}".format(device_id, getDeviceStatePayload()))

                #droneponicsSaveDeviceState()
               # client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

               # device_command_topic = "/devices/{}/commands/#".format(device_id)
               # client.subscribe(device_command_topic, qos=1)
    
               # print("Waiting for device to attach.")
                
            elif(command == "update"):
                os.system('sh /home/pi/updateDroneponics.sh')
                os.system('sudo reboot')

    client.on_message = log_on_message
