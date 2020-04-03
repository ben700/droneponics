class Dose:
   def __init__(self, PumpId, Dose, Led, name, volumePin):
       print("Building object")
       self.pump = None
       self.pumpId = PumpId
       self.dose = Dose
       self.LED = Led
       self.name = name
       self.volumePin = volumePin	
       self.volume = 0	
            
 
class Sensor:
   def __init__(self, SensorId, Name, DisplayPin, Target):
       print("Building Sensor")
       self.sensor = None
       self.sensorId = SensorId
       self.name = Name
       self.displayPin = DisplayPin
       self.target = Target
         
       
