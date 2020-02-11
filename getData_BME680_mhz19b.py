from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import time
import mh_z19
import bme680
import BlynkLib
from BlynkTimer import BlynkTimer

BLYNK_AUTH = 'PU0e7o-qX5ZgGSi5seA-ieutDWJGbIpW'


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/gmail.send']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1iXetyC5Tqg4kvSs-bFt5BiAsYL5_0O3R-XNEmSUJsLs'
RANGE_NAME = 'BME680!A:D'


# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)


def updateGoogle(Temperature, Pressure, Humidity, Gas, CO2):
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
    values = [[str(datetime.datetime.now()), Temperature, Pressure, Humidity, Gas, CO2]]
    body = {'values' : values }
    result = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                                 valueInputOption='USER_ENTERED', body=body).execute()

    
    
    
# Will Print Every 5 Seconds
def blynk_data():
    
    sensor.get_sensor_data()
    
    while (sensor.data.heat_stable == False):
      time.sleep(1)
      sensor.get_sensor_data()

    mhz19b = mh_z19.read()

    
    blynk.virtual_write(4, sensor.data.temperature)
    blynk.virtual_write(5, sensor.data.pressure)
    blynk.virtual_write(6, sensor.data.humidity)
    blynk.virtual_write(10,data.gas_resistance)
    blynk.virtual_write(11, mhz19b['co2'])

    
    updateGoogle(str("{0:.2f}".format(temperature)),
        str("{0:.2f}".format(pressure)),
        str("{0:.2f}".format(humidity)),
        str("{0:.2f}".format(tslData['full'])),
        str("{0:.2f}".format(tslData['lux'])),           
        str("{0:.2f}".format(tslData['ir'])))
    
   
# Add Timers
timer.set_interval(10, blynk_data)


while True:
    blynk.run()
    timer.run()

