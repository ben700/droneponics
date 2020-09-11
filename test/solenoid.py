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


solenoid = drone.Solenoid(_log, 9, "Solenoid"))
while i < 10 :
    _log.info("Turn on solenoid")
    solenoid.turnOn(_log)
 
    time.sleep(10)
    
    _log.info("Turn off solenoid")
    solenoid.turnOff(_log)
    

    time.sleep(10)
    i = i + 1
