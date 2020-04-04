##!/usr/bin/env python3 
BLYNK_AUTH = 'e06jzpI2zuRD4KB5eHyHdCQTGFT7einR' #i2cLogger

LED = [10,11,12,13,14,15]
VolumePin = [26,21,22,23,24,25] 

import blynklib
import blynktimer

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
colours = {0: '#FF0000', 1: '#00FF00', '0': '#FF0000', '1': '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101


try:

    # tune console logging
    _log = logging.getLogger('BlynkLog')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _log.addHandler(consoleHandler)
    _log.setLevel(logging.DEBUG)

    pH=0
    eC=9999	
    sensors = []
    nutrientMix = []
    nutrientMix = drone.buildNutrientMix(nutrientMix, _log)
    sensors = drone.buildSensors(sensors, _log)
    
    # Initialize Blynk
    blynk = blynklib.Blynk(BLYNK_AUTH)        
    timer = blynktimer.Timer()
    blynk.run()
    blynk.virtual_write(98, "clr")
    blynk.set_property(systemLED, 'color', colours['ONLINE'])

    
    
    # Initialize the sensor.
    try:
       # Create the I2C bus
       for dosage in nutrientMix:
           dosage.pump = AtlasI2C(dosage.pumpId)
       blynk.virtual_write(98, "Pumps created" + '\n') 
       for sensor in sensors:
           sensor.sensor = AtlasI2C(sensor.sensorId)
           blynk.set_property(sensor.displayPin, 'color', colours['ONLINE'])
           blynk.set_property(sensor.displayPin, 'label', sensor.name)
       blynk.virtual_write(98, "Sensors created" + '\n') 
    except:

        blynk.virtual_write(98, "Unexpected error: atlas" + '\n') 
        _log.info("Unexpected error: Atlas")
    else:
        try:	
            _log.info("Update Pump volumes")
            for dosage in nutrientMix:
                if(dosage.pump is not None):
                   #dosage.blynkMe(blynk, colours)
                   blynk.set_property(dosage.LED, 'color', colours['ONLINE'])
                   blynk.set_property(dosage.volumePin, 'color', colours['ONLINE'])
                   blynk.set_property(dosage.LED, 'label', dosage.name)
                   blynk.set_property(dosage.volumePin, 'label', dosage.name + "-TVP")
                   dosage.volume = dosage.pump.query("ATV,?").split("TV,")[1].strip().rstrip('\x00')
                   blynk.virtual_write(dosage.volumePin, dosage.volume )
                   _log.info( "Pump id " + str(dosage.pumpId) + " has dosed = " + str(dosage.volume) + '\n')
            _log.info("Pumps all read")          
        except:
            _log.info("Expected error: Use Atlas Error")
            blynk.virtual_write(98, "Expected error: Atlas Error" + '\n') 
            
            
    APP_CONNECT_PRINT_MSG = '[APP_CONNECT_EVENT]'
    APP_DISCONNECT_PRINT_MSG = '[APP_DISCONNECT_EVENT]'
    CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
    DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'
    WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
    READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
    ALLOWED_COMMANDS_LIST = ['ls', 'lsusb', 'ip a', 'ip abc']
    TWEET_MSG = "New value='{}' on VPIN({})"
	
    def doSingleDose():
	        
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " Going to Dose" + '\n')
        for dosage in nutrientMix:           
           if(dosage.pump is not None and dosage.name != "pH"):
                   dosage.volume = dosage.pump.query("TV,?").split("TV,")[1].strip().rstrip('\x00')
                   blynk.set_property(dosage.LED, 'color', colours[0])
                   dosage.pump.query("D,"+str(dosage.dose))
                   while (True):
                        dosed = dosage.pump.query("R").split(":")[1].strip().rstrip('\x00')
                        _log.info( "Pump id " + str(dosage.pumpId) + " has dosed = " + str(dosed) + "ml of "+str(dosage.dose)+"ml")
                        if (str(dosed) == '{:.2f}'.format(dosage.dose)):
                            break	
                   blynk.set_property(dosage.LED, 'color', colours[1])
                   dosage.volume = dosage.pump.query("TV,?").split("TV,")[1].strip().rstrip('\x00')
                   blynk.virtual_write(dosage.volumePin, dosage.volume )
                   
                   if (int(float(dosage.volume)) >= int(float(dosage.bottleSize))):
                        blynk.notify(dosage.name + " has pumped " + str(dosage.volume) + ", so may need topup")
           else:
                   blynk.set_property(dosage.LED, 'color', colours['OFFLINE'])	
    
    
    def doSinglePHDose():
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " Going to PH Dose" + '\n')
        for dosage in nutrientMix:
           if(dosage.pump is not None and dosage.name == "pH"):
                   blynk.set_property(dosage.LED, 'color', colours[0])
                   dosage.pump.query("D,"+str(dosage.dose))
                   while (True):
                        dosed = dosage.pump.query("R").split(":")[1].strip().rstrip('\x00')
                        _log.info( "Pump id " + str(dosage.pumpId) + " has dosed = " + str(dosed) + "ml of "+str(dosage.dose)+"ml")
                        if (str(dosed) == '{:.2f}'.format(dosage.dose)):
                            break	
                   blynk.set_property(dosage.LED, 'color', colours[1])
                   dosage.volume = dosage.pump.query("TV,?").split("TV,")[1]
                   blynk.virtual_write(dosage.volumePin, dosage.volume )
           else:
                   blynk.set_property(dosage.LED, 'color', colours['OFFLINE'])	
    
    
    @blynk.handle_event('write V1')
    def buttonV1Pressed(pin, value):
        doSingleDose()
        blynk.run()
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :Full Dosed Complete" + '\n') 
        blynk.virtual_write(1, 0)
        
    @blynk.handle_event('write V2')
    def buttonV2Pressed(pin, value):
        for i in range (11):
            doSingleDose()
        blynk.run()
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :Full Dosed Complete" + '\n') 
        blynk.virtual_write(2, 0)           

    @blynk.handle_event('write V3')
    def pauseDosing(pin, value):
        _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("P") + '\n')
        dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
        nutrientMix[x].volume = nutrientMix[x].pump.query("TV,?").split("TV,")[1]
        blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
        blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- Paused"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
        blynk.virtual_write(3, 0) 
     
    @blynk.handle_event('write V41')
    def fillLinePump1(pin, value):
        x=0
        _log.info( "Fill Line 1 " + str(value[0]) + '\n')
        lVolume= nutrientMix[x].volume
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
            nutrientMix[x].volume = nutrientMix[x].pump.query("TV,?").split("TV,")[1]
            blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + lVolume + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
        else:
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("D,*") + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 

    @blynk.handle_event('write V42')
    def fillLinePump2(pin, value):
        x=1
        _log.info( "Fill Line 2 " + str(value[0]) + '\n')
        lVolume= nutrientMix[x].volume
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("stop Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
            nutrientMix[x].volume = nutrientMix[x].pump.query("TV,?").split("TV,")[1]
            blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + lVolume + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
        else:
            _log.info("start Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("D,*") + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 

    @blynk.handle_event('write V43')
    def fillLinePump3(pin, value):
        x=2
        _log.info( "Fill Line 3 " + str(value[0]) + '\n')
        lVolume= nutrientMix[x].volume
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
            nutrientMix[x].volume = nutrientMix[x].pump.query("TV,?").split("TV,")[1]
            blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + lVolume + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
        else:
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("D,*") + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 

    @blynk.handle_event('write V44')
    def fillLinePump4(pin, value):
        x=3
        _log.info( "Fill Line 4 " + str(value[0]) + '\n')
        lVolume= nutrientMix[x].volume
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
            nutrientMix[x].volume = nutrientMix[x].pump.query("TV,?").split("TV,")[1]
            blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + lVolume + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
        else:
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("D,*") + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 

    @blynk.handle_event('write V45')
    def fillLinePump5(pin, value):
        x=4
        _log.info( "Fill Line 5 " + str(value[0]) + '\n')
        lVolume= nutrientMix[x].volume
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
            nutrientMix[x].volume = nutrientMix[x].pump.query("TV,?").split("TV,")[1]
            blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + lVolume + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
        else:
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("D,*") + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 
            
    @blynk.handle_event('write V46')
    def fillLinePump6(pin, value):
        x=5
        _log.info( "Fill Line 6 " + str(value[0]) + '\n')
        lVolume= nutrientMix[x].volume
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
            nutrientMix[x].volume = nutrientMix[x].pump.query("TV,?").split("TV,")[1]
            blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + lVolume + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
        else:
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("D,*") + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 
				
    @blynk.handle_event('write V200')
    def clearCounters(pin, value):    
        _log.info( "clear counters")
        for dosage in nutrientMix:
           if(dosage.pump is not None):
                   #dosage.pump.query("clear") 
                   dosage.volume = dosage.pump.query("TV,?").split("TV,")[1]
                   blynk.virtual_write(dosage.volumePin, dosage.volume )            
        now = datetime.now()
        blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Reset Pump Counters " + '\n') 
        blynk.virtual_write(200, 0)
    
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        _log.info( "User reboot")	
        blynk.virtual_write(98, "User Reboot " + '\n')
        for l in LED:
            blynk.set_property(l, 'color', colours['OFFLINE'])
        blynk.set_property(systemLED, 'color', colours['OFFLINE'])	
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')

	
    @timer.register(interval=60, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        #Counter.cycle += 1
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        
	#cTemp = sensors[0].read()
        
        cTemp = sensors[0].sensor.query("R").split(":")[1].strip().rstrip('\x00')
        sensors[0].value = cTemp #Temp
        sensors[1].value = sensors[1].sensor.query("RT,"+cTemp).split(":")[1].strip().rstrip('\x00') #EC
        sensors[2].value = sensors[2].sensor.query("RT,"+sensors[0].value).split(":")[1].strip().rstrip('\x00')  #pH
        if sensors[3] is not None:
            sensors[3].value = sensors[3].sensor.query("R").split(":")[1].strip().rstrip('\x00') #colour
        #_log.info( "Sensors have been read")  
        for sensor in sensors:
             if sensor is not None:
                  _log.info("Going to update pin " + str(sensor.displayPin) + " with value " + str(sensor.value))                  
                  #unhash to continue
                  #sensor.blynk()
                 # blynk.virtual_write(98, "Current " + str(sensor.name) + " reading =[" + str(sensor.value) + "]" + '\n')
                 # _log.info("Updated log")
                  blynk.virtual_write(sensor.displayPin, sensor.value)
                 # _log.info("Updated display")
        #_log.info( "Sensors displays updated")  
        if (sensors[1].target > float(sensors[1].value)): #EC
             _log.info("Do a dose")     
             doSingleDose()     
             blynk.virtual_write(98,"Automatic dose nutrient "+ '\n') 
        elif (sensors[2].target < float(sensors[2].value)): #ph
             _log.info("Do a ph dose") 
             doSinglePHDose()
             blynk.virtual_write(98,"Automatic dose Ph"+ '\n')
       
        _log.info("Completed Timer Function") 

    while True:
        try:
           blynk.run()
           if bootup :
              p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
              #cmdout = str(p.communicate())
              for i in range(0,9):
                   blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
              bootup = False
              now = datetime.now()
              blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
              for l in LED:
                  blynk.virtual_write(l, 255)
              blynk.virtual_write(systemLED, 255)
              #blynk.virtual_write(98, "clr")
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')
           timer.run()
        except:
           _log.info('Unexpected error')
           blynk.virtual_write(98, "System has main loop error" + '\n')
           for l in LED:
                blynk.set_property(l, 'color', colours['OFFLINE'])
           blynk.set_property(systemLED, 'color', colours['OFFLINE'])
           os.system('sh /home/pi/updateDroneponics.sh')
           os.system('sudo reboot') 
  
  
except KeyboardInterrupt:
   _log.info('Keyboard Interrupt')
   blynkErr = blynklib.Blynk(BLYNK_AUTH)
   for l in LED:
        blynkErr.set_property(l, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')

except:
   _log.info('Unexpected error')
   blynkErr = blynklib.Blynk(BLYNK_AUTH)
   for l in LED:
        blynkErr.set_property(l, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
