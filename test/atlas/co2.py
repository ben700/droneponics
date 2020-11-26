from AtlasI2C import (AtlasI2C)
CO2 = AtlasI2C(105)
print(CO2.query("R"))
