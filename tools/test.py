from __future__ import print_function
import array
import glob
import ntpath
import pickle
import png
import re
import sys
import traceback

from Array3D import Array3D

TRANSPARENT = (0, 0, 0, 0)

def error(*objs):
    print("ERROR: ", *objs, file=sys.stderr)

def read_as_pixelarray(filename):
    img = png.Reader(filename = filename)
    (width, height, pixels, meta) = img.asRGBA8()
    data = [row for row in pixels]
    pixelarray = Array3D(data, width, height, depth=4)
    return pixelarray

def color_difference(color1, color2):
    sum = 0
    for i in range(4):
        sum += pow(color1[i] - color2[i], 2)
    return sum

def nearest_color(color, used_colors):
    if color[3] < 120:
        return TRANSPARENT
    min_difference = color_difference(color, used_colors[0])
    nearest = used_colors[0]
    for c in used_colors:
        diff = color_difference(color, c)
        if diff < min_difference:
            min_difference = diff
            nearest = c
    # print('nearest color to %s: %s', (color, nearest))
    return nearest

def sharpen(input_filename, original_pixelarray, pixelarray):
    used_colors = []
    for x in xrange(original_pixelarray.width):
        for y in xrange(original_pixelarray.height):
            color = original_pixelarray.getPixelAt(x, y)
            if not (color in used_colors):
                used_colors.append(color)
    print('used_colors: %s' % (used_colors,))

    for x in xrange(pixelarray.width):
        for y in xrange(pixelarray.height):
            color = pixelarray.getPixelAt(x, y)
            color = nearest_color(color, used_colors)
            pixelarray.setPixelAt(x, y, color)



def sharpen_image(original_filename, input_filename, output_filename):
    original_pixelarray = read_as_pixelarray(original_filename)
    pixelarray = read_as_pixelarray(input_filename)
    sharpen(input_filename, original_pixelarray, pixelarray)

    writer = png.Writer(width=pixelarray.width, height=pixelarray.height, alpha=True, bitdepth=8, compression=9)
    print('writing file %s' % output_filename)
    f = open(output_filename, 'wb')
    try:
        writer.write(f, pixelarray.data)
    finally:
        f.close()

# sharpen_image(sys.argv[1], sys.argv[2])
sharpen_image('Item_1.png', 'Item_1-smooth.png', 'Item_1-sharpened.png')

# import cProfile
# cProfile.run('remove_separators_from_all_tiles()', sort=1)
