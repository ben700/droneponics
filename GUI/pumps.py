#!/usr/bin/python3
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)
import drone
import logging

from tkinter import * 			# imports the Tkinter lib
# pip install pillow
from PIL import Image, ImageTk

    # tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)

restartCode = {'P': "Powered Off", 'S':"Software Reset",'B':"Brown Out",'W':"Watchdog",'U':"Unknown"}


root = Tk()				# create the root object
root.wm_title("GUI")			# sets title of the window

load = Image.open("/home/pi/droneponics/pic/store_logo.png")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render)
img.image = render
img.place(x=0, y=0)
root.configure(bg="#99B898")		# change the background color 
root.attributes("-fullscreen", True) 	# set to fullscreen


def btnExit():
  	root.destroy()

# we can exit when we press the escape key
def end_fullscreen(event):
	root.attributes("-fullscreen", False)


mainLabel = Label(root, text="Droneponics Pump Calibration Interface", font="Verdana 26 bold",
			fg="Black",
			bg="#99B898",
			pady = 1,
			padx = 1)


pump1Button = Button(root, text="Pump 1", background = "#C06C84",
      command=btnExit, height=5, width=15, font = "Arial 16 bold")

pump2Button = Button(root, text="Pump 2", background = "#C06C84",
      command=btnExit, height=5, width=15, font = "Arial 16 bold")

pump3Button = Button(root, text="Pump 3", background = "#C06C84",
      command=btnExit, height=5, width=15, font = "Arial 16 bold")

pump4Button = Button(root, text="Pump 4", background = "#C06C84",
      command=btnExit, height=5, width=15, font = "Arial 16 bold")

pump5Button = Button(root, text="Pump 5", background = "#C06C84",
      command=btnExit, height=5, width=15, font = "Arial 16 bold")

pump6Button = Button(root, text="Pump 6", background = "#C06C84",
      command=btnExit, height=5, width=15, font = "Arial 16 bold")

pump7Button = Button(root, text="Pump 7", background = "#C06C84",
      command=btnExit, height=5, width=15, font = "Arial 16 bold")


exitButton = Button(root, text="Exit", background = "#C06C84",
      command=btnExit, height=5, width=15, font = "Arial 16 bold")
	

mainLabel.grid(row=0, column=1, columnspan=4)
pump1Button.grid(row=3, column=0)
pump2Button.grid(row=3, column=1)
pump3Button.grid(row=3, column=2)
pump4Button.grid(row=3, column=3)
pump5Button.grid(row=4, column=4)
pump6Button.grid(row=4, column=5)
pump7Button.grid(row=4, column=6)
exitButton.grid(row = 1,column = 0, rowspan=3)


	
root.bind("<Escape>", end_fullscreen)
root.mainloop()				# starts the GUI loop
