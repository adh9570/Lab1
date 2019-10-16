import sys
from PIL import Image
from Node import Node

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


def search(terrain_pixel_map, elevation_file_name, path_file_name, output_image_filename, location, target):
    if location == target:
        target = getLoc(path_file_name)
        if target == []:    # if target = [], we're at the end of the search
            return "COMPLETE"
    openList = []
    closedList = []
    start = Node(0, location[0], location[1], target)   # g, x, y, target
    start.setF(0)
    openList.append(start)
    while openList != []:
        currentNode = openList[0]
        # determine node in open list with lowest f
        index = 0
        nodeInx = index
        for node in openList:
            if node.getF() < currentNode.getF():
                currentNode = node
                nodeInx = index
            index += 1
        openList.remove(currentNode)
        if currentNode.getX() == target[0] and currentNode.getY() == target[1]:
            print()

# return location at top of path file, removes top line
def getLoc(path_file_name):
    with open(path_file_name) as path_file:
        line = path_file.readline()
        loc = line.split()
        location = []
        location.append(int(loc[0]))
        location.append(int(loc[1]))
        lines = path_file.readlines()
    with open(path_file_name, 'w') as path_file:
        path_file.writelines(lines[0:])
    return location


def fall():
    print("FALL")


def winter():
    print("WINTER")


def spring():
    print("SPRING")


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

    '''
    TODO: implement fall winter and spring to do changes to globals in writeup
    '''
    if season == 'fall':
        fall()
    elif season == 'winter':
        winter()
    elif season == 'spring':
        spring()

    location = getLoc(path_file_name)   # starting location, first location in path file
    target = getLoc(path_file_name)
    
    search(terrain_pixel_map, elevation_file_name, path_file_name, output_image_filename, location, target)
