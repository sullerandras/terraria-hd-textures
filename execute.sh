#!/usr/bin/env bash

set -e # exit on error
set -x # echo executed lines

SOURCE_XNB_FOLDER=Terraria.v1.4.0.2-read-only/Content/Images
EXTRACTED_FOLDER=temp1
DOWNSCALED_FOLDER=temp2
NO_SEPARATORS_FOLDER=temp3
MAGNIFIED_FOLDER=temp4
REFILLED_FOLDER=temp5
RELEASE_FOLDER=temp6-release
TARGET_XNB_FOLDER=Terraria.v1.4.0.2/Content/Images

function extractPngsFromTerraria() {
    echo "calling TExtract $1 => $2"
    java -jar "tools/TExtract 1.6.0.jar" --outputDirectory $2.temp $1
    mv $2.temp/Images $2
    rm -rf $2.temp
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
    mkdir -p $2/Items
    rsync -ax --delete-after $1/ $2/Others/
    rsync -ax --delete-after $1/UI/ $2/UI/
    mv $2/Others/Item_* $2/Items/
    rm -rf $2/Others/UI/
    if [ "$3" = "blend" ]; then
        wine tools/image_filter.exe "XBR" -wrap $2/Items $2
        wine tools/image_filter.exe "XBRz" $2/Others $2
        wine tools/image_filter.exe "XBRz" $1/UI $2/UI
    else
        wine tools/image_filter.exe "XBR-NoBlend" -wrap $2/Items $2
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
    rm -rf $3/Images/Accessories
    rm -rf $3/Images/Armor
    rm -rf $3/Images/Backgrounds
    rm -rf $3/Images/Misc
    rm -rf $3/Images/SplashScreens
    rm -rf $3/Images/TownNPCs
    rm -rf $3/Images/UI/Bestiary
    rm -rf $3/Images/UI/CharCreation
    rm -rf $3/Images/UI/Creative
    rm -rf $3/Images/UI/Minimap
    rm -rf $3/Images/UI/PlayerResourceSets
    rm -rf $3/Images/UI/WorldCreation
    rm -rf $3/Images/UI/WorldGen
    rm -rf $3/Images/UI/Button*
    echo "Enhanced version of the textures of Terraria 1.4.0.2" > $3/README.txt
    echo "" >> $3/README.txt
    echo "Crated by Andras Suller, `date +%F`, $version." >> $3/README.txt
    echo "For more information visit: http://forums.terraria.org/index.php?threads/enhanced-version-of-the-textures-of-terraria-1-3-0-8.39115/" >> $3/README.txt
    cd $3
    zip -r ../$out_file README.txt Images
    cd ..
}
#SOURCE_XNB_FOLDER="/home/andras/Downloads/Terraria_Soft_Pack_1-10-2016"
# extractPngsFromTerraria $SOURCE_XNB_FOLDER $EXTRACTED_FOLDER
# downscalePngs $EXTRACTED_FOLDER $DOWNSCALED_FOLDER
# removeSeparators $DOWNSCALED_FOLDER $NO_SEPARATORS_FOLDER
# magnifyPngs $NO_SEPARATORS_FOLDER $MAGNIFIED_FOLDER "blend"
# refillMissingPixels $EXTRACTED_FOLDER $MAGNIFIED_FOLDER $REFILLED_FOLDER
# pngsToXnbs $REFILLED_FOLDER $TARGET_XNB_FOLDER
createRelease v0.10-1.4.0.2 $TARGET_XNB_FOLDER $RELEASE_FOLDER
# createRelease v0.8-noblend-1.3.4.2 $TARGET_XNB_FOLDER $RELEASE_FOLDER
