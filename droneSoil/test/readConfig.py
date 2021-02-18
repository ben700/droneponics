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

###CONFIG###

# device specific config
with open('../config/device_config.json') as f:
    dconfig = json.loads(str(f.read()))

device_id = dconfig['DEVICE']['DEVICE_ID']
private_key_file = dconfig['DEVICE']['PRIVATE_KEY']
private_key_file_backup = dconfig['DEVICE']['PRIVATE_KEY_BACKUP']
algorithm = gconfig['DEVICE']['ALGORITHM']
algorithm_backup = gconfig['DEVICE']['ALGORITHM_BACKUP']



#global config
with open('../config/global_config.json') as f:
    gconfig = json.loads(str(f.read()))

project_id = gconfig['GCP']['PROJECT_ID']
cloud_region = gconfig['GCP']['CLOUD_REGION']
registry_id = gconfig['GCP']['REGISTRY_ID']
mqtt_bridge_hostname = gconfig['GCP']['MQTT_BRIDGE_HOSTNAME']
mqtt_bridge_port = gconfig['GCP']['MQTT_BRIDGE_PORT']

#sys specific
ca_certs = dconfig['DEVICE']['CA_CERTS']


# This is the topic that the device will receive configuration updates on.
mqtt_config_topic = '/devices/{}/config'.format(device_id)


def main():
    connected = False
    mqtt_topic = '/devices/{}/events'.format(device_id)
    
    print('Read device_config.json device_id = ' + device_id)
    print('Read global_config.json project_id = ' + project_id)

if __name__ == '__main__':
    main()
