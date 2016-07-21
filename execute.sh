#!/usr/bin/env bash

SOURCE_XNB_FOLDER=Terraria.v1.3.1-read-only/Content/Images
EXTRACTED_FOLDER=temp1
DOWNSCALED_FOLDER=temp2
NO_SEPARATORS_FOLDER=temp3
MAGNIFIED_FOLDER=temp4
REFILLED_FOLDER=temp5
RELEASE_FOLDER=temp6-release
TARGET_XNB_FOLDER=Terraria.v1.3.1/Content/Images

function extractPngsFromTerraria() {
    echo "calling TExtract $1 => $2"
    mkdir -p $2
    mkdir -p $2/UI
    java -jar "tools/TExtract 1.6.0.jar" --outputDirectory $2.temp $1
    mv $2.temp/Images $2
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
    rsync -ax --delete-after $1/*.png $2/Others/
    mkdir -p $2/Items
    mv $2/Others/Item_* $2/Items/
    if [ "$3" = "blend" ]; then
        wine tools/image_filter.exe "XBR" $2/Items $2
        wine tools/image_filter.exe "XBRz" $2/Others $2
        wine tools/image_filter.exe "XBRz" $1/UI $2/UI
    else
        wine tools/image_filter.exe "XBR-NoBlend" $2/Items $2
        wine tools/image_filter.exe "XBR-NoBlend" $2/Others $2
        wine tools/image_filter.exe "XBR-NoBlend" $1/UI $2/UI
    fi
}
function refillMissingPixels() {
    echo "refilling missing pixels in Walls and Tiles $2 => $3"
    mkdir -p $3
    mkdir -p $3/UI
    wine tools/refill_missing_pixels.exe $1 $2 $3
    wine tools/refill_missing_pixels.exe $1/UI $2/UI $3/UI
}
function pngsToXnbs() {
    echo "converting to XNB's $1 => $2"
    mkdir -p $2
    mkdir -p $2/UI
    wine tools/png_to_xnb.exe $1 $2
    wine tools/png_to_xnb.exe $1/UI $2/UI
}
function createRelease() {
    version=$1
    out_file=Images-$version.zip
    echo "Creating zip file Images-$version.zip with all XNB's"
    mkdir -p $3/Images
    rm -f $out_file
    rsync -ax --delete-after $2 $3
    rm -rf $3/Images/Backgrounds
    rm -rf $3/Images/Misc
    rm -rf $3/Images/UI/WorldGen
    rm -rf $3/Images/UI/Button*
    echo "Enhanced version of the textures of Terraria 1.3.0.8" > $3/README.txt
    echo "" >> $3/README.txt
    echo "Crated by Andras Suller, `date +%F`, $version." >> $3/README.txt
    echo "For more information visit: http://forums.terraria.org/index.php?threads/enhanced-version-of-the-textures-of-terraria-1-3-0-8.39115/" >> $3/README.txt
    cd $3
    zip -r ../$out_file README.txt Images
    cd ..
}
extractPngsFromTerraria $SOURCE_XNB_FOLDER $EXTRACTED_FOLDER
downscalePngs $EXTRACTED_FOLDER $DOWNSCALED_FOLDER
removeSeparators $DOWNSCALED_FOLDER $NO_SEPARATORS_FOLDER
magnifyPngs $NO_SEPARATORS_FOLDER $MAGNIFIED_FOLDER "blend"
refillMissingPixels $EXTRACTED_FOLDER $MAGNIFIED_FOLDER $REFILLED_FOLDER
pngsToXnbs $REFILLED_FOLDER $TARGET_XNB_FOLDER
createRelease v0.5-1.3.1 $TARGET_XNB_FOLDER $RELEASE_FOLDER
# createRelease v0.5-noblend-1.3.1 $TARGET_XNB_FOLDER $RELEASE_FOLDER
