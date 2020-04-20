#!/usr/bin/python
#by Daniel Tamm
import sys
sys.path.append('/home/pi/droneponics')
from chirp import Chirp
import sys

if len(sys.argv) < 3:
	print ("Usage: %s old_addr new_addr" % (sys.argv[0]))
	print ("Standard Chirp address is 0x20 (32).")
	print ("Use ''i2cdetect -y 1'' to see your current Chirp addresses.")
	sys.exit()

# Get old address (may be given in decimal or hex)
if sys.argv[1].startswith("0x"):
	old_addr = int(sys.argv[1], 16)
else:
	old_addr = int(sys.argv[1])

# Get new address (may be given in decimal or hex)
if sys.argv[2].startswith("0x"):
	new_addr = int(sys.argv[2], 16)
else:
	new_addr = int(sys.argv[2])

# Check that the new address is not occupied
try:
	chirp1 = Chirp(1, new_addr)
	chirp1.reset()
	print ("The given new address %d is already in use. %s" % (new_addr, chirp1))
	sys.exit()
except IOError:
	pass

try:
	# If the following line throws an error, there is no Chirp on old_addr
	chirp = Chirp(1, old_addr)
except IOError:
	print ("Cannot find a Chirp on address", old_addr)
	print ("Use ''i2cdetect -y 1'' to see your current Chirp addresses.")

print ("Renaming %s to address %d" % (chirp, new_addr))
#chirp.set_addr(new_addr)
chirp.sensor_address(new_addr)
print ("Now your Chirp answers:", chirp)
