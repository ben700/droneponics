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

bootup = True
systemLED=101
rowIndex =0 

parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configOxy/"+drone.gethostname()+".ini")



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

_log.info("/home/pi/droneponics/config/configOxy/"+drone.gethostname()+".ini")

# Initialize Blynk
blynk = blynklib.Blynk(parser.get('droneOxy', 'BLYNK_AUTH'))        
timer = blynktimer.Timer()
blynk.run()
blynk.set_property(systemLED, 'color', drone.colours['ONLINE'])
_log.info("Blynk created")


nutrientMix = []
_log.info("drone.buildNutrientMix")
nutrientMix = drone.buildOxyMix(nutrientMix, _log)

sensors = []
sensors = drone.buildMonitorSensors(sensors, _log)
_log.info("All Monitor Sensors created")


relay = drone.Relay(_log, 21, "Ozone")
relay.turnOff(_log)

def processSensors():   
    for sensor in sensors:
       if sensor is not None:
          sensor.read()
                            	
    try:		
       sensors[0].color = drone.getTempColour(_log, int(round(float(sensors[0].value)*10,0)))
    except:
       _log.critical("Working out sensor colour crashed")	

    for sensor in sensors:
       if sensor is not None:
          sensor.display(blynk)

		
 def doSingleDose():   
        global rowIndex
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        for dosage in nutrientMix:		
           if(dosage.pump is not None and dosage.name == "pH"):
                   _log.info(now.strftime("%d/%m/%Y %H:%M:%S") + " Going to Dose pH")
                 #  dosage.volume = dosage.pump.query("TV,?").split("TV,")[1].strip().rstrip('\x00')
                   blynk.set_property(dosage.LED, 'color', colours[0])
                   if (float(sensors[2].target) > float(sensors[2].read())): #ph
                        _log.critical("Ph target is " + str(float(sensors[2].target)) + " and dosing but ph read is " + str(float(sensors[2].read())))
                        break			
                   dosage.pump.query("D,"+str(dosage.dose))
                   while (True):
                        dosed = dosage.pump.query("R").split(":")[1].split(",")[0].strip().rstrip('\x00')
                        if (float(dosed) >= float(dosage.dose)):
                            break	
                   blynk.set_property(dosage.LED, 'color', colours[1])
                  # dosage.volume = dosage.pump.query("TV,?").split("TV,")[1].strip().rstrip('\x00')
                   dosage.volume = float(dosage.volume) + float(dosed)
                   blynk.virtual_write(98, "159 Dose pH with " + str(dosage.dose) + "ml total volume now " + str(dosage.volume) + "ml" + '\n')
                   blynk.virtual_write(28, "add", rowIndex, dosage.name + " dosed " + str(dosage.dose) + " ml", now.strftime("%d/%m/%Y %H:%M:%S"))
                   rowIndex = rowIndex+1
                   blynk.virtual_write(29,rowIndex)  
                   blynk.virtual_write(dosage.volumePin, dosage.volume )
                   if (int(float(dosage.volume)) >= int(float(dosage.bottleSize))):
                        blynk.notify(dosage.name + " has pumped " + str(dosage.volume) + ", so may need topup")      
    
		
		
@blynk.handle_event('write V255')
def rebooter(pin, value):
    _log.info( "User reboot")
    blynk.virtual_write(250, "Reboot")
    blynk.set_property(250, 'color', drone.colours['OFFLINE'])	
    blynk.virtual_write(98, "User Reboot " + '\n')
    blynk.set_property(systemLED, 'color', drone.colours['OFFLINE'])	
    os.system('sh /home/pi/updateDroneponics.sh')
    blynk.virtual_write(98, "System updated and restarting " + '\n')
     #   os.system('sudo reboot')

@blynk.handle_event('write V41')
def fillLinePump1(pin, value):
#DO pump off, on, auto 
    global rowIndex, sensors
    sensors[1].mode = value[0]
    x=0
    _log.info( "Fill Line 1 " + str(value[0]) + '\n')
    blynk.set_property(nutrientMix[x].LED, 'color', drone.colours[value[0]])
    lVolume= nutrientMix[x].volume
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
    if(value[0] == '1'):
         _log.info("Stop Pump for " +nutrientMix[x].name )
         nutrientMix[x].pump.query("X")
    if(value[0] == '2'):	
         _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
         dosed = nutrientMix[x].pump.query("D,10").split(":")[1].strip().rstrip('\x00')
         if (float(dosed) > 0) :
              nutrientMix[x].volume = float(nutrientMix[x].volume) + float(dosed)
              blynk.virtual_write(98, "255 " + now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + str(lVolume) + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
              blynk.virtual_write(98, "256 " + now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
              blynk.virtual_write(28, "add", rowIndex, nutrientMix[x].name + " dosed " + str(dosed) + " ml", now.strftime("%d/%m/%Y %H:%M:%S"))
              rowIndex = rowIndex+1
              blynk.virtual_write(29,rowIndex)  
         blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
	 blynk.virtual_write(41,0)
    else:
         _log.info("Pump for " +nutrientMix[x].name +" set to Auto ") 
         blynk.virtual_write(98, "263 " + now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- Set to Auto" + '\n') 

@blynk.handle_event('write V42')
def fillLinePump2(pin, value):
    global rowIndex, relay
    sensors[2].mode = value[0]
    _log.info( "Fill Line 2 " + str(value[0]) + '\n')
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
    blynk.set_property(9, 'color', drone.colours[value[0]])
    if(value[0] == '1'):
        _log.info("Turn Off") 
        relay.turnOff(_log)
    elif(value[0] == '2'):
        _log.info("Turn On") 
        relay.turnOn(_log)
    else:
        _log.info("Relay is Auto")
		
			
	
	
@timer.register(interval=30, run_once=False)
def blynk_data():
    _log.info("Update Timer Run")
    blynk.virtual_write(250, "Running")
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    processSensors()

  if (float(sensors[1].target) > float(sensors[1].value) and (int(sensors[1].mode) == 3)): #DO
        _log.info("Do a dose")     
        doSingleDose()     
        blynk.virtual_write(98,"150 Auto dose h2o2"+ '\n')
       

  if(int(sensors[2].mode) == 3):
    if (float(sensors[1].target) > float(sensors[1].value)):                  
      _log.info("Turn on Oxy")
      relay.turnOn(_log) 
      blynk.virtual_write(98,"157 Auto Turn On Ozone"+ '\n')
    else:
      relay.turnOff(_log)
      blynk.virtual_write(98,"160 Auto Turn Off Ozone"+ '\n')

	
    _log.info("Completed Timer Function") 
  
while True:
   ry:
        blynk.run()
     60 timer.ruff()
        if bootup :
           blynk.virtual_write(250, "Boot")
           blynk.set_property(250, 'color', drone.colours['ONLINE'])	
           p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
           #cmdout = str(p.communicate())
           for i in range(0,9):
              blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
           bootup = False
           blynk.set_property(251, "label",drone.gethostname())
           blynk.virtual_write(251, drone.get_ip())
           now = datetime.now()
           blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
           blynk.virtual_write(systemLED, 255)
           #blynk.virtual_write(98, "clr")
           blynk.virtual_write(98, "System now updated and restarted " + '\n')
           blynk.virtual_write(255, 0)
           blynk.virtual_write(9, 255)
           blynk.virtual_write(nutrientMix[0].LED, 255)
	
           _log.info('Just Booted')
    
           _log.info("Boot Completed")

    except:
        _log.info('Unexpected error')
        blynk.virtual_write(250, "Crash")
        blynk.virtual_write(98, "System has main loop error" + '\n')
        blynk.set_property(systemLED, 'color', drone.colours['OFFLINE'])
        os.system('sh /home/pi/updateDroneponics.sh')
    #   os.system('sudo reboot') 
  
 
