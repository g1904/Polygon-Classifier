class Point:
    def __init__(self, x, y):
        if (x < 0 or x > 1 or y < 0 or y > 1):
            raise ValueError('values for x and y have to be between 0 and 1 inclusive')
     
        self.x = x
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    
class Line:
    def __init__(self, startPoint, curvePoint, endPoint):
        self.startPoint = startPoint
        self.curvePoint = curvePoint
        self.endPoint = curvePoint
        
    def getStartPoint(self):
        return self.startPoint
    
    def getCurvePoint(self):
        return self.curvePoint
        
    def getEndPoint(self):
        return self.endPoint    
        
    
class ConnectedSet:
    def __init__(self, points):
        if (len(points) < 3 or len(points) % 2 == 0):
            raise ValueError("invalid shape for connected set")
        self.points = points
        self.lines = []
        for i in range(0, len(self.points) - 2, 2):
            current = Line(self.points[i], self.points[i+1], self.points[i+2])
            self.lines.append(line)
            
    def getPoints(self):
        return self.points
    
    def getLines(self):
        return self.lines 
        
class BLC:
    def __init__(self, connectedSets):
        self.connectedSets = connectedSets
            
    def getConnectedSets(self):
        return self.connectedSets               