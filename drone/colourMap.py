#import colormap
import matplotlib
from colour import Color
from matplotlib import cm

def getTempColour(Temp):
     #normalize item number values to colormap
     norm = matplotlib.colors.Normalize(vmin=0, vmax=400)

     #colormap possible values = viridis, jet, spectral
     rgba_color = cm.coolwarm(norm(Temp),bytes=True) 
     print("rgba_color =" + str(rgba_color))

     c = Color(rgb=(rgba_color[0]/255,rgba_color[1]/255,rgba_color[2]/255))
     print("color =" + str(c))
     return c


def getMoistColour(MoistPer):
     print("getMoistColour(MoistPer) =" + str(MoistPer))
     #normalize item number values to colormap
     norm = matplotlib.colors.Normalize(vmin=0, vmax=100)

     #colormap possible values = viridis, jet, spectral
     rgba_color = cm.RdBu(norm(MoistPer),bytes=True) 
     print("rgba_color =" + str(rgba_color))

     c = Color(rgb=(rgba_color[0]/255,rgba_color[1]/255,rgba_color[2]/255))
     print("color =" + str(c))
     return c


def getPHColour(PH):
     #normalize item number values to colormap
     norm = matplotlib.colors.Normalize(vmin=0, vmax=140)

     #colormap possible values = viridis, jet, spectral
     rgba_color = cm.gist_rainbow(norm(PH),bytes=True) 
     print("rgba_color =" + str(rgba_color))

     c = Color(rgb=(rgba_color[0]/255,rgba_color[1]/255,rgba_color[2]/255))
     print("color =" + str(c))
     return c


def getECColour(EC):
     #normalize item number values to colormap
     norm = matplotlib.colors.Normalize(vmin=0, vmax=2000)

     #colormap possible values = viridis, jet, spectral
     rgba_color = cm.rainbow(norm(EC),bytes=True) 
     print("rgba_color =" + str(rgba_color))

     c = Color(rgb=(rgba_color[0]/255,rgba_color[1]/255,rgba_color[2]/255))
     print("color =" + str(c))
     return c
