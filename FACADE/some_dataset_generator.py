import multiprocessing
import random
from src.facade import FACADE
from src.blc import Point, Line, BLC, BLC_Utils


def generateAPerfect1():
  allPointsInShape = None
  if random.random() < 0.5:
    pointTop = Point(0.5, BLC_Utils.randRange(0.2, 0.4))
    pointBottom = Point(0.5, BLC_Utils.randRange(0.7, 0.8))
    lineTopBottom = Line(pointTop, pointBottom)
    allPointsInShape = [pointTop, pointBottom]
  else:
    pointTip = Point(0.37, 0.35)
    pointTop = Point(0.5, 0.2)
    pointBottom = Point(0.5, 0.8)
    lineTipTop = Line(pointTip, pointTop)
    lineTopBottom = Line(pointTop, pointBottom)
    allPointsInShape = [pointTip, pointTop, pointBottom]

  BLC_Utils.rotatePointsAroundOrigin(allPointsInShape, BLC_Utils.randRange(-7.0, 7.0))
  return BLC.traversePointsToCreateBLC(allPointsInShape)


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


# Setup for using multiple processors
if __name__ == '__main__':
  multiprocessing.freeze_support()

  # This associates the above function with the class name 'digit_1'
  oneClassProps = FACADE.ClassPropertiesObject('digit_1', generateAPerfect1)
  # This associates the above function with the class name 'triangle'
  traiangleClassProps = FACADE.ClassPropertiesObject('triangle', generateAPerfectTriangle)

  # Create a new FACADE instance
  facade = FACADE([oneClassProps, traiangleClassProps])
  # Now Genrate the dataset
  facade.generateDataset(100, 'outputs/test_dataset_2')