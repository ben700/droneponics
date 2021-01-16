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

    client.on_message = log_on_message

    print("@@@@@@@@@@@@@@@@@@@@@------message")
    print(message.payload)
    print("@@@@@@@@@@@@@@@@@@@@@------message decode")
    print(message.payload.decode("utf-8"))
    print("@@@@@@@@@@@@@@@@@@@@@-------topic")
    print(message.topic)
    print("@@@@@@@@@@@@@@@@@@@@@-------qos")
    print(message.qos)
    print("@@@@@@@@@@@@@@@@@@@@@-------retain")
    print(message.retain)
        
    if(message.topic ==  "/devices/{}/commands/#".format(device_id)):
        if(message.payload == "updateState"):
            droneponicsSaveDeviceState()
        elif(message.payload == "update"):
            os.system('sh /home/pi/updateDroneponics.sh')
            os.system('sudo reboot')
