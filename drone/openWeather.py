from datetime import datetime  
from datetime import timedelta  
import time
import shlex, requests
import json
colours = {1: '#FF0000', 0: '#00FF00', 'OFFLINE': '#0000FF', 'ONLINE': '#00FF00'}
class OpenWeather:
   def __init__(self, *args, **kwargs):
      self.timestamp = datetime.now()
      self.useByTime = datetime.now()
      self.openWeatherData = None 
      self.openWeather = None
     
   def refresh(self):
      self.timestamp = datetime.now()
      self.useByTime = datetime.now() + timedelta(minutes=30)
      self.openWeatherData = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=53.801277&lon=-1.548567&exclude=hourly,daily&units=metric&appid=7ab0c16c9b00854f26df8a57435ad6ce")    
      self.openWeather = self.openWeatherData.json()
      return
         
   def getPressure(self):
      if (self.useByTime < datetime.now()):
         self.refresh()
      return self.openWeather["current"]["pressure"]
   
   
   def blynkOpenWeather(self, blynk):
        if (self.useByTime < datetime.now()):
           self.refresh()   
        
        blynk.set_property(200, "urls", "http://openweathermap.org/img/wn/"+self.openWeather["current"]["weather"][0]["icon"]+".png")
        blynk.set_property(200, "label", self.openWeather["current"]["weather"][0]["description"])
        
        blynk.virtual_write(201,self.openWeather["current"]["temp"])
        blynk.set_property(201, "label", "Outside Temp")
        blynk.set_property(201, "color", colours['ONLINE'])
        
        blynk.virtual_write(202,self.openWeather["current"]["dew_point"])
        blynk.set_property(202, "label", "Outside Dew Point")
        blynk.set_property(202, "color", colours['ONLINE'])
        
        blynk.virtual_write(203,self.openWeather["current"]["pressure"])
        blynk.set_property(203, "label", "Outside Pressure")
        blynk.set_property(203, "color", colours['ONLINE'])
        
        blynk.virtual_write(204,self.openWeather["current"]["humidity"])
        blynk.set_property(204, "label", "Outside Humidity")
        blynk.set_property(204, "color", colours['ONLINE'])
        
        blynk.virtual_write(205,self.openWeather["current"]["feels_like"])
        blynk.set_property(205, "label", "Feels Like")
        blynk.set_property(205, "color", colours['ONLINE'])
        print("going to start doing time")
        local_time = time.gmtime(self.openWeather["current"]["sunrise"])
        print(time.strftime("%H:%M:%S", local_time))
       
        blynk.set_property(206, "label", "Sunrise")
        blynk.virtual_write(206, time.strftime("%H:%M:%S", local_time))
        blynk.set_property(206, "color", colours['ONLINE'])
        
        local_time = time.gmtime(self.openWeather["current"]["sunset"])
        blynk.set_property(207, "label", "Sunset")
        blynk.virtual_write(207, time.strftime("%H:%M:%S", local_time))
        blynk.set_property(207, "color", colours['ONLINE'])
       
        local_time = time.gmtime(self.openWeather["current"]["dt"])
        blynk.set_property(208, "label", "Web Time")
        blynk.virtual_write(208, time.strftime("%H:%M:%S", local_time))
        blynk.set_property(208, "color", colours['ONLINE'])        
        return
