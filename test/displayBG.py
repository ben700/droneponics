#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import sys
import os
picdir = '/home/pi/droneponics/pic/'
libdir = '/home/pi/droneponics/lib/'
if os.path.exists(libdir):
    sys.path.append(libdir)

if os.path.exists(picdir):
    sys.path.append(picdir)
    
import logging
import time
from waveshare_2inch_LCD import ST7789
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.INFO)


def updateLCD ():
    print ("2inch LCD Module")
    disp = ST7789.ST7789()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    
    image = Image.new('RGB', (disp.height,disp.width), (255,255,255)) 

    font30 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    # read bmp file 
    bmp = Image.open(os.path.join(picdir, 'droneponics_logo.bmp'))	
    image.paste(bmp, (0,0))  
  
    
    disp.ShowImage(image)

updateLCD ()
