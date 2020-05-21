SOURCE_XNB_FOLDER='Terraria.v1.4.0.2-read-only/Content/Images'
EXTRACTED_FOLDER='temp1'
DOWNSCALED_FOLDER='temp2'
NO_SEPARATORS_FOLDER='temp3'
MAGNIFIED_FOLDER='temp4'
REFILLED_FOLDER='temp5'
RELEASE_FOLDER='temp6-release'
TEXTURE_PACK_FOLDER='temp6-texture-pack'
TARGET_XNB_FOLDER='Terraria.v1.4.0.2/Content/Images'

FOLDERS = [
  '',
  '/UI',
  '/UI/WorldGen',
  '/UI/PlayerResourceSets',
  '/UI/PlayerResourceSets/HorizontalBars',
  '/UI/PlayerResourceSets/FancyClassic',
  '/UI/CharCreation',
  '/UI/WorldCreation',
  '/UI/Minimap',
  '/UI/Minimap/Leaf',
  '/UI/Minimap/StoneGold',
  '/UI/Minimap/Golden',
  '/UI/Minimap/Default',
  '/UI/Minimap/Valkyrie',
  '/UI/Minimap/TwigLeaf',
  '/UI/Minimap/Sticks',
  '/UI/Minimap/Retro',
  '/UI/Minimap/Remix',
  '/UI/Bestiary',
  '/UI/Bestiary/NPCs',
  '/UI/Creative',
  '/Accessories',
  '/TownNPCs',
  '/Armor',
]

def execute(command_string)
  puts command_string
  system(command_string)
end

def extractPngsFromTerraria(input, output)
  puts "calling TExtract #{input} => #{output}"
  execute %(java -jar "tools/TExtract 1.6.0.jar" --outputDirectory #{output}.temp #{input})
  execute %(mv #{output}.temp/Images #{output})
  execute %(rm -rf #{output}.temp)
end

def downscalePngs(input, output)
  puts "downscaling images #{input} => #{output}"
  FOLDERS.each do |folder|
    execute %(mkdir -p #{output}#{folder})
    execute %(wine tools/downscale_pngs.exe "#{input}#{folder}" "#{output}#{folder}")
  end
end

def removeSeparators(input, output)
  puts "removing separators #{input} => #{output}"
  FOLDERS.each do |folder|
    execute %(mkdir -p #{output}#{folder})
    execute %(python tools/remove_separators.py "#{input}#{folder}" "#{output}#{folder}")
  end
end

def magnifyPngs(input, output, blend=true)
  puts "magnifying images #{input} => #{output}"
  temp = "#{output}.temp"
  execute %(rsync -ax --delete-after #{input}/ #{temp}/)
  execute %(mkdir -p #{temp}/items-wrap)
  execute %(mv #{temp}/Item_* #{temp}/items-wrap/)
  FOLDERS.each do |folder|
    execute %(mkdir -p #{output}#{folder})
    if blend
      execute %(wine tools/image_filter.exe "XBRz" #{temp}#{folder} #{output}#{folder})
    else
      execute %(wine tools/image_filter.exe "XBR-NoBlend" #{temp}#{folder} #{output}#{folder})
    end
  end
  # convert Item images with "wrap" magnifier algorithm (does not produce artifacts near the edges)
  if blend
    execute %(wine tools/image_filter.exe "XBR" -wrap #{temp}/items-wrap #{output})
  else
    execute %(wine tools/image_filter.exe "XBR-NoBlend" -wrap #{temp}/items-wrap #{output})
  end
end

def refillMissingPixels(original_folder, input, output)
  puts "refilling missing pixels in Walls and Tiles #{input} => #{output}"
  FOLDERS.each do |folder|
    execute %(mkdir -p #{output}#{folder})
    execute %(wine tools/refill_missing_pixels.exe #{original_folder}#{folder} #{input}#{folder} #{output}#{folder})
  end
end

# def pngsToXnbs()
#     puts "converting to XNB's $1 => $2"
#     mkdir -p $2
#     mkdir -p $2/UI
#     wine tools/png_to_xnb.exe $1 $2
#     wine tools/png_to_xnb.exe $1/UI $2/UI
# end

# def createRelease()
#     version=$1
#     out_file=Images-$version.zip
#     puts "Creating zip file Images-$version.zip with all XNB's"
#     mkdir -p $3/Images
#     rm -f $out_file
#     rsync -ax --delete-after $2/ $3/
#     rm -rf $3/Images/Accessories
#     rm -rf $3/Images/Armor
#     rm -rf $3/Images/Backgrounds
#     rm -rf $3/Images/Misc
#     rm -rf $3/Images/SplashScreens
#     rm -rf $3/Images/TownNPCs
#     rm -rf $3/Images/UI/Bestiary
#     rm -rf $3/Images/UI/CharCreation
#     rm -rf $3/Images/UI/Creative
#     rm -rf $3/Images/UI/Minimap
#     rm -rf $3/Images/UI/PlayerResourceSets
#     rm -rf $3/Images/UI/WorldCreation
#     rm -rf $3/Images/UI/WorldGen
#     rm -rf $3/Images/UI/Button*
#     echo "Enhanced version of the textures of Terraria 1.4.0.2" > $3/README.txt
#     echo "" >> $3/README.txt
#     echo "Crated by Andras Suller, `date +%F`, $version." >> $3/README.txt
#     echo "For more information visit: http://forums.terraria.org/index.php?threads/enhanced-version-of-the-textures-of-terraria-1-3-0-8.39115/" >> $3/README.txt
#     cd $3
#     zip -r ../$out_file README.txt Images pack.json
#     cd ..
# end

def createTexturePack(major_version, minor_version, terraria_version, input, temp)
    version = "v#{major_version}.#{minor_version}-#{terraria_version}"
    out_file = "TexturePack-#{version}.zip"
    puts "Creating zip file #{out_file} with all PNG's"
    execute %(mkdir -p #{temp}/Content/Images)
    execute %(rm -f #{out_file})
    execute %(rsync -ax --delete-after #{input}/ #{temp}/Content/Images/)
    execute %(rm -rf #{temp}/Content/Images/Backgrounds)
    execute %(rm -rf #{temp}/Content/Images/Misc)
    execute %(rm -rf #{temp}/Content/Images/UI/WorldGen)
    execute %(rm -rf #{temp}/Content/Images/UI/Button*)
    File.write("#{temp}/pack.json", %({
    "Name": "HD Textures #{version}",
    "Author": "Andras Suller",
    "Description": "HD Textures #{version}",
    "Version": {
        "major": #{major_version},
        "minor": #{minor_version}
    }
}))
    File.write("#{temp}/README.txt", "Enhanced version of the textures of Terraria #{terraria_version}

Crated by Andras Suller, #{`date +%F`.chomp}, #{version}.
For more information visit: http://forums.terraria.org/index.php?threads/enhanced-version-of-the-textures-of-terraria-1-3-0-8.39115/")
    execute %(cd #{temp} && zip -r ../#{out_file} -0 README.txt Content pack.json && cd ..)
  end

#SOURCE_XNB_FOLDER="/home/andras/Downloads/Terraria_Soft_Pack_1-10-2016"
# extractPngsFromTerraria(SOURCE_XNB_FOLDER, EXTRACTED_FOLDER)
# downscalePngs(EXTRACTED_FOLDER, DOWNSCALED_FOLDER)
# removeSeparators(DOWNSCALED_FOLDER, NO_SEPARATORS_FOLDER)
# magnifyPngs(NO_SEPARATORS_FOLDER, MAGNIFIED_FOLDER, "blend")
# refillMissingPixels(EXTRACTED_FOLDER, MAGNIFIED_FOLDER, REFILLED_FOLDER)
# pngsToXnbs(REFILLED_FOLDER, TARGET_XNB_FOLDER)
# createRelease('v0.10-1.4.0.2', TARGET_XNB_FOLDER, RELEASE_FOLDER)
createTexturePack(0, 11, '1.4.0.2', REFILLED_FOLDER, TEXTURE_PACK_FOLDER)
