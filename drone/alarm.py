class Alarm:
   
   def __init__(self, Name, Type="Low", notify=False *args, **kwargs):
      self.severity = kwargs.get('Severity', None)
      self.name = Name==
      self.type = Type
      self.notify = notify
      self.crititalValue = kwargs.get('VALUE', None)
      self.crititalMessage = kwargs.get('MSG', None)
      self.crititalColour = kwargs.get('COLOR', None)

      
    def addTest(temperature, state, "low", True, VALUE, 20.0, MSG = 'Low TEMP!!!', COLOR = '#c0392b')
       if (type == 'Low'):
         if (VALUE > state):
            if(self.notify):
               blynk.notify(self.crititalMessage)
               self.notify=Falue
    
       blynk.virtual_write(VP, self.temperature)
       blynk.set_property(VP, "label", self.name)
       blynk.set_property(VP, "color", self.colour)

         
def testAlarm('temperature', VALUE);
