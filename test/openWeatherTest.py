from drone import OpenWeather
openWeather = OpenWeather() 
openWeather.refresh()
print(openWeather.openWeather)
