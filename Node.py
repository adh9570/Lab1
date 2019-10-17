class Node:
    def __init__(self, g, x, y, target, parent, speed):
        self.x = x
        self.y = y
        self.g = g
        self.h = self.calculateH(target)
        self.f = g + self.h
        self.parent = parent
        self.speed = speed
    
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

    def calculateH(self, target):
        x = abs(self.x - target[0])
        y = abs(self.y - target[1])
        self.h = (x**2 + y**2)    # pythag theorem # TODO make not pythag
        return self.h