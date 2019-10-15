import sys
from PIL import Image

OPEN_LAND_COLOR = (248, 148, 18, 255)
ROUGH_MEADOW_COLOR = (255, 192, 0, 255)
EASY_MOVE_FOREST_COLOR = (255, 255, 255, 255)
SLOW_RUN_FOREST_COLOR = (2, 208, 60, 255)
WALK_FOREST_COLOR = (2, 136, 40, 255)
IMPASS_VEG_COLOR = (5, 73, 24, 255)
WATER_COLOR = (0, 0, 255, 255)
ROAD_COLOR = (71, 51, 3, 255)
FOOTPATH_COLOR = (0, 0, 0, 255)
OOB_COLOR = (205, 0, 101, 255)

# Speeds in MPH
OPEN_LAND_SPEED = 4
ROUGH_MEADOW_SPEED = 1.5
EASY_MOVE_FOREST_SPEED = 3
SLOW_RUN_FOREST_SPEED = 3
WALK_FOREST_SPEED = 2.5
IMPASS_VEG_SPEED = 0
WATER_SPEED = 0
ROAD_SPEED = 4
FOOTPATH_SPEED = 4
OOB_SPEED = 0

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
    for x in range(0, 395):
        for y in range(0, 500):
            print (terrain_pixel_map[x, y])

    location = [0, 0]   # initialize loc to [0, 0]
    with open(path_file_name) as path_file:
        line = path_file.readline()
        cnt = 0
        for word in line.split():
            print(word)
            line[cnt] = word
            cnt = 1
        location = line
        count = 1
        while line:
            print(line)
            line = path_file.readline()
            count += 1