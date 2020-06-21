import sys
import os
sys.path.append('/home/pi/droneponics')
import socket
import drone
from drone import Alarm, OpenWeather
from datetime import datetime, date
#import date
import time
import shlex, requests
import blynklib
import blynktimer
import logging
import RPi.GPIO as GPIO   
from configparser import ConfigParser
import subprocess
import re
import json
import numbers


# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

relays=[]
relays.append(drone.Relay(_log, 18, parser.get('droneRelay', 'Relay1')))
relays.append(drone.Relay(_log, 23, parser.get('droneRelay', 'Relay2')))
relays.append(drone.Relay(_log, 24, parser.get('droneRelay', 'Relay3')))
relays.append(drone.Relay(_log, 25, parser.get('droneRelay', 'Relay4')))
relays.append(drone.Relay(_log, 12, parser.get('droneRelay', 'Relay5')))
relays.append(drone.Relay(_log, 16, parser.get('droneRelay', 'Relay6')))
relays.append(drone.Relay(_log, 20, parser.get('droneRelay', 'Relay7')))
relays.append(drone.Relay(_log, 21, parser.get('droneRelay', 'Relay8')))

for relay in relays:
    relay.turnOn(_log)
 
time.sleep(10)

for relay in relays:
    relay.turnOff(_log)
 
