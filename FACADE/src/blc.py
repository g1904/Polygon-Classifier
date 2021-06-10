import json
import copy
import math
import random
import numpy as np
from types import SimpleNamespace
from numpy.random import rand


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


  # Based on: https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
  @staticmethod # Uses degrees not radians
  def rotatePointsAroundOrigin(points, angle):
    angle = np.deg2rad(angle)
    originX, originY = (0.5, 0.5)

    for point in points:
      oldX, oldY = point.position

      newX = originX + math.cos(angle) * (oldX - originX) - math.sin(angle) * (oldY - originY)
      newY = originY + math.sin(angle) * (oldX - originX) + math.cos(angle) * (oldY - originY)
      point.x = newX
      point.y = newY
  
  @staticmethod
  def mirrorPoints(points, shouldMirrorHorizontal, shouldMirrorVertical):
    allLines = []
    for point in points:
      if shouldMirrorHorizontal:
        point.x = 1.0 - point.x
      if shouldMirrorVertical:
        point.y = 1.0 - point.y
      for line in point.connectedLines:
        if not line in allLines:
          allLines.append(line)

    if shouldMirrorHorizontal != shouldMirrorVertical:
      for line in allLines:
        line.peakMagnitude = -1.0 * line.peakMagnitude
        line.peakOffset = -1.0 * line.peakOffset
    




class Point:
  def __init__(self, x, y):
    if (x < 0 or x > 1 or y < 0 or y > 1):
      print('Warnning! Values for x and y have to be between 0 and 1 inclusive.')
   
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
    # If there is only one line, then no need to do complicated calculations
    if len(points) == 2:
      startPoint = Point(points[0].x, points[0].y)
      peakPoint = points[0].connectedLines[0].getPeakAsPoint()
      endPoint = Point(points[1].x, points[1].y)
      traversal = [startPoint, peakPoint, endPoint]
      if random.random() < 0.5:
        traversal.reverse()
      return BLC(connectedSets=[ConnectedSet(traversal)])

    # Determine how many lines there are
    allLines = []
    for point in points:
      for line in point.connectedLines:
        if not line in allLines:
          allLines.append(line)
    totalLineCount = len(allLines)

    # Create a traversal of the points
    currentPoint = None
    if random.random() < 0.3:
      currentPoint = points[0]
    elif random.random() < 0.5:
      currentPoint = points[len(points) - 1]
    else:
      currentPoint = points[random.randint(1, len(points) - 2)]
    traversal = [Point(currentPoint.x, currentPoint.y)]
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
        peakPoint = lineToTraverseNext.getPeakAsPoint()
        # Find the point at the other end of this line
        pointA = lineToTraverseNext.startPoint
        pointB = lineToTraverseNext.endPoint
        nextPointToGoTo = None
        if currentPoint == pointA:
          nextPointToGoTo = pointB
        else:
          nextPointToGoTo = pointA
        traversal.extend([peakPoint, nextPointToGoTo])
      else:
        # Find the closest untraversed line
        possiblePathsToUntraversedLine = []
        allCheckedLines = []
        pathsAtEachDistance = [[[currentPoint]]]
        haveFoundUntraversedLine = False
        while not haveFoundUntraversedLine:
          pathsAtCurrentDistance = []
          for path in pathsAtEachDistance[-1]:
            for lineToCheck in path[-1].connectedLines:
              if not lineToCheck in allCheckedLines:
                peakPoint = lineToCheck.getPeakAsPoint()
                # Find the point at the other end of this line
                pointA = lineToCheck.startPoint
                pointB = lineToCheck.endPoint
                endPoint = None
                if path[-1] == pointA:
                  endPoint = pointB
                else:
                  endPoint = pointA
                
                if lineToCheck in allTraversedLines:
                  newPossiblePath = copy.copy(path)
                  newPossiblePath.extend([peakPoint, endPoint])
                  pathsAtCurrentDistance.append(newPossiblePath)
                  allCheckedLines.append(lineToCheck)
                else:
                  haveFoundUntraversedLine = True
                  possiblePathsToUntraversedLine.append(path)
                  break
          pathsAtEachDistance.append(pathsAtCurrentDistance)
        
        # Randomly pick one of the viable paths
        chosenPath = possiblePathsToUntraversedLine[random.randint(0, len(possiblePathsToUntraversedLine) - 1)]
        del chosenPath[0]
        traversal.extend(chosenPath)
        nextPointToGoTo = chosenPath[-1]

      # Continue traversing
      currentPoint = nextPointToGoTo
    
    # This wipes the storred connections off of all the points. We need these to be gone, or our BLC won't be serializable
    for pointIndex in range(len(traversal)):
      traversal[pointIndex] = Point(traversal[pointIndex].x, traversal[pointIndex].y)

    # Create the BLC
    return BLC(connectedSets=[ConnectedSet(traversal)])

  #def getPathToClosestUntraversedLine(currentPoint, allTraversedLines):
  #  bestTraversal = [currentPoint]

  #  uncheckedLines = copy.copy(currentPoint.connectedLines)
  #  while len(uncheckedLines) > 0:
      # Get this line
  #    indexOfLineToCheck = random.randint(0, len(uncheckedLines) - 1)
  #    lineToCheck = uncheckedLines[indexOfLineToCheck]
  #    del uncheckedLines[indexOfLineToCheck]

      # Get the other point
  #    pointA = lineToCheck.startPoint
  #    pointB = lineToCheck.endPoint
  #    otherPoint = None
  #    if currentPoint == pointA:
  #      otherPoint = pointB
  #    else:
  #      otherPoint = pointA
      
      # Traverse the sub lines
  #    if line in allTraversedLines:
  #    else:
      


  #  for line in currentPoint.connectedLines:
      
  #    if line in allTraversedLines:
  #    else:
