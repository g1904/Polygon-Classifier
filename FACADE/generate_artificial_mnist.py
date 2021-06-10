import multiprocessing
import random
import copy
from src.facade import FACADE
from src.blc import ConnectedSet, Point, Line, BLC, BLC_Utils


# 0
def generateAPerfect0():
  allPointsInCircle = []

  # Draw the zero
  topLeft = Point(BLC_Utils.randDev(0.45, 0.045), BLC_Utils.randDev(0.225, 0.05))
  bottom = Point(BLC_Utils.randDev(0.5, 0.035), BLC_Utils.randDev(0.775, 0.05))
  topRight = Point(BLC_Utils.randDev(0.55, 0.045), BLC_Utils.randDev(0.225, 0.05))
  Line(topLeft, bottom, peakMagnitude=BLC_Utils.randRange(-1.0, -0.4), peakOffset=BLC_Utils.randRange(-0.25, 0.25))
  Line(bottom, topRight, peakMagnitude=BLC_Utils.randRange(-1.0, -0.4), peakOffset=BLC_Utils.randRange(-0.25, 0.25))
  allPointsInCircle.extend([topLeft, bottom, topRight])

  # Add some random rotation
  BLC_Utils.rotatePointsAroundOrigin(allPointsInCircle, BLC_Utils.randRange(-180.0, 180.0))

  # Create a BLC for the circle
  zeroBLC = BLC.traversePointsToCreateBLC(allPointsInCircle)

  # Sometimes add a slash
  if random.random() < 0.2:
    slashTop = Point(BLC_Utils.randDev(0.7, 0.05), BLC_Utils.randDev(0.25, 0.035))
    slashBottom = Point(BLC_Utils.randDev(0.3, 0.05), BLC_Utils.randDev(0.75, 0.035))
    if random.random() < 0.5:
      BLC_Utils.rotatePointsAroundOrigin([slashTop, slashBottom], 120.0)
    slash = Line(slashTop, slashBottom)
    startPoint = Point(slashTop.x, slashTop.y)
    peakPoint = slash.getPeakAsPoint()
    endPoint = Point(slashBottom.x, slashBottom.y)
    slashSet = ConnectedSet([startPoint, peakPoint, endPoint])
    zeroBLC.connectedSets.append(slashSet)

  # Return the BLC
  return zeroBLC


# 1
def generateAPerfect1():
  allPointsInShape = []

  # Draw the main, vertical line
  pointTop = Point(0.5, BLC_Utils.randRange(0.2, 0.3))
  pointBottom = Point(0.5, BLC_Utils.randRange(0.7, 0.8))
  Line(pointTop, pointBottom)
  allPointsInShape.extend([pointTop, pointBottom])

  # Sometimes add a tip
  if random.random() < 0.35:
    topX, topY = pointTop.position
    pointTip = Point(BLC_Utils.randDev(topX - 0.1, 0.04), BLC_Utils.randDev(topY + 0.15, 0.065))
    Line(pointTip, pointTop)
    newShapePoints = [pointTip]
    newShapePoints.extend(allPointsInShape)
    allPointsInShape = newShapePoints

  # Sometimes add a base
  if random.random() < 0.35:
    bottomX, bottomY = pointBottom.position
    leftBase = Point(BLC_Utils.randDev(bottomX - 0.125, 0.05), bottomY)
    rightBase = Point(BLC_Utils.randDev(bottomX + 0.125, 0.05), bottomY)
    Line(leftBase, pointBottom)
    Line(rightBase, pointBottom)
    allPointsInShape.extend([leftBase, rightBase])

  # Add some random rotation
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-7.0, 7.0))
  
  # Return the BLC
  return BLC.traversePointsToCreateBLC(allPointsInShape)


# 2
def generateAPerfect2():
  allPointsInShape = []

  # Top line
  topLeft = Point(BLC_Utils.randDev(0.345, 0.0175), BLC_Utils.randDev(0.3, 0.015))
  topRight = Point(BLC_Utils.randDev(0.65, 0.0175), BLC_Utils.randDev(0.3, 0.015))
  Line(topLeft, topRight, peakMagnitude=BLC_Utils.randRange(0.5, 0.8))
  allPointsInShape.extend([topLeft, topRight])

  # Downward slash
  bottomLeft = Point(BLC_Utils.randDev(0.345, 0.015), BLC_Utils.randDev(0.7, 0.015))
  Line(topRight, bottomLeft, peakMagnitude=BLC_Utils.randRange(-0.2, 0.15), peakOffset=BLC_Utils.randRange(0.2, 0.6))
  allPointsInShape.extend([bottomLeft])

  # Bottom line
  bottomRight = Point(BLC_Utils.randDev(0.63, 0.025), BLC_Utils.randDev(0.7, 0.015))
  Line(bottomLeft, bottomRight)
  allPointsInShape.extend([bottomRight])

  # Add some random rotation
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-7.0, 7.0))
  
  # Return the BLC
  return BLC.traversePointsToCreateBLC(allPointsInShape)


# 3
def generateAPerfect3():
  allPointsInShape = []

  # Top arc
  topLeft = Point(BLC_Utils.randDev(0.345, 0.025), BLC_Utils.randDev(0.325, 0.015))
  topRight = Point(BLC_Utils.randDev(0.65, 0.025), BLC_Utils.randDev(0.325, 0.015))
  Line(topLeft, topRight, peakMagnitude=BLC_Utils.randRange(0.5, 0.95))
  allPointsInShape.extend([topLeft, topRight])

  # Upper mid arc
  middle = Point(BLC_Utils.randDev(0.45, 0.075), BLC_Utils.randDev(0.5, 0.045))
  Line(topRight, middle, peakMagnitude=BLC_Utils.randRange(0.15, 0.35))
  allPointsInShape.extend([middle])

  # Lower mid arc
  bottomRight = Point(BLC_Utils.randDev(0.65, 0.025), BLC_Utils.randDev(0.675, 0.015))
  Line(middle, bottomRight, peakMagnitude=BLC_Utils.randRange(0.15, 0.35))
  allPointsInShape.extend([bottomRight])

  # Lower mid arc
  bottomLeft = Point(BLC_Utils.randDev(0.345, 0.025), BLC_Utils.randDev(0.675, 0.015))
  Line(bottomRight, bottomLeft, peakMagnitude=BLC_Utils.randRange(0.5, 0.95))
  allPointsInShape.extend([bottomLeft])

  # Add some random rotation
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-10.0, 10.0))
  
  # Return the BLC
  return BLC.traversePointsToCreateBLC(allPointsInShape)


# 4
def generateAPerfect4():
  allPointsInShape = []
  finalBLC = None

  # Define all points
  topCenter = Point(BLC_Utils.randDev(0.6, 0.035), BLC_Utils.randDev(0.275, 0.05))
  midLeft = Point(BLC_Utils.randDev(0.37, 0.07), BLC_Utils.randDev(0.55, 0.05))
  midRight = Point(BLC_Utils.randDev(0.675, 0.1), BLC_Utils.randDev(midLeft.y, 0.025))
  bottomCenter = Point(BLC_Utils.randDev(topCenter.x, 0.02), BLC_Utils.randDev(midLeft.y + 0.17, 0.05))
  allPointsInShape.extend([topCenter, midLeft, midRight, bottomCenter])
  topLeft = None
  if random.random() < 0.5:
    topLeft = Point(BLC_Utils.randDev(midLeft.x, 0.025), BLC_Utils.randDev(0.275, 0.05))
    allPointsInShape.extend([topLeft])
  midCenter = None
  if random.random() < 0.5:
    midCenter = Point(BLC_Utils.randDev(topCenter.x, 0.02),BLC_Utils.randDev(midLeft.y, 0.05))
    allPointsInShape.extend([midCenter])

  # Add some random rotation
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-5.0, 5.0))

  # Setup lines
  if topLeft != None:
    Line(midLeft, topLeft)
  else:
    Line(midLeft, topCenter)
  if midCenter != None:
    Line(topCenter, midCenter)
    Line(midCenter, bottomCenter)
    Line(midLeft, midCenter)
    Line(midCenter, midRight)
  else:
    Line(topCenter, bottomCenter)
    Line(midLeft, midRight)
  
  # SomeTimes we have two seperate connected sets
  if topLeft != None and midCenter == None:
    blcA = BLC.traversePointsToCreateBLC([topLeft, midLeft, midRight])
    blcB = BLC.traversePointsToCreateBLC([topCenter, bottomCenter])
    blcA.connectedSets.extend(blcB.connectedSets)
    finalBLC = blcA
  else:
    finalBLC = BLC.traversePointsToCreateBLC(allPointsInShape)
  
  # Return the BLC
  return finalBLC


# 5
def generateAPerfect5():
  topLinePoints = []
  extraConnectedSet = None
  allPointsInShape = []
  allPointsInBody = []

  # Top line
  topLeft = Point(BLC_Utils.randDev(0.345, 0.035), BLC_Utils.randDev(0.25, 0.015))
  topRight = Point(BLC_Utils.randDev(0.65, 0.065), BLC_Utils.randDev(topLeft.y, 0.0075))
  topLinePoints.extend([topLeft, topRight])
  topLine = Line(topLeft, topRight)

  # Mid Left Line
  startOfMidLeftLine = None
  if random.random() < 0.5:
    startOfMidLeftLine = topLeft
    allPointsInBody.extend(topLinePoints)
  else:
    startOfMidLeftLine = Point(BLC_Utils.randDev(0.34, 0.025), BLC_Utils.randDev(0.275, 0.015))
    allPointsInBody.extend([startOfMidLeftLine])
    if random.random() < 0.5:
      topLinePoints.reverse()
    topLineStartPoint = Point(topLinePoints[0].x, topLinePoints[0].y)
    topLinePeakPoint = topLine.getPeakAsPoint()
    topLineEndPoint = Point(topLinePoints[1].x, topLinePoints[1].y)
    extraConnectedSet = ConnectedSet([topLineStartPoint, topLinePeakPoint, topLineEndPoint])
  midLeft = Point(BLC_Utils.randDev(startOfMidLeftLine.x, 0.015), BLC_Utils.randDev(startOfMidLeftLine.y + 0.175, 0.05))
  allPointsInBody.extend([midLeft])
  Line(startOfMidLeftLine, midLeft)

  # Upper arc
  lowerRight = Point(BLC_Utils.randDev(0.65, 0.05), BLC_Utils.randDev(midLeft.y + 0.15, 0.025))
  allPointsInBody.extend([lowerRight])
  Line(midLeft, lowerRight, peakMagnitude=BLC_Utils.randRange(0.15, 0.5))

  # Lower arc
  bottomLeft = Point(BLC_Utils.randDev(0.345, 0.025), BLC_Utils.randDev(lowerRight.y + 0.15, 0.025))
  allPointsInBody.extend([bottomLeft])
  Line(lowerRight, bottomLeft, peakMagnitude=BLC_Utils.randRange(0.15, 0.5))

  # Add some random rotation
  allPointsInShape = copy.copy(allPointsInBody)
  if extraConnectedSet != None:
    allPointsInShape.extend(extraConnectedSet.points)
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-8.0, 8.0))
  
  # Return the BLC
  fiveBLC = BLC.traversePointsToCreateBLC(allPointsInBody)
  if extraConnectedSet != None:
    fiveBLC.connectedSets.append(extraConnectedSet)
  return fiveBLC


# 6
def generateAPerfect6():
  # Create the points and lines
  allPointsInShape = None
  if random.random() < 0.25:
    pointA = Point(0.35, 0.6)
    pointB = Point(0.65, 0.6)
    lineAB = Line(pointA, pointB, peakMagnitude=BLC_Utils.randDev(0.75, 0.75))
    lineBA = Line(pointB, pointA, peakMagnitude=BLC_Utils.randDev(0.75, 0.75))
    abPeakX, abPeakY = lineAB.getPeakAsPoint().position
    pointC = Point(BLC_Utils.randDev(0.6, 0.15), BLC_Utils.randRange(0.2, abPeakY - 0.15))
    lineAC = Line(pointA, pointC, peakMagnitude=BLC_Utils.randRange(0.05, 1.0), peakOffset=BLC_Utils.randDev(0.0, 0.35))
    allPointsInShape = [pointA, pointB, pointC]
  else:
    pointA = Point(BLC_Utils.randDev(0.475, 0.05), BLC_Utils.randDev(0.55, 0.025))
    pointB = Point(0.65, 0.6)
    pointC = Point(BLC_Utils.randDev(0.35, 0.025), 0.6)
    lineAB = Line(pointA, pointB, peakMagnitude=BLC_Utils.randDev(0.75, 0.75))
    lineBC = Line(pointB, pointC, peakMagnitude=BLC_Utils.randDev(0.75, 0.75))
    pointD = Point(BLC_Utils.randDev(0.65, 0.15), BLC_Utils.randRange(0.2, pointA.y - 0.175))
    lineCD = Line(pointC, pointD, peakMagnitude=BLC_Utils.randRange(0.05, 1.0), peakOffset=BLC_Utils.randDev(0.0, 0.35))
    allPointsInShape = [pointA, pointB, pointC, pointD]
  # Add some random rotation
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-10.0, 10.0))
  # Return the BLC
  return BLC.traversePointsToCreateBLC(allPointsInShape)


# 7
def generateAPerfect7():
  allPointsInShape = []

  # Top line
  topLeft = Point(BLC_Utils.randRange(0.3, 0.4), BLC_Utils.randRange(0.2, 0.35))
  topRight = Point(BLC_Utils.randRange(0.7, 0.6), BLC_Utils.randDev(topLeft.y, 0.025))
  allPointsInShape.extend([topLeft, topRight])
  Line(topLeft, topRight)

  # Vertical line
  bottomCenter = Point(BLC_Utils.randRange(0.45, 0.55), BLC_Utils.randRange(0.65, 0.8))
  allPointsInShape.extend([bottomCenter])
  Line(topRight, bottomCenter, peakMagnitude=BLC_Utils.randRange(-0.35, 0.025), peakOffset=BLC_Utils.randRange(0.2, 0.6))
  
  # Return the BLC
  return BLC.traversePointsToCreateBLC(allPointsInShape)


# Setup for using multiple processors
if __name__ == '__main__':
  multiprocessing.freeze_support()

  # Define the classes
  facade = FACADE([
    FACADE.ClassPropertiesObject('digit_0', generateAPerfect0),
    FACADE.ClassPropertiesObject('digit_1', generateAPerfect1),
    FACADE.ClassPropertiesObject('digit_2', generateAPerfect2),
    FACADE.ClassPropertiesObject('digit_3', generateAPerfect3),
    FACADE.ClassPropertiesObject('digit_4', generateAPerfect4),
    FACADE.ClassPropertiesObject('digit_5', generateAPerfect5),
    FACADE.ClassPropertiesObject('digit_6', generateAPerfect6),
    FACADE.ClassPropertiesObject('digit_7', generateAPerfect7)
  ])
  
  # Now generate the dataset
  facade.generateDataset(100, 'outputs/artificial_mnist')