import math
import numpy as np
from scipy.stats import norm
from PIL import Image
import random
from src.fluctuating_value import FluctuatingValue

# Controls
BLOB_STEP_SIZE = 0.25
OUTPUT_IMAGE_WIDTH = 112
NOISE_MULTIPLE_ON_SLIP = 0.6


class ArtificialSketchGenerator:
  def createNewGeneratorWithRandomParams():
    return ArtificialSketchGenerator(
      averageBlobRadius=ArtificialSketchGenerator.randomFloatInRange(3.0, 10.0),
      maxBlobRadiusDeviation=ArtificialSketchGenerator.randomFloatInRange(0.5, 1.0),
      maxBlobRadiusChangePercentage=ArtificialSketchGenerator.randomFloatInRange(0.05, 0.15),
      averageBlobPressure=ArtificialSketchGenerator.randomFloatInRange(0.6, 0.9),
      maxBlobPressureChangePercentage=ArtificialSketchGenerator.randomFloatInRange(0.05, 0.12),
      maxAngleOffsetDeviation=ArtificialSketchGenerator.randomFloatInRange(10, 20),
      maxAngleOffsetChangePercentage=ArtificialSketchGenerator.randomFloatInRange(0.1, 0.16),
      maxTexturingNoise=ArtificialSketchGenerator.randomFloatInRange(0.1, 0.2),
      slipThreshold=ArtificialSketchGenerator.randomFloatInRange(0.0, 0.015),
      maxSlipPercentage=ArtificialSketchGenerator.randomFloatInRange(0.05, 0.15))

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

    # Create a new canvas
    self.canvas = Image.new('L', (OUTPUT_IMAGE_WIDTH, OUTPUT_IMAGE_WIDTH), color=255)
    self.canvasPixels = self.canvas.load()
    self.pixelToBlobDistanceMap = [[math.inf for y in range(OUTPUT_IMAGE_WIDTH)] for x in range(OUTPUT_IMAGE_WIDTH)]
  

  # Draw the given BLC
  def sketchBLC(self, initialBLC):
    # Draw each side of a initialBLC
    nextLineStartPoint = initialBLC[0]
    updatedBLC = [initialBLC[0]]
    for i in range(1, len(initialBLC), 2):
      startPoint = nextLineStartPoint
      peakPoint = initialBLC[i]
      endPoint = initialBLC[i + 1]
      newPeakAndEndPoint = self.sketchLine(startPoint, peakPoint, endPoint)
      nextLineStartPoint = newPeakAndEndPoint[1]
      updatedBLC.extend(newPeakAndEndPoint)
    
    # Add some overall noise
    gaussianMask = np.random.normal(0, 255, (OUTPUT_IMAGE_WIDTH, OUTPUT_IMAGE_WIDTH))
    for x in range(OUTPUT_IMAGE_WIDTH):
      for y in range(OUTPUT_IMAGE_WIDTH):
        self.canvasPixels[x, y] = math.floor(np.average([self.canvasPixels[x, y], gaussianMask[x][y]], weights=[5, 1]))
    
    return updatedBLC


  # Draw a line on the canvas
  def sketchLine(self, startPointPercentage, peakPointPercentage, endPointPercentage):
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

    # Setup some loop vars
    blobX = startX
    blobY = startY
    numberOfStepsLeftInSlip = 0
    newPeakX = None
    newPeakY = None
    angleToNextBlob = None

    # Calculate some constants and some inital values
    angleFromStartToEnd = ArtificialSketchGenerator.calculateAngleBasedOnEndpoints(startX, startY, endX, endY)
    angleFromStartToPeak = ArtificialSketchGenerator.calculateAngleBasedOnEndpoints(startX, startY, peakX, peakY)
    optimalAngleAtStart = angleFromStartToPeak - (angleFromStartToEnd - angleFromStartToPeak)
    linearDistanceFromStartToPeak = math.dist([startX, startY], [peakX, peakY])
    linearDistanceFromPeakToEnd = math.dist([peakX, peakY], [endX, endY])
    percentageStartToPeakIsBetweenLineAndSemicircle = np.min([np.abs(peakX - startX), np.abs(peakY - startY)]) / np.max([np.abs(peakX - startX), np.abs(peakY - startY)])
    distanceAlongCurveFromStartToPeak = linearDistanceFromStartToPeak * (1.0 + (percentageStartToPeakIsBetweenLineAndSemicircle * 0.11))
    numberOfStepsFromStartToPeak = round(distanceAlongCurveFromStartToPeak / BLOB_STEP_SIZE)

    # Drop all the blobs
    blobIndex = 0
    while (not ArtificialSketchGenerator.haveReachedEnd(blobX, blobY, endX, endY) and not ArtificialSketchGenerator.havePassedEnd(startX, startY, blobX, blobY, endX, endY)):
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
      self.placeInkBlob(
        blobX=blobX,
        blobY=blobY,
        blobRadius=blobRadius,
        blobPressure=blobPressure,
        numberOfStepsLeftInSlip=numberOfStepsLeftInSlip,
        maxTexturingNoise=self.maxTexturingNoise)

      # Although we won't be drawing a perfect line, we'll want to know what the remainning line would look like if it was perfect
      optimalAngle = None
      percentOfCompletedDistanceToNextTarget = None
      if (blobIndex in range(numberOfStepsFromStartToPeak)):
        # For the first half, our optimal angle will linearly shift from the intital angle to the angle at the peak
        percentOfCompletedDistanceToPeak = (float(blobIndex) + 1.0) / float(numberOfStepsFromStartToPeak)
        # The optimal angle is pased on the shortest path
        shortestAngularDistance = ArtificialSketchGenerator.calculateShortestDistanceBetweenAngles(angleFromStartToEnd, optimalAngleAtStart)
        optimalAngle = (percentOfCompletedDistanceToPeak * shortestAngularDistance) + optimalAngleAtStart
        percentOfCompletedDistanceToNextTarget = percentOfCompletedDistanceToPeak
      else:
        # For the second half, our optimal angle will linearly shift from the angle at the peak to pointing at the end
        remainningDistanceToEnd = math.dist([blobX, blobY], [endX, endY])
        percentOfCompletedDistanceToEnd = 1.0 - (remainningDistanceToEnd / linearDistanceFromPeakToEnd)
        angleToEnd = ArtificialSketchGenerator.calculateAngleBasedOnEndpoints(blobX, blobY, endX, endY)
        shortestAngularDistance = ArtificialSketchGenerator.calculateShortestDistanceBetweenAngles(angleToEnd, angleFromStartToEnd)
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
    tempCanvas = self.canvas.convert('RGB')
    tempCanvasPixels = tempCanvas.load()
    #for x in range(math.floor(startX - 3), math.floor(startX + 4)):
    #  for y in range(math.floor(startY - 3), math.floor(startY + 4)):
    #    self.canvasPixels[x, y] = (0, 250, 0)
    #for x in range(math.floor(peakX - 2), math.floor(peakX + 3)):
    #  for y in range(math.floor(peakY - 2), math.floor(peakY + 3)):
    #    self.canvasPixels[x, y] = (0, 0, 250)
    #for x in range(math.floor(newPeakX - 2), math.floor(newPeakX + 3)):
    #  for y in range(math.floor(newPeakY - 2), math.floor(newPeakY + 3)):
    #    self.canvasPixels[x, y] = (150, 0, 150)
    #for x in range(math.floor(endX - 3), math.floor(endX + 4)):
    #  for y in range(math.floor(endY - 3), math.floor(endY + 4)):
    #    self.canvasPixels[x, y] = (250, 0, 0)

    # !!! - Note: This should probably go somewhere else. - !!!
    #self.canvas.show()
    #self.canvas.save('outputs/sample-artificial-line.png')
    newPeakXPercentage = newPeakX / OUTPUT_IMAGE_WIDTH
    newPeakYPercentage = newPeakY / OUTPUT_IMAGE_WIDTH
    newEndXPercentage = newEndX / OUTPUT_IMAGE_WIDTH
    newEndYPercentage = newEndY / OUTPUT_IMAGE_WIDTH
    return [(newPeakXPercentage, newPeakYPercentage), (newEndXPercentage, newEndYPercentage)]


  # Drops an ink blob with the given specifications at the given location on the given canvas
  def placeInkBlob(self, blobX, blobY, blobRadius, blobPressure, numberOfStepsLeftInSlip, maxTexturingNoise):
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
          if (distanceToThisPixel <= blobRadius) and (distanceToThisPixel < self.pixelToBlobDistanceMap[pixelX][pixelY]):
            pixelColor = math.floor(255.0 * (1.0 - (blobPressure * (1.0 - math.pow(distanceToThisPixel / blobRadius, 2.0)))))

            # For texturing purposes, offset this pixel's color by a random amount
            noiseTexturing = math.floor(255.0 * ((random.random() * 2.0) - 1.0) * maxTexturingNoise)
            if numberOfStepsLeftInSlip > 0:
              noiseTexturing = noiseTexturing * NOISE_MULTIPLE_ON_SLIP
            pixelColor += noiseTexturing
            pixelColor = math.floor(np.max([0, pixelColor]))
            pixelColor = math.floor(np.min([255, pixelColor]))

            # Apply this pixel's color
            self.canvasPixels[pixelX, pixelY] = pixelColor
            self.pixelToBlobDistanceMap[pixelX][pixelY] = distanceToThisPixel


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


for i in range(3):
  # Temp!
  x1 = ArtificialSketchGenerator.randomFloatInRange(0.05, 0.4)
  y1 = ArtificialSketchGenerator.randomFloatInRange(0.0, 0.4)
  x2 = ArtificialSketchGenerator.randomFloatInRange(0.6, 0.95)
  y2 = ArtificialSketchGenerator.randomFloatInRange(0.05, 0.4)
  #x12Peak = np.min([x1, x2]) + 0.05 + (random.random() * (np.abs(x1 - x2) - 0.1))
  x12Peak = np.min([x1, x2]) + (0.5 * np.abs(x1 - x2))
  #y12Peak = np.min([y1, y2]) + 0.05 + (random.random() * (np.abs(y1 - y2) - 0.1))
  y12Peak = np.min([y1, y2]) + (0.5 * np.abs(y1 - y2))
  x3 = ArtificialSketchGenerator.randomFloatInRange(0.05, 0.95)
  y3 = ArtificialSketchGenerator.randomFloatInRange(0.6, 0.95)
  #x23Peak = np.min([x2, x3]) + 0.05 + (random.random() * (np.abs(x2 - x3) - 0.1))
  x23Peak = np.min([x2, x3]) + (0.5 * np.abs(x2 - x3))
  #y23Peak = np.min([y2, y3]) + 0.05 + (random.random() * (np.abs(y2 - y3) - 0.1))
  y23Peak = np.min([y2, y3]) + (0.5 * np.abs(y2 - y3))
  #x31Peak = np.min([x3, x1]) + 0.05 + (random.random() * (np.abs(x3 - x1) - 0.1))
  x31Peak = np.min([x3, x1]) + (0.5 * np.abs(x3 - x1))
  #y31Peak = np.min([y3, y1]) + 0.05 + (random.random() * (np.abs(y3 - y1) - 0.1))
  y31Peak = np.min([y3, y1]) + (0.5 * np.abs(y3 - y1))

  # Sketch the shape
  sketchGenerator = ArtificialSketchGenerator.createNewGeneratorWithRandomParams()
  initialBLC = [(x1, y1), (x12Peak, y12Peak), (x2, y2), (x23Peak, y23Peak), (x3, y3), (x31Peak, y31Peak), (x1, y1) ]
  updatedBLC = sketchGenerator.sketchBLC(initialBLC)
  #print("Updated BLC: " + str(updatedBLC))

  temp = sketchGenerator.canvas.resize((28, 28))
  #temp.show()
  temp.save('outputs/sample-artificial-triangle' + str(i) + '.png')