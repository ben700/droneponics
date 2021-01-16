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
jwt_expires_minutes=5
listen_time=500


connect.send_data_from_bound_device(
    service_account_json,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    gateway_id,
    num_messages,
    rsa_private_path,
    algorithm,
    ca_certs,
    mqtt_bridge_hostname,
    mqtt_bridge_port,
    jwt_expires_minutes,
    getDeviceStatePayload(),
)


def log_callback(client):
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

connect.listen_for_messages(
    service_account_json,
    project_id,
    cloud_region,
    registry_id,
    device_id,
    gateway_id,
    num_messages,
    rsa_private_path,
    algorithm,
    ca_certs,
    mqtt_bridge_hostname,
    mqtt_bridge_port,
    jwt_expires_minutes,
    listen_time,
    log_callback,
)
