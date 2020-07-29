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
print(picdir)

try:
    print ("2inch LCD Module")
    disp = ST7789.ST7789()
    # Initialize library.
    disp.Init()

    # Clear display.
    disp.clear()

    # image = Image.new('RGB', (disp.width,disp.height), (255,255,255)) 
    image = Image.new('RGB', (disp.height,disp.width), (255,255,255)) 

    draw = ImageDraw.Draw(image)

    font30 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    print ("***draw line")
    draw.line([(40,20),(200,20)], fill = "BLUE",width = 5)
    draw.line([(40,20),(40,200)], fill = "BLUE",width = 5)
    draw.line([(40,200),(200,200)], fill = "BLUE",width = 5)
    draw.line([(200,20),(200,200)], fill = "BLUE",width = 5)
    
    print ("***draw rectangle")
    print(str(disp.height))
    print(str(disp.width))
    
    draw.rectangle([(270,310),(10,10)],fill = "RED")
    
    print ("***draw text")
    draw.text((60,30), 'annabella', font = font30, fill = "WHITE")
    draw.text((50, 75), 'Ada', font = font15, fill = "BLUE")
    draw.text((75, 110), 'Shepley ', font = font15, fill = "BLUE")
    draw.text((72, 140), 'Test Program ', font = font15, fill = "BLUE")

    image=image.rotate(180) 
    disp.ShowImage(image)
    time.sleep(3)

    # read bmp file 
    bmp = Image.open(os.path.join(picdir, 'LCD_2inch.bmp'))	
    image.paste(bmp, (0,0))  
    image=image.rotate(180)
    disp.ShowImage(image)

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    exit()
