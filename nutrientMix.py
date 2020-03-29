def buildNutrientMix(nutrientMix):
            nutrientMix.append( Dose(111, 6.00, LED[1], "Hydro Bloom A", VolumePin[1])) 
            nutrientMix.append( Dose(112, 6.00, LED[2], "Hydro Bloom B", VolumePin[2])) 
            nutrientMix.append( Dose(113, 10, LED[3], "Ignition", VolumePin[3]))
            nutrientMix.append( Dose(114, 4, LED[4], "Enzyme", VolumePin[4]))
            nutrientMix.append( Dose(115, 1, LED[5], "Magne-Cal", VolumePin[5])) 
       return nutrientMix     

class Dose:
   def __init__(self, PumpId, Dose, Led, name, volumePin):
       self.pump = None
       self.pumpId = PumpId
       self.dose = Dose
       self.LED = Led
       self.name = name
       self.volumePin = volumePin	
       self.volume = 0	
            
