Compile Terraria textures to higher resolution.

Old technique:
1. extract png files from Terraria xnb files
2. downscale extracted png files to 50%
3. clear separator lines
4. magnify downscaled images with ImageResizer-r133.exe
5. convert magnified images to xnb

New idea:
- instead of clearing the separator lines, we remove those rows and columns from the images (making them smaller)
- after the magnification, we need to reinsert the separator rows and columns
- This would make the magnified images smoother and hopefully no artifacts at the edges / corners
Problems:
- The tiles in the image may not belong to each other. For example there are multiple chests in a single image file, and there should be empty columns between the chests to make them nicely magnified, but no empty columns at the middle of the chests. This is especially hard to do with Walls and Tiles images because there are several variations and each of them should be compatible with any other variation.
