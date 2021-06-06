import json
import copy
import math
import random
import numpy as np
from types import SimpleNamespace


class BLC_Utils:
 @staticmethod
 def randRange(min, max):
  return random.uniform(min, max)
 
 
 @staticmethod
 def randDev(average, maxDeviation):
  min = average - maxDeviation
  max = average + maxDeviation
  return random.uniform(min, max)


 @staticmethod
 def calculateAngleBasedOnEndpoints(startPosition, endPosition):
  startX, startY = startPosition
  endX, endY = endPosition
  magnitude = math.dist([startX, startY], [endX, endY])
  horizontalVector = endX - startX
  if endY > startY:
   return np.arccos(horizontalVector / magnitude)
  else:
   return (2.0 * np.pi) - np.arccos(horizontalVector / magnitude)




class Point:
  def __init__(self, x, y):
    if (x < 0 or x > 1 or y < 0 or y > 1):
      raise ValueError('values for x and y have to be between 0 and 1 inclusive')
   
    self.x = x
    self.y = y

    # This will be updated by Line
    self.connectedLines = []
  
  def getX(self):
    return self.x
  
  def getY(self):
    return self.y

  @property
  def position(self):
    return (self.x, self.y)

  @position.setter
  def position(self, value):
    newX, newY = value
    self.x = newX
    self.y = newY
    
  def __repr__(self):
    return self.__str__() 
      
  def __str__(self):
    return "Point(%s,%s)"%(self.x, self.y)

  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, 
      sort_keys=True, indent=2)



  
class Line:
  def __init__(self, startPoint, endPoint, peakMagnitude=0.0, peakOffset=0.0):
    # Setup the given start and end points
    self.startPoint = startPoint
    self.startPoint.connectedLines.append(self)
    self.endPoint = endPoint
    self.endPoint.connectedLines.append(self)
    self.peakMagnitude = peakMagnitude # right = -1.0  &  left = 1.0
    self.peakOffset = peakOffset # start = -1.0  &  end = 1.0
    
  def getStartPoint(self):
    return self.startPoint
    
  def getEndPoint(self):
    return self.endPoint 

  def getEdgeLength(self):
    return math.dist(self.startPoint.position, self.endPoint.position)

  def getEdgeAngle(self):
    return BLC_Utils.calculateAngleBasedOnEndpoints(self.startPoint.position, self.endPoint.position)
  
  def getPeakAsPoint(self):
    relativePeakX = (self.peakOffset + 1.0) / 2.0
    relativePeakY = -1.0 * self.peakMagnitude / 2.0
    relativePeakPosition = (relativePeakX, relativePeakY)
    relativeDistanceToPeak = math.dist([0.0, 0.0], [relativePeakX, relativePeakY])
    relativeAngleToPeak = BLC_Utils.calculateAngleBasedOnEndpoints((0.0, 0.0), relativePeakPosition)
    if relativeAngleToPeak > np.pi:
      relativeAngleToPeak = relativeAngleToPeak - (2.0 * np.pi)

    absoluteStartX, absoluteStartY = self.startPoint.position
    absoluteAngleToPeak = (self.getEdgeAngle() + relativeAngleToPeak) % (2.0 * np.pi)
    if absoluteAngleToPeak < 0.0:
      absoluteAngleToPeak = (2.0 * np.pi) + absoluteAngleToPeak
    absoluteDistanceToPeak = relativeDistanceToPeak * self.getEdgeLength()
    absolutePeakX = (absoluteDistanceToPeak * math.cos(absoluteAngleToPeak)) + absoluteStartX
    absolutePeakY = (absoluteDistanceToPeak * math.sin(absoluteAngleToPeak)) + absoluteStartY
    return Point(absolutePeakX, absolutePeakY)
    
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
    #self.lines = []
    #for i in range(0, len(self.points) - 2, 2):
    #  line = Line(self.points[i], self.points[i+1], self.points[i+2])
    #  self.lines.append(line)
      
  def getPoints(self):
    return self.points
  
  #def getLines(self):
  #  return self.lines 
  
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

  @staticmethod
  def traversePointsToCreateBLC(points):
    # Determine how many lines there are
    allLines = []
    for point in points:
      for line in point.connectedLines:
        if not line in allLines:
          allLines.append(line)
    totalLineCount = len(allLines)

    # Create a traversal of the points
    currentPoint = points[random.randint(0, len(points) - 1)]
    traversal = [Point(currentPoint.x, currentPoint.y)]
    lastTraversedLine = None
    allTraversedLines = []
    while len(allTraversedLines) < totalLineCount:
      # Sort the options at this point based on whether or not they have been traversed
      untraversedOptions = []
      alreadyTraversedOptions = []
      for lineToSort in currentPoint.connectedLines:
        if lineToSort in allTraversedLines:
          alreadyTraversedOptions.append(lineToSort)
        else:
          untraversedOptions.append(lineToSort)
      
      # Determine which line to traverse next
      lineToTraverseNext = None
      if len(untraversedOptions) > 0:
        lineToTraverseNext = untraversedOptions[random.randint(0, len(untraversedOptions) - 1)]
        allTraversedLines.append(lineToTraverseNext)
      else:
        preferredAlreadyTraversedOptions = copy.copy(alreadyTraversedOptions)
        if lastTraversedLine != None:
          preferredAlreadyTraversedOptions.remove(lastTraversedLine)
        if len(preferredAlreadyTraversedOptions) > 0:
          lineToTraverseNext = preferredAlreadyTraversedOptions[random.randint(0, len(preferredAlreadyTraversedOptions) - 1)]
        else:
          lineToTraverseNext = lastTraversedLine
      
      # Record the chosen route
      peakPoint = lineToTraverseNext.getPeakAsPoint()
      pointA = lineToTraverseNext.startPoint
      pointB = lineToTraverseNext.endPoint
      nextPointToGoTo = None
      if currentPoint == pointA:
        nextPointToGoTo = pointB
      else:
        nextPointToGoTo = pointA
      traversal.extend([peakPoint, Point(nextPointToGoTo.x, nextPointToGoTo.y)])

      # Continue traversing
      currentPoint = nextPointToGoTo
      lastTraversedLine = lineToTraverseNext
    
    # Create the BLC
    return BLC(connectedSets=[ConnectedSet(traversal)])
