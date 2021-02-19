import sys
import os
sys.path.append('/home/pi/droneponics/droneAirAtlas')
from droneSensor import Sensor
    
hum = Sensor(111, "Humidity")
hum.read()

co2 = Sensor(105, "CO2")
co2.read()
