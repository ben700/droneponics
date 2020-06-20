import time
import logging
import sys
import os
sys.path.append('/home/pi/droneponics')
import drone
import RPi.GPIO as GPIO  
import blynklib
import blynktimer   
from configparser import ConfigParser

_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)


parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configRelay_"+drone.gethostname()+".ini")
_log.info("/home/pi/droneponics/config/configRelay_"+drone.gethostname()+".ini")



# Initialize Blynk
_log.info("Initialize Blynk with BLYNK_AUTH = " + parser.get('blynk', 'BLYNK_AUTH'))
blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'), log=_log.info) 
timer = blynktimer.Timer()

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    relays=[0,18,23,24,25,12,16,20,21]
    Relay1 = relays[1] #feed
    Relay2 = relays[2] #fan
    Relay3 = relays[3] #Air
    Relay4 = relays[4] #heater
    Relay5 = relays[5] #Feed
    Relay6 = relays[6] #Air
    Relay7 = relays[7] #Mixer - turned off with low water 
    Relay8 = relays[8]  #Mixer - turned off with low water 

    GPIO.setup(Relay1,GPIO.OUT, initial=1)
    GPIO.setup(Relay2,GPIO.OUT, initial=1)
    GPIO.setup(Relay3,GPIO.OUT, initial=1)
    GPIO.setup(Relay4,GPIO.OUT, initial=1)
    GPIO.setup(Relay5,GPIO.OUT, initial=1)
    GPIO.setup(Relay6,GPIO.OUT, initial=1)
    GPIO.setup(Relay7,GPIO.OUT, initial=1)
    GPIO.setup(Relay8,GPIO.OUT, initial=1)
except:
   _log.info("error creating GPIO")

droneCounter = drone.DroneCounter()
droneCounter.setAutomatic()
droneCounter.reset(_log)
droneCounter.setOnCycle(_log, 1)
droneCounter.setOffCycle(_log, 1)

for x in range(11):
   _log.info("droneCounter.isAutomatic(_log)" + str(droneCounter.isAutomatic(_log)))
   _log.info("droneCounter.onCycleReset = " + str(droneCounter.onCycleReset))
   _log.info("droneCounter.offCycleReset = " + str(droneCounter.offCycleReset))
   _log.info("droneCounter.onCycle = " + str(droneCounter.onCycle))
   _log.info("droneCounter.offCycle = " + str(droneCounter.offCycle))
   _log.info("droneCounter.cycle = " + str(droneCounter.cycle))
   
   
   
   if(droneCounter.getFeedState(_log) == "On"):
        GPIO.output(relays[1],GPIO.LOW)
   else :
        GPIO.output(relays[1],GPIO.HIGH)
               
   droneCounter.incCycle(_log)
   time.sleep(5)
