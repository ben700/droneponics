#!/usr/bin/python
import serial
ser = serial.Serial(
           port='/dev/ttyAMA0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
           baudrate = 38400
      )
#set the default units on probe 
#ser.write(str.encode("I2C,104"+'\r\n'))
ser.write(str.encode("R"+'\r'))

ser.write(str.encode("R"+'\r'))
rawOutput = self.ser.read(5)
o = rawOutput.decode()
print(o)        
