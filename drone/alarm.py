 
from colour import Color

red = Color("red")
colors = list(red.range_to(Color("green"),10))
def displaySensor(blynk, VP, VALUE, NAME , LOW, HIGH):
   blynk.virtual_write(VP,VALUE)
   blynk.set_property(VP, "label", NAME)
   blynk.set_property(VP, "color", colors[round((HIGH-LOW)/10,0)])
   return

  
class Alarm:
   
   def __init__(self, Metric, Type, Name, Value, notify=False, *args, **kwrgs):
      self.metric = Metric
      self.type = Type
      self.name = Name
      self.value = Value
      #self.notify = kwargs.get('Notify', None)
      #self.message = kwargs.get('Message', None)
      #self.colour = kwargs.get('Colour', None)
      #blynk.virtual_write(150, "add", 0, "Max Temp", "20.0")
  
   def display(self,blynk,id):      
     print("alarm id = " + str(id) + " Alarm Name :- " + self.metric + " " + self.name + " Alarm Value :-" + str(self.value))
     
     blynk.virtual_write(150, "add", id, self.metric + " " + self.name, self.value)
     return
    
   def test(self,blynk, Metric, VP, VALUE):
       if (Metric == self.metric):
         blynk.virtual_write(VP, VALUE)
         blynk.set_property(VP, "label", self.name)
         blynk.set_property(VP, "color", self.colour)
         if (self.type == 'Low' and VALUE > self.crititalValue):
           if(self.notify):
               blynk.notify(self.crititalMessage)
               self.notify=False
           if(self.crititalColour is not None):
               blynk.set_property(VP, "color", self.crititalColour)
         elif (self.type == 'High' and VALUE < self.crititalValue):
           if(self.notify):
               blynk.notify(self.crititalMessage)
               self.notify=False
           if(self.crititalColour is not None):
               blynk.set_property(VP, "color", self.crititalColour)
         
