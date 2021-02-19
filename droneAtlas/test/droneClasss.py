import sys
import os
sys.path.append('/home/pi/droneponics/droneAirAtlas/lib')
import drone
    
hum = drone.Sensor(111, "Humidity")
hum.read()

co2 = drone.Sensor(105, "CO2")
co2.read()
