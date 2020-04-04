from drone import *
            
LED = [10,11,12,13,14,15]
VolumePin = [20,21,22,23,24,25]          
 

def buildNutrientMix(nutrientMix, _log):
    _log.info("now building buildNutrientMix") 
    nutrientMix.append( Dose(119, 0.00, LED[0], "pH", VolumePin[0]))
    nutrientMix.append( Dose(111, 6.00, LED[1], "Hydro Bloom A", VolumePin[1]))
    nutrientMix.append( Dose(113, 6.00, LED[2], "Hydro Bloom B", VolumePin[2])) 
    nutrientMix.append( Dose(114, 10.00, LED[3], "Ignition", VolumePin[3]))
    nutrientMix.append( Dose(115, 4.00, LED[4], "Enzyme", VolumePin[4]))
    nutrientMix.append( Dose(116, 1.00, LED[5], "Magne-Cal", VolumePin[5])) 
    return nutrientMix

def buildSensors(sensors, _log):
    _log.info("now building sensors list") 
    sensors.append( Sensor(102, "Temprature", 30, 20))
    sensors.append( Sensor(100, "EC", 31 , 500))
    sensors.append( Sensor(99, "pH", 32, 5.5))
    sensors.append( Sensor(99, "pH", 33, None))        
    return sensors


def readSensors(sensors, _log, blynk):
    blynk.virtual_write(98,"now read sensors temp") 
    sensors[0].value = sensor[0].sensor.query("R").split(":")[1] #Temp
    _log.info("now read sensors EC") 
    sensors[1].value = sensor[1].sensor.query("RT,"+sensors[0].value).split(":")[1] #EC
    _log.info("now read sensors pH") 
    sensors[2].value = sensor[2].sensor.query("RT,"+sensors[0].value).split(":")[1] #pH
    _log.info("now read sensors colour") 
    sensors[3].value = sensor[3].sensor.query("R").split(":")[1] #colour
    blynk.virtual_write(98, "all sensors read") 
    return sensors
