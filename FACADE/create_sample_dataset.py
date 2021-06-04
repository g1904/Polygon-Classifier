import numpy as np
import random
from src.facade import FACADE
from src.blc import Point, ConnectedSet, BLC
from src.artificial_artist import ArtificialArtist
from src.fluctuating_value import FluctuatingValue


def generateAPerfectTriangle():
  x1 = random.uniform(0.1, 0.4)
  y1 = random.uniform(0.1, 0.4)
  x2 = random.uniform(0.6, 0.9)
  y2 = random.uniform(0.1, 0.4)
  x12Peak = np.min([x1, x2]) + (0.5 * np.abs(x1 - x2))
  y12Peak = np.min([y1, y2]) + (0.5 * np.abs(y1 - y2))
  x3 = random.uniform(0.1, 0.9)
  y3 = random.uniform(0.6, 0.9)
  x23Peak = np.min([x2, x3]) + (0.5 * np.abs(x2 - x3))
  y23Peak = np.min([y2, y3]) + (0.5 * np.abs(y2 - y3))
  x31Peak = np.min([x3, x1]) + (0.5 * np.abs(x3 - x1))
  y31Peak = np.min([y3, y1]) + (0.5 * np.abs(y3 - y1))
  connectedSet = ConnectedSet([Point(x1, y1), Point(x12Peak, y12Peak), Point(x2, y2), Point(x23Peak, y23Peak), Point(x3, y3), Point(x31Peak, y31Peak), Point(x1, y1)])
  return BLC(connectedSets=[connectedSet])


def generateAPerfectSix():
  points = [Point(0.35, 0.6), Point(0.5, 0.5), Point(0.65, 0.6), Point(0.5, 0.7), Point(0.35, 0.6), Point(0.37, 0.37), Point(0.6, 0.3)]
  return BLC(connectedSets=[ConnectedSet(points)])


drawingSettings = ArtificialArtist.DrawingSettings(
  imageWidth=112,
  blobRadiusFluctuatorConstraints=FluctuatingValue.RandomFluctuatorConstraints(
    averageValue_min=3.0, averageValue_max=9.0,
    maxDeviationFromAverage_min=0.1, maxDeviationFromAverage_max=2.0,
    maxChangePercentage_min=0.0001, maxChangePercentage_max=0.0075),
  blobPressureFluctuatorConstraints=FluctuatingValue.RandomFluctuatorConstraints(
    averageValue_min=0.6, averageValue_max=0.9,
    maxDeviationFromAverage_min=0.05, maxDeviationFromAverage_max=0.4,
    maxChangePercentage_min=0.001, maxChangePercentage_max=0.005),
  angleOffsetFluctuatorConstraints=FluctuatingValue.RandomFluctuatorConstraints(
    averageValue_min=0.0, averageValue_max=0.0,
    maxDeviationFromAverage_min=5.0, maxDeviationFromAverage_max=20.0,
    maxChangePercentage_min=0.001, maxChangePercentage_max=0.005),
  maxTexturingNoise=random.uniform(0.1, 0.2),
  slipThreshold=random.uniform(0.0, 0.025),
  maxSlipPercentage=random.uniform(0.05, 0.15),
  finalGaussianNoiseAmount=0.01)

classPropertiesObjects = [
  FACADE.ClassPropertiesObject('six', generateAPerfectSix),
  FACADE.ClassPropertiesObject('triangle', generateAPerfectTriangle)]
facade = FACADE(classPropertiesObjects, 28, drawingSettings)
facade.generateDataset(20, 'outputs/test_dataset')
