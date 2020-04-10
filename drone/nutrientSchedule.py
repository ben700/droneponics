from drone import *         
 
def lightPin(): 
    return 26
            
            
def buildNutrientMix(nutrientMix, _log): 
    nutrientMix.append( Dose(119, 1.00, LED[0], "pH", VolumePin[0], 1000))
    nutrientMix.append( Dose(111, 6.00, LED[1], "Hydro Bloom A", VolumePin[1], 5000))
    nutrientMix.append( Dose(114, 10.00, LED[3], "Ignition", VolumePin[3], 1000))
    nutrientMix.append( Dose(115, 4.00, LED[4], "Enzyme", VolumePin[4], 5000))
    nutrientMix.append( Dose(116, 1.00, LED[5], "Magne-Cal", VolumePin[5], 5000)) 
    nutrientMix.append( Dose(113, 6.00, LED[2], "Hydro Bloom B", VolumePin[2], 5000)) 
    return nutrientMix

            
def buildOxyMix(nutrientMix, _log): 
    nutrientMix.append( Dose(103, 5.00, LED[0], "Oxy Plus", VolumePin[0], 10))
    return nutrientMix

   
def buildSensors(sensors, _log):
    sensors.append( Sensor(102, "Temprature", 30, Target=20, LowAlarm=10, HighAlarm=25))
    sensors.append( Sensor(100, "EC", 31 , Target=1000, LowAlarm=500, HighAlarm=1500))
    sensors.append( Sensor(99, "pH Down", 32, Target=5.5, LowAlarm=5.3, HighAlarm=6.5))
    sensors.append( Sensor(112, "Colour", 33, None))        
    return sensors

def buildOxySensors(sensors, _log):
    sensors.append( Sensor(97, "Dissolved Oxygen", 30, Target=10))
    return sensors

def buildExperimentalSensors(sensors, _log):
    sensors.append( Sensor(97, "Dissolved Oxygen", 30, Target=10))
    return sensors
