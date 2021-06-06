from src.facade import FACADE
from src.blc import Point, Line, BLC, BLC_Utils


def generateAPerfectTriangle():
  # Create the points and lines
  pointA = Point(BLC_Utils.randRange(0.1, 0.4), BLC_Utils.randRange(0.1, 0.4))
  pointB = Point(BLC_Utils.randRange(0.6, 0.9), BLC_Utils.randRange(0.1, 0.4))
  pointC = Point(BLC_Utils.randRange(0.1, 0.9), BLC_Utils.randRange(0.6, 0.9))
  lineAB = Line(pointA, pointB)
  lineBC = Line(pointB, pointC)
  lineCA = Line(pointC, pointA)
  # Return the BLC
  return BLC.traversePointsToCreateBLC([pointA, pointB, pointC])

# This associates the above function with the class name 'triangle'
triangleClassProperties = FACADE.ClassPropertiesObject('triangle', generateAPerfectTriangle)


def generateAPerfectSix():
  # Create the points and lines
  pointA = Point(0.35, 0.6)
  pointB = Point(0.65, 0.6)
  lineAB = Line(pointA, pointB, peakMagnitude=BLC_Utils.randDev(0.75, 0.5))
  lineBA = Line(pointB, pointA, peakMagnitude=BLC_Utils.randDev(0.75, 0.5))
  abPeakX, abPeakY = lineAB.getPeakAsPoint().position
  pointC = Point(BLC_Utils.randDev(0.6, 0.15), BLC_Utils.randRange(0.2, abPeakY - 0.15))
  lineAC = Line(pointA, pointC, peakMagnitude=BLC_Utils.randRange(0.05, 1.0), peakOffset=BLC_Utils.randDev(0.0, 0.35))
  # Return the BLC
  return BLC.traversePointsToCreateBLC([pointA, pointB, pointC])

# This associates the above function with the class name 'digit_6'
digitSixClassProperties = FACADE.ClassPropertiesObject('digit_6', generateAPerfectSix)


# We then create a new FACADE instance with our set of classes
facade = FACADE([triangleClassProperties, digitSixClassProperties])
# And ask it to output several images from each of the classes we gave it
facade.generateDataset(100, 'outputs/test_dataset')
