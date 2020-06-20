from drone import * 
class Relay:
   GPIO.setmode(GPIO.BCM)
   GPIO.setwarnings(False)

   def __init__(self, gpioPin, Name, *args, **kwargs):
       print("Building object")
       self.gpioPin = gpioPin
       self.name = Name
       self.gpio = GPIO.setup(gpioPin, GPIO.OUT)
       
def turnOn(relays, _log): 
    try:
         _log.info("Turning on relay " + self.name)
         self.gpio.output(self.gpioPin,GPIO.HIGH) 
    except:
         _log.error("Except: Turning on relay " + self.name)
      
def turnOff(relays, _log): 
    
    try:
         _log.info("Turning off relay " + self.name)
         self.gpio.output(self.gpioPin,GPIO.LOW) 
    except:
         _log.error("Except: Turning off relay " + self.name)
      
