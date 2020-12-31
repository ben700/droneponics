
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
from math import *
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)

LARGE_FONT= ("Verdana", 12)
f=None
pumpId=None
nutrientMix = []
sensors = []
calibrationEntry=None
calibrationLabel=None
resultLabel=None



class WiFiNetworkConfigurationPage(tk.Frame):

    def __init__(self, parent, controller):
        global nutrientMix, calibrationEntry, resultLabel, calibrationLabel
  
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="WiFi Network Configuration Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        
        
