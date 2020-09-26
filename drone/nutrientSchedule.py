from drone import *         
 
LED =[10,11,12,13,14,15,16]
VolumePin =[20,21,22,23,24,25,26]

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
    nutrientMix.append( Dose(17, 1.00, LED[6], "Boost", VolumePin[56], 1000)) 
 
    
    return nutrientMix

            
def buildOxyMix(nutrientMix, _log): 
    nutrientMix.append( Dose(103, 5.00, LED[0], "Oxy Plus", VolumePin[0], 5000))
    return nutrientMix

   
