Convert Terraria textures to HD
===============================

How to run on Windows
---------------------

1. Clone the `https://github.com/sullerandras/terraria-hd-textures.git` repository in a folder. I recommend to use TortoiseGIT on Windows because it is easy to use.
2. Copy `c:\Program Files (x86)\Steam\steamapps\common\Terraria` to `terraria-hd-textures` and rename it to `Terraria.v1.3.5.1-read-only`. This is the input folder, make sure folder `terraria-hd-textures\Terraria.v1.3.5.1-read-only\Content\Images` exist.
3. Open a `cmd` window in `terraria-hd-textures`
4. Execute `bash execute.sh`. It should take 10-20 minutes to convert all Terraria textures. The resulting HD textures will be put into `terraria-hd-textures\Terraria.v1.3.5.1\Content\Images`.


How it works
------------

The `execute.sh` script is a Bash shell script. It can be edited by any text editor (e.g. VSCode or Atom).
At the end of the file you can see the what steps the script will execute:

```sh
extractPngsFromTerraria $SOURCE_XNB_FOLDER $EXTRACTED_FOLDER
downscalePngs $EXTRACTED_FOLDER $DOWNSCALED_FOLDER
removeSeparators $DOWNSCALED_FOLDER $NO_SEPARATORS_FOLDER
magnifyPngs $NO_SEPARATORS_FOLDER $MAGNIFIED_FOLDER "blend"
refillMissingPixels $EXTRACTED_FOLDER $MAGNIFIED_FOLDER $REFILLED_FOLDER
pngsToXnbs $REFILLED_FOLDER $TARGET_XNB_FOLDER
createRelease v0.9-1.3.5.1 $TARGET_XNB_FOLDER $RELEASE_FOLDER
```

1. Extract PNGs from XNB files
2. Resize images to 50% of the original size. This is because the original textures are made of 2x2 pixels, so we scale the images down first and they will be magnified in a later step.
3. Removing and filling separators from various tiles. Bigger textures like backgrounds and furnitures are made of smaller tiles, e.g. there is a "left side of the workbench" and "right side of the workbench" in one texture file with an empty line in between. In some of these textures the separator lines are filled with pink pixels. These pink lines caused lots of trouble because the magnified textures had pinkish lines around the edges (because the magnified images are anti aliased). In this step these pink lines are cleared.
4. Magnifying pngs. This step uses this project: https://code.google.com/archive/p/2dimagefilter/
5. Refill missing pixels. After magnification, some background textures had a few semi-transparent pixels at the corners of the little tiles. This step attempts to fill these so the background will be completely opaque (those transparent pixels were very annoying during play).
6. Convert magnified PNGs to XNBs.
7. Create a release by packing all XNBs into a "zip" file.

Configuration
-------------

At the top of the `execute.sh` file can be configured where to find the input XNBs and where to put the HD XNBs.

This is where the script will read the original XNB files:

```sh
SOURCE_XNB_FOLDER=Terraria.v1.3.5.1-read-only/Content/Images
```

This is where the HD textures will appear at the end:

```sh
TARGET_XNB_FOLDER=Terraria.v1.3.5.1/Content/Images
```

Feel free to configure these folders to your liking, but use forward slash `/` instead of backslash `\` as path separator.

Troubleshooting
---------------

If you get an error like below it means your textures are already HD:
```
writing file temp3/Gem_5.png
writing file temp3/Gem_6.png
writing file temp3/Ghost.png
ERROR:  Unexpected error while processing temp2\GlowSnail.png: Wrong column index: 8, colors: {"array('B', [55, 239, 233, 255])", "array('B', [13, 59, 58, 63])", "array('B', [101, 173, 181, 255])"}, y: 30
ERROR:  Traceback (most recent call last):
  File "tools/remove_separators.py", line 663, in remove_separators_from_images_in_folder
    remove_separators_from_file(input_filename=input_filename, output_filename=output_filename)
  File "tools/remove_separators.py", line 520, in remove_separators_from_file
    remove_separators(input_filename, clazz, pixelarray)
  File "tools/remove_separators.py", line 490, in remove_separators
    raise Exception('Wrong column index: %s, colors: %s, y: %s' % (x, pixels, y))
Exception: Wrong column index: 8, colors: {"array('B', [55, 239, 233, 255])", "array('B', [13, 59, 58, 63])", "array('B', [101, 173, 181, 255])"}, y: 30

Traceback (most recent call last):
  File "tools/remove_separators.py", line 673, in <module>
    remove_separators_from_images_in_folder(sys.argv[1], sys.argv[2])
  File "tools/remove_separators.py", line 667, in remove_separators_from_images_in_folder
    raise err
  File "tools/remove_separators.py", line 663, in remove_separators_from_images_in_folder
    remove_separators_from_file(input_filename=input_filename, output_filename=output_filename)
  File "tools/remove_separators.py", line 520, in remove_separators_from_file
    remove_separators(input_filename, clazz, pixelarray)
  File "tools/remove_separators.py", line 490, in remove_separators
    raise Exception('Wrong column index: %s, colors: %s, y: %s' % (x, pixels, y))
Exception: Wrong column index: 8, colors: {"array('B', [55, 239, 233, 255])", "array('B', [13, 59, 58, 63])", "array('B', [101, 173, 181, 255])"}, y: 30
```
