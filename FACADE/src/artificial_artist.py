import math
import numpy as np
from scipy.stats import norm
from PIL import Image
import random
from src.fluctuating_value import FluctuatingValue
from src.blc import BLC_Utils, Point, ConnectedSet, BLC

# Controls
BLOB_STEP_SIZE = 0.5
NOISE_MULTIPLE_ON_SLIP = 0.6


# Artificial artists draw BLCs
class ArtificialArtist:
  # Creates a new, random artist
  @staticmethod
  def newWithRandomParams(drawingSettings):
    return ArtificialArtist(
      imageWidth=drawingSettings.imageWidth,
      blobRadiusFluctuator=FluctuatingValue.newWithRandomParams(
        drawingSettings.blobRadiusFluctuatorConstraints,
        drawingSettings.imageWidth),
      blobPressureFluctuator=FluctuatingValue.newWithRandomParams(
        drawingSettings.blobPressureFluctuatorConstraints,
        drawingSettings.imageWidth),
      angleOffsetFluctuator=FluctuatingValue.newWithRandomParams(
        drawingSettings.angleOffsetFluctuatorConstraints,
        drawingSettings.imageWidth),
      maxTexturingNoise=drawingSettings.maxTexturingNoise,
      slipThreshold=drawingSettings.slipThreshold,
      maxSlipPercentage=drawingSettings.maxSlipPercentage,
      finalGaussianNoiseAmount=random.uniform(drawingSettings.finalGaussianNoiseAmount_min, drawingSettings.finalGaussianNoiseAmount_max))
  

  # Define the drawing settings in a way that can be passed around
  class DrawingSettings:
    def __init__(self, imageWidth,
      blobRadiusFluctuatorConstraints,
      blobPressureFluctuatorConstraints,
      angleOffsetFluctuatorConstraints,
      maxTexturingNoise,
      slipThreshold,
      maxSlipPercentage,
      finalGaussianNoiseAmount_min,
      finalGaussianNoiseAmount_max):
      # Just hang onto everything for a bit
      self.imageWidth = imageWidth
      self.blobRadiusFluctuatorConstraints = blobRadiusFluctuatorConstraints
      self.blobPressureFluctuatorConstraints = blobPressureFluctuatorConstraints
      self.angleOffsetFluctuatorConstraints = angleOffsetFluctuatorConstraints
      self.maxTexturingNoise = maxTexturingNoise
      self.slipThreshold = slipThreshold
      self.maxSlipPercentage = maxSlipPercentage
      self.finalGaussianNoiseAmount_min = finalGaussianNoiseAmount_min
      self.finalGaussianNoiseAmount_max = finalGaussianNoiseAmount_max


  # Create a new artist
  def __init__(self, imageWidth, blobRadiusFluctuator, blobPressureFluctuator, angleOffsetFluctuator, maxTexturingNoise, slipThreshold, maxSlipPercentage, finalGaussianNoiseAmount):
    self.imageWidth = imageWidth
    self.blobRadiusFluctuator = blobRadiusFluctuator
    self.blobPressureFluctuator = blobPressureFluctuator
    self.angleOffsetFluctuator = angleOffsetFluctuator
    self.maxTexturingNoise = maxTexturingNoise
    self.maxSlipPercentage = maxSlipPercentage
    self.slipThreshold = slipThreshold
    self.finalGaussianNoiseAmount = finalGaussianNoiseAmount

    # Create a new canvas
    self.canvas = Image.new('L', (self.imageWidth, self.imageWidth), color=255)
    self.canvasPixels = self.canvas.load()
    self.pixelToBlobDistanceMap = [[math.inf for y in range(self.imageWidth)] for x in range(self.imageWidth)]
  

  # Draw the given BLC
  def drawBLC(self, perfectBLC):
    # Slice some verties, and shift all the points
    slicedAndShiftedBLC = ArtificialArtist.randomlySliceSetsAndShiftPoints(perfectBLC)

    # As we draw, due to randomness, we'll actually end up drawing a slightly different BLC than the given one
    updatedConnectedSets = []

    # Draw each connected set in this BLC
    for setIndex in range(len(slicedAndShiftedBLC.connectedSets)):
      # Draw each line in the connected set
      pointsInSet = slicedAndShiftedBLC.connectedSets[setIndex].points
      nextLineStartPoint = pointsInSet[0]
      updatedSetPoints = [pointsInSet[0]]
      for i in range(1, len(pointsInSet), 2):
        startPoint = nextLineStartPoint
        peakPoint = pointsInSet[i]
        endPoint = pointsInSet[i + 1]
        allowOverAndUnderShooting = (i == (len(pointsInSet) - 2))
        newPeakAndEndPoint = self.drawAWholeLine(startPoint, peakPoint, endPoint, allowOverAndUnderShooting)
        nextLineStartPoint = newPeakAndEndPoint[1]
        updatedSetPoints.extend(newPeakAndEndPoint)
      
      # Record the BLC points, in this set, that we ended up drawing
      updatedConnectedSets.append(ConnectedSet(updatedSetPoints))
      
    # Add some optional, overall Gaussain noise
    gaussianMask = np.random.normal(0, 255, (self.imageWidth, self.imageWidth))
    canvasWeight = 1.0 - self.finalGaussianNoiseAmount
    noiseWeight = self.finalGaussianNoiseAmount
    for x in range(self.imageWidth):
      for y in range(self.imageWidth):
        self.canvasPixels[x, y] = math.floor(np.average([self.canvasPixels[x, y], gaussianMask[x][y]], weights=[canvasWeight, noiseWeight]))
    
    # Return the image, as well as a descritpion of the actual BLC we ended up drawing
    updatedBLC = BLC(updatedConnectedSets)
    return (self.canvas, updatedBLC)


  # Draw a line on the canvas
  def drawAWholeLine(self, startPointPercentage, peakPointPercentage, endPointPercentage, allowOverAndUnderShooting):
    # We get values of 0-1 in for our x's and y's. We'll scale these up to pixel values
    startX = float(startPointPercentage.x) * self.imageWidth
    startY = float(startPointPercentage.y) * self.imageWidth
    peakX = float(peakPointPercentage.x) * self.imageWidth
    peakY = float(peakPointPercentage.y) * self.imageWidth
    endX = float(endPointPercentage.x) * self.imageWidth
    endY = float(endPointPercentage.y) * self.imageWidth

    # Draw the first half of the line
    # Calculate the nessecary angles for the first half of the line
    angleFromStartToEnd = ArtificialArtist.calculateAngleBasedOnEndpoints(startX, startY, endX, endY)
    angleFromStartToPeak = ArtificialArtist.calculateAngleBasedOnEndpoints(startX, startY, peakX, peakY)
    angleFormedByEndStartPeak = ArtificialArtist.getAngleBetween(angleFromStartToEnd, angleFromStartToPeak)
    angleAtStart = (2.0 * angleFormedByEndStartPeak) + angleFromStartToEnd
    angleAtPeak = angleFromStartToEnd
    diffBetweenStartAndPeakAngles = ArtificialArtist.getAngleBetween(angleAtStart, angleAtPeak)
    # clalculate the number of blobs in the first half of the line
    linearDistanceFromStartToPeak = math.dist([startX, startY], [peakX, peakY])
    amountToInflateLinearDistanceToPeak = (math.pow(np.abs(diffBetweenStartAndPeakAngles), 2) / 16.0) + 1.0
    distanceAlongCurveFromStartToPeak = linearDistanceFromStartToPeak * amountToInflateLinearDistanceToPeak
    numberOfStepsFromStartToPeak = round(distanceAlongCurveFromStartToPeak / BLOB_STEP_SIZE)
    # Draw the first half of the line
    newPeakX, newPeakY = self.drawHalfOfALine(startX, startY, angleAtStart, diffBetweenStartAndPeakAngles, numberOfStepsFromStartToPeak, False)

    # Draw the second half of the line
    # Calculate the nessecary angles for the second half of the line
    angleFromPeakToEnd = ArtificialArtist.calculateAngleBasedOnEndpoints(newPeakX, newPeakY, endX, endY)
    diffBetweenPeakAndEndAngles = 2.0 * ArtificialArtist.getAngleBetween(angleAtPeak, angleFromPeakToEnd)
    # clalculate the number of blobs in the second half of the line
    linearDistanceFromPeakToEnd = math.dist([newPeakX, newPeakY], [endX, endY])
    amountToInflateLinearDistanceToEnd = (math.pow(np.abs(diffBetweenPeakAndEndAngles), 2) / 16.0) + 1.0
    distanceAlongCurveFromPeakToEnd = linearDistanceFromPeakToEnd * amountToInflateLinearDistanceToEnd
    numberOfStepsFromPeakToEnd = round(distanceAlongCurveFromPeakToEnd / BLOB_STEP_SIZE)
    # Draw the second half of the line
    newEndX, newEndY = self.drawHalfOfALine(newPeakX, newPeakY, angleAtPeak, diffBetweenPeakAndEndAngles, numberOfStepsFromPeakToEnd, allowOverAndUnderShooting)

    # We want the trainning BLC to stay true to the sketch, not nessecarily the original procedural BLC
    newPeakPointAsPercentage = Point(newPeakX / self.imageWidth, newPeakY / self.imageWidth)
    newEndPointAsPercentage = Point(newEndX / self.imageWidth, newEndY / self.imageWidth)
    return [newPeakPointAsPercentage, newEndPointAsPercentage]

  
  # Draws from the start of a line to its peak, or from the peak of a line to its end
  def drawHalfOfALine(self, startX, startY, startAngle, totalAmountToRotate, numberOfBlobsToPlace, allowOverAndUnderShooting):
    blobX = startX
    blobY = startY
    numberOfStepsLeftInSlip = 0

    # Calculate over/under shooting
    if allowOverAndUnderShooting:
      maxOverShoot = 0.1 * numberOfBlobsToPlace
      overshootAmount = round(BLC_Utils.randRange(-1.5 * maxOverShoot, maxOverShoot))
      numberOfBlobsToPlace += overshootAmount

    
    # Drop all the blobs
    for blobIndex in range(numberOfBlobsToPlace):
      # Calculate this blob's properties based on the previous blobs
      blobRadius = self.imageWidth * (self.blobRadiusFluctuator.getNext() / 100.0)
      blobPressure = self.blobPressureFluctuator.getNext()

      # Handle artificial pen slips
      if (numberOfStepsLeftInSlip > 0):
        blobPressure = blobPressure * 0.2
        numberOfStepsLeftInSlip -= 1
      elif (random.random() < self.slipThreshold):
        numberOfStepsLeftInSlip = random.random() * self.maxSlipPercentage * self.imageWidth

      # Drop this blob
      self.placeInkBlob(
        blobX=blobX,
        blobY=blobY,
        blobRadius=blobRadius,
        blobPressure=blobPressure,
        numberOfStepsLeftInSlip=numberOfStepsLeftInSlip,
        maxTexturingNoise=self.maxTexturingNoise)

      # Only calculate a new x and y if we haven't reached the end of this half of the lline
      if blobIndex + 1 != numberOfBlobsToPlace:
        # Although we won't be drawing a perfect line, we'll want to know what a perfect line would look like
        percentOfWayToEnd = (float(blobIndex) + 1.0) / float(numberOfBlobsToPlace)
        optimalAngleRightNow = (percentOfWayToEnd * totalAmountToRotate) + startAngle
        
        # We want our line to be messy in the middle, but still have the correct angle at certain key points
        angleOffset = math.radians(self.angleOffsetFluctuator.getNext())
        angleOffsetWeight = 1.0 - math.pow((2.0 * percentOfWayToEnd) - 1.0, 4.0)
        angleToNextBlob = optimalAngleRightNow + (angleOffset * angleOffsetWeight)
        blobX = blobX + (BLOB_STEP_SIZE * np.cos(angleToNextBlob))
        blobY = blobY + (BLOB_STEP_SIZE * np.sin(angleToNextBlob))
    
    # Record where we ended up
    return (blobX, blobY)


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
        if (pixelX in range(0, self.imageWidth)) and (pixelY in range(0, self.imageWidth)):
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
  

  # Randomly split some vertices apart, and shift all the points around a little bit 
  @staticmethod
  def randomlySliceSetsAndShiftPoints(perfectBLC):
    initialConnectedSets = perfectBLC.connectedSets
    finalConnectedSets = []

    # Randomly split up some of the existing sets
    for connectedSet in initialConnectedSets:
      numberOfVertices = math.floor((len(connectedSet.points) + 1) / 2)
      chanceOfSplitingAnyVertex = 1.0 / 5.0

      indexOfLastSplit = 0
      for vertexIndex in range(2, len(connectedSet.points) - 2, 2):
        if random.random() <= chanceOfSplitingAnyVertex:
          # Clone and disconnect at the current vertex
          newSet = connectedSet.points[indexOfLastSplit:vertexIndex]
          pointX, pointY = connectedSet.points[vertexIndex].position
          newSet.append(Point(pointX, pointY))
          finalConnectedSets.append(ConnectedSet(newSet))
          indexOfLastSplit = vertexIndex
      newSet = connectedSet.points[indexOfLastSplit:(len(connectedSet.points))]
      finalConnectedSets.append(ConnectedSet(newSet))

    # Randomly reverse some of the sets
    for connectedSet in finalConnectedSets:
      if random.random() < 0.5:
        connectedSet.points.reverse()

    # Randomly shift all the verticies and peaks little bit
    for connectedSet in finalConnectedSets:
      for pointIndex in range(len(connectedSet.points)):
        offsetRange = None
        if pointIndex == 0 or pointIndex == len(connectedSet.points) - 1:
          offsetRange = 0.05
        elif pointIndex % 2 == 1:
          offsetRange = 0.0065
        else:
          offsetRange = 0.0175
        offsetX = BLC_Utils.randRange(-1.0 * offsetRange, offsetRange)
        offsetY = BLC_Utils.randRange(-1.0 * offsetRange, offsetRange)
        connectedSet.points[pointIndex].x += offsetX
        connectedSet.points[pointIndex].y += offsetY

    # Randomly shift the whole shape a bit
    shapeOffsetX = BLC_Utils.randRange(-0.075, 0.075)
    shapeOffsetY = BLC_Utils.randRange(-0.075, 0.075)
    for connectedSet in finalConnectedSets:
      for point in connectedSet.points:
        point.x += shapeOffsetX
        point.y += shapeOffsetY

    # Return a new BLC
    return BLC(finalConnectedSets)


  @staticmethod
  def calculateAngleBasedOnEndpoints(startX, startY, endX, endY):
    magnitude = math.dist([startX, startY], [endX, endY])
    horizontalVector = endX - startX
    if endY > startY:
      return np.arccos(horizontalVector / magnitude)
    else:
      return (2.0 * np.pi) - np.arccos(horizontalVector / magnitude)


  @staticmethod
  def getAngleBetween(source, target):
    a = target - source
    if a > np.pi:
      a -= 2.0 * np.pi
    elif a < -1.0 * np.pi:
      a += 2.0 * np.pi
    return a
