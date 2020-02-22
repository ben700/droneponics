import AtlasI2C

device = AtlasI2C()
device.set_i2c_address(device.default_address)

#   print(device.query("D,10"))
#   time.sleep(61)
#   print(device.query("Cal,clear"))

#   print(device.query("Cal,8.25"))
#
#   print(device.query("Cal,?"))
#   print(device.write("L,1"))

#   print(device.write("R"))
#   print(device.query("R"))

#   print(device.write("D,15"))
#   print(device.query("D,10"))

print(device.query("I"))

#   print(device.query("PV,?"))
#   print(device.query("ATV,?"))

#   print(device.query("Status"))
#   print(device.query("X"))