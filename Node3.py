import math

class Node:
    def __init__(self, g, x, y, target, parent):
        self.x = x
        self.y = y
        self.g = g
        self.h = self.calculateH(target)    # initial h value is pythag
        self.f = g + self.h
        self.parent = parent
        self.speed = 0
    
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

    def setSpeed(self, speed):
        self.speed = speed

    def setH(self, h):
        self.h = h

    def getH(self):
        return self.h

    def calculateH(self, target):
        x = abs(self.x - target[0])
        y = abs(self.y - target[1])
        self.h = math.sqrt(x**2 + y**2)    # pythag theorem 
        return self.h