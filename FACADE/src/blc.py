import json
from types import SimpleNamespace

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
    
    def asTupple(self):
        return (self.x, self.y)
        
    def __repr__(self):
        return self.__str__() 
            
    def __str__(self):
        return "Point(%s,%s)"%(self.x, self.y)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)

    
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

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)
        
    
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
    
    def __repr__(self):
        return '[' + self.__str__() + ']'
        
    def __str__(self): 
        return ', '.join([str(elem) for elem in self.points])

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)


class BLC:
    def __init__(self, connectedSets):
        self.connectedSets = connectedSets
            
    def getConnectedSets(self):
        return self.connectedSets
    
    @staticmethod
    def open(filePath):
        objectFile = open(filePath, 'r')
        serializedObject = objectFile.read()
        pythonObject = json.loads(serializedObject, object_hook=lambda d: SimpleNamespace(**d))
        objectFile.close()
        return pythonObject

    def save(self, filePath):
        # We want to overwrite the old file
        oldFile = open(filePath, 'w')
        oldFile.write(self.toJSON())
        oldFile.close()

    def __repr__(self):
        return '[' + self.__str__() + ']'
        
    def __str__(self): 
        return ', '.join([str(elem) for elem in self.connectedSets])   

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)   