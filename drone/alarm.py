
Alarm('temperature', "low", "low",15.0, Notify=False,  Message = 'Low TEMP!!!', Colour = '#c0392b')
Alarm('temperature', "High", "high", 35.0, Notify=False, Message = 'High TEMP!!!', Colour = '#c0392b')
Alarm('temperature', "low", "lowlow", 20.0, Notify=True,  Message = 'Low Low TEMP!!!', Colour = '#c0392b')
Alarm('temperature', "High", "highhigh", 40.0,Notify=True, Message = 'High High TEMP!!!', Colour = '#c0392b')
   
class Alarm:
   
   def __init__(self, Metric, Type, Name, Value, notify=False *args, **kwargs):
      self.metric = Metric
      self.type = Type
      self.name = Name
      self.value = Value
      self.notify = kwargs.get('Notify', None)
      self.message = kwargs.get('Message', None)
      self.colour = kwargs.get('Colour', None)

      
   
   def test(blynk, VP, type, VALUE)   
       if (type == 'Low'):
         if (VALUE > self.crititalValue):
            if(self.notify):
               blynk.notify(self.crititalMessage)
               self.notify=False
            if(self.crititalColour is not None):
               blynk.set_property(VP, "color", self.crititalColour)
               
       blynk.virtual_write(VP, self.temperature)
       blynk.set_property(VP, "label", self.name)
       blynk.set_property(VP, "color", self.colour)

         
     def testAlarm('temperature', VALUE);
