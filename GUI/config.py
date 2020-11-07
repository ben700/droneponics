#!/usr/bin/python3
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)

from tkinter import * 			# imports the Tkinter lib
root = Tk()				# create the root object
root.wm_title("GUI")			# sets title of the window
root.configure(bg="#99B898")		# change the background color 
root.attributes("-fullscreen", True) 	# set to fullscreen
ledB= False


def btnClicked():
  global ledB    
  if(ledB):
    ledButton["text"]="LED OFF"
    ledB= False
  else:
    ledButton["text"]="LED ON"
    ledB= True



def tempCalClicked():	
    label_1["text"]="Temp Calibration"
    probe = AtlasI2C(102)
    label_info["text"]= probe.query("i").strip().rstrip('\x00')
    label_cal["text"]= probe.query("cal,?").strip().rstrip('\x00')
    label_status["text"]= probe.query("Status").strip().rstrip('\x00')
    readTempButton.forget()
    calTempButton.forget()
    readTempClicked()

def phCalClicked():
    label_1["text"]="pH Calibration"
    probe = AtlasI2C(99)
    label_info["text"]= probe.query("i").strip().rstrip('\x00')	
    label_cal["text"]= probe.query("cal,?").strip().rstrip('\x00')
    label_status["text"]= probe.query("Status").strip().rstrip('\x00')


def ecCalClicked():
    label_1["text"]="EC Calibration"
    probe = AtlasI2C(100)
    label_info["text"]= probe.query("i").strip().rstrip('\x00')	
    label_cal["text"]= probe.query("cal,?").strip().rstrip('\x00')
    label_status["text"]= probe.query("Status").strip().rstrip('\x00')


def readTempClicked():	
    probe = AtlasI2C(102)
    tempRead_label["text"]= probe.query("R").strip().rstrip('\x00')


def btnExit():
  	root.destroy()

# we can exit when we press the escape key
def end_fullscreen(event):
	root.attributes("-fullscreen", False)


label_1 = Label(root, text="Raspberry Pi Graphical User Interface", font="Verdana 26 bold",
			fg="#000",
			bg="#99B898",
			pady = 1,
			padx = 1)

label_info = Label(root, text="", font="Verdana 26 bold",
			fg="#000",
			bg="#99B898",
			pady = 1,
			padx = 1)
label_cal = Label(root, text="", font="Verdana 26 bold",
			fg="#000",
			bg="#99B898",
			pady = 1,
			padx = 1)
label_status = Label(root, text="", font="Verdana 26 bold",
			fg="#000",
			bg="#99B898",
			pady = 1,
			padx = 1)

calTempButton = Button(root, text="Calibrate Temp", background = "#C06C84",
      command=btnExit, height=10, width=20, font = "Arial 16 bold")

readTempButton = Button(root, text="Read Temp", background = "#C06C84",
      command=readTempClicked, height=10, width=20, font = "Arial 16 bold")
		

exitButton = Button(root, text="Exit", background = "#C06C84",
      command=btnExit, height=10, width=20, font = "Arial 16 bold")
	

ledButton = Button(root, text="LED OFF",background = "#C06C84", 
      command=btnClicked, height=10, width=20, font = "Arial 16 bold")

tempCalButton = Button(root, text="Cal Temp",background = "#C06C84", 
      command=tempCalClicked, height=10, width=20, font = "Arial 16 bold")

tempRead_label = Button(root, text="",background = "#C06C84", 
      command=tempCalClicked, height=10, width=20, font = "Arial 16 bold")


phCalButton = Button(root, text="Cal pH",background = "#C06C84", 
      command=phCalClicked, height=10, width=20, font = "Arial 16 bold")


ecCalButton = Button(root, text="Cal EC",background = "#C06C84", 
      command=ecCalClicked, height=10, width=20, font = "Arial 16 bold")


label_1.grid(row=0, column=0, columnspan=3)
label_info.grid(row=1, column=1, columnspan=2)
label_cal.grid(row=2, column=1, columnspan=2)
label_status.grid(row=3, column=1, columnspan=2)
exitButton.grid(row = 1 ,column = 0, rowspan=3)
tempCalButton.grid(row = 4 ,column = 0)
phCalButton.grid(row = 4 ,column = 1)
ecCalButton.grid(row = 4 ,column = 2)
readTempButton.grid(row = 5 ,column = 0)
tempRead_label.grid(row = 5 ,column = 1)
calTempButton.grid(row = 5 ,column = 2)
readTempButton.forget()
calTempButton.forget()

root.bind("<Escape>", end_fullscreen)
root.mainloop()				# starts the GUI loop
