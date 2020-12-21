import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import urllib
import urllib.request
import shlex, requests
import json
import time
import pandas as pd
import numpy as np
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)
import drone
from configparser import ConfigParser
import logging
sys.path.append('/home/pi/droneponics/GUI')
from droneGUI import *
import droneGUI

parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configOxy/"+drone.gethostname()+".ini")



# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))
_log.critical("critical")
_log.error("error")
_log.warning("warning")
_log.info("info")
_log.debug("debug")

_log.info("/home/pi/droneponics/config/configOxy/"+drone.gethostname()+".ini")


droneGUI.nutrientMix = drone.buildOxyMix(nutrientMix, _log)


nutrientMix[0].pump=AtlasI2C(nutrientMix[0].pumpId)
label1Text = nutrientMix[0].pump.query("Cal,?").strip().rstrip('\x00')
print(label1Text)
label2Text = nutrientMix[0].pump.query("Cal,clear").strip().rstrip('\x00')
print(label2Text)
nutrientMix[0].pump.query("D,10")
time.sleep(10)
label3Text = nutrientMix[0].pump.query("Cal,10").strip().rstrip('\x00')
print(label3Text)
label4Text = nutrientMix[0].pump.query("Cal,?").strip().rstrip('\x00')
print(label4Text)
