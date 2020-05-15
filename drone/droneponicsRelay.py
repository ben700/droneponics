colours = {1: '#FF0000', 0: '#00FF00', '1': '#FF0000', '0': '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
systemLED=101

import blynklib
import blynktimer
import RPi.GPIO as GPIO   

def processButtinePressed(blynk, LED, Button, Relay,VALUE):
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        blynk.set_property(LED, 'color', colours[VALUE])
        blynk.set_property(Button, 'onBackColor', colours[VALUE])
        GPIO.output(Relay,VALUE)
        blynk.virtual_write(98,"Flipped Switch 1" + '\n')
        blynk.virtual_write(250, "Running")
        blynk.set_property(systemLED, 'color', colours[0])
