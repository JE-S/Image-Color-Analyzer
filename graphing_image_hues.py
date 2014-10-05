import matplotlib.colors as colors
from matplotlib import gridspec
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image
import os, os.path
import matplotlib
import numpy


# functions:

def getPixels(filename):
    ''' receives an image and returns numpy array of RGB pixel values '''
    image = Image.open(filename)
    image_data = image.getdata()
    pixel_data = numpy.array(image_data)

    return pixel_data

def getVariableValues(pixel):
    ''' receives pixel and returns max, min, and delta of values (between 0 and 1) for R, G, B ''' 
    R_ratio = pixel[0] / 255
    G_ratio = pixel[1] / 255
    B_ratio = pixel[2] / 255

    max_value = max(R_ratio, G_ratio, B_ratio)
    min_value = min(R_ratio, G_ratio, B_ratio)

    delta = max_value - min_value

    return R_ratio, G_ratio, B_ratio, max_value, min_value, delta

def getHue(r, g, b, max_val, min_val, delt):
    ''' receives R, G, B, max, min, and delta value of a pixel and returns the hue number (0 - 359) '''
    if (delt > 0):
        if (max_val == r):
            hue = 60 * (((g - b) / delt) % 6)
        if (max_val == g):
            hue = 60 * (((b - r) / delt) + 2)
        if (max_val == b):
            hue = 60 * (((r - g) / delt) + 4)
    else:
        hue = 0

    hue = int(round(hue, 0))
    
    return hue


# graph pixel hues in image:

hue_values = dict.fromkeys(range(0, 360), 0)
hue_list, keys, values = ([] for i in range(3))

image = str(input("Enter image path: "))

while os.path.exists(image) == False:
    image = str(input("File not found. Enter image path: "))
    

pixels = getPixels(image) # numpy array of RGB values of all pixels in image

for pixel in pixels: # determine hue for each pixel and append hue to list
    r, g, b, maxv, minv, delt = getVariableValues(pixel)
    hue = getHue(r, g, b, maxv, minv, delt)
    hue_list.append(hue)

for hue in hue_list: # raise value in dictionary by one for each time hue appears in list
    hue_values[hue] += 1 

for k in hue_values.keys(): # separate keys to own list
    keys.append(k)

for v in hue_values.values(): # separate key values to own list
    values.append(v)


fig = plt.figure() # make linegraph

gs = gridspec.GridSpec(2, 1, height_ratios = [10, 1]) 

plt.subplot(gs[0])
plt.plot(keys, values)
plt.title('Pixel Hues of "{}"\n'.format(image.split("\\")[-1]))
plt.xlim([0, 359])
plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
plt.ylabel('Num of Pixels\n({} total pixels)'.format(len(hue_list)))

ax = fig.add_subplot(gs[1])
norm = matplotlib.colors.Normalize(vmin = 0, vmax = 359)
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap = matplotlib.cm.hsv, orientation='horizontal', norm = norm, ticks = [])                              

plt.show()
