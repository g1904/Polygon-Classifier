import multiprocessing
import random
import copy
from src.facade import FACADE
from src.blc import ConnectedSet, Point, Line, BLC, BLC_Utils


# 0
def generateAPerfect0():
  allPointsInShape = []

  # Draw the zero
  topLeft = Point(BLC_Utils.randDev(0.45, 0.075), BLC_Utils.randDev(0.225, 0.06))
  bottom = Point(BLC_Utils.randDev(0.5, 0.035), BLC_Utils.randDev(0.775, 0.05))
  topRight = Point(BLC_Utils.randDev(0.55, 0.075), BLC_Utils.randDev(0.235, 0.07))
  Line(topLeft, bottom, peakMagnitude=BLC_Utils.randRange(-1.1, -0.2), peakOffset=BLC_Utils.randRange(-0.4, 0.4))
  Line(bottom, topRight, peakMagnitude=BLC_Utils.randRange(-1.1, -0.2), peakOffset=BLC_Utils.randRange(-0.4, 0.4))
  allPointsInShape.extend([topLeft, bottom, topRight])

  # Add some random rotation
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-180.0, 180.0))

  # Randomly mirror vertically and horizontally
  shouldMirrorHorizontal = random.random() < 0.5
  shouldMirrorVertical = random.random() < 0.5
  BLC_Utils.mirrorPoints(allPointsInShape, shouldMirrorHorizontal, shouldMirrorVertical)
  
  # Return the BLC
  return BLC.traversePointsToCreateBLC(allPointsInShape)



# 1
def generateAPerfect1():
  allPointsInShape = []

  # Draw the main, vertical line
  pointTop = Point(0.5, BLC_Utils.randRange(0.2, 0.3))
  pointBottom = Point(0.5, BLC_Utils.randRange(0.7, 0.8))
  Line(pointTop, pointBottom)
  allPointsInShape.extend([pointTop, pointBottom])

  # Sometimes add a tip
  addedTip = False
  if random.random() < 0.35:
    topX, topY = pointTop.position
    pointTip = Point(BLC_Utils.randDev(topX - 0.15, 0.1), BLC_Utils.randDev(topY + 0.15, 0.065))
    Line(pointTip, pointTop)
    newShapePoints = [pointTip]
    newShapePoints.extend(allPointsInShape)
    allPointsInShape = newShapePoints
    addedTip = True

  # Sometimes add a base
  if (addedTip and random.random() < 0.85) or (not addedTip and random.random() < 0.15):
    bottomX, bottomY = pointBottom.position
    leftBase = Point(BLC_Utils.randDev(bottomX - 0.125, 0.05), bottomY)
    rightBase = Point(BLC_Utils.randDev(bottomX + 0.125, 0.05), bottomY)
    Line(leftBase, pointBottom)
    Line(rightBase, pointBottom)
    allPointsInShape.extend([leftBase, rightBase])

  # Add some random rotation
  if addedTip:
    BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-15.0, 15.0))
  else:
    BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-31.0, 31.0))
  
  # Return the BLC
  return BLC.traversePointsToCreateBLC(allPointsInShape)


# 2
def generateAPerfect2():
  allPointsInShape = []

  # Top line
  topLeft = Point(BLC_Utils.randDev(0.345, 0.0175), BLC_Utils.randDev(0.3, 0.015))
  topRight = Point(BLC_Utils.randDev(0.65, 0.0175), BLC_Utils.randDev(0.3, 0.015))
  Line(topLeft, topRight, peakMagnitude=BLC_Utils.randRange(0.5, 0.9), peakOffset=BLC_Utils.randRange(-0.5, 0.5))
  allPointsInShape.extend([topLeft, topRight])

  # Downward slash
  bottomLeft = Point(BLC_Utils.randDev(0.345, 0.015), BLC_Utils.randDev(0.7, 0.015))
  Line(topRight, bottomLeft, peakMagnitude=BLC_Utils.randRange(-0.2, 0.55), peakOffset=BLC_Utils.randRange(-0.3, 0.8))
  allPointsInShape.extend([bottomLeft])

  # sometimes add a more pronounced bottom loop
  if random.random() < 0.4:
    bottomLeft.x -= BLC_Utils.randRange(0.075, 0.175)
    bottomLeft.y += BLC_Utils.randRange(0.075, 0.175)
    newBottomLeft = Point(BLC_Utils.randDev(0.345, 0.015), BLC_Utils.randDev(0.7, 0.015))
    Line(bottomLeft, newBottomLeft, peakMagnitude=BLC_Utils.randRange(0.0, 0.75), peakOffset=BLC_Utils.randRange(-0.5, 0.75))
    allPointsInShape.extend([newBottomLeft])
    bottomLeft = newBottomLeft

  # Bottom line
  bottomRight = Point(BLC_Utils.randDev(0.63, 0.02), BLC_Utils.randDev(0.65, 0.015))
  Line(bottomLeft, bottomRight, peakMagnitude=BLC_Utils.randRange(-0.2, 0.4), peakOffset=BLC_Utils.randRange(-0.95, 0.4))
  allPointsInShape.extend([bottomRight])

  # Add some random rotation
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-20.0, 20.0))
  
  # Return the BLC
  return BLC.traversePointsToCreateBLC(allPointsInShape)


# 3
def generateAPerfect3():
  allPointsInShape = []

  # Top arc
  topLeft = Point(BLC_Utils.randRange(0.3, 0.37), BLC_Utils.randDev(0.335, 0.025))
  topRight = Point(BLC_Utils.randDev(0.65, 0.025), BLC_Utils.randDev(0.325, 0.025))
  Line(topLeft, topRight, peakMagnitude=BLC_Utils.randRange(0.1, 0.95))
  allPointsInShape.extend([topLeft, topRight])

  # Upper mid arc
  middle = Point(BLC_Utils.randRange(0.4, 0.5), BLC_Utils.randRange(0.575, topRight.y + 0.075))
  Line(topRight, middle, peakMagnitude=BLC_Utils.randRange(-0.4, 0.65))
  allPointsInShape.extend([middle])

  # Sometimes add a middle loop
  if random.random() < 0.25:
    newMiddle = Point(middle.x, middle.y)
    middle.x += 0.1
    middle.y -= 0.05
    Line(middle, newMiddle, peakMagnitude=BLC_Utils.randRange(0.0, 0.7), peakOffset=BLC_Utils.randRange(-0.5, 0.75))
    allPointsInShape.extend([newMiddle])
    middle = newMiddle

  # Lower mid arc
  bottomRight = Point(BLC_Utils.randDev(0.65, 0.025), BLC_Utils.randDev(0.675, 0.015))
  Line(middle, bottomRight, peakMagnitude=BLC_Utils.randRange(-0.2, 0.65))
  allPointsInShape.extend([bottomRight])

  # Lower mid arc
  bottomLeft = Point(BLC_Utils.randRange(0.275, middle.x - 0.075), BLC_Utils.randRange(middle.y + 0.075, 0.725))
  Line(bottomRight, bottomLeft, peakMagnitude=BLC_Utils.randRange(0.5, 1.1))
  allPointsInShape.extend([bottomLeft])

  # Add some random rotation
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-17.0, 17.0))
  
  # Return the BLC
  return BLC.traversePointsToCreateBLC(allPointsInShape)


# 4
def generateAPerfect4():
  allPointsInShape = []
  finalBLC = None

  # Define all points
  topCenter = Point(BLC_Utils.randRange(0.5, 0.85), BLC_Utils.randRange(0.225, 0.375))
  midLeft = Point(BLC_Utils.randRange(0.25, 0.4), BLC_Utils.randRange(0.5, 0.7))
  midRight = Point(BLC_Utils.randRange(topCenter.x, topCenter.x + 0.15), BLC_Utils.randDev(midLeft.y, 0.025))
  bottomCenter = Point(BLC_Utils.randRange(topCenter.x - 0.15, topCenter.x + 0.05), BLC_Utils.randDev(midLeft.y + 0.1, 0.05))
  allPointsInShape.extend([topCenter, midLeft, midRight, bottomCenter])
  topLeft = None
  if random.random() < 0.15:
    topLeft = Point(BLC_Utils.randRange(midLeft.x, topCenter.x - 0.15), BLC_Utils.randRange(0.225, 0.375))
    allPointsInShape.extend([topLeft])
  midCenter = None
  if random.random() < 0.5:
    midCenter = Point(BLC_Utils.randDev(topCenter.x, 0.02),BLC_Utils.randDev(midLeft.y, 0.05))
    allPointsInShape.extend([midCenter])

  # Add some random rotation
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-15.0, 15.0))

  # Setup lines
  if topLeft != None:
    Line(midLeft, topLeft, peakMagnitude=BLC_Utils.randRange(-0.2, 0.2))
  else:
    Line(midLeft, topCenter)
  if midCenter != None:
    Line(topCenter, midCenter, peakMagnitude=BLC_Utils.randRange(-0.2, 0.2))
    Line(midCenter, bottomCenter, peakMagnitude=BLC_Utils.randRange(-0.2, 0.2))
    Line(midLeft, midCenter, peakMagnitude=BLC_Utils.randRange(-0.2, 0.2))
    Line(midCenter, midRight)
  else:
    Line(topCenter, bottomCenter, peakMagnitude=BLC_Utils.randRange(-0.2, 0.2))
    Line(midLeft, midRight, peakMagnitude=BLC_Utils.randRange(-0.2, 0.2))
  
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
  topLeft = Point(BLC_Utils.randDev(0.345, 0.035), BLC_Utils.randRange(0.225, 0.375))
  topRight = Point(BLC_Utils.randRange(0.475, 0.75), BLC_Utils.randRange(0.215, 0.3))
  topLinePoints.extend([topLeft, topRight])
  topLine = Line(topLeft, topRight, peakMagnitude=BLC_Utils.randRange(-0.2, 0.2))

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
  midLeft = Point(BLC_Utils.randDev(startOfMidLeftLine.x, 0.03), BLC_Utils.randDev(startOfMidLeftLine.y + 0.175, 0.05))
  allPointsInBody.extend([midLeft])
  Line(startOfMidLeftLine, midLeft, peakMagnitude=BLC_Utils.randRange(-0.2, 0.2))

  # Upper arc
  lowerRight = Point(BLC_Utils.randRange(0.5, 0.75), BLC_Utils.randDev(midLeft.y + 0.1, 0.07))
  allPointsInBody.extend([lowerRight])
  Line(midLeft, lowerRight, peakMagnitude=BLC_Utils.randRange(0.15, 0.75))

  # Lower arc
  bottomLeft = Point(BLC_Utils.randRange(0.225, lowerRight.x - 0.1), BLC_Utils.randDev(lowerRight.y + 0.1, 0.09))
  allPointsInBody.extend([bottomLeft])
  Line(lowerRight, bottomLeft, peakMagnitude=BLC_Utils.randRange(0.15, 0.75))

  # Add some random rotation
  allPointsInShape = copy.copy(allPointsInBody)
  if extraConnectedSet != None:
    allPointsInShape.extend(extraConnectedSet.points)
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-15.0, 15.0))
  
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
    lineAB = Line(pointA, pointB, peakMagnitude=BLC_Utils.randRange(0.35, 0.75))
    lineBA = Line(pointB, pointA, peakMagnitude=BLC_Utils.randRange(0.35, 0.75))
    abPeakX, abPeakY = lineAB.getPeakAsPoint().position
    pointC = Point(BLC_Utils.randDev(0.6, 0.15), BLC_Utils.randRange(0.2, abPeakY - 0.15))
    lineAC = Line(pointA, pointC, peakMagnitude=BLC_Utils.randRange(0.05, 1.0), peakOffset=BLC_Utils.randDev(0.0, 0.35))
    allPointsInShape = [pointA, pointB, pointC]
  else:
    pointA = Point(BLC_Utils.randRange(0.325, 0.58), BLC_Utils.randDev(0.55, 0.025))
    pointB = Point(0.65, 0.6)
    pointC = Point(BLC_Utils.randDev(0.35, 0.025), 0.6)
    lineAB = Line(pointA, pointB, peakMagnitude=BLC_Utils.randRange(0.35, 0.75))
    lineBC = Line(pointB, pointC, peakMagnitude=BLC_Utils.randRange(0.35, 0.75))
    pointD = Point(BLC_Utils.randDev(0.65, 0.15), BLC_Utils.randRange(0.2, pointA.y - 0.175))
    lineCD = Line(pointC, pointD, peakMagnitude=BLC_Utils.randRange(0.05, 1.0), peakOffset=BLC_Utils.randDev(0.0, 0.35))
    allPointsInShape = [pointA, pointB, pointC, pointD]
  # Add some random rotation
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-90.0, 15.0))
  # Return the BLC
  return BLC.traversePointsToCreateBLC(allPointsInShape)


# 7
def generateAPerfect7():
  allPointsBody = []
  allPointsInSlash = []
  slashSet = None

  # Top line
  topLeft = Point(BLC_Utils.randRange(0.25, 0.4), BLC_Utils.randRange(0.2, 0.35))
  topRight = Point(BLC_Utils.randRange(0.6, 0.75), BLC_Utils.randDev(topLeft.y, 0.025))
  allPointsBody.extend([topLeft, topRight])
  Line(topLeft, topRight, peakMagnitude=BLC_Utils.randRange(-0.15, 0.15))

  # Somtimes add a droop
  if random.random() < 0.4:
    droopTip = Point(BLC_Utils.randDev(topLeft.x, 0.065), BLC_Utils.randRange(topLeft.y + 0.05, topLeft.y + 0.15))
    tempAllPointsBody = [droopTip]
    tempAllPointsBody.extend(allPointsBody)
    allPointsBody = tempAllPointsBody
    Line(droopTip, topLeft)

  # Vertical line
  bottomCenter = Point(BLC_Utils.randRange(0.45, 0.55), BLC_Utils.randRange(0.65, 0.8))
  allPointsBody.extend([bottomCenter])
  Line(topRight, bottomCenter, peakMagnitude=BLC_Utils.randRange(-0.35, 0.025), peakOffset=BLC_Utils.randRange(0.2, 0.6))
  
  # Sometimes add a slash
  if random.random() < 0.35:
    approxVerticalLineX = ((topRight.x - bottomCenter.x) / 2.0) + topRight.x
    slashLeft = Point(BLC_Utils.randRange(0.25, approxVerticalLineX), BLC_Utils.randRange(topRight.y + 0.15, bottomCenter.y - 0.1))
    slashRight = Point(BLC_Utils.randRange(approxVerticalLineX, 0.75), BLC_Utils.randRange(topRight.y + 0.15, bottomCenter.y - 0.1))
    allPointsInSlash.extend([slashLeft, slashRight])
    slashLine = Line(slashLeft, slashRight, peakMagnitude=BLC_Utils.randRange(-0.25, 0.25))
    startPoint = Point(slashLeft.x, slashLeft.y)
    peakPoint = slashLine.getPeakAsPoint()
    endPoint = Point(slashRight.x, slashRight.y)
    slashSet = [startPoint, peakPoint, endPoint]
    if random.random() > 0.5:
      slashSet.reverse()
    slashSet = ConnectedSet(slashSet)

  # Add some random rotation
  allPointsInShape = copy.copy(allPointsBody)
  allPointsInShape.extend(allPointsInSlash)
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-6.0, 6.0))

  # Generate the BLC
  sevenBLC = BLC.traversePointsToCreateBLC(allPointsBody)
  if slashSet != None:
    sevenBLC.connectedSets.append(slashSet)
  
  # Return the BLC
  return sevenBLC


# 8
def generateAPerfect8():
  allPointsInShape = []

  # Top arc
  topLeft = Point(BLC_Utils.randRange(0.3, 0.45), BLC_Utils.randDev(0.325, 0.05))
  topRight = Point(BLC_Utils.randRange(0.525, 0.7), BLC_Utils.randDev(0.325, 0.05))
  allPointsInShape.extend([topLeft, topRight])
  Line(topLeft, topRight, peakMagnitude=BLC_Utils.randRange(0.05, 1.0))

  # Upper right arc
  middle = Point(BLC_Utils.randDev(0.475, 0.075), BLC_Utils.randDev(0.5, 0.075))
  allPointsInShape.extend([middle])
  Line(topRight, middle, peakMagnitude=BLC_Utils.randRange(0.05, 0.65))

  # Upper Left Arc
  if random.random() < 0.25:
    Line(middle, topLeft, peakMagnitude=BLC_Utils.randRange(0.05, 0.65))
  else:
    alternateTopLeft = Point(BLC_Utils.randDev(topLeft.x + 0.075, 0.045), BLC_Utils.randDev(0.365, 0.035))
    allPointsInShape.extend([alternateTopLeft])
    Line(middle, alternateTopLeft, peakMagnitude=BLC_Utils.randRange(0.05, 0.65))

  # Lower right arc
  bottomRight = Point(BLC_Utils.randRange(0.525, 0.7), BLC_Utils.randDev(0.675, 0.05))
  allPointsInShape.extend([bottomRight])
  Line(middle, bottomRight, peakMagnitude=BLC_Utils.randRange(0.05, 0.65))

  # Bottom arc
  bottomLeft = Point(BLC_Utils.randRange(0.3, 0.475), BLC_Utils.randDev(0.675, 0.05))
  allPointsInShape.extend([bottomLeft])
  Line(bottomRight, bottomLeft, peakMagnitude=BLC_Utils.randRange(0.05, 1.0))

  # Lower left arc
  Line(bottomLeft, middle, peakMagnitude=BLC_Utils.randRange(0.05, 0.65))

  # Randomly mirror vertically and horizontally
  shouldMirrorHorizontal = random.random() < 0.5
  shouldMirrorVertical = random.random() < 0.5
  BLC_Utils.mirrorPoints(allPointsInShape, shouldMirrorHorizontal, shouldMirrorVertical)

  # Add some random rotation
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-23.0, 23.0))
  
  # Return the BLC
  return BLC.traversePointsToCreateBLC(allPointsInShape)


# 9
def generateAPerfect9():
  allPointsInShape = []

  # Points
  topLeft = Point(BLC_Utils.randRange(0.25, 0.45), BLC_Utils.randRange(0.25, 0.3))
  topRight = Point(BLC_Utils.randRange(0.7, 0.55), BLC_Utils.randDev(topLeft.y, 0.01))
  midLeft = Point(BLC_Utils.randRange(0.25, 0.45), BLC_Utils.randDev(topLeft.y + 0.2, 0.1))
  allPointsInShape.extend([topLeft, topRight, midLeft])
  midRight = None
  if random.random():
    midRight = Point(BLC_Utils.randDev(topRight.x, 0.025), BLC_Utils.randRange(topRight.y + 0.05, midLeft.y + 0.05))
    allPointsInShape.extend([midRight])
  bottomRight = Point(BLC_Utils.randDev(topRight.x - 0.15, 0.2), BLC_Utils.randRange(0.72, 0.8))
  allPointsInShape.extend([bottomRight])

  # Lines
  Line(midLeft, topLeft, peakMagnitude=BLC_Utils.randRange(0.1, 0.7))
  Line(topLeft, topRight, peakMagnitude=BLC_Utils.randRange(0.1, 0.7))
  if midRight != None:
    Line(topRight, midRight)
    Line(midRight, midLeft, peakMagnitude=BLC_Utils.randRange(0.1, 0.7))
    Line(midRight, bottomRight, peakMagnitude=BLC_Utils.randRange(0.0, 0.55), peakOffset=BLC_Utils.randDev(0.1, 0.65))
  else:
    Line(topRight, midLeft, peakMagnitude=BLC_Utils.randRange(0.3, 0.9), peakOffset=BLC_Utils.randDev(0.25, 0.75))
    Line(topRight, bottomRight, peakMagnitude=BLC_Utils.randRange(0.0, 0.55), peakOffset=BLC_Utils.randDev(0.1, 0.65))
  
  # Add some random rotation
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-15.0, 15.0))
  
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
    FACADE.ClassPropertiesObject('digit_7', generateAPerfect7),
    FACADE.ClassPropertiesObject('digit_8', generateAPerfect8),
    FACADE.ClassPropertiesObject('digit_9', generateAPerfect9)
  ])
  
  # Now generate the dataset
  facade.generateDataset(8000, 'outputs/artificial_mnist')