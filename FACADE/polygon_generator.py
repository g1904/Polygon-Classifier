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
  
def generateAPerfectSquare():
  # Create the points and lines
  pointA = Point(BLC_Utils.randRange(0.15, 0.35), BLC_Utils.randRange(0.15, 0.35))
  pointB = Point(BLC_Utils.randRange(0.65, 0.85), BLC_Utils.randRange(0.15, 0.35))
  pointC = Point(BLC_Utils.randRange(0.15, 0.35), BLC_Utils.randRange(0.65, 0.85))
  pointD = Point(BLC_Utils.randRange(0.65, 0.85), BLC_Utils.randRange(0.65, 0.85))
  lineAB = Line(pointA, pointB)
  lineAC = Line(pointA, pointC)
  lineBD = Line(pointB, pointD)
  lineCD = Line(pointC, pointD)
  # Return the BLC
  return BLC.traversePointsToCreateBLC([pointA, pointB, pointC, pointD])
  
def generateAPerfectRectangle():
  allPointsInShape = None
    
  # Create the points and lines
  if random.random() < 0.5: # narrow shape
      pointA = Point(BLC_Utils.randRange(0.30, 0.40), BLC_Utils.randRange(0.15, 0.20))
      pointB = Point(BLC_Utils.randRange(0.60, 0.80), BLC_Utils.randRange(0.15, 0.20))
      pointC = Point(BLC_Utils.randRange(0.30, 0.40), BLC_Utils.randRange(0.80, 0.85))
      pointD = Point(BLC_Utils.randRange(0.60, 0.80), BLC_Utils.randRange(0.80, 0.85))
  else: # wide shape
      pointA = Point(BLC_Utils.randRange(0.15, 0.20), BLC_Utils.randRange(0.25, 0.35))
      pointB = Point(BLC_Utils.randRange(0.80, 0.85), BLC_Utils.randRange(0.25, 0.35))
      pointC = Point(BLC_Utils.randRange(0.15, 0.20), BLC_Utils.randRange(0.65, 0.75))
      pointD = Point(BLC_Utils.randRange(0.80, 0.85), BLC_Utils.randRange(0.65, 0.75))
      

  lineAB = Line(pointA, pointB)
  lineAC = Line(pointA, pointC)
  lineBD = Line(pointB, pointD)
  lineCD = Line(pointC, pointD)
  # Return the BLC
  allPointsInShape = [pointA, pointB, pointC, pointD]
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-7.0, 7.0))
  return BLC.traversePointsToCreateBLC([pointA, pointB, pointC, pointD])
  
def generateAPerfectHexagon():
    
  allPointsInShape = None
  # Create the points and lines
  if random.random() < 0.1: # narrow shape
      pointA = Point(BLC_Utils.randRange(0.45, 0.55), BLC_Utils.randRange(0.15, 0.20)) # (0.50, 0.15)
      pointB = Point(BLC_Utils.randRange(0.65, 0.75), BLC_Utils.randRange(0.30, 0.35)) # (0.70, 0.30)
      pointC = Point(BLC_Utils.randRange(0.65, 0.75), BLC_Utils.randRange(0.65, 0.70)) # (0.70, 0.70)
      pointD = Point(BLC_Utils.randRange(0.45, 0.55), BLC_Utils.randRange(0.80, 0.85)) # (0.50, 0.85)
      pointE = Point(BLC_Utils.randRange(0.25, 0.35), BLC_Utils.randRange(0.65, 0.70)) # (0.30, 0.70)
      pointF = Point(BLC_Utils.randRange(0.25, 0.35), BLC_Utils.randRange(0.30, 0.35)) # (0.30, 0.30)
  else:
      pointA = Point(BLC_Utils.randRange(0.30, 0.35), BLC_Utils.randRange(0.25, 0.30)) # (0.30, 0.30)
      pointB = Point(BLC_Utils.randRange(0.65, 0.70), BLC_Utils.randRange(0.25, 0.30)) # (0.70, 0.30)
      pointC = Point(BLC_Utils.randRange(0.80, 0.85), BLC_Utils.randRange(0.45, 0.55)) # (0.85, 0.50)
      pointD = Point(BLC_Utils.randRange(0.65, 0.70), BLC_Utils.randRange(0.65, 0.70)) # (0.70, 0.70)
      pointE = Point(BLC_Utils.randRange(0.30, 0.35), BLC_Utils.randRange(0.65, 0.70)) # (0.30, 0.70)
      pointF = Point(BLC_Utils.randRange(0.15, 0.20), BLC_Utils.randRange(0.45, 0.55)) # (0.15, 0.50)
  lineAB = Line(pointA, pointB)
  lineBC = Line(pointB, pointC)
  lineCD = Line(pointC, pointD)
  lineDE = Line(pointD, pointE)
  lineEF = Line(pointE, pointF)
  lineFA = Line(pointF, pointA)
  
  allPointsInShape = [pointA, pointB, pointC, pointD, pointE, pointF]
  # BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-5.0, 5.0))
  
  # Return the BLC
  return BLC.traversePointsToCreateBLC(allPointsInShape)
  
# Setup for using multiple processors
if __name__ == '__main__':
  multiprocessing.freeze_support()

  # This associates the above function with the class name 'triangle'
  triangleClassProperties = FACADE.ClassPropertiesObject('triangle', generateAPerfectTriangle)
  # This associates the above function with the class name 'square'
  squareClassProperties = FACADE.ClassPropertiesObject('square', generateAPerfectSquare)
  # This associates the above function with the class name 'rectangle'
  rectangleClassProperties = FACADE.ClassPropertiesObject('rectangle', generateAPerfectRectangle)
  # This associates the above function with the class name 'rectangle'
  hexagonClassProperties = FACADE.ClassPropertiesObject('hexagon', generateAPerfectHexagon)


  # We then create a new FACADE instance with our set of classes
  facade = FACADE([triangleClassProperties, squareClassProperties, rectangleClassProperties, hexagonClassProperties])
  # And ask it to output several images from each of the classes we gave it
  facade.generateDataset(100, 'outputs/polygons')