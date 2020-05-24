colours = {1: '#FF0000', '1': '#FF0000', 0: '#00FF00', '0': '#00FF00', 2: '#00FF00', 3: '#80FF00',4: '#00FF80', 5: '#80FF80','OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101

import blynklib
import blynktimer
import RPi.GPIO as GPIO   
from datetime import datetime 
import time

        
def droneRelayWriteHandler(pin, button_state, blynk, relays):
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.set_property(pin, 'onColor', colours[0])
        blynk.set_property(pin, 'onBackColor', colours[1])
        blynk.set_property(pin, 'offColor', colours[1])
        blynk.set_property(pin, 'offBackColor', colours[0])
        
        if (button_state in (1,"1")):
           blynk.virtual_write(98, "State of button "+ str(pin) + " now on" + '\n')
           blynk.set_property(10+pin, 'color', colours[0])
           GPIO.output(relays[pin],1)
        else:
           blynk.virtual_write(98, "State of button "+ str(pin) + " now off" + '\n')
           blynk.set_property(10+pin, 'color', colours[1])
           GPIO.output(relays[pin],0)
        blynk.virtual_write(250, "Running")
        blynk.set_property(systemLED, 'color', colours[0])        
       
def turnButtonsOffline(blynk):
        blynk.set_property(1, 'color', colours['OFFLINE'])
        blynk.set_property(2, 'color', colours['OFFLINE'])
        blynk.set_property(3, 'color', colours['OFFLINE'])
        blynk.set_property(4, 'color', colours['OFFLINE'])
        blynk.set_property(5, 'color', colours['OFFLINE'])
        blynk.set_property(6, 'color', colours['OFFLINE'])
        blynk.set_property(7, 'color', colours['OFFLINE'])
        blynk.set_property(8, 'color', colours['OFFLINE'])
        
def turnButtonsOnline(blynk):
        blynk.set_property(1, 'color', colours['ONLINE'])
        blynk.set_property(2, 'color', colours['ONLINE'])
        blynk.set_property(3, 'color', colours['ONLINE'])
        blynk.set_property(4, 'color', colours['ONLINE'])
        blynk.set_property(5, 'color', colours['ONLINE'])
        blynk.set_property(6, 'color', colours['ONLINE'])
        blynk.set_property(7, 'color', colours['ONLINE'])
        blynk.set_property(8, 'color', colours['ONLINE'])
        
def turnLEDsOffline(blynk):
        blynk.set_property(11, 'color', colours['OFFLINE'])
        blynk.set_property(12, 'color', colours['OFFLINE'])
        blynk.set_property(13, 'color', colours['OFFLINE'])
        blynk.set_property(14, 'color', colours['OFFLINE'])
        blynk.set_property(15, 'color', colours['OFFLINE'])
        blynk.set_property(16, 'color', colours['OFFLINE'])
        blynk.set_property(17, 'color', colours['OFFLINE'])
        blynk.set_property(18, 'color', colours['OFFLINE'])
        
def turnLEDsOnline(blynk):
        blynk.set_property(11, 'color', colours['ONLINE'])
        blynk.set_property(12, 'color', colours['ONLINE'])
        blynk.set_property(13, 'color', colours['ONLINE'])
        blynk.set_property(14, 'color', colours['ONLINE'])
        blynk.set_property(15, 'color', colours['ONLINE'])
        blynk.set_property(16, 'color', colours['ONLINE'])
        blynk.set_property(17, 'color', colours['ONLINE'])
        blynk.set_property(18, 'color', colours['ONLINE'])
        
