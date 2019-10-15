import sys
from PIL import Image

OPEN_LAND_COLOR = '#F89412'
ROUGH_MEADOW_COLOR = '#FFC000'
EASY_MOVE_FOREST_COLOR = '#FFFFFF'
SLOW_RUN_FOREST_COLOR = '#02D03C'
WALK_FOREST_COLOR = '#028828'
IMPASS_VEG_COLOR = '#054918'
WATER_COLOR = '#0000FF'
ROAD_COLOR = '#473303'
FOOTPATH_COLOR = '#000000'
OOB_COLOR = '(205, 0, 101, 255)'

if __name__ == "__main__":
    # Read in arguments
    terrain_image_name = ''
    elevation_file_name = ''
    path_file_name = ''
    season = ''
    output_image_filename = ''

    try:
        terrain_image_name = sys.argv[1]
        elevation_file_name = sys.argv[2]
        path_file_name = sys.argv[3]
        season = sys.argv[4]
        output_image_filename = sys.argv[5] 
    except:
        print("Error: args should be formatted [terrain-image, elevation-file, path-file, season (summer,fall,winter,or spring), output-image-filename]")
        sys.exit()

    print(terrain_image_name)
    print(elevation_file_name)
    print(path_file_name)
    print(season)
    print(output_image_filename)

    terrain_image = Image.open(terrain_image_name)
    terrain_pixel_map = terrain_image.load()
    for x in range(terrain_image.size[0]):
        for y in range(terrain_image.size[1]):
            print (terrain_pixel_map[x, y])
            if OOB_COLOR == terrain_pixel_map[x, y]:
                print("OOB")
