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

ICE_COLOR = (0, 255, 255, 255)  # for winter only
PATH_COLOR = (255, 0, 0, 255)   # path will be red

# Speed in miles per hour
def getSpeed(node, terrain_pixel_map, elevation_file_name):
    x = node.getX()
    y = node.getY()

    location = terrain_pixel_map[x, y]

    speed = 0

    # Set base speed based on terrain
    if location == OOB_COLOR or location == IMPASS_VEG_COLOR or location == WATER_COLOR:
        print("Speed zero")
        print(location)
        speed = 0
    elif location == ROUGH_MEADOW_COLOR:
        print("Speed 1.5")
        print(location)
        speed = 1.5
    elif location == WALK_FOREST_COLOR:
        print("Speed 2.5")
        print(location)
        speed = 2.5
    elif location == EASY_MOVE_FOREST_COLOR or location == SLOW_RUN_FOREST_COLOR:
        print("Speed 3")
        print(location)
        speed = 3
    elif location == OPEN_LAND_COLOR or location == ROAD_COLOR or location == FOOTPATH_COLOR:
        print ("Speed 4")
        print(location)
        speed = 4
    else:
        print("Terrain not recognized.")
        print(location)

    # Edit speed based on elevation change
    with open(elevation_file_name) as elevation_file:
        pass

    # print("end speed gotten")
    return speed


def getAdj(currentNode, target, terrain_pixel_map):
    x = currentNode.getX()
    y = currentNode.getY()
    nodes = []
    if (x - 1) >= 0:
        node = Node(currentNode.getG() + 1, x - 1, y, target)
        speed = getSpeed(node, terrain_pixel_map, elevation_file_name)
        if speed != 0:
            nodes.append(node)
        if (y - 1) >= 0:
            node = Node(currentNode.getG() + 2, x - 1, y - 1, target)
            speed = getSpeed(node, terrain_pixel_map, elevation_file_name)
            if speed != 0:
                nodes.append(node)
        if (y + 1) < 500:   # 500 is max height of map
            node = Node(currentNode.getG() + 2, x - 1, y + 1, target)
            speed = getSpeed(node, terrain_pixel_map, elevation_file_name)
            if speed != 0:
                nodes.append(node)
    if (x + 1) < 395:       # 395 is max width of map
        node = Node(currentNode.getG() + 1, x + 1, y, target)
        speed = getSpeed(node, terrain_pixel_map, elevation_file_name)
        if speed != 0:
            nodes.append(node)
        if (y - 1) >= 0:
            node = Node(currentNode.getG() + 2, x + 1, y - 1, target)
            speed = getSpeed(node, terrain_pixel_map, elevation_file_name)
            if speed != 0:
                nodes.append(node)
        if (y + 1) < 500:   # 500 is max height of map
            node = Node(currentNode.getG() + 2, x + 1, y + 1, target)
            speed = getSpeed(node, terrain_pixel_map, elevation_file_name)
            if speed != 0:
                nodes.append(node)
    if (y - 1) >= 0:
        node = Node(currentNode.getG() + 1, x, y - 1, target)
        speed = getSpeed(node, terrain_pixel_map, elevation_file_name)
        if speed != 0:
            nodes.append(node)
    if (y + 1) < 500:
        node = Node(currentNode.getG() + 1, x, y + 1, target)
        speed = getSpeed(node, terrain_pixel_map, elevation_file_name)
        if speed != 0:
            nodes.append(node)

    return nodes


def drawPath(path, terrain_image, output_image_filename):
    # out_image = Image.new("RGBA", (395, 500), None)
    # out_image = terrain_image
    out_image = Image.open(terrain_image_name)
    out_pixel_map = out_image.load()
    for node in path:
        x = node.getX()
        y = node.getY()
        out_pixel_map[x, y] = PATH_COLOR
    
    out_image.save(output_image_filename)

    out_image.show()



# simple A* search
def search(terrain_pixel_map, elevation_file_name, path_file_name, output_image_filename, location, target):
    openList = []
    closedList = []
    start = Node(0, location[0], location[1], target)   # g, x, y, target
    start.setF(0)
    openList.append(start)
    while openList != []:
        currentNode = openList[0]
        # determine node in open list with lowest f
        for node in openList:
            if node.getF() < currentNode.getF():
                currentNode = node
        openList.remove(currentNode)

        # Base case
        if currentNode.getX() == target[0] and currentNode.getY() == target[1]:
            print("LOCAL TARGET FOUND", currentNode.getX(), currentNode.getY())
            target = getLoc(path_file_name)
            if target == []:    # if target = [], we're at the end of the search
                print("FINAL TARGET FOUND", target[0], target[1])
                return currentNode
            continue

        # Get adjacent nodes to currentNode
        nodes = getAdj(currentNode, target, terrain_pixel_map)

        for node in nodes:
            # if node is contained in closedList
            contained = False
            for element in closedList:
                if node == element:
                    contained = True
                    break
            if contained:
                continue
            ## node.setG(currentNode.getG() + distance between node and currentNode)
            # node.setH(distance from node to target)
            # node.setF(node.getG() + node.getH())

            continuer = False
            for element in openList:
                continuer = False
                if node.getX() == element.getX() and node.getY() == element.getY():
                    if node.getG() > element.getG():
                        continuer = True
                        break
            
            if continuer:
                continue
                        
                # else:
            openList.append(node)
            


# Trims the last 5 elements from every line to make each line 395 long
def trimElev(elevation_map_name):
    with open(elevation_file_name, 'r+') as elevation_file:
        lines = elevation_file.readlines()
        for line in lines:
            words = line.split()
            elevation_file.writelines(words[0:-5])


# return location at top of path file, removes top line
def getLoc(path_file_name):
    with open(path_file_name) as path_file:
        line = path_file.readline()
        loc = line.split()
        location = []
        if(loc != []):
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

    trimElev(elevation_file_name)

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
    
    # search(terrain_pixel_map, elevation_file_name, path_file_name, output_image_filename, location, target)

    location = getLoc(path_file_name)

    path = [Node(0, location[0], location[1], target), Node(0, location[0] + 1, location[1] + 1, target), Node(0, location[0] + 2, location[1] + 2, target), Node(0, location[0] + 3, location[1] + 3, target), Node(0, location[0] + 4, location[1] + 4, target), Node(0, location[0] + 5, location[1] + 5, target), Node(0, location[0] + 6, location[1] + 6, target), Node(0, location[0] + 7, location[1] + 7, target), Node(0, location[0] + 8, location[1] + 8, target), Node(0, location[0] + 9, location[1] + 9, target), Node(0, location[0] + 10, location[1] + 10, target)]

    drawPath(path, terrain_image, output_image_filename)

    # x1 = Node(0, location[0], location[1], target)
    # x2 = Node(0, location[0] + 1, location[1] + 1, target)
    # x3 = Node(0, location[0] + 2, location[1] + 2, target)
    # x4 = Node(0, location[0] + 3, location[1] + 3, target)
    # x5 = Node(0, location[0] + 4, location[1] + 4, target)
    # x6 = Node(0, location[0] + 5, location[1] + 5, target)
    # x7 = Node(0, location[0] + 6, location[1] + 6, target)
    # x8 = Node(0, location[0] + 7, location[1] + 7, target)
    # x9 = Node(0, location[0] + 8, location[1] + 8, target)
    # x10 = Node(0, location[0] + 9, location[1] + 9, target)
    # x11 = Node(0, location[0] + 10, location[1] + 10, target)

    # path = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11
