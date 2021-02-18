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

import argparse
import datetime
import os
import random
import ssl
import time
import json
import io

import jwt
import paho.mqtt.client as mqtt
import json
import sys
sys.path.append('/home/pi/droneponics')
import chirp
import time

# These values needs to be calibrated for the percentage to work!
# The highest and lowest value the individual sensor outputs.
min_moist = 240
max_moist = 790

# Initialize the sensor.
chirp = chirp.Chirp(address=0x20,
                    read_moist=True,
                    read_temp=True,
                    read_light=True,
                    min_moist=min_moist,
                    max_moist=max_moist,
                    temp_scale='celsius',
                    temp_offset=0)

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

    # Since a disconnect occurred, the next loop iteration will wait with
    # exponential backoff.
    global should_backoff
    should_backoff = True


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print('on_publish')


def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    global  ph_Dose
    global  ec_Dose
    payload = message.payload.decode('utf-8')
    print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, message.topic, str(message.qos)))

    if not payload:
      return



def get_client(
        project_id, cloud_region, registry_id, device_id, private_key_file,
        algorithm, ca_certs, mqtt_bridge_hostname, mqtt_bridge_port):
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
    client.username_pw_set(
            username='unused',
            password=create_jwt(
                    project_id, private_key_file, algorithm))

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Register message callbacks. 
    client.on_connect = on_connect
    #client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to the Google MQTT bridge.
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    # Subscribe to the config topic.
    client.subscribe(mqtt_config_topic, qos=0)

    

    return client

def toggle_led(status):
   print("toggle_led status =" + status);

###CONFIG###

# device specific config
with open('config/device_config.json') as f:
    dconfig = json.loads(str(f.read()))

device_id = dconfig['DEVICE']['DEVICE_ID']
private_key_file = dconfig['DEVICE']['PRIVATE_KEY']
sys_type = dconfig['DEVICE']['TYPE']


#global config
with open('config/global_config.json') as f:
    gconfig = json.loads(str(f.read()))

project_id = gconfig['GCP']['PROJECT_ID']
cloud_region = gconfig['GCP']['CLOUD_REGION']
registry_id = gconfig['GCP']['REGISTRY_ID']
mqtt_bridge_hostname = gconfig['GCP']['MQTT_BRIDGE_HOSTNAME']
mqtt_bridge_port = gconfig['GCP']['MQTT_BRIDGE_PORT']
algorithm = gconfig['GCP']['ALGORITHM']

#sys specific
ca_certs = dconfig['DEVICE']['CA_CERTS']


# This is the topic that the device will receive configuration updates on.
mqtt_config_topic = '/devices/{}/config'.format(device_id)


print("this is where to setup GPIO for led status");


def main():
    global minimum_backoff_time
    global connected
    connected = False
    global hr_limit

    #args = parse_command_line_args()

    mqtt_topic = '/devices/{}/events'.format(device_id)

    
    
    jwt_iat = datetime.datetime.utcnow()
    jwt_exp_mins = 120
    
    client = get_client(
        project_id, cloud_region, registry_id, device_id,
        private_key_file, algorithm, ca_certs,
        mqtt_bridge_hostname, mqtt_bridge_port)

    # Process network events on new thread
    client.loop_start()

    while True:
        try:
            chirp.trigger()
        
            payload["moisture"] = chirp.moist
            payload["moisturePercent"] = chirp.moist_percent 
            payload["rootTemp"] = chirp.temp
            payload["rootLight"] = chirp.light
            payload["minMoist"] = min_moist
            payload["maxMoist"] = max_moist
            payload["timestamp"] = int(datetime.datetime.now().strftime("%s")) * 1000

            serializedPayload= json.dumps(payload, sort_keys=False, indent=2)
            print(serializedPayload)
            
        except KeyboardInterrupt:
            print('\nCtrl-C Pressed! Exiting.\n')
        except :
            print('\nExcept! Reading moisture Exiting.\n')            
        finally:
            print('Bye!')
        
        if connected:
            print('publishing ' + str(serializedPayload) + ' on ' + mqtt_topic)
            print(client.publish(mqtt_topic, serializedPayload, qos=0))


        # Send events every second. limit to 1 per second due to fs limits
        time.sleep(1)



if __name__ == '__main__':
    main()