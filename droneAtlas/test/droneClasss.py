sys.path.append('/home/pi/droneponics/droneAirAtlas')
from droneSensor import Sensor
    
hum = Sensor(111, "Humidity")
hum.read()
