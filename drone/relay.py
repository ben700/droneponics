from drone import * 
class Relay:
   GPIO.setmode(GPIO.BCM)
   GPIO.setwarnings(False)

   def __init__(self, gpioPin, Name, *args, **kwargs):
       print("Building object")
       self.gpioPin = gpioPin
       self.name = Name
       self.gpio = GPIO.setup(gpioPin)
       
def turnOn(relays, _log): 
    self.gpio.output(self.gpioPin,GPIO.HIGH) 
      
def turnOff(relays, _log): 
    self.gpio.output(self.gpioPin,GPIO.LOW) 
