colours = {1: '#FF0000', 0: '#00FF00', '1': '#FF0000', '0': '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101

import socket
import drone
from drone import Alarm, OpenWeather
import datetime
import time
import shlex, requests
import blynklib
import blynktimer
import logging
from datetime import datetime 
import RPi.GPIO as GPIO   
import sys
import os
from configparser import ConfigParser
import subprocess
import re
import json

def processButtinePressed(blynk, LED, Button, Relay,VALUE):
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        blynk.set_property(LED, 'color', colours[VALUE])
        blynk.set_property(Button, 'onBackColor', colours[VALUE])
        GPIO.output(Relay,VALUE)
        blynk.virtual_write(98,"Flipped Switch 1" + '\n')
        blynk.virtual_write(250, "Running")
        blynk.set_property(systemLED, 'color', colours[0])
