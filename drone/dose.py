class Dose:
   def __init__(self, PumpId, Dose, Led, name, volumePin, BottleSize):
       print("Building object")
       self.pump = None
       self.pumpId = PumpId
       self.dose = Dose
       self.LED = Led
       self.name = name
       self.volumePin = volumePin	
       self.volume = 0	
       self.bottleSize = BottleSize
      
   
   def blynkMe(self, blynk, colours):
       print("Building Sensor")
       blynk.set_property(self.LED, 'color', colours['ONLINE'])
       blynk.set_property(self.LED, 'label', self.name)
       blynk.set_property(self.volumePin, 'label', self.name + "-TVP")
       self.volume = self.pump.query("TV,?").split("TV,")[1].strip().rstrip('\x00')
       blynk.virtual_write(self.volumePin, self.volume )
      
 
class Sensor:
   def __init__(self, SensorId, Name, DisplayPin, Target):
       print("Building Sensor")
       self.sensor = None
       self.sensorId = SensorId
       self.name = Name
       self.displayPin = DisplayPin
       self.target = Target
       self.value = None
   def read(self):
       print("Building object")   
       return self.sensor.query("R").split(":")[1].strip().rstrip('\x00')   
   
   def blynkMe(self, blynk):
       print("blynk object")   
       blynk.virtual_write(self.displayPin, self.value)
