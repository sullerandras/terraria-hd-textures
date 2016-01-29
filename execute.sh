#!/usr/bin/env bash

TERRARIA_CONTENT_FOLDER=Terraria.v1.3.0.8-read-only/Content
EXTRACTED_FOLDER=temp1
DOWNSCALED_FOLDER=temp2
NO_SEPARATORS_FOLDER=temp3
MAGNIFIED_FOLDER=temp4
REFILLED_FOLDER=temp5
RELEASE_FOLDER=temp6-release
TARGET_TERRARIA_CONTENT_FOLDER=Terraria.v1.3.0.8/Content

function extractPngsFromTerraria() {
    echo "calling TExtract $1 => $2"
    mkdir -p $2
    mkdir -p $2/UI
    java -jar "tools/TExtract 1.6.0.jar" --outputDirectory $2 $1/Images/*.xnb
    java -jar "tools/TExtract 1.6.0.jar" --outputDirectory $2/UI $1/Images/UI/*.xnb
}
function downscalePngs() {
    echo "downscaling images $1 => $2"
    mkdir -p $2
    mkdir -p $2/UI
    wine tools/downscale_pngs.exe "$1" "$2"
    wine tools/downscale_pngs.exe "$1/UI" "$2/UI"
}
function removeSeparators() {
    echo "removing separators $1 => $2"
    mkdir -p $2
    mkdir -p $2/UI
    python tools/remove_separators.py "$1" "$2"
    python tools/remove_separators.py "$1/UI" "$2/UI"
}
function magnifyPngs() {
    echo "magnifying images $1 => $2"
    mkdir -p $2
    mkdir -p $2/UI
    RESIZE_METHOD="XBRz 2x(vbounds=wrap,hbounds=wrap)"

    for filename in `ls $1 | grep -i png`; do
      echo /load "$1/$filename" /resize auto "\"$RESIZE_METHOD\"" /save "$2/$filename"
    done > test.scr
    for filename in `ls $1/UI | grep -i png`; do
      echo /load "$1/UI/$filename" /resize auto "\"$RESIZE_METHOD\"" /save "$2/UI/$filename"
    done >> test.scr
    wine tools/ImageResizer-r133.exe /script test.scr
}
function refillMissingPixels() {
    echo "refilling missing pixels in Walls and Tiles $1 => $2"
    mkdir -p $2
    mkdir -p $2/UI
    wine tools/refill_missing_pixels.exe $1 $2
    wine tools/refill_missing_pixels.exe $1/UI $2/UI
}
function pngsToXnbs() {
    echo "converting to XNB's $1 => $2"
    mkdir -p $2/Images
    mkdir -p $2/Images/UI
    wine tools/png_to_xnb.exe $1 $2/Images
    wine tools/png_to_xnb.exe $1/UI $2/Images/UI
}
function createRelease() {
    version=$1
    out_file=Images-$version.zip
    echo "Creating zip file Images-$version.zip with all XNB's"
    mkdir -p $3/Images
    rm -f $out_file
    rsync -ax --delete-after $2/Images/ $3/Images/
    rm -rf --preserve-root $3/Images/Backgrounds
    rm -rf --preserve-root $3/Images/Misc
    echo "Enhanced version of the textures of Terraria 1.3.0.8" > $3/README.txt
    echo "" >> $3/README.txt
    echo "Crated by Andras Suller, `date +%F`, $version." >> $3/README.txt
    echo "For more information visit: http://forums.terraria.org/index.php?threads/enhanced-version-of-the-textures-of-terraria-1-3-0-8.39115/" >> $3/README.txt
    cd $3
    zip -r ../$out_file README.txt Images
    cd ..
}
function horizontalFlipImages() {
    echo "horizontal flip images $1 => $2"
    mkdir -p $2
    mkdir -p $2/UI
    wine tools/flip_horizontally.exe $1 $2
    wine tools/flip_horizontally.exe $1/UI $2/UI
}
function mergeNormalAndFlippedImages() {
    echo "merge normal magnified and flipped magnified images $1 + $2 => $3"
    mkdir -p $3
    mkdir -p $3/UI
    wine tools/merge_images.exe $1 $2 $3
    wine tools/merge_images.exe $1/UI $2/UI $3/UI
}
extractPngsFromTerraria $TERRARIA_CONTENT_FOLDER $EXTRACTED_FOLDER
downscalePngs $EXTRACTED_FOLDER $DOWNSCALED_FOLDER
removeSeparators $DOWNSCALED_FOLDER $NO_SEPARATORS_FOLDER
horizontalFlipImages $NO_SEPARATORS_FOLDER $NO_SEPARATORS_FOLDER-hflip
magnifyPngs $NO_SEPARATORS_FOLDER $MAGNIFIED_FOLDER
magnifyPngs $NO_SEPARATORS_FOLDER-hflip $MAGNIFIED_FOLDER-hflip
horizontalFlipImages $MAGNIFIED_FOLDER-hflip $MAGNIFIED_FOLDER-hflip-hflip
mergeNormalAndFlippedImages $MAGNIFIED_FOLDER $MAGNIFIED_FOLDER-hflip-hflip $MAGNIFIED_FOLDER-merged
refillMissingPixels $MAGNIFIED_FOLDER-merged $REFILLED_FOLDER
pngsToXnbs $REFILLED_FOLDER $TARGET_TERRARIA_CONTENT_FOLDER
createRelease v0.3 $TARGET_TERRARIA_CONTENT_FOLDER $RELEASE_FOLDER
