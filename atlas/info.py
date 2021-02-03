from AtlasI2C import (AtlasI2C)

# Create the I2C bus
pump = AtlasI2C(102)
pump.query("i")
