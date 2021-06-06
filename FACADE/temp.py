import math
import random
import numpy as np

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
      



class TPoint:
  def __init__(self, position):
    self.position = position
    self.connectedLines = []




class TLine:
  def __init__(self, startPoint, endPoint):
    # Setup the given start and end points
    self.startPoint = startPoint
    self.startPoint.connectedLines.append(self)
    self.endPoint = endPoint
    self.endPoint.connectedLines.append(self)

    # Initially a edge has no peak
    self.peakMagnitude = 0.0 # right = -1.0  &  left = 1.0
    self.peakOffset = 0.0 # start = -1.0  &  end = 1.0
  

  def getEdgeLength(self):
    return math.dist(self.startPoint.position, self.endPoint.position)
  

  def getEdgeAngle(self):
    return BLC_Utils.calculateAngleBasedOnEndpoints(self.startPoint.position, self.endPoint.position)
  
  
  def getPeakAsPoint(self):
    relativePeakX = (self.peakOffset + 1.0) / 2.0
    relativePeakY = self.peakMagnitude / 2.0
    relativePeakPosition = (relativePeakX, relativePeakY)
    relativeDistanceToPeak = math.dist([0.0, 0.0], [relativePeakX, relativePeakY])
    relativeAngleToPeak = BLC_Utils.calculateAngleBasedOnEndpoints((0.0, 0.0), relativePeakPosition)

    absoluteStartX, absoluteStartY = self.startPoint.position
    absoluteAngleToPeak = self.getEdgeAngle() + relativeAngleToPeak
    absoluteDistanceToPeak = relativeDistanceToPeak * self.getEdgeLength()
    absolutePeakX = (absoluteDistanceToPeak * math.cos(absoluteAngleToPeak)) + absoluteStartX
    absolutePeakY = (absoluteDistanceToPeak * math.sin(absoluteAngleToPeak)) + absoluteStartY
    return TPoint((absolutePeakX, absolutePeakY))

def pointsToBLC(points):
  # Determine how many lines there are
  allLines = []
  for point in points:
    for line in point.connectedLines:
      if not line in allLines:
        allLines.append(line)
  totalLineCount = len(allLines)

  # Create a traversal of the points
  traversal = []
  currentPoint = points[random.randint(0, len(points) - 1)]
  lastTraversedLine = None
  allTraversedLines = []
  while len(allTraversedLines) < totalLineCount:
    # Sort the options at this point based on whether or not they have been traversed
    untraversedOptions = []
    alreadyTraversedOptions = []
    for lineIndex in currentPoint.connectedLines:
      lineToSort = currentPoint.connectedLines[lineIndex]
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
      preferredAlreadyTraversedOptions = None
      if lastTraversedLine != None:
        preferredAlreadyTraversedOptions = alreadyTraversedOptions.remove(lastTraversedLine)
      if len(preferredAlreadyTraversedOptions) > 0:
        lineToTraverseNext = preferredAlreadyTraversedOptions[random.randint(0, len(preferredAlreadyTraversedOptions) - 1)]
      else:
        lineToTraverseNext = lastTraversedLine
    
    # Take the chosen route
    peakPoint = lineToTraverseNext.getPeakAsPoint()
    pointA = lineToTraverseNext.startPoint
    pointB = lineToTraverseNext.endPoint
    nextPointToGoTo = None
    if currentPoint == pointA:
      nextPointToGoTo =  pointB
    else:
      nextPointToGoTo = pointA
    traversal.extend([peakPoint, nextPointToGoTo])

    # Continue traversing
    currentPoint = nextPointToGoTo
  
  # Create the BLC
  return BLC(connectedSets=[ConnectedSet(traversal)])






startPoint = TPoint((0.25, 0.5))
endPoint = TPoint((0.6, 0.25))
line = TLine(startPoint, endPoint)
line.peakMagnitude = (-0.8)
line.peakOffset = (-0.3)
peakPoint = line.getPeakAsPoint()
peakX, peakY = peakPoint.position
print("PeakX: %.3f, PeakY: %.3f"%(peakX, peakY))