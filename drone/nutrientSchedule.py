from drone import *         
 
def lightPin(): 
    return 26
            
            
def buildNutrientMix(nutrientMix, _log, scheduleWeek='Grow'):
 #weekGrow
    _log.info("The Schedule Week is " + scheduleWeek)
    nutrientMix.append( Dose(11, 1.00, LED[0], "pH", VolumePin[0], 1000))
    nutrientMix.append( Dose(12, 6.00, LED[1], "Part A", VolumePin[1], 5000))
    nutrientMix.append( Dose(13, 6.00, LED[2], "Part B", VolumePin[2], 5000)) 
    nutrientMix.append( Dose(14, 10.00, LED[3], "Rhizotonic", VolumePin[3], 1000))
    nutrientMix.append( Dose(15, 4.00, LED[4], "Cannazym", VolumePin[4], 1000))
    nutrientMix.append( Dose(16, 1.00, LED[5], "PK 13-14", VolumePin[5], 500)) 
    nutrientMix.append( Dose(17, 1.00, LED[5], "Boost", VolumePin[5], 1000)) 
 
    
    return nutrientMix

            
def buildOxyMix(nutrientMix, _log): 
    nutrientMix.append( Dose(103, 5.00, LED[0], "Oxy Plus", VolumePin[0], 5000))
    return nutrientMix

   
def buildSensors(sensors, _log):
    _log.debug("in built sensors function")
    sensors.append( Sensor(102, "Temprature", 30, Target=20, LowAlarm=10, HighAlarm=25))
    _log.debug("built temperature sensor")
    sensors.append( Sensor(100, "EC", 31 , Target=100, LowAlarm=50, HighAlarm=1500))
    _log.debug("built ec sensor")
    sensors.append( Sensor(99, "pH", 32, Target=5.5, LowAlarm=5.3, HighAlarm=6.5))
    _log.debug("built ph sensor")
    return sensors

def buildOxySensors(sensors, _log):
    sensors.append( Sensor(97, "Dissolved Oxygen", 30, Target=10))
    return sensors

def buildExperimentalSensors(sensors, _log):
    sensors.append( Sensor(97, "Dissolved Oxygen", 30, Target=10))
    return sensors
