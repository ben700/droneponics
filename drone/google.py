
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
import requests
# Droneponics End


# Define some project-based variables to be used below. This should be the only
# block of variables that you need to edit in order to run this script


# end of user-variables
def buildPayloadField(sString):
    if(sString is None):
         return ""
    else:
         return str(sString)
      
   
def buildSensorPayload(sensors, _log):
    _log("buildSensorPayload")
    _log(sensors[1].name)
   
    if(sensors[1].name == "EC"):
        payload = '{ "deviceTime": "{}", "deviceMAC": "{}", "temperature": "{}", "pH": "{}", "conductivity": "{}", "totalDissolvedSolids": "{}", "salinity": "{}", "specificGravity": "{}"}'.format(int(time.time()), drone.get_mac(), buildPayloadField(sensors[0].value), buildPayloadField(sensors[2].value), buildPayloadField(sensors[1].value), buildPayloadField(sensors[1].value2), buildPayloadField(sensors[1].value3), buildPayloadField(sensors[1].value4) )
    elif(sensors[1].name == "Dissolved Oxygen"):      
        payload = '{ "deviceTime": "{}", "deviceMAC": "{}", "temperature": "{}", "dissolvedOxygen": "{}", "saturation": "{}", "oxidationReductionPotential": "{}"}'.format(int(time.time()), drone.get_mac(), buildPayloadField(sensors[0].value), buildPayloadField(sensors[1].value), buildPayloadField(sensors[1].value2), buildPayloadField(sensors[2].value) )
    return payload   
   

def create_jwt(project_id, ssl_private_key_filepath, ssl_algorithm):
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
    pass
    #print('on_connect', error_str(rc))

def on_publish(unused_client, unused_userdata, unused_mid):
   pass
   #print('on_publish')


def pubGoolgeCloud(_MQTT_TOPIC, payload):
    
    # Droneponics Start
    parser = ConfigParser()
    parser.read("/home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")


    ssl_private_key_filepath = parser.get('Google', 'ssl_private_key_filepath')
    ssl_algorithm = parser.get('Google', 'ssl_algorithm')
    root_cert_filepath = parser.get('Google', 'root_cert_filepath')
    project_id = parser.get('Google', 'project_id')
    gcp_location = parser.get('Google',     'gcp_location')
    registry_id = parser.get('Google', 'registry_id')
    device_id = parser.get('Google', 'device_id')
    device_sensor_type = parser.get('Google', 'device_sensor_type')


    _CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, gcp_location, registry_id, device_id)
    
    client = mqtt.Client(client_id=_CLIENT_ID)
    # authorization is handled purely with JWT, no user/pass, so username can be whatever
    client.username_pw_set(
        username='unused',
        password=create_jwt(project_id, ssl_private_key_filepath, ssl_algorithm))
    
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.tls_set(ca_certs=root_cert_filepath) # Replace this with 3rd party cert if that was used when creating registry
    client.connect('mqtt.googleapis.com', 8883)

    client.loop_start()


    # Uncomment following line when ready to publish
    client.publish(_MQTT_TOPIC, payload, qos=1)

    # Droneponics End
    
    client.loop_stop()
    return True


def pubDeviceBootToGoolgeCloud():

    # Droneponics Start
    parser = ConfigParser()
    parser.read("/home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")
    device_id = parser.get('Google', 'device_id')

    _MQTT_TOPIC = '/devices/{}/events/deviceBoot'.format(device_id)
    payload = '{ "bootTime": "{}", "deviceMAC": "{}", "deviceName": "{}", "deviceIP": "{}"}'.format(int(time.time()), drone.get_mac(), drone.gethostname(), drone.get_ip())

    return pubGoolgeCloud(_MQTT_TOPIC, payload)
 

def pubEnviromentalReadingsToGoolgeCloud(dronePayload):

    # Droneponics Start
    parser = ConfigParser()
    parser.read("/home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")
    device_id = parser.get('Google', 'device_id')

    _MQTT_TOPIC = '/devices/{}/events/environmentalData'.format(device_id)
      
    return pubGoolgeCloud(_MQTT_TOPIC, dronePayload.get())
 

def pubLightReadingsToGoolgeCloud(dronePayload):

    # Droneponics Start
    parser = ConfigParser()
    parser.read("/home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")
    device_id = parser.get('Google', 'device_id')

    _MQTT_TOPIC = '/devices/{}/events/lightData'.format(device_id)
      
    return pubGoolgeCloud(_MQTT_TOPIC, dronePayload.get())
 
def pubGasiousReadingsToGoolgeCloud(dronePayload):

    # Droneponics Start
    parser = ConfigParser()
    parser.read("/home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")
    device_id = parser.get('Google', 'device_id')

    _MQTT_TOPIC = '/devices/{}/events/gasious'.format(device_id)
      
    return pubGoolgeCloud(_MQTT_TOPIC, dronePayload.get())
   
def pubSensorReadingsToGoolgeCloud(sensors, _log):
    # Droneponics Start
    _log.info("pubSensorReadingsToGoolgeCloud")
    parser = ConfigParser()
    parser.read("/home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")
    _log.info("parser.read")
    
   
    device_id = parser.get('Google', 'device_id')
    _log.info("device_id = {}".format(device_id))
   
    _MQTT_TOPIC = '/devices/{}/events/sensorReading'.format(device_id)
    payload = ""
    
    
    if(sensors[1].name == "EC"):
        _log.info("build payload ec")
#        payload = '{{ "deviceTime": "{}", "deviceMAC": "{}", "temperature": "{}", "pH": "{}", "conductivity": "{}", "totalDissolvedSolids": "{}", "salinity": "{}", "specificGravity": "{}"}}'.format(int(time.time()), drone.get_mac(), buildPayloadField(sensors[0].value), buildPayloadField(sensors[2].value), buildPayloadField(sensors[1].value), buildPayloadField(sensors[1].value2), buildPayloadField(sensors[1].value3), buildPayloadField(sensors[1].value4) )
        payload = '{ "deviceTime": "{}", "deviceMAC": "{}", "temperature": "{}", "pH": "{}", "conductivity": "{}", "totalDissolvedSolids": "{}", "salinity": "{}", "specificGravity": "{}"}'.format(int(time.time()), drone.get_mac(), sensors[0].value, sensors[2].value, sensors[1].value, sensors[1].value2, sensors[1].value3, sensors[1].value4 )
    elif(sensors[1].name == "Dissolved Oxygen"):      
        payload = '{ "deviceTime": "{}", "deviceMAC": "{}", "temperature": "{}", "dissolvedOxygen": "{}", "saturation": "{}", "oxidationReductionPotential": "{}"}'.format(int(time.time()), drone.get_mac(), buildPayloadField(sensors[0].value), buildPayloadField(sensors[1].value), buildPayloadField(sensors[1].value2), buildPayloadField(sensors[2].value) )
  
    _log.info(payload)
    return pubGoolgeCloud(_MQTT_TOPIC, payload )

   
def pubDoseVolumeToGoolgeCloud(dose, _log):
    if(str(dose.dose)[0:3] == "0.0"):
        return True
 
    # Droneponics Start
    parser = ConfigParser()
    parser.read("/home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")
    _MQTT_TOPIC = '/devices/{}/events/dosed'.format(parser.get('Google', 'device_id'))
    payload = ''
    payload = dose.buildDosePayload(payload)
    _log.info(payload)

    return pubGoolgeCloud( _MQTT_TOPIC, payload)
   

def pubSensorReadingsToThingSpeak(sensors, _log):
   
   r =requests.get("https://api.thingspeak.com/update?api_key=OFS8JOTQUXNIEXLI&field1=" + str(sensors[0].value) + "&field2=" + str(sensors[1].value) + "&field3=" + str(sensors[2].value))
   _log.info("Status Code =" + str(r.status_code) + " from GET https://api.thingspeak.com/update?api_key=OFS8JOTQUXNIEXLI&field1=" + str(sensors[0].value))
   while (r.status_code is not 200):
      r =requests.get("https://api.thingspeak.com/update?api_key=OFS8JOTQUXNIEXLI&field1=" + str(sensors[0].value))
      _log.info("Status Code =" + str(r.status_code) + " from GET https://api.thingspeak.com/update?api_key=OFS8JOTQUXNIEXLI&field1=" + str(sensors[0].value))
   return True

class dronePayloadItem:
   def __init__(self, key, value):
     self.key = key
     self.value = value

   def get(self):
     if (self.value is None):
         return ""
     else:
         return '"{}": "{}",'.format(self.key, self.value)
      
   def getSub(self):
     if (self.value is None):
         return ""
     else:
         return '"{}":{},'.format(self.key, self.value)
      
      
class dronePayload:
   def __init__(self, _log, *args, **kwargs):
     self._log = _log
     self.objects = []
     
   def add(self, key, value):
     self.objects.append( dronePayloadItem(key, value))
    
   def get(self):
     payloadString = '{ "deviceTime": "{}", "deviceMAC": "{}",'.format(int(time.time()), drone.get_mac())
     for pItem in self.objects:
          payloadString = payloadString + pItem.get()

     payloadString =  payloadString[:-1] + '}'
     return payloadString
    
   def getSub(self):
     payloadString = '{'
     for pItem in self.objects:
          payloadString = payloadString + pItem.get()

     payloadString =  payloadString[:-1] + '}'
     return payloadString
    
   def getWithSub(self):
     payloadString = '{ "deviceTime": "{}", "deviceMAC": "{}",'.format(int(time.time()), drone.get_mac())
     for pItem in self.objects:
          payloadString = payloadString + pItem.getSub()

     payloadString =  payloadString[:-1] + '}'
     return payloadString
    
