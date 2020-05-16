from drone import *         
 
def lightPin(): 
    return 26
            
            
def buildNutrientMix(nutrientMix, _log, scheduleWeek='Grow'):
 #weekGrow
 if (scheduleWeek=='Grow'):
    nutrientMix.append( Dose(119, 1.00, LED[0], "pH", VolumePin[0], 1000))
    nutrientMix.append( Dose(111, 6.00, LED[1], "Hydro Grow A", VolumePin[1], 3000))
    nutrientMix.append( Dose(114, 10.00, LED[3], "Root Stimulant", VolumePin[3], 3000))
    nutrientMix.append( Dose(115, 4.00, LED[4], "Enzyme", VolumePin[4], 3000))
    nutrientMix.append( Dose(116, 1.00, LED[5], "Hydro-Silicon", VolumePin[5], 500)) 
    nutrientMix.append( Dose(113, 6.00, LED[2], "Hydro Grow B", VolumePin[2], 3000)) 
 elif (scheduleWeek==1):
    nutrientMix.append( Dose(119, 1.00, LED[0], "pH", VolumePin[0], 1000))
    nutrientMix.append( Dose(111, 6.00, LED[1], "Hydro Grow A", VolumePin[1], 5000))
    nutrientMix.append( Dose(114, 10.00, LED[3], "Ignition", VolumePin[3], 1000))
    nutrientMix.append( Dose(115, 4.00, LED[4], "Enzyme", VolumePin[4], 5000))
    nutrientMix.append( Dose(116, 1.00, LED[5], "Magne-Cal", VolumePin[5], 5000)) 
    nutrientMix.append( Dose(113, 6.00, LED[2], "Hydro Grow B", VolumePin[2], 5000)) 
 elif (scheduleWeek==2):
    nutrientMix.append( Dose(119, 1.00, LED[0], "pH", VolumePin[0], 1000))
    nutrientMix.append( Dose(111, 6.00, LED[1], "Hydro Bloom A", VolumePin[1], 5000))
    nutrientMix.append( Dose(114, 10.00, LED[3], "Ignition", VolumePin[3], 1000))
    nutrientMix.append( Dose(115, 4.00, LED[4], "Enzyme", VolumePin[4], 5000))
    nutrientMix.append( Dose(116, 1.00, LED[5], "Magne-Cal", VolumePin[5], 5000)) 
    nutrientMix.append( Dose(113, 6.00, LED[2], "Hydro Bloom B", VolumePin[2], 5000)) 
 elif (scheduleWeek==3):
    nutrientMix.append( Dose(119, 1.00, LED[0], "pH", VolumePin[0], 1000))
    nutrientMix.append( Dose(111, 6.00, LED[1], "Hydro Bloom A", VolumePin[1], 5000))
    nutrientMix.append( Dose(114, 10.00, LED[3], "Ignition", VolumePin[3], 1000))
    nutrientMix.append( Dose(115, 4.00, LED[4], "Enzyme", VolumePin[4], 5000))
    nutrientMix.append( Dose(116, 1.00, LED[5], "Magne-Cal", VolumePin[5], 5000)) 
    nutrientMix.append( Dose(113, 6.00, LED[2], "Hydro Bloom B", VolumePin[2], 5000)) 
 elif (scheduleWeek==8):
    nutrientMix.append( Dose(119, 1.00, LED[0], "pH", VolumePin[0], 1000))
    nutrientMix.append( Dose(111, 6.00, LED[1], "Hydro Bloom A", VolumePin[1], 5000))
    nutrientMix.append( Dose(114, 10.00, LED[3], "Ignition", VolumePin[3], 1000))
    nutrientMix.append( Dose(115, 4.00, LED[4], "Enzyme", VolumePin[4], 5000))
    nutrientMix.append( Dose(116, 1.00, LED[5], "Magne-Cal", VolumePin[5], 5000)) 
    nutrientMix.append( Dose(113, 6.00, LED[2], "Hydro Bloom B", VolumePin[2], 5000)) 
 else :
    nutrientMix.append( Dose(119, 1.00, LED[0], "pH", VolumePin[0], 1000))
    
    return nutrientMix

            
def buildOxyMix(nutrientMix, _log): 
    nutrientMix.append( Dose(103, 5.00, LED[0], "Oxy Plus", VolumePin[0], 5000))
    return nutrientMix

   
def buildSensors(sensors, _log, scheduleWeek='Grow'):
    sensors.append( Sensor(102, "Temprature", 30, Target=20, LowAlarm=10, HighAlarm=25))
    sensors.append( Sensor(100, "EC", 31 , Target=600, LowAlarm=500, HighAlarm=1500))
#    sensors.append( Sensor(100, "EC", 31 , Target=1000, LowAlarm=500, HighAlarm=1500))
  #week6-8  sensors.append( Sensor(100, "EC", 31 , Target=100, LowAlarm=500, HighAlarm=1500))
    sensors.append( Sensor(99, "pH", 32, Target=5.5, LowAlarm=5.3, HighAlarm=6.5))
    return sensors

def buildOxySensors(sensors, _log):
    sensors.append( Sensor(97, "Dissolved Oxygen", 30, Target=10))
    return sensors

def buildExperimentalSensors(sensors, _log):
    sensors.append( Sensor(97, "Dissolved Oxygen", 30, Target=10))
    return sensors
