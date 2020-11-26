##!/usr/bin/env python3 
import blynklib
import blynktimer
from configparser import ConfigParser
from datetime import datetime
import time
import logging
import sys
import os
import RPi.GPIO as GPIO

from AtlasI2C import (
   AtlasI2C
)
import math  
import subprocess
import re
import drone

from drone import Alarm, OpenWeather
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '15k0r_tAI1dmK_to0wwvIW8E1wyUqH-mhEMQgRs3X_9U'
RANGE_NAME = 'CO2!A:E'


parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configMonitor/"+drone.gethostname()+".ini")

# tune console logging
_log = logging.getLogger('BlynkLog')
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

_log.info("/home/pi/droneponics/config/configMonitor/"+drone.gethostname()+".ini")
sensors[]
sensors = drone.buildCO2Sensors(sensors, _log)
sensor = sensors[0]
def updateGoogle(CO2):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
   
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    values = [[str(datetime.datetime.now()), CO2]]
    body = {'values' : values }
    result = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                                 valueInputOption='USER_ENTERED', body=body).execute() 
                                                                  
                                 
def processSensors():   
    if sensor is not None:
        sensor.read()
        updateGoogle(sensor.value)
        
if __name__ == "__main__":
    processSensors()        
