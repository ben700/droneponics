import RPi.GPIO as GPIO   

LED = [10,11,12,13,14,15]
VolumePin = [20,21,22,23,24,25] 
colours = {1: '#FF0000', 0: '#00FF00', '0': '#00FF00', '1': '#FF0000', 2: '#00FF00', 3: '#80FF00',4: '#00FF80', 5: '#80FF80','OFFLINE': '#0000FF', 'ONLINE': '#00FF00', 'UNAVILABLE': '#002700'}

systemLED=101

class Relay:
   def __init__(self, PIN, NAME, *args, **kwargs):
       print("++++++++++++++++++++++Creating Relay " + NAME + " on pin " + STR(PIN) + '/n')
       self.pin = PIN
       self.name=NAME
       GPIO.setup(PIN,GPIO.OUT, initial=1)
    
    def turnOn(self):
       print("++++++++++++++++++++++turnOn Relay " + self.NAME + " on pin " + STR(self.PIN) + '/n')
       return GPIO.output(self.pin,GPIO.LOW)
    
    def turnOff(self):
       print("++++++++++++++++++++++turnOff Relay " + self.NAME + " on pin " + STR(self.PIN) + '/n')
       return GPIO.output(self.pin,GPIO.HIGH)
