#!/usr/bin/env bash

#set -e # exit on error
set -x # echo executed lines

SOURCE_XNB_FOLDER=~/.local/share/Steam/steamapps/common/Terraria/Content/Images
EXTRACTED_FOLDER=EXTRACTED_FOLDER
DOWNSCALED_FOLDER=DOWNSCALED_FOLDER
NO_SEPARATORS_FOLDER=NO_SEPARATORS_FOLDER
MAGNIFIED_FOLDER=MAGNIFIED_FOLDER
REFILLED_FOLDER=REFILLED_FOLDER
RELEASE_FOLDER=pack/Content

function extractPngsFromTerraria() {
    mkdir -p $2
    echo "calling TExtract $1 => $2"
    java -jar "tools/TExtract.jar" --outputDirectory $2 $1
}
function downscalePngs() {
    echo "downscaling images $1 => $2"
    mkdir -p $2
    mkdir -p $2/UI
    wine tools/downscale_pngs.exe $1/Images $2
    wine tools/downscale_pngs.exe $1/Images/UI $2/UI
}
function removeSeparators() {
    echo "removing separators $1 => $2"
    mkdir -p $2
    mkdir -p $2/UI
    python tools/remove_separators.py $1 $2
    python tools/remove_separators.py $1/UI $2/UI
}
function magnifyPngs() {
    echo "magnifying images $1 => $2"
    mkdir -p $2rm -rf $EXTRACTED_FOLDER

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
    wine tools/refill_missing_pixels.exe $1/Images $2 $3
    wine tools/refill_missing_pixels.exe $1/Images/UI $2/UI $3/UI
}
function createRelease() {
    version=$1
    echo "Making pack folder"
    mkdir -p $3/Images
    #mv -v $2 $3/Images
    find $2 -type f -print0 | xargs -0 mv -t $3/Images
    echo "Enhanced version of the textures of Terraria 1.4.0.2" > $3/README.txt
    echo "" >> $3/README.txt
    rm pack/pack.json
    echo " {
    \"Name\": \"HD Textures\",
    \"Author\": \"sullerandras\",
    \"Description\": \"HD Textures\",
    \"Version\": {
        \"major\": 1,
        \"minor\": 0
    }
}" >> pack/pack.json
    echo "Crated by Andras Suller, modified by Danny Piper for Terraria 1.4.0.* texture pack `date +%F`, $version." >> $3/README.txt
    echo "For more information visit: http://forums.terraria.org/index.php?threads/enhanced-version-of-the-textures-of-terraria-1-3-0-8.39115/" >> $3/README.txt
}

 extractPngsFromTerraria $SOURCE_XNB_FOLDER $EXTRACTED_FOLDER
 downscalePngs $EXTRACTED_FOLDER $DOWNSCALED_FOLDER
 removeSeparators $DOWNSCALED_FOLDER $NO_SEPARATORS_FOLDER
 magnifyPngs $NO_SEPARATORS_FOLDER $MAGNIFIED_FOLDER "blend"
 refillMissingPixels $EXTRACTED_FOLDER $MAGNIFIED_FOLDER $REFILLED_FOLDER
 createRelease v0.10-1.4.0.2 $REFILLED_FOLDER $RELEASE_FOLDER

echo "Deleting temp folders"
rm -rf $EXTRACTED_FOLDER
rm -rf $DOWNSCALED_FOLDER
rm -rf $NO_SEPARATORS_FOLDER
rm -rf $MAGNIFIED_FOLDER
rm -rf $REFILLED_FOLDER
