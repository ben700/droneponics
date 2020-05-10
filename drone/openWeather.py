import json
class OpenWeather:
   def __init__(self, *args, **kwargs):
      openWeatherAPI = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=53.801277&lon=-1.548567&exclude=hourly,daily&units=metric&appid=7ab0c16c9b00854f26df8a57435ad6ce")   
      openWeather = openWeatherAPI.json()
      return openWeather
      
   def getPressure(self):
      openWeatherAPI = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=53.801277&lon=-1.548567&exclude=hourly,daily&units=metric&appid=7ab0c16c9b00854f26df8a57435ad6ce")   
      openWeather = openWeatherAPI.json()
      return openWeather["current"]["pressure"]
   
   
   def blynkOpenWeather(self, blynk):
        
        openWeatherAPI = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=53.801277&lon=-1.548567&exclude=hourly,daily&units=metric&appid=7ab0c16c9b00854f26df8a57435ad6ce")   
        openWeather = openWeatherAPI.json()

        blynk.set_property(200, "urls", "http://openweathermap.org/img/wn/"+openWeather["current"]["weather"][0]["icon"]+".png")
        blynk.set_property(200, "label", openWeather["current"]["weather"][0]["description"])
        
        blynk.virtual_write(201,openWeather["current"]["temp"])
        blynk.set_property(201, "label", "Outside Temp")
        blynk.set_property(201, "color", colours['ONLINE'])
        
        blynk.virtual_write(202,openWeather["current"]["dew_point"])
        blynk.set_property(202, "label", "Outside Dew Point")
        blynk.set_property(202, "color", colours['ONLINE'])
        
        blynk.virtual_write(203,openWeather["current"]["pressure"])
        blynk.set_property(203, "label", "Outside Pressure")
        blynk.set_property(203, "color", colours['ONLINE'])
        
        blynk.virtual_write(204,openWeather["current"]["humidity"])
        blynk.set_property(204, "label", "Outside Humidity")
        blynk.set_property(204, "color", colours['ONLINE'])
        
        blynk.virtual_write(205,openWeather["current"]["feels_like"])
        blynk.set_property(205, "label", "Feels Like")
        blynk.set_property(205, "color", colours['ONLINE'])
        print("going to start doing time")
        local_time = time.gmtime(openWeather["current"]["sunrise"])
        print(time.strftime("%H:%M:%S", local_time))
        
        blynk.set_property(206, "label", "Sunrise")
        blynk.virtual_write(206, time.strftime("%H:%M:%S", local_time))
        blynk.set_property(206, "color", colours['ONLINE'])
        
        local_time = time.gmtime(openWeather["current"]["sunset"])
        blynk.set_property(207, "label", "Sunset")
        blynk.virtual_write(207, time.strftime("%H:%M:%S", local_time))
        blynk.set_property(207, "color", colours['ONLINE'])
       
        local_time = time.gmtime(openWeather["current"]["dt"])
        blynk.set_property(208, "label", "Web Time")
        blynk.virtual_write(208, time.strftime("%H:%M:%S", local_time))
        blynk.set_property(208, "color", colours['ONLINE'])        
        return
