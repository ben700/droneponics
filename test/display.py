#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import sys
import os
picdir = '/home/pi/droneponics/pic/'
libdir = '/home/pi/droneponics/lib/'
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import time
from waveshare_2inch_LCD import ST7789
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)


def updateLCD ():
    print ("2inch LCD Module")
    disp = ST7789.ST7789()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    
    image = Image.new('RGB', (disp.height,disp.width), (255,255,255)) 
    # read bmp file 
    bmp = Image.open(os.path.join(picdir, 'droneponics_logo.bmp'))	
    image.paste(bmp, (10,10))  
    disp.ShowImage(image)

updateLCD ()

