import sys
from PIL import Image
from Node import Node
import time

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

EASY_MOVE_FOREST_SPEED = 75

# Speed represented as % of potential speed (100 being fastest, 0 being impossible to traverse)
def calcSpeed(node, terrain_pixel_map, elevation_file_name):
    x = node.getX()
    y = node.getY()

    location = terrain_pixel_map[x, y]

    speed = 0

    # Set base speed based on terrain
    if location == OOB_COLOR or location == IMPASS_VEG_COLOR or location == WATER_COLOR:
        speed = 0
    elif location == ROUGH_MEADOW_COLOR:
        speed = 30
    elif location == WALK_FOREST_COLOR:
        speed = 60
    elif location == EASY_MOVE_FOREST_COLOR:
        speed = EASY_MOVE_FOREST_SPEED
    elif location == SLOW_RUN_FOREST_COLOR:
        speed = 75
    elif location == OPEN_LAND_COLOR or location == ROAD_COLOR or location == FOOTPATH_COLOR:
        speed = 100
    else:
        print("Terrain not recognized.")
        print(location)

    elevations = []

    # Edit speed based on elevation change
    with open(elevation_file_name) as elevation_file:
        lines = elevation_file.readlines()
        for line in lines:
            words = line.split()
            elevations.append(words)
    
    if node.parent == None:
        elevChange = 0
    else:
        elevChange = float(elevations[node.getX()][node.getY()]) - float(elevations[node.parent.getX()][node.parent.getY()])

    # downhill
    if elevChange < 0:
        speed += 30
    # uphill
    elif elevChange > 0:
        speed -= 30

    return speed


def getAdj(currentNode, target, terrain_pixel_map):
    x = currentNode.getX()
    y = currentNode.getY()
    nodes = []
    if (x - 1) >= 0:
        node = Node(currentNode.getG() + 1, x - 1, y, currentNode)
        speed = calcSpeed(node, terrain_pixel_map, elevation_file_name)
        node.setSpeed(speed)
        if speed != 0:      # avoid any impassable 
            nodes.append(node)
        if (y - 1) >= 0:
            node = Node(currentNode.getG() + 1, x - 1, y - 1, currentNode)
            speed = calcSpeed(node, terrain_pixel_map, elevation_file_name)
            node.setSpeed(speed)
            if speed != 0:
                nodes.append(node)
        if (y + 1) < 500:   # 500 is max height of map
            node = Node(currentNode.getG() + 1, x - 1, y + 1, currentNode)
            speed = calcSpeed(node, terrain_pixel_map, elevation_file_name)
            node.setSpeed(speed)
            if speed != 0:
                nodes.append(node)
    if (x + 1) < 395:       # 395 is max width of map
        node = Node(currentNode.getG() + 1, x + 1, y, currentNode)
        speed = calcSpeed(node, terrain_pixel_map, elevation_file_name)
        node.setSpeed(speed)
        if speed != 0:
            nodes.append(node)
        if (y - 1) >= 0:
            node = Node(currentNode.getG() + 1, x + 1, y - 1, currentNode)
            speed = calcSpeed(node, terrain_pixel_map, elevation_file_name)
            node.setSpeed(speed)
            if speed != 0:
                nodes.append(node)
        if (y + 1) < 500:   # 500 is max height of map
            node = Node(currentNode.getG() + 1, x + 1, y + 1, currentNode)
            speed = calcSpeed(node, terrain_pixel_map, elevation_file_name)
            node.setSpeed(speed)
            if speed != 0:
                nodes.append(node)
    if (y - 1) >= 0:
        node = Node(currentNode.getG() + 1, x, y - 1, currentNode)
        speed = calcSpeed(node, terrain_pixel_map, elevation_file_name)
        node.setSpeed(speed)
        if speed != 0:
            nodes.append(node)
    if (y + 1) < 500:
        node = Node(currentNode.getG() + 1, x, y + 1, currentNode)
        speed = calcSpeed(node, terrain_pixel_map, elevation_file_name)
        node.setSpeed(speed)
        if speed != 0:
            nodes.append(node)

    return nodes


# Path drawn in red
def drawPath(path, terrain_image, output_image_filename):
    out_image = Image.open(terrain_image_name)
    out_pixel_map = out_image.load()
    for node in path:
        x = node.getX()
        y = node.getY()
        out_pixel_map[x, y] = PATH_COLOR
    
    out_image.save(output_image_filename)


# simple A* search
def search(terrain_pixel_map, elevation_file_name, path_file_name, output_image_filename, location, target):
    openList = []
    closedList = []
    start = Node(0, location[0], location[1], None)   # g, x, y, parent, speed
    speed = calcSpeed(start, terrain_pixel_map, elevation_file_name)
    start.setSpeed(speed)
    start.setF(0)
    openList.append(start)
    count = 0
    while openList != []:
        currentNode = openList[0]
        # print("F is ", currentNode.getF())
        print("Current node ", currentNode.getX(), currentNode.getY())
        
        # determine node in open list with lowest f
        # oIndex = 0
        # index = 0
        currentIndex = 0
        for index, node in enumerate(openList):
            # print("Node in open list", node.getX(), node.getY())
            if node.getF() < currentNode.getF():
                # print("node's f is smaller than current's f")
                currentNode = node
                currentIndex = index
                # currentIndex = oIndex
                # print("INDEX ", oIndex)
            # oIndex += 1
        # openList.remove(currentNode)
        openList.pop(currentIndex)
        # print(openList)
        closedList.append(currentNode)

        # Base case
        if currentNode.getX() == target[0] and currentNode.getY() == target[1]:
            print("LOCAL TARGET FOUND", currentNode.getX(), currentNode.getY())
            target = getLoc(path_file_name)
            if target == []:    # if target = [], we're at the end of the search
                print("FINAL TARGET FOUND", currentNode.getX(), currentNode.getY())
                path = []
                current = currentNode
                while current is not None:
                    # print("Current node ", current)
                    path.append(current)
                    current = current.parent
                return path[::-1]

        # Get adjacent nodes to currentNode
        nodes = getAdj(currentNode, target, terrain_pixel_map)

        for node in nodes:
            for element in closedList:
                if element == node:
                    continue
            
            speed = node.getSpeed()
            pythag = node.getX()**2 + node.getY()**2    # pythagorean theorem used as additional heuristic
            node.setH(speed + pythag)
            node.setF(node.getG() + node.getH())

            cont = True
            for element in openList:
                if node.getX() == element.getX() and node.getY() == element.getY() and node.getG() > element.getG():
                    print("continuing", count)
                    cont = False
            if cont:
                print("not continued", count)
                openList.append(node)
            count+=1
            


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
    global EASY_MOVE_FOREST_SPEED
    EASY_MOVE_FOREST_SPEED = 60


def winter():
    print("WINTER")


def spring():
    print("SPRING")


if __name__ == "__main__":

    start = time.time()

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

    if location == [] or target == []:
        print("The path only has one node.")
        sys.exit()
    
    path = search(terrain_pixel_map, elevation_file_name, path_file_name, output_image_filename, location, target)
    drawPath(path, terrain_image, output_image_filename)

    end = time.time()

    print("Time elapsed " + (end - start))
