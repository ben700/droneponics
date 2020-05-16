from colour import Color
import blynklib

def displaySensor(blynk, VP, VALUE, NAME , LOW, HIGH):
 print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
 red = Color("red")
 print("loaded color class")
 colors = list(red.range_to(Color("green"),10))
 print("done colour list")
 print(colors)
 print("Going to update blynk")
 blynk.virtual_write(VP,VALUE)
 blynk.set_property(VP, "label", NAME)
 print("Going to update blynk colors")
 blynk.set_property(VP, "color", colors[round((HIGH-LOW)/10,0)])
 print("####################################################")
 return

class Sensor:
   def __init__(self, SensorId, name *args, **kwargs):
       self.sensor = AtlasI2C(SensorId)
       self.sensorId = SensorId
       self.name = Name
       self.displayPin = kwargs.get('DisplayPin', None)
       self.target = kwargs.get('Target', None)
       self.value = None
       self.lowAlarm = kwargs.get('LowAlarm', None)
       self.highAlarm = kwargs.get('HighAlarm', None)
       
      self.name = None
      self.object = AtlasI2C(SensorId)
  def read():
  return self.sensor.query("R").split(":")[1].strip().rstrip('\x00')
    
class PH(Sensor):  
   def __init__(self, *args, **kwargs):
    Sensor.__init__(self, 99, "pH", 32, Target=5.5, LowAlarm=5.3, HighAlarm=6.5, *args, **kwargs)
 def read(cTemp):
  return self.sensor.query("RT,"+cTemp).split(":")[1].strip().rstrip('\x00')
 
class EC(Sensor):
   def __init__(self, *args, **kwargs):
      Sensor.__init__(self, 100, "EC",  31 , Target=600, LowAlarm=500, HighAlarm=1500, *args, **kwargs) 
   def read(cTemp):
      return self.sensor.query("RT,"+cTemp).split(":")[1].strip().rstrip('\x00')
  
class TEMP(Sensor):  
   def __init__(self, *args, **kwargs):
      Sensor.__init__(self, 102, "Temprature", 30, Target=20, LowAlarm=10, HighAlarm=25, *args, **kwargs) 
