from drone import * 
class Dose:
   def __init__(self, PumpId, Dose, Led, name, volumePin, BottleSize, *args, **kwargs):
     #  print("Building object")
       self.operational = False
       self.pump = None
       self.pumpId = PumpId
       self.dose = Dose
       self.LED = Led
       self.name = name
       self.volumePin = volumePin	
       self.volume = 0	
       self.bottleSize = BottleSize
       self.notify = False
       self.I2CRelay = None
       self.I2CRelayId = kwargs.get('I2CRelayId', None)
       self.relay = None
       self.relayId = kwargs.get('relayId', None)
         
         
      
   
   def blynkMe(self, blynk, colours):
       print("Building Sensor")
       blynk.set_property(self.LED, 'color', colours['ONLINE'])
       blynk.set_property(self.LED, 'label', self.name)
       blynk.set_property(self.volumePin, 'label', self.name + "-TVP")
    #   self.volume = self.pump.query("TV,?").split("TV,")[1].strip().rstrip('\x00')
    #   blynk.virtual_write(self.volumePin, self.volume )
      
 
class SensorOld:
   def __init__(self, SensorId, Name, DisplayPin, *args, **kwargs):
       self.sensor = None
       self.sensorId = SensorId
       self.name = Name
       self.displayPin = DisplayPin
       self.target = kwargs.get('Target', None)
       self.value = None
       self.lowAlarm = kwargs.get('LowAlarm', None)
       self.highAlarm = kwargs.get('HighAlarm', None)
   
   def read(self):
       return self.sensor.query("R").split(":")[1].strip().rstrip('\x00')   
   
   def blynkMe(self, blynk):
       blynk.virtual_write(self.displayPin, self.value)
