# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import socket
import sys
import drone
from configparser import ConfigParser
from colors import bcolors


# Droneponics Start
parser = ConfigParser()
parser.read("/home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")

# tune console logging
_log = logging.getLogger('GoogleLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))
_log.critical("critical")
_log.error("error")
_log.warning("warning")
_log.info("info")
_log.debug("debug")
_log.info("ConfigParser path = /home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")



ssl_private_key_filepath = parser.get('Google', 'ssl_private_key_filepath')
ssl_algorithm = parser.get('Google', 'ssl_algorithm')
root_cert_filepath = parser.get('Google', 'root_cert_filepath')
project_id = parser.get('Google', 'project_id')
gcp_location = parser.get('Google', 'gcp_location')
registry_id = parser.get('Google', 'sensor_registry_id')
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

relay = drone.Relay(_log, 21, "Ozone")

ADDR = ''
PORT = 10000
# Create a UDP socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (ADDR, PORT)

device_id = sys.argv[1]
if not device_id:
    sys.exit('The device id must be specified.')

print('Bringing up device {}'.format(device_id))


def SendCommand(sock, message):
    print('sending "{}"'.format(message))
    sock.sendto(message.encode(), server_address)

    # Receive response
    print('waiting for response')
    response = sock.recv(4096)
    print('received: "{}"'.format(response))

    return response


def MakeMessage(device_id, action, data=''):
    if data:
        return '{{ "device" : "{}", "action":"{}", "data" : "{}" }}'.format(
            device_id, action, data)
    else:
        return '{{ "device" : "{}", "action":"{}" }}'.format(
            device_id, action)


def RunAction(action, data=''):
    global client_sock
    message = MakeMessage(device_id, action, data)
    if not message:
        return
    print('Send data: {} '.format(message))
    event_response = SendCommand(client_sock, message)
    print('Response: {}'.format(event_response))


try:
    RunAction('detach')
    RunAction('attach')
    RunAction('event', 'Doser is online')
    RunAction('subscribe')

    while True:
        response = client_sock.recv(4096).decode('utf8')
        print('Client received {}'.format(response))
        if response.upper() == 'ON' or response.upper() == b'ON':
            relay.turnOn(_log) 
            sys.stdout.write('\r>> ' + bcolors.OKGREEN + bcolors.CBLINK +
                             " Doser is ON " + bcolors.ENDC + ' <<')
            sys.stdout.flush()
        elif response.upper() == "OFF" or response.upper() == b'OFF':
            relay.turnOff(_log)
            sys.stdout.write('\r >>' + bcolors.CRED + bcolors.BOLD +
                             ' Doser is OFF ' + bcolors.ENDC + ' <<')
            sys.stdout.flush()
        else:
            print('Invalid message {}'.format(response))

finally:
    print('closing socket', file=sys.stderr)
    client_sock.close()
