import math
from matplotlib import pyplot as plt

class Point:
    def __init__(self, x, y):
        if (x < 0 or x >= 1 or y < 0 or y >= 1):
            raise ValueError('values for x and y have to be in the interval [0, 1)')
     
        self.x = x
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def midpointTo(self, other):
        midX = (self.x + other.x) / 2
        midY = (self.y + other.y) / 2
        return Point(midX, midY)
        
    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.hypot(dx, dy)
        
    def __eq__(self, other): 
        if not isinstance(other, Point):
            return NotImplemented

        return self.x == other.x and self.y == other.y
        
        
    def __repr__(self):
        return self.__str__() 
            
    def __str__(self):
        return "Point(%s,%s)"%(self.x, self.y) 

    
class Line:
    def __init__(self, startPoint, curvePoint, endPoint):
        self.startPoint = startPoint
        self.curvePoint = curvePoint
        self.endPoint = endPoint
        
    def getStartPoint(self):
        return self.startPoint
    
    def getCurvePoint(self):
        return self.curvePoint
        
    def getEndPoint(self):
        return self.endPoint  
        
    def __repr__(self):
        return self.__str__() 
        
    def __str__(self): 
        return "Line(%s,%s,%s)"%(self.startPoint, self.curvePoint, self.endPoint)
        
    
class ConnectedSet:
    def __init__(self, points):
        if (len(points) < 3 or len(points) % 2 == 0):
            raise ValueError("invalid shape for connected set")
        self.points = points
        self.lines = []
        for i in range(0, len(self.points) - 2, 2):
            line = Line(self.points[i], self.points[i+1], self.points[i+2])
            self.lines.append(line)
            
    def getPoints(self):
        return self.points
    
    def getLines(self):
        return self.lines 
    
    def getXs(self):
        return [p.getX() for p in self.points]
        
    def getYs(self):
        return [p.getY() for p in self.points]
    
    def __repr__(self):
        return '[' + self.__str__() + ']'
        
    def __str__(self): 
        return ', '.join([str(elem) for elem in self.points])
        
class BLC:
    def __init__(self, connectedSets):
        self.connectedSets = connectedSets
            
    def getConnectedSets(self):
        return self.connectedSets  
        
    def __repr__(self):
        return '[' + self.__str__() + ']'
        
    def __str__(self): 
        return ', '.join([str(elem) for elem in self.connectedSets])    
        
        
        
################    

class ConnectedPolygon(ConnectedSet): 
    def __init__(self, points, n):
        if (len(points) != n):
            raise ValueError("invalid shape for ConnectedPolygon")
        if (points[0] != points[-1]):
            raise ValueError("for connected triangles, the last point has to be equal to the 1st")
            
        super().__init__(points)
        
        self.n = n # 7 for triangles, 9 for squares, 13 for hexagons
        
    def draw(self, ax):
        ax.plot(self.getXs(), self.getYs())