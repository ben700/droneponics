colours = {1: '#FF0000', 0: '#00FF00', '0': '#00FF00', '1': '#FF0000', 2: '#00FF00', 3: '#80FF00',4: '#00FF80', 5: '#80FF80','OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101

import blynklib
import blynktimer
import RPi.GPIO as GPIO   
from datetime import datetime 
import time

        
def droneRelayWriteHandler(pin, button_state, blynk, relays):
        if button_state not in (0,1,"0","1"):
            print ("button_state was " + str(button_state) + " so updated to 0")
            button_state = 0
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        blynk.virtual_write(98, "Change state of button "+ str(pin) + '\n')
        
       
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        blynk.set_property(10+pin, 'color', colours[button_state])
        blynk.set_property(pin, 'onBackColor', colours[button_state])
        if(button_state == '0'):
           GPIO.output(relays[pin],0)
        elif (button_state == '1'):
           GPIO.output(relays[pin],1)
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
        
