import RPi.GPIO as GPIO   
from datetime import datetime

LED = [10,11,12,13,14,15]
VolumePin = [20,21,22,23,24,25] 
colours = {1: '#FF0000', 0: '#00FF00', '0': '#00FF00', '1': '#FF0000', '2': '#00FF00', '3': '#80FF00','4': '#00FF80', '5': '#80FF80','OFFLINE': '#0000FF', 'ONLINE': '#00FF00', 'UNAVILABLE': '#002700'}
systemLED=101
TARGET_EMAIL = 'benslittlebitsandbobs@gmail.com'


class Relays:
   def __init__(self):
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)
      self.relays =[]

      
   def add(self, Relay):
      return self.relays.append(Relay)
  


class Counter:
    cycle = 0
    onCycle=0 
    offCycle=0 
         
    def isItAnOnCycle(self, _log) :
        _log.debug("in class counter function isItAnOnCycle states are")
        _log.debug("in class counter function isItAnOnCycle this.cycle = " + str(self.cycle))
        _log.debug("in class counter function isItAnOnCycle this.onCycle = " + str(self.onCycle))
        _log.debug("in class counter function isItAnOnCycle this.offCycle = " + str(self.offCycle))
        
#        if (self.cycle < self.onCycle):
        if (True):
         
            _log.debug("in class counter function isItAnOnCycle and it is true")
            return True
        else:
            _log.debug("in class counter function isItAnOnCycle and it is false")
            return False
        
    def isItAnOffCycle(self, _log) :
        _log.debug("in class counter function isItAnOffCycle")
        if ((self.cycle-self.onCycle) < self.offCycle):
            _log.debug("in class counter function isItAnOffCycle and it is true")
            return True
        else:
            _log.debug("in class counter function isItAnOffCycle and if is false")
            return False
        
    def setOnCycle(self, _log, onCycleValue):
      _log.debug("current this.cycle = " + str(self.cycle))
      _log.debug("current this.onCycle = " + str(self.onCycle))
      _log.debug("going to set onCycleValue to " + str(onCycleValue))
      self.onCycle = onCycleValue 
        
    def setOffCycle(self, _log, offCycleValue):
      _log.debug("current this.cycle = " + str(self.cycle))
      _log.debug("current this.onCycle = " + str(self.onCycle))
      _log.debug("going to set offCycleValue to " + str(offCycleValue))
      self.offCycle = offCycleValue 
      
    def info(self):
        return "Feed is on for " + str(self.onCycle) + " mins and then off for " + str(self.offCycle) + " mins."
   
    def infoCounter(self):
         return "Counter.cycle = " + str(self.cycle) + " and Counter.onCycle is " + str(self.onCycle) + " and Counter.offCycle = " + str(self.offCycle)
        
    def  incCycle(self, _log):
        _log.debug("in class counter function incCycle")
        _log.debug("Cycle was " + str(self.cycle))
        self.cycle = self.cycle + 1
        _log.debug("Cycle now " + str(self.cycle))
        return self.cycle
         
         
 
class SwitchRelay:
    def __init__(self, PIN, NAME, VPIN):
#       print("++++++++++++++++++++++Creating Relay " + NAME + " on pin " + str(PIN) )
       self.gpioPin = PIN
       self.name=NAME
       self.vPin=VPIN
       self.dPin=VPIN+10
       self.state = 0
       self.cycle=0
       GPIO.setup(self.gpioPin,GPIO.OUT, initial=1)
       return
    
    def setDisplay(self, blynk):
         blynk.set_property(self.vPin, "label", self.name)
         blynk.set_property(self.dPin, "label", self.name)
         blynk.virtual_write(self.dPin, 255)
         return

    def unsetDisplay(self, blynk):
         blynk.set_property(self.vPin, "label", self.name)
         blynk.set_property(self.dPin, "label", self.name)
         blynk.virtual_write(self.dPin, 255)
         return
           
            
    def turnOn(self):
 #      print("++++++++++++++++++++++turnOn Relay " + self.name + " on pin " + str(self.gpioPin) )
       return GPIO.output(self.gpioPin,GPIO.LOW)
    
    def turnOff(self):
  #     print("++++++++++++++++++++++turnOff Relay " + self.name + " on pin " + str(self.gpioPin) )
       return GPIO.output(self.gpioPin,GPIO.HIGH) 

    def setState(self, STATE):
       self.state = STATE
       return
 
    def blynkWriteHandler(self, blynk, STATE):
        self.setState(STATE)
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        blynk.virtual_write(98, "Change state of button "+ str(self.gpioPin) + '\n')
        blynk.set_property(systemLED, 'color', colours[1])
        blynk.virtual_write(250, "Updating")
        blynk.set_property(self.dPin, 'color', colours[self.state])
        blynk.set_property(self.vPin, 'onBackColor', colours[self.state])
        if(self.state == '0'):
           self.turnOn()
        elif (self.state == '1'):
           self.turnOff()
        blynk.set_property(systemLED, 'color', colours[0]) 
      
      
    def blynkTimerHandler(self, blynk):
      if(self.state == '0'):
         return
      if(self.state == '1'):
         return         
      self.cycle += 1
      if(self.state == '2'):
         if self.cycle % 2 == 0:
            self.cycle = 0
      if(self.state =='3'):
         if self.cycle % 4 == 0:
            self.cycle = 0
      if(self.state =='4'):
         if self.cycle % 10 == 0:
            self.cycle = 0
      if (self.cycle == 0): 
         self.turnOn()
      else:
         self.turnOff()
      
