
import RPi.GPIO as GPIO   

relays=[0,18,23,24,25,12,16,20,21]
Relay1 = relays[1] #feed
Relay2 = relays[2] #fan
Relay3 = relays[3] #Air
Relay4 = relays[4] #heater
Relay5 = relays[5] #Feed
Relay6 = relays[6] #Air
Relay7 = relays[7] #Mixer - turned off with low water 
Relay8 = relays[8]  #Mixer - turned off with low water 


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Relay1,GPIO.OUT, initial=1)

GPIO.output(Relay1,1)
