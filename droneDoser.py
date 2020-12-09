##!/usr/bin/env python3 

LED = [10,11,12,13,14,15,16]

import blynklib
import blynktimer
from configparser import ConfigParser
from datetime import datetime
import time
import logging
import sys
import os
sys.path.append('/home/pi/droneponics')
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

    _log.info("/home/pi/droneponics/config/configDoser/"+drone.gethostname()+".ini")

    pH=0
    eC=9999	
    sensors = []
    nutrientMix = []
    _log.info("drone.buildNutrientMix")
    nutrientMix = drone.buildNutrientMix(nutrientMix, _log, scheduleWeek='Grow')
    _log.info("drone.buildSensors(sensors")
    sensors = drone.buildSensors(sensors, _log)
    _log.info("all senses created")
	
	

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
       labelPin = 70
       for dosage in nutrientMix:
           dosage.pump = AtlasI2C(dosage.pumpId)
           _log.info("Created Pump" + str(dosage.pumpId))
           blynk.set_property(labelPin, 'label', dosage.name)
           labelPin = labelPin + 1
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
                   blynk.set_property(100+dosage.volumePin, 'color', colours['ONLINE'])
                   blynk.set_property(100+dosage.volumePin, 'label', dosage.name + "- Bottle Size")
                   blynk.virtual_write(100+dosage.volumePin, dosage.bottleSize )
                   #dosage.volume = dosage.pump.query("ATV,?").split("TV,")[1].strip().rstrip('\x00')
                   #dosage.volume = dosage.pump.query("ATV,?").split("TV,")[1].split(".")[0].strip().rstrip('\x00')
                 #  blynk.virtual_write(dosage.volumePin, dosage.volume )
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
        global rowIndex
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        _log.info(now.strftime("%d/%m/%Y %H:%M:%S") + " Going to Dose nutrients")
        for dosage in nutrientMix:
           if(dosage.pump is not None and dosage.name != "pH"):
                   if(str(dosage.dose) == "0.0"):
                        continue
                   blynk.virtual_write(98,now.strftime("%d/%m/%Y %H:%M:%S") + " Going to Dose " +str (dosage.name)+ '\n')
                   #dosage.volume = dosage.pump.query("TV,?").split("TV,")[1].strip().rstrip('\x00')
                   blynk.set_property(dosage.LED, 'color', colours[0])
                   dosage.pump.query("D,"+str(dosage.dose))
                   while (True):
                        dosed = dosage.pump.query("R").split(":")[1].split(",")[0].strip().rstrip('\x00')
                        if (float(dosed) >= float(dosage.dose)):
                            break	
                   blynk.set_property(dosage.LED, 'color', colours[1])
                  # dosage.volume = dosage.pump.query("TV,?").split("TV,")[1].strip().rstrip('\x00')
                   dosage.volume = float(dosage.volume) + float(dosed)
                   blynk.virtual_write(dosage.volumePin, dosage.volume )
                   blynk.virtual_write(98, "Dose " + dosage.name + " with " + str(dosage.dose) + "ml total volume now " + str(dosage.volume) + "ml" + '\n')
                   blynk.virtual_write(28, "add", rowIndex, dosage.name + " dosed " + str(dosage.dose) + " ml", now.strftime("%d/%m/%Y %H:%M:%S"))
                   rowIndex = rowIndex+1
                   blynk.virtual_write(29,rowIndex)  
                   _log.debug("Check to see if user needs notify")
                   if (int(float(dosage.volume)) >= int(float(dosage.bottleSize))):
                        if not dosage.notify :
                             blynk.notify(dosage.name + " has pumped " + str(dosage.volume) + ", so may need topup")	
                             dosage.notify = True
    
    def doSinglePHDose():   
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
                   blynk.virtual_write(98, "Dose pH with " + str(dosage.dose) + "ml total volume now " + str(dosage.volume) + "ml" + '\n')
                   blynk.virtual_write(28, "add", rowIndex, dosage.name + " dosed " + str(dosage.dose) + " ml", now.strftime("%d/%m/%Y %H:%M:%S"))
                   rowIndex = rowIndex+1
                   blynk.virtual_write(29,rowIndex)  
                   blynk.virtual_write(dosage.volumePin, dosage.volume )
                   if (int(float(dosage.volume)) >= int(float(dosage.bottleSize))):
                        blynk.notify(dosage.name + " has pumped " + str(dosage.volume) + ", so may need topup")      
    
    def processSensors():   
        for sensor in sensors:
           if sensor is not None:
              sensor.read()
                            	
        try:		
           sensors[0].color = drone.getTempColour(_log, int(round(float(sensors[0].value)*10,0)))
           sensors[1].color = drone.getECColour(_log, round(float(sensors[1].value),0))
           sensors[2].color = drone.getPHColour(_log, round(float(sensors[2].value)*10,0))
        except:
           _log.critical("Working out sensor colour crashed")	
           _log.critical("sensors[0].value = " + str(sensors[0].value))
           _log.critical("sensors[1].value = " + str(sensors[1].value))
           _log.critical("sensors[2].value = " + str(sensors[2].value))
           _log.critical("sensors[0].colour = " + str(drone.getTempColour(_log, int(round(float(sensors[0].value)*10,0)))))
           _log.critical("sensors[1].colour = " + str(drone.getECColour(_log, round(float(sensors[1].value),0))))
           _log.critical("sensors[2].colour = " + str(drone.getPHColour(_log, round(float(sensors[2].value)*10,0))))

        for sensor in sensors:
           if sensor is not None:
              sensor.display(blynk)
   
	

    @blynk.handle_event('write V27')
    def v27write_handler(pin, value):
        global rowIndex, nutrientMix
        rowIndex = 0
        for dosage in nutrientMix:
             dosage.volume =0
             dosage.pump.query("clear")
             blynk.virtual_write(dosage.volumePin, dosage.volume )
             _log.info("reset TVP for " + dosage.name + " to " + str(dosage.volume) + " using pin " + str(dosage.volumePin))
        blynk.virtual_write(29, rowIndex)
        blynk.virtual_write(28, "clr")
        blynk.virtual_write(27, 0)
        blynk.virtual_write(98, "Reset the pump volume counters"+'\n')
      
	
    @blynk.handle_event('write V29')
    def v29write_handler(pin, value):
        global rowIndex
        rowIndex = int(value[0])
        

    
    @blynk.handle_event('write V38')
    def v38write_handler(pin, value): 
        sensors[1].target = float(value[0])
        blynk.virtual_write(98, "EC Trigger Level set to " + str(sensors[1].target)+ '\n') 
			    
    @blynk.handle_event('write V39')
    def v39write_handler(pin, value):
        sensors[1].mode = value[0]
        blynk.virtual_write(98, "EC Mode set to " + str(sensors[1].mode)+ '\n')
    
    @blynk.handle_event('write V48')
    def v48write_handler(pin, value): 
        sensors[2].target = float(value[0])
        blynk.virtual_write(98, "pH Trigger Level set to " + str(sensors[2].target) + '\n') 
		
    @blynk.handle_event('write V49')
    def v49write_handler(pin, value):
        sensors[2].mode = value[0]
        blynk.virtual_write(98, "pH Mode set to " + str(sensors[2].mode)+ '\n')
 	
     
    @blynk.handle_event('write V41')
    def fillLinePump1(pin, value):
        global rowIndex
        x=0
        _log.info( "Fill Line 1 " + str(value[0]) + '\n')
        lVolume= nutrientMix[x].volume
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
        #    volumeThisTime = nutrientMix[x].pump.query("TV,?").split("TV,")[1]
            if (float(dosed) > 0) :
                 nutrientMix[x].volume = float(nutrientMix[x].volume) + float(dosed)
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + str(lVolume) + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
                 blynk.virtual_write(28, "add", rowIndex, nutrientMix[x].name + " dosed " + str(dosed) + " ml", now.strftime("%d/%m/%Y %H:%M:%S"))
                 rowIndex = rowIndex+1
                 blynk.virtual_write(29,rowIndex)  
            blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
        else:
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("D,*") + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 

    @blynk.handle_event('write V42')
    def fillLinePump2(pin, value):
        global rowIndex
        x=1
        _log.info( "Fill Line 2 " + str(value[0]) + '\n')
        lVolume= nutrientMix[x].volume
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("stop Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
            if (float(dosed) > 0) :
                 nutrientMix[x].volume = float(nutrientMix[x].volume) + float(dosed)
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + str(lVolume) + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
                 blynk.virtual_write(28, "add", rowIndex, nutrientMix[x].name + " dosed " + str(dosed) + " ml", now.strftime("%d/%m/%Y %H:%M:%S"))
                 rowIndex = rowIndex+1
                 blynk.virtual_write(29,rowIndex)  
            blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
        else:
            _log.info("start Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("D,*") + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 

    @blynk.handle_event('write V43')
    def fillLinePump3(pin, value):
        global rowIndex
        x=2
        _log.info( "Fill Line 3 " + str(value[0]) + '\n')
        lVolume= nutrientMix[x].volume
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
            if (float(dosed) > 0) :
                 nutrientMix[x].volume = float(nutrientMix[x].volume) + float(dosed)
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + str(lVolume) + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
                 blynk.virtual_write(28, "add", rowIndex, nutrientMix[x].name + " dosed " + str(dosed) + " ml", now.strftime("%d/%m/%Y %H:%M:%S"))
                 rowIndex = rowIndex+1
                 blynk.virtual_write(29,rowIndex)  
            blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
        else:
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("D,*") + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 

    @blynk.handle_event('write V44')
    def fillLinePump4(pin, value):
        global rowIndex
        x=3
        _log.info( "Fill Line 4 " + str(value[0]) + '\n')
        lVolume= nutrientMix[x].volume
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
            if (float(dosed) > 0) :
                 nutrientMix[x].volume = float(nutrientMix[x].volume) + float(dosed)
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + str(lVolume) + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
                 blynk.virtual_write(28, "add", rowIndex, nutrientMix[x].name + " dosed " + str(dosed) + " ml", now.strftime("%d/%m/%Y %H:%M:%S"))
                 rowIndex = rowIndex+1
                 blynk.virtual_write(29,rowIndex)  
            blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
        else:
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("D,*") + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 

    @blynk.handle_event('write V45')
    def fillLinePump5(pin, value):
        global rowIndex
        x=4
        _log.info( "Fill Line 5 " + str(value[0]) + '\n')
        lVolume= nutrientMix[x].volume
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
            if (float(dosed) > 0) :
                 nutrientMix[x].volume = float(nutrientMix[x].volume) + float(dosed)
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + str(lVolume) + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
                 blynk.virtual_write(28, "add", rowIndex, nutrientMix[x].name + " dosed " + str(dosed) + " ml", now.strftime("%d/%m/%Y %H:%M:%S"))
                 rowIndex = rowIndex+1
                 blynk.virtual_write(29,rowIndex)  
            blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
        else:
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("D,*") + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 
            
    @blynk.handle_event('write V46')
    def fillLinePump6(pin, value):
        global rowIndex
        x=5
        _log.info( "Fill Line 6 " + str(value[0]) + '\n')
        lVolume= nutrientMix[x].volume
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
            if (float(dosed) > 0) :
                 _log.info("dosed more than 0 = " + str(float(dosed)))
                 _log.info("nutrientMix[x].volume  = " + str(float(nutrientMix[x].volume)))
			
                 nutrientMix[x].volume = float(nutrientMix[x].volume) + float(dosed)
                 _log.info("updated nutrientMix[x].volume  = " + str(float(nutrientMix[x].volume)))
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + str(lVolume) + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
                 _log.info("Add row to table " + nutrientMix[x].name + " dosed " + str(dosed))

                 _log.info("Add row to table rowIndex = " + str(rowIndex))

                 blynk.virtual_write(28, "add", rowIndex, nutrientMix[x].name + " dosed " + str(dosed) + " ml", now.strftime("%d/%m/%Y %H:%M:%S"))
                 rowIndex = rowIndex+1
                 blynk.virtual_write(29,rowIndex)  
                  
                 _log.info("Add row to table rowIndex = " + str(rowIndex))
		
            blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
        else:
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("D,*") + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 
				
		
    @blynk.handle_event('write V47')
    def fillLinePump7(pin, value):
        global rowIndex
        x=6
        _log.info( "Fill Line 7 " + str(value[0]) + '\n')
        lVolume= nutrientMix[x].volume
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
            if (float(dosed) > 0) :
                 nutrientMix[x].volume = float(nutrientMix[x].volume) + float(dosed)
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Had used " + str(lVolume) + " ml| Now Dosed :"+ str(nutrientMix[x].volume) + "ml" + '\n') 
                 blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED"  + " Dosed :"+ str(dosed) + "ml" + '\n') 
                 blynk.virtual_write(28, "add", rowIndex, nutrientMix[x].name + " dosed " + str(dosed) + " ml", now.strftime("%d/%m/%Y %H:%M:%S"))
                 rowIndex = rowIndex+1
                 blynk.virtual_write(29,rowIndex)  
            blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
        else:
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("D,*") + '\n') 
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 
		
    @blynk.handle_event('write V60')
    def v60write_handler(pin, value):
        global nutrientMix
        nutrientMix[0].dose = value[0]
        blynk.virtual_write(98, nutrientMix[0].name + " dose volume set to " + str(nutrientMix[0].dose)+ '\n')
        _log.info(nutrientMix[0].name + " dose volume set to " + str(nutrientMix[0].dose)+ '\n')
 	 	
    @blynk.handle_event('write V61')
    def v61write_handler(pin, value):
        global nutrientMix
        nutrientMix[1].dose = value[0]
        blynk.virtual_write(98, nutrientMix[1].name + " dose volume set to " + str(nutrientMix[1].dose)+ '\n')
    
    @blynk.handle_event('write V62')
    def v62write_handler(pin, value):
        global nutrientMix
        nutrientMix[2].dose = value[0]
        blynk.virtual_write(98, nutrientMix[2].name + " dose volume set to " + str(nutrientMix[2].dose)+ '\n')
    
    @blynk.handle_event('write V63')
    def v63write_handler(pin, value):
        global nutrientMix
        nutrientMix[3].dose = value[0]
        blynk.virtual_write(98, nutrientMix[3].name + " dose volume set to " + str(nutrientMix[3].dose)+ '\n')
    
    @blynk.handle_event('write V64')
    def v64write_handler(pin, value):
        global nutrientMix
        nutrientMix[4].dose = value[0]
        blynk.virtual_write(98, nutrientMix[4].name + " dose volume set to " + str(nutrientMix[4].dose)+ '\n')

    @blynk.handle_event('write V65')
    def v65write_handler(pin, value):
        global nutrientMix
        nutrientMix[5].dose = value[0]
        blynk.virtual_write(98, nutrientMix[5].name + " dose volume set to " + str(nutrientMix[5].dose)+ '\n')

    @blynk.handle_event('write V66')
    def v66write_handler(pin, value):
        global nutrientMix
        print("-------------------------------------------")
        print(value)
        print(pin)
        print("-------------------------------------------")
        nutrientMix[6].dose = value[0]
        blynk.virtual_write(98, nutrientMix[6].name + " dose volume set to " + str(nutrientMix[6].dose)+ '\n')
        _log.info(nutrientMix[6].name + " dose volume set to " + str(nutrientMix[6].dose)+ '\n')

    @blynk.handle_event('write V90')
    def v90write_handler(pin, value):
        nutrientMix[0].volume = float(value[0])
        _log.info("Loading passed volume for " + nutrientMix[0].name + " value[0] is " + str(value[0]))

    @blynk.handle_event('write V91')
    def v91write_handler(pin, value):
        nutrientMix[1].volume = float(value[0])
        _log.info("Loading passed volume for " + nutrientMix[1].name + " value[0] is " + str(value[0]))
	
    @blynk.handle_event('write V92')
    def v92write_handler(pin, value):
        nutrientMix[2].volume = float(value[0])
        _log.info("Loading passed volume for " + nutrientMix[2].name + " value[0] is " + str(value[0]))
	
    @blynk.handle_event('write V93')
    def v93write_handler(pin, value):
        nutrientMix[3].volume = float(value[0])
        _log.info("Loading passed volume for " + nutrientMix[3].name + " value[0] is " + str(value[0]))
	
    @blynk.handle_event('write V94')
    def v94write_handler(pin, value):
        nutrientMix[4].volume = float(value[0])
        _log.info("Loading passed volume for " + nutrientMix[4].name + " value[0] is " + str(value[0]))
	
    @blynk.handle_event('write V95')
    def v95write_handler(pin, value):
        nutrientMix[5].volume = float(value[0])
        _log.info("Loading passed volume for " + nutrientMix[5].name + " value[0] is " + str(value[0]))
	
    @blynk.handle_event('write V96')
    def v96write_handler(pin, value):
        nutrientMix[6].volume = float(value[0])
        _log.info("Loading passed volume for " + nutrientMix[6].name + " value[0] is " + str(value[0]))

	
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        _log.critical( "User reboot")
        blynk.virtual_write(250, "Reboot")
        blynk.set_property(250, 'color', colours['OFFLINE'])	
        blynk.virtual_write(98, "User Reboot " + '\n')
        blynk.set_property(systemLED, 'color', colours['OFFLINE'])	
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')
	
    @blynk.handle_event("connect")
    def connect_handler():
        _log.warning("Connected")
        blynk.virtual_write(250, "Connected")
        pins = [ 1, 10, 11, 12, 13, 14, 15, 16, 27, 38,39,41,42,43,44,45,46,47,48,49, 60, 61, 62, 63, 64, 65, 66, 90, 91, 92, 93, 94, 95, 96, 1]
        for pin in pins:
           _log.info('Syncing virtual buttons {}'.format(pin))
           blynk.virtual_sync(pin)
           blynk.read_response(timeout=0.5)
        
    @timer.register(interval=60, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        blynk.virtual_write(250, "Running")
        blynk.set_property(250, 'color', colours['ONLINE'])
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
	
        processSensors()
	
        _log.info( "Going to start dosing process")  
        doneDose = False
	
        if (float(sensors[1].target) > float(sensors[1].value)): #EC
             if (int(sensors[1].mode) == 3):
                  _log.info("Do a dose")     
                  doneDose = True
                  blynk.virtual_write(98,"Automatic dose nutrient "+ '\n') 
                  doSingleDose()
		
        _log.debug("float(sensors[2].target) < float(sensors[2].value) = " + str(float(sensors[2].target)) + " < " + str(float(sensors[2].value)))	
        if (doneDose is False): #don't auto dose ph same time as food
             if (float(sensors[2].target) < float(sensors[2].value)): #ph
                  _log.info("Would do ph dose; mode is " + str(sensors[2].mode))
                  if (int(sensors[2].mode) == 3):                  
                      _log.info("Do a ph dose") 
                      blynk.virtual_write(98,"Automatic dose Ph"+ '\n')
                      doSinglePHDose()
                      #blynk.notify("Ben has stopped ph pump. Is adding ph now correct!")      
			
        if (int(sensors[1].mode) == 2):
             _log.info("Do a dose")     
             doSingleDose()     
             blynk.virtual_write(98,"Manual dose nutrient "+ '\n')
             blynk.virtual_write(39,1)
             sensors[1].mode = 1
	
        if (int(sensors[2].mode) == 2):                  
             _log.info("Do a ph dose") 
             doSinglePHDose()
             blynk.virtual_write(98,"Manual dose Ph"+ '\n')
             blynk.virtual_write(49,1)
             sensors[2].mode = 1
		
        _log.info("Completed Timer Function") 

    while True:
        try:
           blynk.run()
           timer.run()
           if bootup :
              blynk.virtual_write(250, "Initializing")
              blynk.set_property(250, 'color', '#ff00dd')	
              p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
              #cmdout = str(p.communicate())
              for i in range(0,9):
                   blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
              bootup = False
              blynk.set_property(251, "label",drone.gethostname())
              blynk.virtual_write(251, drone.get_ip())
              now = datetime.now()
              blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
              for l in LED:
                  blynk.virtual_write(l, 255)
              blynk.virtual_write(systemLED, 255)
	
              #blynk.virtual_write(98, "clr")
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')
  
              _log.info("Now look as sensors")
              blynk.virtual_write(98,"Temp Cal " + sensors[0].sensor.query("Cal,?")+ '\n')
              blynk.virtual_write(98,"EC Cal " + sensors[1].sensor.query("Cal,?")+ '\n')
              blynk.virtual_write(98,"Temp Cal " + sensors[2].sensor.query("Cal,?")+ '\n')

              _log.info('processSensors')
              processSensors()
		
              blynk.virtual_write(51,"EC Settings")
              blynk.virtual_write(52,"pH Settings")
              blynk.set_property(38, "label", "EC Trigger Level")
              blynk.set_property(48, "label", "pH Trigger Level")
              blynk.set_property(39, "label", "EC Mode")
              blynk.set_property(49, "label", "pH Mode")
	
              u=41
              labelPin = 70
              for dosage in nutrientMix:
                   blynk.set_property(u, "label", dosage.name + " Fill")
                   blynk.set_property(labelPin, 'label', dosage.name)
                   blynk.virtual_write(labelPin, dosage.name)
                   u = u+1
                   labelPin = labelPin + 1
              
              pins = [ 1, 10, 11, 12, 13, 14, 15, 16, 27, 38,39,41,42,43,44,45,46,47,48,49, 60, 61, 62, 63, 64, 65, 66, 90, 91, 92, 93, 94, 95, 96, 1]
              for pin in pins:
                   _log.info('Syncing virtual buttons {}'.format(pin))
                   blynk.virtual_sync(pin)
                   blynk.read_response(timeout=0.5)
	
              _log.critical("Boot Completed")
              blynk.virtual_write(250, "Started")
              blynk.set_property(250, 'color', colours['ONLINE'])
              blynk.set_property(systemLED, 'color', colours['ONLINE'])

        except:
           _log.critical('Unexpected error')
           blynk.virtual_write(250, "Crash")
           blynk.virtual_write(98, "System has main loop error" + '\n')
           for l in LED:
                blynk.set_property(l, 'color', colours['OFFLINE'])
           blynk.set_property(systemLED, 'color', colours['OFFLINE'])
           os.system('sh /home/pi/updateDroneponics.sh')
           os.system('sudo reboot') 
  
   
except KeyboardInterrupt:
   _log.critical('Keyboard Interrupt')
   blynkErr = blynklib.Blynk(parser.get('droneDoser', 'BLYNK_AUTH'))
   blynkErr.run()
   blynkErr.virtual_write(250, "Keyboard Interrupt")
   blynkErr.set_property(systemLED, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')

except:
   _log.critical('Final except: Unexpected error')
   blynkErr = blynklib.Blynk(parser.get('droneDoser', 'BLYNK_AUTH'))
   blynkErr.run()
   blynkErr.virtual_write(250, "Crash")
   blynkErr.set_property(systemLED, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
