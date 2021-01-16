import datetime
import time
import jwt
import paho.mqtt.client as mqtt
import re
from devicePayload import  getDeviceStatePayload
import sys
import os
sys.path.append('/home/pi/droneponics')
import drone
from configparser import ConfigParser

def logDroneponicsCallback(client):
    print("@@@@@@@@@@@@@@@@@@@@@--client")
    print(client)
    def log_on_message(unused_client, unused_userdata, message):
        print("@@@@@@@@@@@@@@@@@@@@@------message")
        print(message)
        print("@@@@@@@@@@@@@@@@@@@@@-------topic")
        print(message.topic)
            #/devices/droneOxy/commands
        print(message.payload.decode("utf-8"))
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
