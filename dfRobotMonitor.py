#!/usr/bin/python

import logging
import blynklib
import blynktimer
from datetime import datetime
import io
import sys
import fcntl
import time
import copy
import string
from AtlasI2C import (
	 AtlasI2C
)
import RPi.GPIO as GPIO
import board
import busio
from adafruit_seesaw.seesaw import Seesaw
import os
import logging
from busio import I2C
import adafruit_bme680
import Adafruit_ADS1x15
ADS1115_REG_CONFIG_PGA_6_144V        = 0x00 # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V        = 0x02 # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V        = 0x04 # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V        = 0x06 # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V        = 0x08 # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V        = 0x0A # 0.256V range = Gain 16

from DFRobot_ADS1115 import ADS1115
from DFRobot_PH      import DFRobot_PH
from DFRobot_EC      import DFRobot_EC


 
bootup = True 

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BLYNK_GREEN     ="#23C48E"
BLYNK_BLUE      ="#04C0F8"
BLYNK_YELLOW    ="#ED9D00"
BLYNK_RED       ="#D3435C"
BLYNK_DARK_BLUE ="#5F7CD8"
colors = {'1': '#23C48E', '0': '#D3435C', 'OFFLINE': '#FF0000'}


buttFullSensor =  20
buttEmptySensor =21


Relay1 = 16



#setup sensor 2
GPIO.setup(buttFullSensor, GPIO.IN)
GPIO.setup(buttEmptySensor, GPIO.IN)
GPIO.setup(Relay1, GPIO.OUT)
GPIO.output(Relay1,GPIO.input(buttEmptySensor))   
 
# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

ads1115 = ADS1115()
ph      = DFRobot_PH()
ec      = DFRobot_EC()

ph.begin()
ec.begin()

#Set the IIC address
ads1115.setAddr_ADS1115(0x48)
#Sets the gain and input voltage range.
ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)
#Get the Digital Value of Analog of selected channel

    
# Initialize the GPIO Pins
os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm') # Turns on the Temperature module

 
# Finds the correct device file that holds the temperature data
base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'


# The ID and range of a sample spreadsheet.
BLYNK_AUTH = '00vIt07mIauITIq4q_quTOakFvcvpgGb' #robot Mon

# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)
timer = blynktimer.Timer()

APP_CONNECT_PRINT_MSG = '[APP_CONNECT_EVENT]'
APP_DISCONNECT_PRINT_MSG = '[APP_DISCONNECT_EVENT]'
CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
ALLOWED_COMMANDS_LIST = ['ls', 'lsusb', 'ip a', 'ip abc']
TWEET_MSG = "New value='{}' on VPIN({})"




@blynk.handle_event("connect")
def connect_handler():
    _log.info('SCRIPT_START')
    for pin in range(5):
        _log.info('Syncing virtual pin {}'.format(pin))
        blynk.virtual_sync(pin)

        # within connect handler after each server send operation forced socket reading is required cause:
        #  - we are not in script listening state yet
        #  - without forced reading some portion of blynk server messages can be not delivered to HW
        blynk.read_response(timeout=0.5)
    
@blynk.handle_event("write V255")
def buttonV255Pressed(value):
    blynk.virtual_write(98, "User Reboot " + '\n')
    os.system('sh /home/pi/updateDroneponics.sh')
    blynk.virtual_write(98, "System updated and restarting " + '\n')
    os.system('sudo reboot')
    
    
    
    # Will Print Every 10 Seconds
@timer.register(interval=10, run_once=False)
def blynk_data():
    _log.info("Start of blynk_data:- do actions")
    GPIO.output(Relay1,GPIO.input(buttEmptySensor))   
    _log.info("Start Logging data")
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "Log BME data")
    blynk.virtual_write(1, bme680.temperature)
    blynk.virtual_write(2, bme680.humidity)
    blynk.virtual_write(3,  bme680.pressure)
    blynk.virtual_write(4,  bme680.altitude)
    blynk.virtual_write(5,  bme680.gas)
    _log.info("Log GPIO data")
    blynk.virtual_write(37, GPIO.input(buttEmptySensor))
    blynk.virtual_write(38, GPIO.input(buttFullSensor))
        
    _log.info("Log ADC data")
    temperature = 25
    adc0 = ads1115.readVoltage(0) #ph
    adc1 = ads1115.readVoltage(1) #ec
    adc2 = ads1115.readVoltage(2) #co2
    adc3 = ads1115.readVoltage(3) #light
    print(adc2)
	
    _log.info("Read Ph data")
    #Convert voltage to PH with temperature compensation
    pH = ph.readPH(adc0['r'],temperature)
    _log.info("pH Value ={}".format(pH))
    
    _log.info("Read EC data")
    eC = ec.readEC(adc1['r'],temperature)
    _log.info("eC Value ={}".format(eC))
    
    _log.info("Read CO2 data")
    sensorValue = adc2['r']
    blynk.virtual_write(10, sensorValue)
    
    _log.info("sensorValue ={}".format(sensorValue))
    voltage = sensorValue*(5000/1024.0)
    _log.info("voltage ={}".format(voltage))
    if(voltage == 0):
       _log.info("Fault")
   # elif(voltage < 400): 
   #    _log.info("preheating")
   # else:
   #    voltage_diference=voltage-400
   #    _log.info("voltage ={}".format(voltage_diference))
   #    concentration=voltage_diference*50.0/16.0
   #    _log.info("concentration ={}".format(concentration))
      
    
    _log.debug("Read Light data")
    light = adc3['r']
    blynk.virtual_write(13, light)
    _log.info("light ={}".format(light))
    blynk.virtual_write(98, "Completed Timer Function" + '\n') 
    
    
    
while True:
    try:
       blynk.run()
       if bootup :
          bootup = False
          now = datetime.now()
          blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
          blynk.virtual_write(98, "clr")
          blynk.virtual_write(98, "System now updated and restarted " + '\n')
          blynk.virtual_write(255, 0)
          _log.info('Just Booted')
          
       timer.run()
    except:
       _log.info('Unexpected error')
       os.system('sh /home/pi/updateDroneponics.sh')
    