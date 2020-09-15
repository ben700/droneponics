#import colormap
import matplotlib
from colour import Color
from matplotlib import cm

#normalize item number values to colormap
norm = matplotlib.colors.Normalize(vmin=0, vmax=400)

#colormap possible values = viridis, jet, spectral
rgba_color = cm.coolwarm(norm(100),bytes=True) 
print("rgba_color =" + str(rgba_color))

c = Color(rgb=(rgba_color[0]/255,rgba_color[1]/255,rgba_color[2]/255))
print("color =" + str(c))


#400 is one of value between 0 and 1000
