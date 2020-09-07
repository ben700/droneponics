#!/usr/bin/python
# cannot use python3 because smbus not working there
# Modified script from https://github.com/JasperWallace/chirp-graphite/blob/master/chirp.py
# by DanielTamm

import drone

if __name__ == "__main__":
	addr = 0x20
	if len(sys.argv) == 2:
		if sys.argv[1].startswith("0x"):
			addr = int(sys.argv[1], 16)
		else:
			addr = int(sys.argv[1])
	chirp = drone.Chirp(1, addr)

	print (chirp)
	print ("Moisture\tTemperature\tBrightness")
	while True:
		print "%d\t%d\t%d" % (chirp.moist(), chirp.temp(), chirp.light())
		time.sleep(1)
