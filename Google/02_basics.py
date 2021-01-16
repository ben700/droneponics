###
 # Copyright 2018, Google, Inc.
 # Licensed under the Apache License, Version 2.0 (the `License`);
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 # 
 #    http://www.apache.org/licenses/LICENSE-2.0
 # 
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an `AS IS` BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
### 

#!/usr/bin/python

#from sense_hat import SenseHat
import datetime
import time
import jwt
import paho.mqtt.client as mqtt
import re
import devicePayload
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

# Define some project-based variables to be used below. This should be the only
# block of variables that you need to edit in order to run this script


# end of user-variables

cur_time = datetime.datetime.utcnow()

def create_jwt():
  token = {
      'iat': cur_time,
      'exp': cur_time + datetime.timedelta(minutes=60),
      'aud': project_id
  }

  with open(rsa_private_path, 'r') as f:
    private_key = f.read()

  return jwt.encode(token, ca_certs, algorithm)

_CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, cloud_region, registry_id, device_id)
_MQTT_TELEMETRY_TOPIC = '/devices/{}/events'.format(device_id)
_MQTT_CONFIG_TOPIC = '/devices/{}/config'.format(device_id)
_MQTT_COMMANDS_TOPIC = '/devices/{}/commands/#'.format(device_id)
_MQTT_STATE_TOPIC = '/devices/{}/state'.format(device_id)


client = mqtt.Client(client_id=_CLIENT_ID)
# authorization is handled purely with JWT, no user/pass, so username can be whatever
client.username_pw_set(
    username='unused',
    password=create_jwt())

regExp = re.compile('1')

def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))

def on_connect(unusued_client, unused_userdata, unused_flags, rc):
    print('on_connect', error_str(rc))

def on_publish(unused_client, unused_userdata, unused_mid):
    print('on_publish')

# I have seen, occasionally, some noise come through that needs to be stripped out
# This code ensures that it's stripped out properly
def message_text(orig):
    print ('matching message text: {}'.format(orig))
    ma = re.match(r'^b\'(.*)\'$', orig)
    if ma == None:
        return orig
    else:
        return ma.group(1)

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


# Method which handles parsing the text message coming back from the Cloud
# This is where you could add your own messages to play with different
# actions based on messages coming back from the Cloud
def respondToMsg(msg):
    if msg == "state":
        client.publish(_MQTT_STATE_TOPIC, getDeviceStatePayload(), qos=1)
    else:
        client.publish(_MQTT_TELEMETRY_TOPIC, {"event":"respondToMsg"}, qos=1)


def on_message(unused_client, unused_userdata, message):
    payload = str(message.payload)
    print('Received message \'{}\' on topic \'{}\''.format(payload, message.topic))
    respondToMsg(message_text(payload))

client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message

client.tls_set(ca_certs=root_cert_filepath) # Replace this with 3rd party cert if that was used when creating registry
client.connect('mqtt.googleapis.com', 8883)
client.subscribe(_MQTT_CONFIG_TOPIC, qos=1)
client.subscribe(_MQTT_COMMANDS_TOPIC, qos=1)
client.loop_start()


# Send 5 seconds worth of data back up to IoT Core
payload = getDeviceStatePayload()
# Uncomment following line when ready to publish to IoT Core
client.publish(_MQTT_STATE_TOPIC, payload, qos=1)

print("{}\n".format(payload))

time.sleep(1)

# This is sleeping for an arbitrarily long time because it has to be connected
# in order to receive the command/config messages. Well, the config messages would
# come through next time the device connected, but that's not as interesting
# from a starting point
time.sleep(999)
client.loop_stop()
