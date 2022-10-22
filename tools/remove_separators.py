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


SEPARATORS = [
        array.array('B', [0x60, 0x33, 0x57, 0xff]),
        array.array('B', [0x6c, 0x4c, 0x6c, 0xff]),
        array.array('B', [0x78, 0x37, 0x79, 0xff]),
        array.array('B', [0x7e, 0x50, 0x7e, 0xff]),
        array.array('B', [0x7f, 0x4b, 0x80, 0xff]),
        array.array('B', [0x85, 0x57, 0x86, 0xff]),
        array.array('B', [0x8b, 0x77, 0xf9, 0xff]),
        array.array('B', [0x8f, 0x50, 0x90, 0xff]),
        array.array('B', [0x92, 0x5c, 0x93, 0xff]),
        array.array('B', [0x9a, 0x46, 0x9c, 0xff]),
        array.array('B', [0xa0, 0x61, 0xa1, 0xff]),
        array.array('B', [0xa7, 0x6d, 0xa8, 0xff]),
        array.array('B', [0xae, 0x4f, 0xb0, 0xff]),
        array.array('B', [0xaf, 0x73, 0xb0, 0xff]),
        array.array('B', [0xb6, 0x6f, 0xb8, 0xff]),
        array.array('B', [0xb9, 0x46, 0xb9, 0xff]),
        array.array('B', [0xbd, 0x6a, 0xa2, 0xff]),
        array.array('B', [0xc4, 0x9e, 0xe0, 0xff]),
        array.array('B', [0xd5, 0xa8, 0xc2, 0xff]),
        array.array('B', [0xd9, 0xc2, 0x98, 0xff]),
        array.array('B', [0xdf, 0x77, 0xf9, 0xff]),
        array.array('B', [0xe1, 0x55, 0xe5, 0xff]),
        array.array('B', [0xe2, 0x8a, 0xee, 0xff]),
        array.array('B', [0xe3, 0x36, 0xe8, 0xff]),
        array.array('B', [0xe5, 0x8b, 0xe6, 0xff]),
        array.array('B', [0xe8, 0xd5, 0x36, 0xff]),
        array.array('B', [0xed, 0x77, 0xf9, 0xff]),
        array.array('B', [0xf6, 0x77, 0xf9, 0xff]),
        array.array('B', [0xf7, 0x73, 0xff, 0xff]),
        array.array('B', [0xf7, 0x77, 0xf9, 0xff]),
        array.array('B', [0xf8, 0x77, 0xf9, 0xff]),
        array.array('B', [0xf8, 0x80, 0xf9, 0xff]),
        array.array('B', [0xf9, 0x77, 0x8f, 0xff]),
        array.array('B', [0xf9, 0x77, 0xc3, 0xff]),
        array.array('B', [0xf9, 0xc5, 0xfa, 0xff]),
        array.array('B', [0xfa, 0x6b, 0xfc, 0xff]),
        array.array('B', [0xfd, 0x71, 0xff, 0xff]),
        array.array('B', [0xff, 0x00, 0xd4, 0xff]),
        array.array('B', [0xff, 0x71, 0xdb, 0xff]),
        array.array('B', [137, 65, 138, 210]),
        array.array('B', [167, 80, 168, 210]),
        array.array('B', [185, 102, 200, 204]),
        array.array('B', [196, 94, 198, 247]),
        array.array('B', [199, 96, 201, 206]),
        array.array('B', [203, 98, 205, 210]),
        array.array('B', [21, 10, 22, 76]),
        ]

def SEP(grid_size):
    return lambda x: x % grid_size == (grid_size - 1)
SEP9 = lambda x: x % 9 == 8

CLASS_SEPARATORS = {
    'glowsnail-27x378': {
        'column': [8, 17, 26],
        'row': lambda x: x % 9 == 8
    },
    'jellyfishbowl-18x180': {
        'column': [8, 17],
        'row': lambda x: x % 9 == 8
    },
    'liquid-153x8': {
        'column': lambda x: x % 9 == 8,
        'row': []
    },
    'shroomtops-93x22': {
        'column': lambda x: x % 31 == 30,
        'row': [21]
    },
    'glow-144x198': SEP(9),
    'glow-72x252': {
        'column': SEP(9),
        'row':    lambda x: x % 28 == 27 or x % 28 == 17 or x % 28 == 8
    },
    'glow-65x108': {
        'column': [],
        'row': SEP(9),
    },
    'tilecracks-54x36': SEP(9),
    'tiles-144x135': SEP(9),
    'tiles-144x198': SEP(9),
    'tiles-gross-144x198': SEP(9),
    'tilesbeach-144x198': SEP(9),
    'tiles-26x991': SEP(9),
    'tiles-35x604': SEP(9),
    'tiles-35x991': SEP(9),
    'tiles-883x35': SEP(9),
    'tiles-26x35': SEP(9),
    'tiles-109x8': SEP(9),
    'tiles-550x44': SEP(9),
    'tiles-918x27': SEP(9),
    'tiles-27x54': SEP(9),
    'tiles-117x45': SEP(9),
    'tiles-18x198': SEP(9),
    'tiles-35x26': SEP(9),
    'tiles-162x36': SEP(9),
    'tiles-72x18': SEP(9),
    'tiles-36x18': SEP(9),
    'tiles-17x45': {
        'column': [],
        'row': [],
    },
    'tiles-36x684': SEP(9),
    'tiles-27x18': SEP(9),
    'tiles-54x36': SEP(9),
    'tiles-270x54': SEP(9),
    'tiles-35x17': SEP(9),
    'tiles-63x108': SEP(9),
    'tiles-954x36': SEP(9),
    'tiles-945x18': SEP(9),
    'tiles-945x36': SEP(9),
    'tiles-243x293': SEP(9),
    'tiles-198x252': SEP(9),
    'tiles-108x243': SEP(9),
    'tiles-53x26': SEP(9),
    'tiles-162x162': SEP(9),
    'tiles-27x90': SEP(9),
    'tiles-27x36': SEP(9),
    'tiles-27x270': SEP(9),
    'tiles-27x108': SEP(9),
    'tiles-27x81': SEP(9),
    'tiles-27x189': SEP(9),
    'tiles-243x36': SEP(9),
    'tiles-54x18': SEP(9),
    'tiles-17x72': SEP(9),
    'tiles-207x9': SEP(9),
    'tiles-972x54': SEP(9),
    'tiles-36x243': SEP(9),
    'tiles-107x971': SEP(9),
    'tiles-27x162': SEP(9),
    'tiles-54x108': SEP(9),
    'tiles-126x27': SEP(9),
    'tiles-26x400': SEP(9),
    'tiles-27x216': SEP(9),
    'tiles-90x108': SEP(9),
    'tiles-162x45': SEP(9),
    'tiles-117x90': SEP(9),
    'tiles-54x594': SEP(9),
    'tiles-54x486': SEP(9),
    'tiles-54x648': SEP(9),
    'tiles-54x513': SEP(9),
    'tiles-54x612': SEP(9),
    'tiles-18x306': SEP(9),
    'tiles-27x378': SEP(9),
    'tiles-18x288': SEP(9),
    'tiles-18x9': SEP(9),
    'tiles-27x432': SEP(9),
    'tiles-27x360': SEP(9),
    'tiles-27x135': SEP(9),
    'tiles-27x324': SEP(9),
    'tiles-54x432': SEP(9),
    'tiles-35x35': SEP(9),
    'tiles-27x342': SEP(9),
    'tiles-72x72': SEP(9),
    'tiles-18x180': SEP(9),
    'tiles-18x27': SEP(9),
    'tiles-117x360': SEP(9),
    'tiles-54x27': SEP(9),
    'tiles-117x180': SEP(9),
    'tiles-648x27': SEP(9),
    'tiles-53x1000': SEP(9),
    'tiles-36x162': SEP(9),
    'tiles-117x135': SEP(9),
    'tiles-72x9': SEP(9),
    'tiles-36x297': SEP(9),
    'tiles-162x180': SEP(9),
    'tiles-36x72': SEP(9),
    'tiles-9x126': SEP(9),
    'tiles-27x558': SEP(9),
    'tiles-27x612': SEP(9),
    'tiles-90x18': SEP(9),
    'tiles-26x26': SEP(9),
    'tiles-17x712': SEP(9),
    'tiles-53x8': SEP(9),
    'tiles-197x17': SEP(9),
    'tiles-26x17': SEP(9),
    'tiles-829x17': SEP(9),
    'tiles-775x17': SEP(9),
    'tiles-910x17': SEP(9),
    'tiles-71x585': SEP(9),
    'tiles-1000x81': SEP(9),
    'tiles-18x53': SEP(9),
    'tiles-18x856': SEP(9),

    # ===================================
    'tiles-207x11': { 'column': SEP9, 'row': [10] },
    'tiles-72x17': { 'column': SEP9, 'row': [16] },
    'tiles-27x20': { 'column': SEP9, 'row': [19] },
    'tiles-162x19': { 'column': SEP9, 'row': [8, 18] },
    'tiles-27x27': { 'column': SEP9, 'row': [] },
    'tiles-17x17': {
        'column': [8],
        'row':    [8]
    },
    'tiles-18x18': {
        'column': [8, 17],
        'row':    [17] # this is tricky as 8 should be here for some images for example Tiles_142 and 143
    },
    'tiles-34x17': { 'column': SEP9, 'row': [8] },
    'tiles-53x36': { 'column': SEP9, 'row': [8, 17, 26] },
    'tiles-81x9': { 'column': SEP9, 'row': [8] },
    'tiles-35x9': { 'column': SEP9, 'row': [] },
    'tiles-36x10': { 'column': SEP9, 'row': [9] },
    'tiles-45x11': { 'column': SEP9, 'row': [10] },
    'tiles-189x17': { 'column': SEP9, 'row': [16] },
    'tiles-153x17': { 'column': SEP9, 'row': [16] },
    'tiles-8x100': { 'column': [], 'row': [] },
    'tiles-32x64': { 'column': [], 'row': [] },
    'tiles-8x8': { 'column': [], 'row': [] },
    'tiles-9x9': { 'column': [], 'row': [] },
    'tiles-9x18': { 'column': [8], 'row': [8, 17] },
    'tiles-18x11': { 'column': [8, 17], 'row': [10] },
    'tiles-18x760': {
        'column': SEP9,
        'row':    lambda x: x % 20 >= 18 or x % 20 == 8
    },
    'tiles-26x228': {
        'column': SEP9,
        'row':    [8, 18, 27, 37, 46, 56, 65, 75, 85, 94, 103, 113, 122, 132, 141, 151, 160, 170, 179, 189, 198, 208, 217, 227]
    },
    'tiles-18x651': {
        'column': SEP9,
        'row':    lambda x: x % 19 == 18 or x % 19 == 8
    },
    'tiles-1000x57': {
        'column': SEP9,
        'row':    lambda x: x % 19 == 18 or x % 19 == 8
    },
    'tiles-53x114': {
        'column': SEP9,
        'row':    lambda x: x % 19 == 18 or x % 19 == 8
    },
    'tiles-964x18': {
        'column': SEP9,
        'row':    [8]
    },
    'tiles-54x19': {
        'column': SEP9,
        'row':    lambda x: x % 19 == 18 or x % 19 == 8
    },
    'tiles-54x76': {
        'column': SEP9,
        'row':    lambda x: x % 19 == 18 or x % 19 == 8
    },
    'tiles-54x153': {
        'column': SEP9,
        'row':    lambda x: x % 19 == 18 or x % 19 == 8
    },
    'tiles-36x19': {
        'column': SEP9,
        'row':    lambda x: x % 19 == 18 or x % 19 == 8
    },
    'tiles-25x228': {
        'column': SEP9,
        'row':    lambda x: x % 19 == 18 or x % 19 == 8
    },
    'tiles-72x605': {
        'column': SEP9,
        'row':    lambda x: (x < 566 and x % 18 == 8) or (x >= 566 and x - 1 % 18 == 8) # row 567 is the empty row instead of 566
    },
    'tiles-27x196': {
        'column': SEP9,
        'row':    lambda x: x % 28 == 27 or x % 28 == 17
    },
    'tiles-72x252': {
        'column': SEP9,
        'row':    lambda x: x % 28 == 27 or x % 28 == 17 or x % 28 == 8
    },
    'tiles-65x108': {
        'column': lambda x: x % 11 == 10,
        'row':    SEP9
    },
    'tiles-270x19': {
        'column': SEP9,
        'row':    lambda x: x % 19 == 18
    },
    'tiles-63x27': {
        'column': SEP9,
        'row':    []
    },
    'tiles-10x76': {
        'column': [9],
        'row':    lambda x: x % 20 == 8
    },
    'tiles-204x20': {
        'column': lambda x: x % 17 == 16,
        'row':    [19]
    },
    'tiles-121x44': {
        'column': lambda x: x % 11 == 10,
        'row':    lambda x: x % 11 == 10
    },
    'tiles-32x22': {
        'column': lambda x: x % 11 == 10,
        'row':    lambda x: x % 11 == 10
    },
    'tiles-32x22': {
        'column': lambda x: x % 11 == 10,
        'row':    lambda x: x % 11 == 10
    },
    'tiles-88x132': {
        'column': lambda x: x % 11 == 10,
        'row':    lambda x: x % 11 == 10
    },
    'tiles-78x14': {
        'column': lambda x: x % 13 == 12,
        'row':    [13]
    },
    'tiles-63x11': {
        'column': SEP9,
        'row':    [10]
    },
    'tiles-18x447': {
        'column': SEP9,
        'row':    lambda x: x % 11 == 10
    },
    'tiles-9x11': {
        'column': SEP9,
        'row':    lambda x: x % 11 == 10
    },
    'tiles-9x94': {
        'column': SEP9,
        'row':    [9, 18, 27, 36, 46, 56, 65, 74, 83, 93]
    },
    'tiles-604x10': {
        'column': SEP9,
        'row':    [9]
    },
    'tiles-66x176': {
        'column': [10, 21, 32, 43, 54, 65],
        'row':    [10, 21, 32, 43, 54, 65, 76, 87, 98, 109, 120, 131, 142, 153, 164, 175]
    },

    'treebranches-42x63': SEP(21),
    'treebranches-42x189': SEP(21),
    'treetops-123x41': SEP(41),
    'treetops-174x49': { 'column': SEP(58), 'row': [48] },
    'treetops-123x164': SEP(41),
    'treetops-369x71': { 'column': SEP(41), 'row': [70] },
    'wall-234x90': lambda x: x % 18 >= 16,
    'wall-234x720': lambda x: x % 18 >= 16,
    'wall-234x810': lambda x: x % 18 >= 16,
    'wall-234x180': lambda x: x % 18 >= 16,
    'wall-234x126': lambda x: x % 18 >= 16,
    'wires-45x36': SEP(9),
    'wires-20x20': [],
    'wires-16x16': [],
    'wires-8x8': [],
    'wiresnew-144x144': SEP(9),
    'wizarddefault-20x736': [],
    'wizarddefaultparty-20x736': [],
    'wraitheyes-13x100': [],
    'xmas-32x64': [],
    'xmas-198x65': { 'column': SEP(33), 'row': [64] },
    'xmas-363x65': { 'column': SEP(33), 'row': [64] },
    'xmas-132x65': { 'column': SEP(33), 'row': [64] },
    'xmas-363x260': { 'column': SEP(33), 'row': SEP(65) },
    'xmaslight-54x36': SEP(9),
}

def get_separators_for_class(clazz, width, height):
    key = '%s-%dx%d' % (clazz, width, height)
    if key not in CLASS_SEPARATORS:
        if clazz < 'wires' or clazz == 'yzszgq':
            return ([], [])
        raise Exception('add "%s" to CLASS_SEPARATORS' % key)
    s = CLASS_SEPARATORS[key]
    if isinstance(s, dict):
        column = s['column']
        row    = s['row']
    else:
        column = s
        row = s
    if callable(column):
        column = [x for x in range(width) if column(x)]
    if callable(row):
        row = [x for x in range(height) if row(x)]
    return (row, column)

def is_separator_color(color):
    return color[3] == 0 or color in SEPARATORS

# def check_grid_size(pixelarray, gridx, gridy):
#     if (pixelarray.width < gridx) or (pixelarray.height < gridy):
#         return False # cannot be sure that the grid is matching
#     total = 0
#     match = 0
#     for y in range(gridy - 1, pixelarray.height, gridy):
#         for x in range(pixelarray.width):
#             total += 1
#             if is_separator_color(pixelarray.getPixelAt(x, y)):
#                 match += 1
#         for x in range(gridx - 1, pixelarray.width, gridx):
#             for yy in range(y - gridy + 1, y):
#                 total += 1
#                 if is_separator_color(pixelarray.getPixelAt(x, yy)):
#                     match += 1
#     if (float(match) / float(total)) > 0.99:
#         return True
#     else:
#         print("total: %s, match: %s (%.2f%%)" % (total, match, 100.0 * match / total))
#         return False

# def detect_grid_size(pixelarray):
#     for x in range(5, pixelarray.width):
#         if pixelarray.isTransparent(x, 0):
#             continue
#         color = pixelarray.getPixelAt(x, 0)
#         for y in range(pixelarray.height):
#             good = True
#             for xx in range(x, -1, -1):
#                 if color != pixelarray.getPixelAt(xx, y):
#                     good = False
#                     break
#             if good:
#                 return (x + 1, y + 1)
#             if xx == x:
#                 break
#     # try 9:9 as grid size
#     if check_grid_size(pixelarray, 9, 9):
#         return (9, 9)
#     return (0, 0)

def is_column_all_separator(pixelarray, x):
    for y in range(pixelarray.height):
        if not is_separator_color(pixelarray.getPixelAt(x, y)):
            return False
    return True

def is_row_all_separator(pixelarray, y):
    for x in range(pixelarray.width):
        if not is_separator_color(pixelarray.getPixelAt(x, y)):
            return False
    return True

def detect_and_clear_separators(pixelarray):
    """ Returns: (row_indexes, column_indexes) """
    flags = [is_column_all_separator(pixelarray, x) for x in range(pixelarray.width)]
    for x in range(pixelarray.width):
        if flags[x]:
            for y in range(pixelarray.height):
                pixelarray.setPixelAt(x, y, TRANSPARENT)

    column_indexes = [i - 1 for i in range(2, len(flags)) if not flags[i - 2] and flags[i - 1] and not flags[i]]

    flags = [is_row_all_separator(pixelarray, y) for y in range(pixelarray.height)]
    for y in range(pixelarray.height):
        if flags[y]:
            for x in range(pixelarray.width):
                pixelarray.setPixelAt(x, y, TRANSPARENT)
    row_indexes = [i - 1 for i in range(2, len(flags)) if not flags[i - 2] and flags[i - 1] and not flags[i]]

    return (row_indexes, column_indexes)

def remove_separators(input_filename, clazz, pixelarray):
    # (row_indexes, column_indexes) = detect_and_clear_separators(pixelarray)
    (row_indexes, column_indexes) = get_separators_for_class(clazz, pixelarray.width, pixelarray.height)
    # clear separator lines first, because if 2 separator lines are next to
    # each other then both lines would remain the same color
    for x in column_indexes:
        pixels = set()
        for y in range(pixelarray.height):
            if not pixelarray.isTransparent(x, y):
                pixels.add(str(pixelarray.getPixelAt(x, y)))
                if len(pixels) >= 3:
                    if ntpath.basename(input_filename) in ['Tiles_11.png', 'Tiles_19.png', 'Tiles_73.png', 'Tiles_190.png', 'Tiles_198.png', 'Tiles_222.png', 'Tiles_229.png', 'Tiles_247.png', 'Tiles_274.png', 'Tree_Branches_3.png', 'Wall_60.png', 'Wall_73.png', 'Wall_136.png', 'Tiles_505.png']:
                        # print('Wrong column index in file %s: %s, colors: %s' % (ntpath.basename(input_filename), x, pixels))
                        pixels = set()
                    else:
                        raise Exception('Wrong column index: %s, colors: %s' % (x, pixels))
            pixelarray.setPixelAt(x, y, TRANSPARENT)

    for y in row_indexes:
        pixels = set()
        for x in range(pixelarray.width):
            if not pixelarray.isTransparent(x, y):
                pixels.add(str(pixelarray.getPixelAt(x, y)))
                if len(pixels) >= 3:
                    if ntpath.basename(input_filename) in ['Tiles_17.png', 'Tiles_73.png', 'Tiles_126.png', 'Tiles_203.png', 'Tiles_229.png', 'Tiles_274.png', 'Tiles_32.png', 'Tiles_352.png', 'Tiles_443.png', 'Tiles_69.png', 'Wall_60.png', 'Wall_73.png', 'Tiles_575.png', 'Tiles_80.png']:
                        # print('Wrong row index in file %s: %s, colors: %s' % (ntpath.basename(input_filename), y, pixels))
                        pixels = set()
                    else:
                        raise Exception('Wrong row index: %s, colors: %s' % (y, pixels))
            pixelarray.setPixelAt(x, y, TRANSPARENT)
    # fill the now empty separator lines with the nearest pixel
    if ntpath.basename(input_filename)[0 : 5] != 'Wall_': # don't fill for walls, it looks clunky
        for x in column_indexes:
            for y in range(pixelarray.height):
                pixelarray.setPixelAt(x, y, pixelarray.nearestNonSeparator(x, y, vertical=True))
        for y in row_indexes:
            for x in range(pixelarray.width):
                pixelarray.setPixelAt(x, y, pixelarray.nearestNonSeparator(x, y, vertical=False))

def remove_separators_from_file(input_filename, output_filename):
    img=png.Reader(filename=input_filename)
    (width, height, pixels, meta) = img.asRGBA8()
    data = [row for row in pixels]
    pixelarray = Array3D(data, width, height, depth=4)
    clazz = class_for_filename(ntpath.basename(input_filename))
    remove_separators(input_filename, clazz, pixelarray)

    writer = png.Writer(width=width, height=height, alpha=True, bitdepth=8, greyscale=False, compression=9)
    print('writing file %s' % output_filename)
    f = open(output_filename, 'wb')
    try:
        writer.write(f, pixelarray.data)
    finally:
        f.close()

# remove_separators_from_file(
#     input_filename='/Users/andras/Downloads/Images_original_extracted-downsized/Tiles_1.png',
#     output_filename='/Users/andras/Downloads/Tiles_1.png')
# remove_separators_from_file(
#     input_filename='/Users/andras/Downloads/Images_original_extracted-downsized/Wall_87.png',
#     output_filename='/Users/andras/Downloads/Wall_87.png')

def stats_for_file(input_filename):
    img = png.Reader(filename = input_filename)
    (width, height, pixels, meta) = img.asRGBA()
    data = [row for row in pixels]
    pixelarray = Array3D(data, width, height, depth=4)
    column_indexes = [x for x in range(pixelarray.width) if is_column_all_separator(pixelarray, x)]
    row_indexes = [y for y in range(pixelarray.height) if is_row_all_separator(pixelarray, y)]
    return (ntpath.basename(input_filename), width, height, row_indexes, column_indexes)

def save_to_file(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_from_file(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def generate_stats_file():
    stats = {}
    for input_filename in glob.glob('/Users/andras/Downloads/Images_original_extracted-downsized/*.png'):
        print(input_filename)
        data = stats_for_file(input_filename=input_filename)
        key = '%dx%d' % (data[1], data[2])
        if key not in stats:
            stats[key] = []
        stats[key].append(data)
    save_to_file(stats, 'stats.pickle')

def class_for_filename(filename):
    filename = filename.lower()
    filename = filename.replace('.png', '')
    filename = re.sub(r"[_0-9]+", "", filename)
    return filename

def process_stats():
    stats = load_from_file('stats.pickle')
    for key, values in sorted(stats.items()):
        if len(values) > 1:
            column_index_counts = {}
            row_index_counts = {}
            class_counts = {}
            for (filename, width, height, row_indexes, column_indexes) in values:
                for i in column_indexes:
                    if i not in column_index_counts:
                        column_index_counts[i] = 0
                    column_index_counts[i] += 1
                for i in row_indexes:
                    if i not in row_index_counts:
                        row_index_counts[i] = 0
                    row_index_counts[i] += 1
                clazz = class_for_filename(filename)
                if clazz not in class_counts:
                    class_counts[clazz] = 0
                class_counts[clazz] += 1
            if len(column_index_counts) > 0 or len(row_index_counts) > 0:
                print(key, len(values))
                print('  column_index_counts: %s' % (sorted(column_index_counts.items()),))
                print('  row_index_counts: %s' % (sorted(row_index_counts.items()),))
                print('  types: %s' % (sorted(class_counts.items()),))

def process_grouped_stats():
    stats = load_from_file('stats.pickle')
    values = [item for items in stats.values() for item in items]
    stats = {}
    for (filename, width, height, row_indexes, column_indexes) in values:
        clazz = class_for_filename(filename)
        key = "%s-%4dx%4d" % (clazz, width, height)
        if key not in stats:
            stats[key] = {
                'column_index_counts': {},
                'row_index_counts': {},
                'class_counts': {},
                'count': 0,
                'width': width,
                'height': height
                }
        stats[key]['count'] += 1
        for i in column_indexes:
            if i not in stats[key]['column_index_counts']:
                stats[key]['column_index_counts'][i] = 0
            stats[key]['column_index_counts'][i] += 1
        for i in row_indexes:
            if i not in stats[key]['row_index_counts']:
                stats[key]['row_index_counts'][i] = 0
            stats[key]['row_index_counts'][i] += 1
        clazz = class_for_filename(filename)
        if clazz not in stats[key]['class_counts']:
            stats[key]['class_counts'][clazz] = 0
        stats[key]['class_counts'][clazz] += 1

    for key, value in sorted(stats.items()):
        column_index_counts = value['column_index_counts']
        row_index_counts = value['row_index_counts']
        class_counts = value['class_counts']
        count = value['count']
        width = value['width']
        height = value['height']
        lencic = len(column_index_counts)
        lenric = len(row_index_counts)
        # if count >= 10 and ((lencic > 0 and lencic*100/width < 50) or (lenric > 0 and lenric*100/height < 50)):
        if True:
            print('%s (count: %s)' % (key, count))
            print('  column_index_counts (%d): %s' % (lencic, sorted(column_index_counts.items()),))
            common = [x for x in sorted(column_index_counts.items()) if x[1]>=0.8*count]
            print('  common column indexes (%d): %s' % (len(common), common,))
            print('  row_index_counts (%d): %s' % (lenric, sorted(row_index_counts.items()),))
            common = [x for x in sorted(row_index_counts.items()) if x[1]>=0.8*count]
            print('  common row indexes (%d): %s' % (len(common), common,))
            print('  types: %s' % (sorted(class_counts.items()),))

def remove_separators_from_all_tiles():
    for input_filename in glob.glob('/Users/andras/Downloads/Images_original_extracted-downsized/*.png'):
        output_filename = '/Users/andras/Downloads/Images-downsized-removed-separators/%s' % (ntpath.basename(input_filename))
        try:
            remove_separators_from_file(
                input_filename=input_filename,
                output_filename=output_filename)
        except Exception as err:
            print("Unexpected error while processing %s: %s" % (ntpath.basename(input_filename), str(err)))
            traceback.print_exc()
            raise err

def remove_separators_from_images_in_folder(input_dir, output_dir):
    for input_filename in sorted(glob.glob('%s/*.png' % (input_dir,))):
        output_filename = '%s/%s' % (output_dir, ntpath.basename(input_filename))
        try:
            remove_separators_from_file(input_filename=input_filename, output_filename=output_filename)
        except Exception as err:
            error("Unexpected error while processing %s: %s" % (input_filename, str(err)))
            error(traceback.format_exc())
            raise err

if len(sys.argv) < 3:
    print("Usage: python %s input_dir output_dir" % (sys.argv[0],))
    print("Remove separators from all images in input_dir and saves the result in output_dir (with the same name).")
else:
    remove_separators_from_images_in_folder(sys.argv[1], sys.argv[2])
# stats_for_file('/Users/andras/Downloads/Images_original_extracted-downsized/Tiles_206.png')
# generate_stats_file()
# process_stats()
# process_grouped_stats()

# import cProfile
# cProfile.run('remove_separators_from_all_tiles()', sort=1)
