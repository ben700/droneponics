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
    bmp = Image.open(os.path.join(picdir, 'background.bmp'))	
    image.paste(bmp, (0,0))  
  
    draw = ImageDraw.Draw(image)
    draw.text((50, 50), 'Pump 1 = On', font = font30, fill = "BLACK")
    draw.text((50, 95), 'Pump 2 = On', font = font30, fill = "BLACK")
    draw.text((50, 140), 'Pump 3 = On', font = font30, fill = "BLACK")
    draw.text((50, 185), 'Pump 4 = On', font = font30, fill = "BLACK")
    
    
    disp.ShowImage(image)

updateLCD ()
