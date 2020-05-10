class Alarm:
   def __init__(self, name, notify=False *args, **kwargs):
       self.severity = kwargs.get('Severity', None)
       self.name = None
       self.notify = notify
