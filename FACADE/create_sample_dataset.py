import multiprocessing
import random
import numpy as np
from src.facade import FACADE
from src.blc import Point, Line, BLC, BLC_Utils

  
def generateAPerfectTriangle():
  # Create the points and lines
  pointA = Point(BLC_Utils.randRange(0.15, 0.35), BLC_Utils.randRange(0.15, 0.35))
  pointB = Point(BLC_Utils.randRange(0.65, 0.85), BLC_Utils.randRange(0.15, 0.35))
  pointC = Point(BLC_Utils.randRange(0.15, 0.85), BLC_Utils.randRange(0.65, 0.85))
  lineAB = Line(pointA, pointB)
  lineBC = Line(pointB, pointC)
  lineCA = Line(pointC, pointA)
  # Return the BLC
  return BLC.traversePointsToCreateBLC([pointA, pointB, pointC])


def generateAPerfectSix():
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


# Setup for using multiple processors
if __name__ == '__main__':
  multiprocessing.freeze_support()

  # This associates the above function with the class name 'triangle'
  triangleClassProperties = FACADE.ClassPropertiesObject('triangle', generateAPerfectTriangle)
  # This associates the above function with the class name 'digit_6'
  digitSixClassProperties = FACADE.ClassPropertiesObject('digit_6', generateAPerfectSix)


  # We then create a new FACADE instance with our set of classes
  facade = FACADE([triangleClassProperties, digitSixClassProperties])
  # And ask it to output several images from each of the classes we gave it
  facade.generateDataset(100, 'outputs/test_dataset')
