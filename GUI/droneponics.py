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

import tkinter as tk
root=tk.Tk()
root.wm_title("GUI")			# sets title of the window

load = Image.open("/home/pi/droneponics/pic/store_logo.png")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render)
img.image = render
img.place(x=0, y=0)
root.configure(bg="#99B898")		# change the background color 
root.attributes("-fullscreen", True) 	# set to fullscreen


frame=tk.Frame(root,bg='lightblue')
frame.place(relx=0.2,rely=0.2,relheight=0.6,relwidth=0.6)

def pumpPage1():
    label=tk.Label(frame,text='this is the pump 1')
    label.place(relx=0.3,rely=0.4)

def pumpPage2():
    label=tk.Label(frame,text='this is the pump 2')
    label.place(relx=0.3,rely=0.4)

def pumpPage3():
    label=tk.Label(frame,text='this is the pump 3')
    label.place(relx=0.3,rely=0.4)

def pumpPage4():
    label=tk.Label(frame,text='this is the pump 4')
    label.place(relx=0.3,rely=0.4)
	

def btnExit():
  	root.destroy()

# we can exit when we press the escape key
def end_fullscreen(event):
	root.attributes("-fullscreen", False)


label_1 = Label(root, text="Droneponics AI Interface", font="Verdana 26 bold",
			fg="Black",
			bg="#99B898",
			pady = 1,
			padx = 1)


label_1.grid(row=0, column=1, columnspan=4)

bt1=tk.Button(root,text='Set-up',command=pumpPage1)
bt1.grid(row=1,column=0)

bt2=tk.Button(root,text='Operation',command=pumpPage2)
bt2.grid(row=1,column=1)

bt3=tk.Button(root,text='Calibration',command=pumpPage3)
bt3.grid(row=1,column=2)

exitBt=tk.Button(root,text='Exit',command=btnExit)
exitBt.grid(row=1,column=3)

root.bind("<Escape>", end_fullscreen)
root.mainloop()				# starts the GUI loop
