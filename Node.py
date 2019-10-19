class Node:
    def __init__(self, g, x, y, parent):
        self.x = x
        self.y = y
        self.g = g
        self.f = 0
        self.parent = parent
    
    def getH(self):
        return self.h

    def setH(self, h):
        self.h = h
        self.updateF()
    
    # for start node
    def setF(self, f):
        self.f = f

    def getF(self):
        return self.f


    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getG(self):
        return self.g

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

    def updateF(self):
        self.f = self.g + self.h