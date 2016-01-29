from __future__ import print_function
import glob
import ntpath
import png
import traceback
import sys

from Array3D import Array3D

def error(*objs):
    print("ERROR: ", *objs, file=sys.stderr)

def downscale_pixelarray(pixelarray):
    width = (pixelarray.width + 1) / 2
    height = (pixelarray.height + 1) / 2
    data = [[0 for x in xrange(0, width * pixelarray.depth)] for y in xrange(0, height)]
    for y in xrange(0, height):
        for x in xrange(0, width):
            for i in xrange(4):
                data[y][x * pixelarray.depth + i] = pixelarray.data[y * 2][x * pixelarray.depth * 2 + i]
    return Array3D(data, width, height, pixelarray.depth)

def downscale_image(input_filename, output_filename):
    img = png.Reader(filename=input_filename)
    (width, height, pixels, meta) = img.asRGBA8()
    data = [row for row in pixels]
    pixelarray = Array3D(data, width, height, depth=4)
    pixelarray = downscale_pixelarray(pixelarray)

    writer = png.Writer(width=pixelarray.width, height=pixelarray.height, alpha=True, bitdepth=8, compression=9)
    print('writing file %s' % output_filename)
    f = open(output_filename, 'wb')
    try:
        writer.write(f, pixelarray.data)
    finally:
        f.close()

def downscale_images(input_dir, output_dir):
    for input_filename in glob.glob('%s/*.png' % (input_dir,)):
        output_filename = '%s/%s' % (output_dir, ntpath.basename(input_filename))
        try:
            downscale_image(input_filename=input_filename, output_filename=output_filename)
        except Exception as err:
            error("Unexpected error while processing %s: %s" % (input_filename, str(err)))
            error(traceback.format_exc())
            raise err

if len(sys.argv) < 3:
    print("Usage: python %s input_dir output_dir" % (sys.argv[0],))
    print("Downcale all *.png images in input_dir and saves the result in output_dir (with the same name).")
else:
    downscale_images(sys.argv[1], sys.argv[2])
