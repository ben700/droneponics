#import colormap
import matplotlib
from colour import Color
from matplotlib import cm

colours = {1: '#00FF00', 0: '#FFFFFF', '0': '#FFFFFF', '1': '#00FF00', 2: '#FF0000', '2': '#FF0000', 3: '#00FFFF', '3': '#00FFFF','OFFLINE': '#0000FF', 'ONLINE': '#00FF00', 'UNAVILABLE': '#002700'}

def getTempColour(_log, Temp):
     try:
          _log.info("getTempColour Temp =" + str(Temp))
          #normalize item number values to colormap
          norm = matplotlib.colors.Normalize(vmin=0, vmax=400)

          #colormap possible values = viridis, jet, spectral
          rgba_color = cm.coolwarm(norm(int(Temp)),bytes=True) 
          #rgba_color = cm.RdBu(norm(Temp),bytes=True) 
     
          _log.info("rgba_color =" + str(rgba_color))
          c = Color(rgb=(rgba_color[0]/255,rgba_color[1]/255,rgba_color[2]/255))
          _log.info("getTempColour =" + str(c))
     except:
          _log.error("Error in Fx getTempColour")
          c = '#0000FF'
     return c

def getCO2Colour(_log, CO2):
     try:
          norm = matplotlib.colors.Normalize(vmin=0, vmax=2000)
          #rgba_color = cm.winter(norm(int(CO2)),bytes=True) 
          rgba_color = cm.spring(norm(int(CO2)),bytes=True)           
          c = Color(rgb=(rgba_color[0]/255,rgba_color[1]/255,rgba_color[2]/255))
     except:
          _log.error("Error in Fx getCO2Colour")
          c = '#0000FF'
     return c

def getMoistColour(_log, MoistPer):
     _log.info("getMoistColour(MoistPer) =" + str(MoistPer))
     #normalize item number values to colormap
     norm = matplotlib.colors.Normalize(vmin=0, vmax=100)

     #colormap possible values = viridis, jet, spectral
     rgba_color = cm.coolwarm(norm(int(MoistPer)),bytes=True) 
     #rgba_color = cm.RdBu(norm(MoistPer),bytes=True) 
     _log.info("rgba_color =" + str(rgba_color))

     c = Color(rgb=(rgba_color[0]/255,rgba_color[1]/255,rgba_color[2]/255))
     _log.info("getMoistColour =" + str(c))
     return c

def getLightColors(_log, LightPer):
     try:
          _log.info("lightColors(LightPer) =" + str(LightPer))
          #normalize item number values to colormap
          norm = matplotlib.colors.Normalize(vmin=0, vmax=100)

          #colormap possible values = viridis, jet, spectral
          #rgba_color = cm.RdBu(norm(LightPer),bytes=True) 
          rgba_color = cm.autumn(norm(int(LightPer)),bytes=True) 
     
          _log.info("rgba_color =" + str(rgba_color))

          c = Color(rgb=(rgba_color[0]/255,rgba_color[1]/255,rgba_color[2]/255))
          _log.info("getLightColors =" + str(c))
     except:
          c= '#00FF00'
     return c


def getPHColour(_log, PH):
     #normalize item number values to colormap
     norm = matplotlib.colors.Normalize(vmin=0, vmax=140)

     #colormap possible values = viridis, jet, spectral
     rgba_color = cm.plasma(norm(int(PH)),bytes=True) 
     _log.info("rgba_color =" + str(rgba_color))

     c = Color(rgb=(rgba_color[0]/255,rgba_color[1]/255,rgba_color[2]/255))
     _log.info("getPHColour =" + str(c))
     return c


def getECColour(_log, EC):
     _log.info("getECColour(_log, EC) EC = " + str(EC))
     #normalize item number values to colormap
     norm = matplotlib.colors.Normalize(vmin=0, vmax=2000)

     #colormap possible values = viridis, jet, spectral,gist_rainbow,  BrBG
     rgba_color = cm.BrBG(norm(int(EC)),bytes=True) 
     _log.info("rgba_color =" + str(rgba_color))

     c = Color(rgb=(rgba_color[0]/255,rgba_color[1]/255,rgba_color[2]/255))
     _log.info("getECColour =" + str(c))
     return c
