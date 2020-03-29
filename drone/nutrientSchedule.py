import drone
            
LED = [10,11,12,13,14,15]
VolumePin = [0,21,22,23,24,25]          
 

def buildNutrientMix(nutrientMix, _log):
    _log.info("now building buildNutrientMix")        
    nutrientMix.append( Dose(111, 6.00, LED[1], "Hydro Bloom A", VolumePin[1]))
    _log.info("Added first object")                
    nutrientMix.append( Dose(112, 6.00, LED[2], "Hydro Bloom B", VolumePin[2])) 
    nutrientMix.append( Dose(113, 10, LED[3], "Ignition", VolumePin[3]))
    nutrientMix.append( Dose(114, 4, LED[4], "Enzyme", VolumePin[4]))
    nutrientMix.append( Dose(115, 1, LED[5], "Magne-Cal", VolumePin[5])) 
    return nutrientMix
