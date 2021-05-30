import math
import numpy as np
from scipy.stats import norm
from PIL import Image
import random
from src.fluctuating_value import FluctuatingValue

# Controls
BLOB_STEP_SIZE = 0.25
OUTPUT_IMAGE_WIDTH = 256
NOISE_MULTIPLE_ON_SLIP = 0.6


class ArtificialArtist:
  def generateRandomArtist():
    return ArtificialArtist(
      averageBlobRadius=ArtificialArtist.randomFloatInRange(1.25, 5.0),
      maxBlobRadiusDeviation=ArtificialArtist.randomFloatInRange(0.5, 1.0),
      maxBlobRadiusChangePercentage=ArtificialArtist.randomFloatInRange(0.05, 0.15),
      averageBlobPressure=ArtificialArtist.randomFloatInRange(0.7, 0.9),
      maxBlobPressureChangePercentage=ArtificialArtist.randomFloatInRange(0.1, 0.15),
      maxAngleOffsetDeviation=ArtificialArtist.randomFloatInRange(10, 20),
      maxAngleOffsetChangePercentage=ArtificialArtist.randomFloatInRange(0.1, 0.16),
      maxTexturingNoise=ArtificialArtist.randomFloatInRange(0.1, 0.2),
      slipThreshold=ArtificialArtist.randomFloatInRange(0.01, 0.02),
      maxSlipPercentage=ArtificialArtist.randomFloatInRange(0.05, 0.15))

  def __init__(self, averageBlobRadius, maxBlobRadiusDeviation, maxBlobRadiusChangePercentage, averageBlobPressure, maxBlobPressureChangePercentage, maxAngleOffsetDeviation, maxAngleOffsetChangePercentage, maxTexturingNoise, slipThreshold, maxSlipPercentage):
    minBlobRadius = averageBlobRadius - maxBlobRadiusDeviation
    maxBlobRadius = averageBlobRadius + maxBlobRadiusDeviation
    maxBlobRadiusChangeDelta = maxBlobRadiusChangePercentage * (maxBlobRadius - minBlobRadius)
    self.blobRadiusFluctuator = FluctuatingValue(maxBlobRadius, minBlobRadius, maxBlobRadiusChangeDelta)
    minBlobPressure = averageBlobPressure - (1.0 - averageBlobPressure)
    maxBlobPressure = 1.0
    maxBlobPressureChangeDelta = maxBlobPressureChangePercentage * (maxBlobPressure - minBlobPressure)
    self.blobPressureFluctuator = FluctuatingValue(maxBlobPressure, minBlobPressure, maxBlobPressureChangeDelta)
    minAngleOffset = -1.0 * maxAngleOffsetDeviation
    maxAngleOffset = maxAngleOffsetDeviation
    maxAngleOffsetChangeDelta = maxAngleOffsetChangePercentage * (maxAngleOffset - minAngleOffset)
    self.angleOffsetFluctuator = FluctuatingValue(maxAngleOffset, minAngleOffset, maxAngleOffsetChangeDelta)
    self.maxTexturingNoise = maxTexturingNoise
    self.maxSlipPercentage = maxSlipPercentage
    self.slipThreshold = slipThreshold


  # Actually draw a line
  def sketchLine(self, startPointPercentage, peakPointPercentage, endPointPercentage):
    # Create a new canvas
    canvas = Image.new('L', (OUTPUT_IMAGE_WIDTH, OUTPUT_IMAGE_WIDTH), color=255)
    canvasPixels = canvas.load()

    # We get values of 0-1 in for our x's and y's. We'll scale these up to pixel values
    startXAsPercentage, startYAsPercentage = startPointPercentage
    peakXAsPercentage, peakYAsPercentage = peakPointPercentage
    endXAsPercentage, endYAsPercentage = endPointPercentage
    startX = startXAsPercentage * OUTPUT_IMAGE_WIDTH
    startY = startYAsPercentage * OUTPUT_IMAGE_WIDTH
    peakX = peakXAsPercentage * OUTPUT_IMAGE_WIDTH
    peakY = peakYAsPercentage * OUTPUT_IMAGE_WIDTH
    endX = endXAsPercentage * OUTPUT_IMAGE_WIDTH
    endY = endYAsPercentage * OUTPUT_IMAGE_WIDTH

    # Draw the line
    pixelToBlobDistanceMap = [[math.inf for y in range(OUTPUT_IMAGE_WIDTH)] for x in range(OUTPUT_IMAGE_WIDTH)]
    blobX = startX
    blobY = startY
    numberOfStepsLeftInSlip = 0
    newPeakX = None
    newPeakY = None
    angleToNextBlob = None

    # Calculate some constants and some inital values
    angleFromStartToEnd = ArtificialArtist.calculateAngleBasedOnEndpoints(startX, startY, endX, endY)
    angleFromStartToPeak = ArtificialArtist.calculateAngleBasedOnEndpoints(startX, startY, peakX, peakY)
    optimalAngleAtStart = angleFromStartToPeak - (angleFromStartToEnd - angleFromStartToPeak)
    linearDistanceFromStartToPeak = math.dist([startX, startY], [peakX, peakY])
    linearDistanceFromPeakToEnd = math.dist([peakX, peakY], [endX, endY])
    percentageStartToPeakIsBetweenLineAndSemicircle = np.min([np.abs(peakX - startX), np.abs(peakY - startY)]) / np.max([np.abs(peakX - startX), np.abs(peakY - startY)])
    distanceAlongCurveFromStartToPeak = linearDistanceFromStartToPeak * (1.0 + (percentageStartToPeakIsBetweenLineAndSemicircle * 0.11))
    numberOfStepsFromStartToPeak = round(distanceAlongCurveFromStartToPeak / BLOB_STEP_SIZE)

    # Drop all the blobs
    blobIndex = 0
    while (not ArtificialArtist.haveReachedEnd(blobX, blobY, endX, endY) and not ArtificialArtist.havePassedEnd(startX, startY, blobX, blobY, endX, endY)):
      # The first loop we'll use the pre-initialized values from above
      if blobIndex != 0:
        blobX = blobX + (BLOB_STEP_SIZE * np.cos(angleToNextBlob))
        blobY = blobY + (BLOB_STEP_SIZE * np.sin(angleToNextBlob))
      # The peak we draw might end up in a slightly different location than the peak we were given.
      # We'll want to store the new location for future reference.
      if (blobIndex + 1) == numberOfStepsFromStartToPeak:
        newPeakX = blobX
        newPeakY = blobY

      # Calculate this blob's values based on the previous blobs
      blobRadius = self.blobRadiusFluctuator.getNext()
      blobPressure = self.blobPressureFluctuator.getNext()

      # Handle artificial pen slips
      if (numberOfStepsLeftInSlip > 0):
        blobPressure = blobPressure * 0.2
        numberOfStepsLeftInSlip -= 1
      elif (random.random() < self.slipThreshold):
        numberOfStepsLeftInSlip = random.random() * self.maxSlipPercentage * OUTPUT_IMAGE_WIDTH

      # Drop this blob
      ArtificialArtist.placeInkBlob(
        blobX=blobX,
        blobY=blobY,
        blobRadius=blobRadius,
        blobPressure=blobPressure,
        numberOfStepsLeftInSlip=numberOfStepsLeftInSlip,
        maxTexturingNoise=self.maxTexturingNoise,
        canvasPixels=canvasPixels,
        pixelToBlobDistanceMap=pixelToBlobDistanceMap)

      # Although we won't be drawing a perfect line, we'll want to know what the remainning line would look like if it was perfect
      optimalAngle = None
      percentOfCompletedDistanceToNextTarget = None
      if (blobIndex in range(numberOfStepsFromStartToPeak)):
        # For the first half, our optimal angle will linearly shift from the intital angle to the angle at the peak
        percentOfCompletedDistanceToPeak = (float(blobIndex) + 1.0) / float(numberOfStepsFromStartToPeak)
        # The optimal angle is pased on the shortest path
        shortestAngularDistance = ArtificialArtist.calculateShortestDistanceBetweenAngles(angleFromStartToEnd, optimalAngleAtStart)
        optimalAngle = (percentOfCompletedDistanceToPeak * shortestAngularDistance) + optimalAngleAtStart
        percentOfCompletedDistanceToNextTarget = percentOfCompletedDistanceToPeak
      else:
        # For the second half, our optimal angle will linearly shift from the angle at the peak to pointing at the end
        remainningDistanceToEnd = math.dist([blobX, blobY], [endX, endY])
        percentOfCompletedDistanceToEnd = 1.0 - (remainningDistanceToEnd / linearDistanceFromPeakToEnd)
        angleToEnd = ArtificialArtist.calculateAngleBasedOnEndpoints(blobX, blobY, endX, endY)
        shortestAngularDistance = ArtificialArtist.calculateShortestDistanceBetweenAngles(angleToEnd, angleFromStartToEnd)
        optimalAngle = (percentOfCompletedDistanceToEnd * shortestAngularDistance) + angleFromStartToEnd
        percentOfCompletedDistanceToNextTarget = percentOfCompletedDistanceToEnd
      
      # We want our line to be messy in the middle, but still hit the right angle at the peak
      angleOffset = self.angleOffsetFluctuator.getNext()
      angleOffsetWeight = 1.0 - math.pow((2.0 * percentOfCompletedDistanceToNextTarget) - 1.0, 4.0)
      angleToNextBlob = optimalAngle + math.radians(angleOffset * angleOffsetWeight)
      blobIndex += 1

    # We want the trainning BLC to stay true to the sketch, not nessecarily the original procedural BLC.
    # So, if we've missed the mark, update the starting location.
    newEndX = blobX
    newEndY = blobY

    # Temp!
    canvas = canvas.convert('RGB')
    canvasPixels = canvas.load()
    for x in range(math.floor(startX - 3), math.floor(startX + 4)):
      for y in range(math.floor(startY - 3), math.floor(startY + 4)):
        canvasPixels[x, y] = (0, 250, 0)
    for x in range(math.floor(peakX - 2), math.floor(peakX + 3)):
      for y in range(math.floor(peakY - 2), math.floor(peakY + 3)):
        canvasPixels[x, y] = (0, 0, 250)
    for x in range(math.floor(newPeakX - 2), math.floor(newPeakX + 3)):
      for y in range(math.floor(newPeakY - 2), math.floor(newPeakY + 3)):
        canvasPixels[x, y] = (150, 0, 150)
    for x in range(math.floor(endX - 3), math.floor(endX + 4)):
      for y in range(math.floor(endY - 3), math.floor(endY + 4)):
        canvasPixels[x, y] = (250, 0, 0)

    # !!! - Note: This should probably go somewhere else. - !!!
    canvas.show()
    canvas.save('outputs/sample-artificial-line.png')
    return [(newPeakX, newPeakY), (newEndX, newEndY)]


  # Drops an ink blob with the given specifications at the given location on the given canvas
  @staticmethod
  def placeInkBlob(blobX, blobY, blobRadius, blobPressure, numberOfStepsLeftInSlip, maxTexturingNoise, canvasPixels, pixelToBlobDistanceMap):
    # We only need to look at a subset of the pixels in the overall canvas
    minPossiblePixelX = math.floor(blobX - blobRadius)
    maxPossiblePixelX = math.ceil(blobX + blobRadius)
    minPossiblePixelY = math.floor(blobY - blobRadius)
    maxPossiblePixelY = math.ceil(blobY + blobRadius)

    # Go through each possible pixel and determine if and how much to color it.
    for pixelX in range(minPossiblePixelX, maxPossiblePixelX + 1):
      for pixelY in range(minPossiblePixelY, maxPossiblePixelY + 1):
        if (pixelX in range(0, OUTPUT_IMAGE_WIDTH)) and (pixelY in range(0, OUTPUT_IMAGE_WIDTH)):
          distanceToThisPixel = math.dist([pixelX + 0.5, pixelY + 0.5], [blobX, blobY])
          # Only color this pixel if it is within this blob's radius, and no previous blob is already colser to the pixel than this one.
          if (distanceToThisPixel <= blobRadius) and (distanceToThisPixel < pixelToBlobDistanceMap[pixelX][pixelY]):
            pixelColor = math.floor(255.0 * (1.0 - (blobPressure * (1.0 - math.pow(distanceToThisPixel / blobRadius, 2.0)))))

            # For texturing purposes, offset this pixel's color by a random amount
            noiseTexturing = math.floor(255.0 * ((random.random() * 2.0) - 1.0) * maxTexturingNoise)
            if numberOfStepsLeftInSlip > 0:
              noiseTexturing = noiseTexturing * NOISE_MULTIPLE_ON_SLIP
            pixelColor += noiseTexturing
            pixelColor = math.floor(np.max([0, pixelColor]))
            pixelColor = math.floor(np.min([255, pixelColor]))

            # Apply this pixel's color
            canvasPixels[pixelX, pixelY] = pixelColor
            pixelToBlobDistanceMap[pixelX][pixelY] = distanceToThisPixel


  @staticmethod
  def haveReachedEnd(blobX, blobY, endX, endY):
    return math.dist([blobX, blobY], [endX, endY]) < BLOB_STEP_SIZE


  @staticmethod
  def havePassedEnd(startX, startY, blobX, blobY, endX, endY):
    haveHorizontallyPasedEnd = np.abs(blobX - startX) > np.abs(endX - startX)
    haveVerticallyPasedEnd = np.abs(blobY - startY) > np.abs(endY - startY)
    return haveHorizontallyPasedEnd and haveVerticallyPasedEnd


  @staticmethod
  def calculateAngleBasedOnEndpoints(startX, startY, endX, endY):
    magnitude = math.dist([startX, startY], [endX, endY])
    horizontalVector = endX - startX
    if endY > startY:
      return np.arccos(horizontalVector / magnitude)
    else:
      return (2.0 * np.pi) - np.arccos(horizontalVector / magnitude)


  @staticmethod
  def calculateShortestDistanceBetweenAngles(angleA, angleB):
    _2pi = 2.0 * np.pi
    option1 = angleA - angleB
    option2 = ((angleA + np.pi) % _2pi) - ((angleB + np.pi) % _2pi)
    if np.abs(option1) < np.abs(option2):
      return option1
    else:
      return option2


  @staticmethod
  def randomFloatInRange(min, max):
    return min + (random.random() * (max - min))

# Temp!
x1 = None
y1 = None
yPeak = None
xPeak = None
x2 = None
y2 = None
if random.random() > 0.5:
  x1 = 0.125 + (random.random() * 0.25)
  x2 = 0.625 + (random.random() * 0.25)
else:
  x1 = 0.625 + (random.random() * 0.25)
  x2 = 0.125 + (random.random() * 0.25)
if random.random() > 0.5:
  y1 = 0.125 + (random.random() * 0.25)
  y2 = 0.625 + (random.random() * 0.25)
else:
  y1 = 0.625 + (random.random() * 0.25)
  y2 = 0.125 + (random.random() * 0.25)
xPeak = np.min([x1, x2]) + 0.05 + (random.random() * (np.abs(x1 - x2) - 0.1))
yPeak = np.min([y1, y2]) + 0.05 + (random.random() * (np.abs(y1 - y2) - 0.1))

artificialArtist = ArtificialArtist.generateRandomArtist()
artificialArtist.sketchLine((x1, y1), (xPeak, yPeak), (x2, y2))