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



btFrame=tk.Frame(root,bg='darkblue')
btFrame.place(relx=0.2,rely=0.1,relheight=0.2,relwidth=0.6)

def pumpPage1():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 1')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pumpPage1)
    bbt2=tk.Button(actionFrame,text='Start',command=pumpPage1)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)

def pumpPage2():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 2')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pumpPage1)
    bbt2=tk.Button(actionFrame,text='Start',command=pumpPage1)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)

def pumpPage3():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 3')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pumpPage1)
    bbt2=tk.Button(actionFrame,text='Start',command=pumpPage1)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)

def pumpPage4():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 4')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pumpPage1)
    bbt2=tk.Button(actionFrame,text='Start',command=pumpPage1)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)

def pumpPage5():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 5')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pumpPage1)
    bbt2=tk.Button(actionFrame,text='Start',command=pumpPage1)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)

def pumpPage6():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 6')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pumpPage1)
    bbt2=tk.Button(actionFrame,text='Start',command=pumpPage1)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)

def pumpPage7():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 7')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pumpPage1)
    bbt2=tk.Button(actionFrame,text='Start',command=pumpPage1)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)


def pumpPage8():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 8')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pumpPage1)
    bbt2=tk.Button(actionFrame,text='Start',command=pumpPage1)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)


def btnExit():
  	root.destroy()

# we can exit when we press the escape key
def end_fullscreen(event):
	root.attributes("-fullscreen", False)


exitBt=tk.Button(btFrame,text='Exit',command=btnExit)
exitBt.grid(row=1,column=3)

bt1=tk.Button(btFrame,text='Relay 1',command=pumpPage1)
bt1.grid(row=1,column=0)

bt2=tk.Button(btFrame,text='Relay 2',command=pumpPage2)
bt2.grid(row=1,column=1)

bt3=tk.Button(btFrame,text='Relay 3',command=pumpPage3)
bt3.grid(row=1,column=2)

bt4=tk.Button(btFrame,text='Relay 4',command=pumpPage4)
bt4.grid(row=1,column=3)

bt5=tk.Button(btFrame,text='Relay 5',command=pumpPage5)
bt5.grid(row=2,column=0)

bt6=tk.Button(btFrame,text='Relay 6',command=pumpPage6)
bt6.grid(row=2,column=1)

bt7=tk.Button(btFrame,text='Relay 7',command=pumpPage7)
bt7.grid(row=2,column=2)

bt8=tk.Button(btFrame,text='Relay 8',command=pumpPage8)
bt8.grid(row=2,column=3)

root.bind("<Escape>", end_fullscreen)
root.mainloop()				# starts the GUI loop
