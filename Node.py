class Node:
    def __init__(self, g, x, y, parent, speed):
        self.x = x
        self.y = y
        self.g = g
        self.f = g + self.h
        self.parent = parent
        self.speed = speed
    
    def setH(self, h):
        self.h = h
    
    def getF(self):
        return self.f

    # for start node
    def setF(self, f):
        self.f = f

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getG(self):
        return self.g

    def getSpeed(self):
        return self.speed

    def getParent(self):
        return self.parent

    def setSpeed(self, speed):
        self.speed = speed
