
###
 # Copyright 2017, Google, Inc.
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

import datetime
import time
import jwt
import paho.mqtt.client as mqtt
# Droneponics Start
import time
import sys
import os
sys.path.append('/home/pi/droneponics')
import drone
from configparser import ConfigParser
import logging
# Droneponics End


# Define some project-based variables to be used below. This should be the only
# block of variables that you need to edit in order to run this script


# end of user-variables


def create_jwt():
    cur_time = datetime.datetime.utcnow()
    token = {
      'iat': cur_time,
      'exp': cur_time + datetime.timedelta(minutes=60),
      'aud': project_id
    }
    with open(ssl_private_key_filepath, 'r') as f:
        private_key = f.read()

    return jwt.encode(token, private_key, ssl_algorithm)


def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))

def on_connect(unusued_client, unused_userdata, unused_flags, rc):
    print('on_connect', error_str(rc))

def on_publish(unused_client, unused_userdata, unused_mid):
    print('on_publish')




def pubToGoolgeCloud:(sensor, _log):

    # Droneponics Start
    parser = ConfigParser()
    parser.read("/home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")
    _log.info("ConfigParser path = /home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")


    ssl_private_key_filepath = parser.get('Google', 'ssl_private_key_filepath')
    ssl_algorithm = parser.get('Google', 'ssl_algorithm')
    root_cert_filepath = parser.get('Google', 'root_cert_filepath')
    project_id = parser.get('Google', 'project_id')
    gcp_location = parser.get('Google',     'gcp_location')
    registry_id = parser.get('Google', 'registry_id')
    device_id = parser.get('Google', 'device_id')
    device_sensor_type = parser.get('Google', 'device_sensor_type')

    _log.info('-------------------- device_sensor_type = ' + str(device_sensor_type))
    _log.info("ssl_private_key_filepath = " + str(ssl_private_key_filepath))
    _log.info("ssl_algorithm = " + str(ssl_algorithm))
    _log.info("root_cert_filepath = " + str(root_cert_filepath))
    _log.info("project_id = " + str(project_id))
    _log.info("gcp_location = " + str(gcp_location))
    _log.info("registry_id = " + str(registry_id))
    _log.info("device_id = " + str(device_id))


    _CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, gcp_location, registry_id, device_id)
    _MQTT_TOPIC = '/devices/{}/events'.format(device_id)

    client = mqtt.Client(client_id=_CLIENT_ID)
    # authorization is handled purely with JWT, no user/pass, so username can be whatever
    client.username_pw_set(
        username='unused',
        password=create_jwt())
    
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.tls_set(ca_certs=root_cert_filepath) # Replace this with 3rd party cert if that was used when creating registry
    client.connect('mqtt.googleapis.com', 8883)

    client.loop_start()


    _log.debug("Going to buildPayload")      
    payload = ''
    payload = drone.buildPayload(sensors, _log, payload)


    # Uncomment following line when ready to publish
    client.publish(_MQTT_TOPIC, payload, qos=1)

    _log.info("{}\n".format(payload))
    # Droneponics End

    client.loop_stop()
    return True
