import multiprocessing
import random
import numpy as np
from src.facade import FACADE
from src.blc import ConnectedSet, Point, Line, BLC, BLC_Utils

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
  # if statements not necessary with rotation
  if random.random() < 0.5: # pointy top
      pointA = Point(BLC_Utils.randDev(0.50, 0.05), BLC_Utils.randDev(0.20, 0.05)) 
      pointB = Point(BLC_Utils.randDev(0.70, 0.05), BLC_Utils.randDev(0.30, 0.05)) 
      pointC = Point(BLC_Utils.randDev(0.70, 0.05), BLC_Utils.randDev(0.70, 0.05)) 
      pointD = Point(BLC_Utils.randDev(0.50, 0.05), BLC_Utils.randDev(0.80, 0.05)) 
      pointE = Point(BLC_Utils.randDev(0.30, 0.05), BLC_Utils.randDev(0.70, 0.05)) 
      pointF = Point(BLC_Utils.randDev(0.30, 0.05), BLC_Utils.randDev(0.30, 0.05)) 
  else: # wide side at the top
      pointA = Point(BLC_Utils.randDev(0.30, 0.05), BLC_Utils.randDev(0.30, 0.05)) 
      pointB = Point(BLC_Utils.randDev(0.70, 0.05), BLC_Utils.randDev(0.30, 0.05)) 
      pointC = Point(BLC_Utils.randDev(0.80, 0.05), BLC_Utils.randDev(0.50, 0.05)) 
      pointD = Point(BLC_Utils.randDev(0.70, 0.05), BLC_Utils.randDev(0.70, 0.05)) 
      pointE = Point(BLC_Utils.randDev(0.30, 0.05), BLC_Utils.randDev(0.70, 0.05)) 
      pointF = Point(BLC_Utils.randDev(0.20, 0.05), BLC_Utils.randDev(0.50, 0.05)) 
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
  
def generateAPerfectOctagon():
    
  allPointsInShape = None
  
  pointA = Point(BLC_Utils.randDev(0.15, 0.01), BLC_Utils.randDev(0.35, 0.01)) 
  pointB = Point(BLC_Utils.randDev(0.35, 0.01), BLC_Utils.randDev(0.15, 0.01)) 
  pointC = Point(BLC_Utils.randDev(0.65, 0.01), BLC_Utils.randDev(0.15, 0.01)) 
  pointD = Point(BLC_Utils.randDev(0.85, 0.01), BLC_Utils.randDev(0.35, 0.01)) 
  pointE = Point(BLC_Utils.randDev(0.85, 0.01), BLC_Utils.randDev(0.65, 0.01)) 
  pointF = Point(BLC_Utils.randDev(0.65, 0.01), BLC_Utils.randDev(0.85, 0.01)) 
  pointG = Point(BLC_Utils.randDev(0.35, 0.01), BLC_Utils.randDev(0.85, 0.01)) 
  pointH = Point(BLC_Utils.randDev(0.15, 0.01), BLC_Utils.randDev(0.65, 0.01)) 
  
  lineAB = Line(pointA, pointB)
  lineBC = Line(pointB, pointC)
  lineCD = Line(pointC, pointD)
  lineDE = Line(pointD, pointE)
  lineEF = Line(pointE, pointF)
  lineFG = Line(pointF, pointG)
  lineGH = Line(pointG, pointH)
  lineHA = Line(pointH, pointA)
  
  allPointsInShape = [pointA, pointB, pointC, pointD, pointE, pointF, pointG, pointH]
  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-180.0, 180.0))
  
  # Return the BLC
  return BLC.traversePointsToCreateBLC(allPointsInShape)  
  
def generateAPerfectCircle(): # similar to zero MNIST shape
    allPointsInCircle = []

    # Draw the circle
    topLeft = Point(BLC_Utils.randDev(0.45, 0.045), BLC_Utils.randDev(0.225, 0.05))
    bottom = Point(BLC_Utils.randDev(0.5, 0.035), BLC_Utils.randDev(0.775, 0.05))
    topRight = Point(BLC_Utils.randDev(0.55, 0.045), BLC_Utils.randDev(0.225, 0.05))
    Line(topLeft, bottom, peakMagnitude=BLC_Utils.randRange(-1.0, -0.4), peakOffset=BLC_Utils.randRange(-0.25, 0.25))
    Line(bottom, topRight, peakMagnitude=BLC_Utils.randRange(-1.0, -0.4), peakOffset=BLC_Utils.randRange(-0.25, 0.25))
    allPointsInCircle.extend([topLeft, bottom, topRight])

    # Add some random rotation
    BLC_Utils.rotatePointsAroundOrigin(allPointsInCircle, BLC_Utils.randRange(-180.0, 180.0))

    # Create a BLC for the circle
    circleBLC = BLC.traversePointsToCreateBLC(allPointsInCircle)
    
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
        circleBLC.connectedSets.append(slashSet)
    
    return circleBLC

  
# Setup for using multiple processors
if __name__ == '__main__':
  multiprocessing.freeze_support()
  
  # Define the classes
  facade = FACADE([
    FACADE.ClassPropertiesObject('triangle', generateAPerfectTriangle),
    #FACADE.ClassPropertiesObject('square', generateAPerfectSquare),
    FACADE.ClassPropertiesObject('rectangle', generateAPerfectRectangle),
    FACADE.ClassPropertiesObject('hexagon', generateAPerfectHexagon),
    FACADE.ClassPropertiesObject('octagon', generateAPerfectOctagon),
    FACADE.ClassPropertiesObject('circle', generateAPerfectCircle)
  ])
  
  # Now generate the dataset
  facade.generateDataset(1400, 'outputs/polygons')