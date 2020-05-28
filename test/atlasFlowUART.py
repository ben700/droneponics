#!/usr/bin/python
import serial
self.ser = serial.Serial(
           port='/dev/ttyAMA0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
           baudrate = 38400
      )
#set the default units on probe 
self.ser.write(str.encode("I2C,104"+'\r'))
      
