import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
#from matplotlib.colors import hsv_to_rgb

imageOri = cv.imread( 'Lenna_512_color.tif' )
imgHSI = cv.cvtColor( imageOri, cv.COLOR_BGR2HSV )
imageOri = cv.cvtColor( imageOri, cv.COLOR_BGR2RGB )

h, s, i = cv.split( imgHSI )
fig = plt.figure()
axis = fig.add_subplot( 1, 1, 1, projection = "3d" )

pixel_colors = imageOri.reshape((np.shape( imageOri )[0]*np.shape( imageOri )[1], 3 ))
norm = colors.Normalize( vmin = -1., vmax = 1. )
norm.autoscale( pixel_colors )
pixel_colors = norm( pixel_colors ).tolist()

axis.scatter( h.flatten(), s.flatten(), i.flatten(), edgecolors = pixel_colors, marker = "." )
axis.set_xlabel( "Hue" )
axis.set_ylabel( "Saturation" )
axis.set_zlabel( "value" )
plt.show()

