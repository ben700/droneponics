##!/usr/bin/env python3 

LED = [10,11,12,13,14,15]
VolumePin = [26,21,22,23,24,25] 
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
alarmList=[]
#load Temperature alarms
alarmList.append(Alarm('temperature', "low", "low",18.0, Notify=False,  Message = 'Low TEMP!!!', Colour = '#c0392b'))
alarmList.append(Alarm('temperature', "High", "high", 26.0, Notify=False, Message = 'High TEMP!!!', Colour = '#c0392b'))
alarmList.append(Alarm('temperature', "low", "lowlow", 15.0, Notify=True,  Message = 'Low Low TEMP!!!', Colour = '#c0392b'))
alarmList.append(Alarm('temperature', "High", "highhigh", 30.0,Notify=True, Message = 'High High TEMP!!!', Colour = '#c0392b'))

#from drone import Alarm, OpenWeather
#sensorList=[]
#load Temperature alarms
#sensorList.append(PH())
#sensorList.append(EC())
#sensorList.append(TEMP())#


bootup = True
colours = {0: '#FF0000', 1: '#00FF00', '0': '#FF0000', '1': '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101
rowIndex=1

parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configDoser/"+drone.gethostname()+".ini")


try:

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

    _log.info("/home/pi/droneponics/config/configRelay/"+drone.gethostname()+".ini")

    pH=0
    eC=9999	
    sensors = []
    nutrientMix = []
    _log.info("drone.buildNutrientMix")
    nutrientMix = drone.buildNutrientMix(nutrientMix, _log, scheduleWeek='Grow')
    _log.info("drone.buildSensors(sensors")
    sensors = drone.buildSensors(sensors, _log)
    _log.info("all senses created")
    lcdDisplay=drone.Display(_log)
    _log.info("all senses created")
		

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    relays=[]
    relays.append(drone.Relay(_log, 18, parser.get('droneRelay', 'Relay1')))
    relays.append(drone.Relay(_log, 23, parser.get('droneRelay', 'Relay2')))
    relays.append(drone.Relay(_log, 24, parser.get('droneRelay', 'Relay3')))
    relays.append(drone.Relay(_log, 25, parser.get('droneRelay', 'Relay4')))
    

    #relays[0].setInfoPin(24)
        

    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('droneDoser', 'BLYNK_AUTH'))        
    timer = blynktimer.Timer()
    blynk.run()
    #blynk.virtual_write(98, "clr")
    blynk.set_property(systemLED, 'color', colours['ONLINE'])
    _log.info("Blynk created")
    
    # Initialize the sensor.
    try:
       # Create the I2C bus
       for dosage in nutrientMix:
           _log.info("Pre Pump" + str(dosage.pumpId))
           dosage.pump = AtlasI2C(dosage.pumpId)
           _log.info("Pump" + str(dosage.pumpId))
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
                   #dosage.volume = dosage.pump.query("ATV,?").split("TV,")[1].strip().rstrip('\x00')
                   dosage.volume = dosage.pump.query("ATV,?").split("TV,")[1].split(".")[0].strip().rstrip('\x00')
                   blynk.virtual_write(dosage.volumePin, dosage.volume )
                  # blynk.virtual_write(98, dosage.name + " " + dosage.pump.query("O,V,1").strip().rstrip('\x00') + '\n')
                  # blynk.virtual_write(98, dosage.name + " " + dosage.pump.query("O,TV,0").strip().rstrip('\x00') + '\n')
                  # blynk.virtual_write(98, dosage.name + " " + dosage.pump.query("O,ATV,0").strip().rstrip('\x00') + '\n')
                  # blynk.virtual_write(98, dosage.name + " " + dosage.pump.query("O,?").strip().rstrip('\x00') + '\n')
                   #blynk.virtual_write(98, dosage.name + " TV =" + dosage.pump.query("TV,?").strip().rstrip('\x00') + '\n')
                   #blynk.virtual_write(98, dosage.name + " ATV =" + dosage.pump.query("ATV,?").strip().rstrip('\x00') + '\n')
                   #blynk.virtual_write(98, dosage.name + " R =" + dosage.pump.query("R").strip().rstrip('\x00') + '\n')
                   #blynk.virtual_write(98, dosage.name + " Pump id " + str(dosage.pumpId) + " has dosed = " + str(dosage.volume) + '\n')
            _log.info("Pumps all read")          
        except:
            _log.info("Expected error: Use Atlas Error")
            blynk.virtual_write(98, "Expected error: Atlas Error" + '\n') 
            
	
    def doSingleDose():        
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " Going to Dose" + '\n')
        for dosage in nutrientMix:
           if(dosage.pump is not None and dosage.name != "pH"):
                   blynk.virtual_write(98,now.strftime("%d/%m/%Y %H:%M:%S") + " Going to Dose " +str (dosage.name)+ '\n')
                   dosage.volume = dosage.pump.query("TV,?").split("TV,")[1].strip().rstrip('\x00')
                   blynk.set_property(dosage.LED, 'color', colours[0])
                   dosage.pump.query("D,"+str(dosage.dose))
                   while (True):
                        dosed = dosage.pump.query("R").split(":")[1].split(",")[0].strip().rstrip('\x00')
                        if (float(dosed) >= float(dosage.dose)):
                            break	
                   blynk.set_property(dosage.LED, 'color', colours[1])
                  # dosage.volume = dosage.pump.query("TV,?").split("TV,")[1].strip().rstrip('\x00')
                   dosage.volume = dosage.pump.query("TV,?").split("TV,")[1].split(".")[0].strip().rstrip('\x00')
                   blynk.virtual_write(dosage.volumePin, dosage.volume )
                   blynk.virtual_write(98,"Check to see if user needs notify" + '\n')
                   if (int(float(dosage.volume)) >= int(float(dosage.bottleSize))):
                        if not dosage.notify :
                             blynk.notify(dosage.name + " has pumped " + str(dosage.volume) + ", so may need topup")	
                             dosage.notify = True
    
    def doSinglePHDose():   
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " Going to Dose pH" + '\n')
        for dosage in nutrientMix:		
           if(dosage.pump is not None and dosage.name == "pH"):
                   dosage.volume = dosage.pump.query("TV,?").split("TV,")[1].strip().rstrip('\x00')
                   blynk.set_property(dosage.LED, 'color', colours[0])
                   dosage.pump.query("D,"+str(dosage.dose))
                   while (True):
                        dosed = dosage.pump.query("R").split(":")[1].split(",")[0].strip().rstrip('\x00')
                        if (float(dosed) >= float(dosage.dose)):
                            break	
                   blynk.set_property(dosage.LED, 'color', colours[1])
                  # dosage.volume = dosage.pump.query("TV,?").split("TV,")[1].strip().rstrip('\x00')
                   dosage.volume = dosage.pump.query("TV,?").split("TV,")[1].split(".")[0].strip().rstrip('\x00')
                   blynk.virtual_write(dosage.volumePin, dosage.volume )
                   if (int(float(dosage.volume)) >= int(float(dosage.bottleSize))):
                        blynk.notify(dosage.name + " has pumped " + str(dosage.volume) + ", so may need topup")      
    
    @blynk.handle_event('write V1')
    def write_handler(pin, value):
        staus = value[0]
        relay = 0       
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing off relay " + relays[relay].name)
                 relays[relay].turnOff(_log)
                 relays[relay].setManual("Off")
                 _log.debug(relays[relay].name + " in now off : v1write_handler completed")
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
                
           blynk.virtual_write(250, "Stopped")
        elif (staus is "2" ):
           try:
                 _log.debug("in v1write_handler turing on relay")
                 relays[relay].turnOn(_log)
                 relays[relay].setManual("On")
                 _log.debug(relays[relay].name + " in now on : v1write_handler completed")
                 
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning on")
           blynk.virtual_write(250, "Feeding")
        else:
           try:
                 _log.debug("in v1write_handler turing on relay")
                 relays[relay].setAutomatic()
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning auto")
           blynk.virtual_write(250, "Auto")
           relays[relay].cycleOnReset()
           relays[relay].setOffCycleReset() 
        blynk.virtual_write(relays[relay].getInfoPin(), relays[relay].info())
                 
                

    @blynk.handle_event('write V2')
    def write_handler(pin, value):  
        staus = value[0]
        relay = 1
        _log.debug("in v2write_handler and the staus = " + str(value[0]))
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing on relay " + relays[relay].name)
                 relays[relay].turnOn(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning On")
        else:
           try:
                 _log.debug("in v2write_handler turing off relay")
                 relays[relay].turnOff(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
                
    @blynk.handle_event('write V3')
    def write_handler(pin, value):  
        staus = value[0]
        relay = 2
        _log.debug("in v2write_handler and the staus = " + str(value[0]))
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing on relay " + relays[relay].name)
                 relays[relay].turnOn(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning On")
        else:
           try:
                 _log.debug("in v2write_handler turing off relay")
                 relays[relay].turnOff(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
 

    @blynk.handle_event('write V4')
    def write_handler(pin, value):  
        staus = value[0]
        relay = 3
        _log.debug("in v2write_handler and the staus = " + str(value[0]))
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing on relay " + relays[relay].name)
                 relays[relay].turnOn(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning On")
        else:
           try:
                 _log.debug("in v2write_handler turing off relay")
                 relays[relay].turnOff(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
                
 
    @blynk.handle_event('write V5')
    def write_handler(pin, value):  
        staus = value[0]
        relay = 4
        _log.debug("in v2write_handler and the staus = " + str(value[0]))
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing on relay " + relays[relay].name)
                 relays[relay].turnOn(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning On")
        else:
           try:
                 _log.debug("in v2write_handler turing off relay")
                 relays[relay].turnOff(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")
                
 
    @blynk.handle_event('write V6')
    def write_handler(pin, value):  
        staus = value[0]
        relay = 5
        _log.debug("in v2write_handler and the staus = " + str(value[0]))
        if (staus is "1" ):
           try:
                 _log.debug("in v"+str(relay+1)+"write_handler turing on relay " + relays[relay].name)
                 relays[relay].turnOn(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning On")
        else:
           try:
                 _log.debug("in v2write_handler turing off relay")
                 relays[relay].turnOff(_log)
           except:
                 _log.error("Except handle_event V"+str(relay+1)+" Turning Off")

                
    @blynk.handle_event('write V7')
    def v7write_handler(pin, value):
        staus = value[0]
        relay = 6
        if (staus is "1" ):
            try:
                 _log.debug("in v7write_handler and turning off relay " + relays[relay].name + " on pin " + str(relays[relay].gpioPin))
                 relays[relay].turnOff(_log)
                 _log.debug("waste turnOff() completed")
                 relays[relay].setManual("Off")
                 _log.debug("waste setManual() completed")
                 blynk.virtual_write(relays[relay].getInfoPin(), relays[relay].info())
                 _log.debug("in v7write_handler and turning off relay completed")
            except:
                 _log.error("Except handle_event V7 Turning Off waste")
                 blynk.virtual_write(28, "Except handle_event V7 Turning Off waste")           
        elif (staus is "2" ):
            try:
                 _log.debug("in v7write_handler and turning on relay " + relays[relay].name + " on pin " + str(relays[relay].gpioPin))
                 relays[relay].turnOn(_log)
                 relays[relay].setManual("On")
                 blynk.virtual_write(relays[relay].getInfoPin(), relays[relay].info())
                 _log.debug("in v7write_handler and turning on relay completed")
            except:
                 _log.error("Except handle_event V7 Turning on waste")
                 blynk.virtual_write(relays[relay].getInfoPin(), "Except handle_event V7 Turning on waste")
        else : 
            try:
                 _log.debug("in v7write_handler and turning relay " + relays[relay].name + " auto on pin " + str(relays[relay].gpioPin))
                 relays[relay].setAutomatic() 
                 _log.debug("waste setAutomatic()")
                 relays[relay].cycleOnReset()
                 _log.debug("waste cycleReset()")
                 relays[relay].cycleOffResetClear()
                 blynk.virtual_write(relays[relay].getInfoPin(), relays[relay].info())
                 _log.debug("waste cycleOffResetClear()")
            except:
                 _log.error("Except handle_event V7 Turning waste auto")
                 blynk.virtual_write(relays[relay].getInfoPin(), "Except handle_event V7 Turning waste auto")
                 
                
    @blynk.handle_event('write V8')
    def write_handler(pin, value):
        relay = 7
        relays[relay].setTimer(int(value[0]), int(value[1]))

    @blynk.handle_event('write V35')
    def v25write_handler(pin, value):
        relays[0].cycleResetSet(value[0])
        blynk.virtual_write(relays[0].getInfoPin(), relays[0].info())
        
    @blynk.handle_event('write V36')
    def v26write_handler(pin, value):
        relays[0].cycleOffResetSet(value[0])
        blynk.virtual_write(relays[0].getInfoPin(), relays[0].info())
         
    @blynk.handle_event('write V37')
    def v27write_handler(pin, value):
        relays[6].cycleResetSet(value[0])
        relays[6].cycleOffResetClear()
        blynk.virtual_write(relays[0].getInfoPin(), relays[0].info())
    
    @blynk.handle_event('write V29')
    def v29write_handler(pin, value):
        _log.debug("v29write_handler rowIndex =" + str(value[0]))
        global rowIndex
        rowIndex = int(value[0])
          
    @blynk.handle_event('write V96')
    def v96write_handler(pin, value):
        _log.debug("v96write_handler")
        blynk.virtual_write(97,"clr")
        blynk.virtual_write(96,0)
        blynk.virtual_write(29,0)
      
    @blynk.handle_event('write V111')
    def buttonV1Pressed(pin, value):
        doSingleDose()
        blynk.run()
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :Full Dosed Complete" + '\n') 
        blynk.virtual_write(1, 0)
          
     
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
	
    @blynk.handle_event("connect")
    def connect_handler():
        _log.warning("Connected")
        for pin in range(0,11):
           _log.info('Syncing virtual buttons {}'.format(pin))
           blynk.virtual_sync(pin)
           blynk.read_response(timeout=0.5)
        for pin in range(24,30):
           _log.info('Syncing virtual buttons {}'.format(pin))
           blynk.virtual_sync(pin)
           blynk.read_response(timeout=0.5)
        blynk.virtual_write(250, "Connected")
	
    @timer.register(interval=60, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))

        cTemp = sensors[0].sensor.query("R").split(":")[1].strip().rstrip('\x00')
        if (float(cTemp) < 0) :
             _log.critical("cTemp = " + str(cTemp))
        else :
             _log.critical("cTemp -ve = " + str(cTemp))
    
        sensors[0].value = cTemp #Temp
        sensors[1].value = sensors[1].sensor.query("RT,"+cTemp).split(":")[1].strip().rstrip('\x00') #EC
        sensors[2].value = sensors[2].sensor.query("RT,"+sensors[0].value).split(":")[1].strip().rstrip('\x00')  #pH
     #   if sensors[3] is not None and sensors[3].sensor is not None:
     #       sensors[3].value = sensors[3].sensor.query("R").split(":")[1].strip().rstrip('\x00') #colour
     #       blynk.virtual_write(34, sensors[3].value.split(",")[0])
     #       blynk.virtual_write(35, sensors[3].value.split(",")[1])
     #       blynk.virtual_write(36, sensors[3].value.split(",")[2])
        for sensor in sensors:
             if sensor is not None:
                  _log.info("Going to update " + str(sensor.name) + "using pin " + str(sensor.displayPin) + " with value " + str(sensor.value))                  
                  #unhash to continue
                  #sensor.blynk()
                  blynk.virtual_write(98, "Current " + str(sensor.name) + " reading =[" + str(sensor.value) + "]" + '\n')
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
       
        if (parser.get('blynkBridge', 'BLYNK_AUTH', fallback=None) is not None):
            _log.warning("Send Temp data via blynkBridge")
            blynkBridge = blynklib.Blynk(parser.get('blynkBridge', 'BLYNK_AUTH'))
            blynkBridge.run()
            TEMP_VPIN = parser.get('blynkBridge', 'TEMP_VPIN', fallback=30)
            blynkBridge.virtual_write(TEMP_VPIN, cTemp)
            blynkBridge.set_property(TEMP_VPIN, 'label', "from " + drone.gethostname())
            blynkBridge.virtual_sync(30)
            _log.info("blynkBridge Temp data sent")


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
              blynk.set_property(251, "label",drone.gethostname())
              blynk.virtual_write(251, drone.get_ip())
              x = 1 
              for relay in relays:
                 relay.setBlynkLabel(blynk, x, 10+x)
                 x = x +1 
              now = datetime.now()
              blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
              blynk.virtual_write(97, "add", rowIndex, "Reboot", now.strftime("%d/%m/%Y %H:%M:%S"))
              blynk.virtual_write(29,rowIndex+1)
              for l in LED:
                  blynk.virtual_write(l, 255)
              blynk.virtual_write(systemLED, 255)
              #blynk.virtual_write(98, "clr")
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')
              text= ""
              sPH= ""
              sEC= ""
              sTemp= ""
		
              cTemp = sensors[0].sensor.query("R").split(":")[1].strip().rstrip('\x00')
              sensors[0].value = cTemp #Temp 
              if (float(cTemp) <= 2) :
                    sTemp= "NO TEMP PROBE. "
                    _log.critical(sTemp)
                    text = text + sTemp
                    cTemp="20.00"
              else:
                    sTemp= "TEMP PROBE FOUND : " + sensors[0].value
                    _log.critical(sTemp)
			
              _log.info(sensors[0].sensor.query("I"))
              _log.info(sensors[0].sensor.query("Status"))
              tempCal = sensors[0].sensor.query("Cal,?")
              _log.info(tempCal)
              _log.info(sensors[0].sensor.query("S,?"))
              tempCal = tempCal.split("CAL,")[1].strip()
              tempCal = " " + tempCal + " "
              tempCalPoints = tempCal[1]
              if(tempCalPoints == "0"):	
                    cTemp= "TEMP Not CAL. "
                    _log.critical(cTemp)
                    text = text + cTemp
              else:
                    cTemp= "TEMP CAL to " + tempCalPoints +" points."
              
		
              
              sensors[1].value = sensors[1].sensor.query("RT,"+cTemp).split(":")[1].strip().rstrip('\x00') #EC
              sensors[2].value = sensors[2].sensor.query("RT,"+sensors[0].value).split(":")[1].strip().rstrip('\x00')  #pH
			    
              if(float(sensors[1].value) <= 2):
                    sEC= "NO EC PROBE. "
                    _log.critical(sEC)
                    text = text + sEC
              else:
                    sEC= "EC PROBE FOUND : " + sensors[1].value
                    _log.critical(sEC)
				
              _log.info(sensors[1].sensor.query("I"))
              _log.info(sensors[1].sensor.query("Status"))
              _log.info(sensors[1].sensor.query("K,?"))
              ecCal = sensors[1].sensor.query("Cal,?")
              _log.info(ecCal)		
              ecCal = ecCal.split("CAL,")[1].strip().rstrip('\x00')
              ecCal = " " + ecCal + " "	
              ecCalPoints = ecCal[1] 
             
              if(ecCalPoints == "0"):		
                    _log.critical("EC Not CAL : " + ecCal)
                    text = text + "EC Not CAL. "
              
              if(float(sensors[2].value) <= 0):
                    sPH="NO pH PROBE. "
                    _log.critical(sPH)
                    text = text + sPH
              else:
                    sPH="pH PROBE FOUND : " + sensors[2].value
                    _log.critical(sPH)
              
              _log.info(sensors[2].sensor.query("I"))
              _log.info(sensors[2].sensor.query("Status"))
              pHCal = sensors[2].sensor.query("Cal,?")
              _log.info(pHCal)
              _log.info(sensors[2].sensor.query("Slope,?"))
              pHCal = pHCal.split("CAL,")[1].strip().rstrip('\x00')
              pHCal = " " + pHCal + " "	
              pHCalPoints = pHCal[1] 
              if(pHCalPoints == "0"):		
                    _log.critical("pH Not CAL : " + pHCal)
                    text = text + "pH Not CAL. "
              
              blynk.virtual_write(240, text)
              lcdDisplay.updateLCDProbe (sPH, sEC, sTemp)
              if (text == ""):
                   blynk.set_property(240, 'color', colours['ONLINE'])
              else:
                   blynk.set_property(240, 'color', colours['OFFLINE'])

              timer.run()
        except:
           _log.info('Unexpected error')
           blynk.virtual_write(98, "System has main loop error" + '\n')
           for l in LED:
                blynk.set_property(l, 'color', colours['OFFLINE'])
           blynk.set_property(systemLED, 'color', colours['OFFLINE'])
           os.system('sh /home/pi/updateDroneponics.sh')
    #       os.system('sudo reboot') 
  
   
except KeyboardInterrupt:
   _log.info('Keyboard Interrupt')
   blynkErr = blynklib.Blynk(parser.get('droneDoser', 'BLYNK_AUTH'))
   for l in LED:
        blynkErr.set_property(l, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
#   os.system('sudo reboot')

except:
   _log.info('Unexpected error')
   blynkErr = blynklib.Blynk(parser.get('droneDoser', 'BLYNK_AUTH'))
   for l in LED:
        blynkErr.set_property(l, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
 #  os.system('sudo reboot')
