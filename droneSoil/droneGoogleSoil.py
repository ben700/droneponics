#!/usr/bin/env python3

# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pathlib import Path
appFolder = Path("/home/pi/droneponics/droneSoil/")

import argparse
import datetime
import os
import random
import ssl
import time
import json
import io
import sys
import jwt
import paho.mqtt.client as mqtt
import drone
import chirp


# These values needs to be calibrated for the percentage to work!
# The highest and lowest value the individual sensor outputs.
min_moist = 240
max_moist = 790
sample_Rate = 60

def initializeTheSensor():
  return chirp.Chirp(address=0x20,
                    read_moist=True,
                    read_temp=True,
                    read_light=True,
                    min_moist=min_moist,
                    max_moist=max_moist,
                    temp_scale='celsius',
                    temp_offset=0)
soilSensor = initializeTheSensor()
# [START iot_mqtt_jwt]
def create_jwt(project_id, private_key_file, algorithm):

    token = {
            # The time that the token was issued at
            'iat': datetime.datetime.utcnow(),
            # The time the token expires.
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            # The audience field should always be set to the GCP project id.
            'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
            algorithm, private_key_file))

    
    return jwt.encode(token, private_key, algorithm=algorithm)
# [END iot_mqtt_jwt]


# [START iot_mqtt_config]
def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print('on_connect', mqtt.connack_string(rc))

    # After a successful connect, reset backoff time and stop backing off.
    global should_backoff
    global minimum_backoff_time
    global connected
    connected = True
    should_backoff = False
    minimum_backoff_time = 1



def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print('on_disconnect', error_str(rc))
    os.execv(sys.argv[0], sys.argv)
    sys.exit(error_str(rc))
    # Since a disconnect occurred, the next loop iteration will wait with
    # exponential backoff.
    global should_backoff
    should_backoff = True


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print('on_publish')


def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    global  max_moist
    global  min_moist
    global sample_Rate
    payload = message.payload.decode('utf-8')
    print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, message.topic, str(message.qos)))

    if not payload:
      return
    
    data = json.loads(payload)
    if 'minMoist' in data:
      min_moist  =  data["minMoist"]
    if 'maxMoist' in data:
      max_moist  =  data["maxMoist"]
    if 'sampleRate' in data:
      sample_Rate  =  data["sampleRate"]

   
def get_client(
        project_id, cloud_region, registry_id, device_id, private_key_file,
        algorithm, private_key_file_backup, algorithm_backup, ca_certs, mqtt_bridge_hostname, mqtt_bridge_port):
    """Create our MQTT client. The client_id is a unique string that identifies
    this device. For Google Cloud IoT Core, it must be in the format below."""
    client = mqtt.Client(
            client_id=('projects/{}/locations/{}/registries/{}/devices/{}'
                       .format(
                               project_id,
                               cloud_region,
                               registry_id,
                               device_id)))

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    print("Try to connect with private_key_file = " + str(private_key_file) + " and algorithm = " + algorithm)
    try:
        client.username_pw_set(
                username='unused',
                password=create_jwt(
                        project_id, private_key_file, algorithm))
    except:
      print("Failed to connect with private_key_file")
      print("Try to connect with private_key_file_backup = " + str(private_key_file_backup) + " and algorithm = " + algorithm_backup)
      client.username_pw_set(
              username='unused',
              password=create_jwt(
                      project_id, private_key_file_backup, algorithm_backup))
      print("Success: Connect with private_key_file_backup = " + str(private_key_file_backup) + " and algorithm = " + algorithm_backup)


    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Register message callbacks. 
    client.on_connect = on_connect
    #client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to the Google MQTT bridge.
    if(client.connect(mqtt_bridge_hostname, mqtt_bridge_port) != mqtt.MQTT_ERR_SUCCESS):
      print("Failed to connect with private_key_file")
      client.username_pw_set(
            username='unused',
            password=create_jwt(
                    project_id, private_key_file_backup, algorithm_backup))
      if(client.connect(mqtt_bridge_hostname, mqtt_bridge_port) != mqtt.MQTT_ERR_SUCCESS):
        print("Failed to connect with private_key_file_backup")
     
    
    # Subscribe to the config topic.
    client.subscribe(mqtt_config_topic, qos=1)

    

    return client

def toggle_led(status):
   print("toggle_led status =" + status);

###CONFIG###

# device specific config
with open(appFolder / "config/device_config.json") as f:
    dconfig = json.loads(str(f.read()))

device_id = dconfig['DEVICE']['DEVICE_ID']
private_key_file =appFolder /  dconfig['DEVICE']['PRIVATE_KEY']
private_key_file_backup =appFolder /  dconfig['DEVICE']['PRIVATE_KEY_BACKUP']
algorithm = dconfig['DEVICE']['ALGORITHM']
algorithm_backup = dconfig['DEVICE']['ALGORITHM_BACKUP']



#global config
with open(appFolder / "config/global_config.json") as f:
    gconfig = json.loads(str(f.read()))

project_id = gconfig['GCP']['PROJECT_ID']
cloud_region = gconfig['GCP']['CLOUD_REGION']
registry_id = gconfig['GCP']['REGISTRY_ID']
mqtt_bridge_hostname = gconfig['GCP']['MQTT_BRIDGE_HOSTNAME']
mqtt_bridge_port = gconfig['GCP']['MQTT_BRIDGE_PORT']

#sys specific
ca_certs = appFolder / dconfig['DEVICE']['CA_CERTS']


# This is the topic that the device will receive configuration updates on.
mqtt_config_topic = '/devices/{}/config'.format(device_id)


#print("this is where to setup GPIO for led status")


def main():
    global minimum_backoff_time
    global connected
    connected = False
    global hr_limit
    global soilSensor
    global min_moist
    global max_moist
    global sample_Rate

    #args = parse_command_line_args()

    mqtt_topic = '/devices/{}/events'.format(device_id)

    
    
    jwt_iat = datetime.datetime.utcnow()
    jwt_exp_mins = 120
    
    client = get_client(
        project_id, cloud_region, registry_id, device_id,
        private_key_file, algorithm, private_key_file_backup, algorithm_backup, ca_certs,
        mqtt_bridge_hostname, mqtt_bridge_port)

    # Process network events on new thread
    client.loop_start()
    print("Google : Waiting to be connected")
    while not connected:
        continue
    print("Success : Connected")
    
    print("Sending Boot data over to Goolge")
    payload = {}
    drone.payload(payload)    
    serializedPayload = json.dumps(payload, sort_keys=False, indent=2)
  
    if (connected):
        print('publishing boot data ' + str(serializedPayload) + ' on ' + mqtt_topic + '/deviceBoot')
        print(client.publish(mqtt_topic+'/deviceBoot', serializedPayload, qos=0))
    else:
        print("Failed : Wasn't connected after boot")
        
    while True:
      seconds_since_issue = (datetime.datetime.utcnow() - jwt_iat).seconds
      if seconds_since_issue > 60 * jwt_exp_mins:
        print('Refreshing token after {}s').format(seconds_since_issue)
        jwt_iat = datetime.datetime.utcnow()
        client.loop()
        client.disconnect()
        client = get_client(
          project_id, cloud_region, registry_id, device_id,
          private_key_file, algorithm, private_key_file_backup, algorithm_backup, ca_certs,
          mqtt_bridge_hostname, mqtt_bridge_port)
            
      payload = {}
      try:
          soilSensor.trigger()
          if (soilSensor.moist > max_moist):
            max_moist = soilSensor.moist
            soilSensor = initializeTheSensor()
            soilSensor.trigger()
            
          if (soilSensor.moist < min_moist):
            min_moist = soilSensor.moist
            soilSensor = initializeTheSensor()
            soilSensor.trigger()
       
          payload["moisture"] = soilSensor.moist
          payload["moisturePercent"] = soilSensor.moist_percent 
          payload["rootTemp"] = soilSensor.temp
          payload["rootLight"] = soilSensor.light
          payload["minMoist"] = min_moist
          payload["maxMoist"] = max_moist
          payload["timestamp"] = int(datetime.datetime.now().strftime("%s")) * 1000
          
       
          serializedPayload= json.dumps(payload, sort_keys=False, indent=2)
    
          if (connected and len(serializedPayload) > 0):
              print('publishing ' + str(serializedPayload) + ' on ' + mqtt_topic)
              print(client.publish(mqtt_topic, serializedPayload, qos=0))

          # Send events every second. limit to 1 per second due to fs limits
          time.sleep(sample_Rate)
      
      except KeyboardInterrupt:
         sys.exit('\nCtrl-C Pressed! Exiting.\n')
      except :
          sys.exit('\nExcept! Reading moisture Exiting.\n')            
        
if __name__ == '__main__':
    main()
