import math
import numpy as np
from scipy.stats import norm
from PIL import Image
import random
from src.fluctuating_value import FluctuatingValue
from src.blc import Point, ConnectedSet, BLC

# Controls
BLOB_STEP_SIZE = 0.5
NOISE_MULTIPLE_ON_SLIP = 0.6


# Artificial artists sketch BLCs
class ArtificialArtist:
  # Creates a new, random artist
  @staticmethod
  def newWithRandomParams(drawingSettings):
    return ArtificialArtist(
      imageWidth=drawingSettings.imageWidth,
      blobRadiusFluctuator=FluctuatingValue.newWithRandomParams(
        drawingSettings.blobRadiusFluctuatorConstraints),
      blobPressureFluctuator=FluctuatingValue.newWithRandomParams(
        drawingSettings.blobPressureFluctuatorConstraints),
      angleOffsetFluctuator=FluctuatingValue.newWithRandomParams(
        drawingSettings.angleOffsetFluctuatorConstraints),
      maxTexturingNoise=drawingSettings.maxTexturingNoise,
      slipThreshold=drawingSettings.slipThreshold,
      maxSlipPercentage=drawingSettings.maxSlipPercentage,
      finalGaussianNoiseAmount=drawingSettings.finalGaussianNoiseAmount)
  

  # Define the drawing settings in a way that can be passed around
  class DrawingSettings:
    def __init__(self, imageWidth,
      blobRadiusFluctuatorConstraints,
      blobPressureFluctuatorConstraints,
      angleOffsetFluctuatorConstraints,
      maxTexturingNoise,
      slipThreshold,
      maxSlipPercentage,
      finalGaussianNoiseAmount):
      # Just hang onto everything for a bit
      self.imageWidth = imageWidth
      self.blobRadiusFluctuatorConstraints = blobRadiusFluctuatorConstraints
      self.blobPressureFluctuatorConstraints = blobPressureFluctuatorConstraints
      self.angleOffsetFluctuatorConstraints = angleOffsetFluctuatorConstraints
      self.maxTexturingNoise = maxTexturingNoise
      self.slipThreshold = slipThreshold
      self.maxSlipPercentage = maxSlipPercentage
      self.finalGaussianNoiseAmount = finalGaussianNoiseAmount


  # Crate a new artist
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
    # As we draw, due to randomness, we'll actually end up drawing a slightly different BLC than the given one
    updatedConnectedSets = []

    for setIndex in range(len(perfectBLC.connectedSets)):
      # Draw each line in the connected set
      blcPoints = perfectBLC.connectedSets[setIndex].points
      nextLineStartPoint = blcPoints[0]
      updatedSetPoints = [blcPoints[0]]
      for i in range(1, len(blcPoints), 2):
        startPoint = nextLineStartPoint
        peakPoint = blcPoints[i]
        endPoint = blcPoints[i + 1]
        newPeakAndEndPoint = self.drawAWholeLine(startPoint, peakPoint, endPoint)
        nextLineStartPoint = newPeakAndEndPoint[1]
        updatedSetPoints.extend(newPeakAndEndPoint)
      
      # Record the BLC points, in this set, that we ended up drawing
      updatedConnectedSets.append(ConnectedSet(updatedSetPoints))
      
    # Add some optional, overall noise
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
  def drawAWholeLine(self, startPointPercentage, peakPointPercentage, endPointPercentage):
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
    newPeakX, newPeakY = self.drawHalfOfALine(startX, startY, angleAtStart, diffBetweenStartAndPeakAngles, numberOfStepsFromStartToPeak)

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
    newEndX, newEndY = self.drawHalfOfALine(newPeakX, newPeakY, angleAtPeak, diffBetweenPeakAndEndAngles, numberOfStepsFromPeakToEnd)

    # We want the trainning BLC to stay true to the sketch, not nessecarily the original procedural BLC
    newPeakPointAsPercentage = Point(newPeakX / self.imageWidth, newPeakY / self.imageWidth)
    newEndPointAsPercentage = Point(newEndX / self.imageWidth, newEndY / self.imageWidth)
    return [newPeakPointAsPercentage, newEndPointAsPercentage]

  
  # Draws from the start of a line to its peak, or from the peak of a line to its end
  def drawHalfOfALine(self, startX, startY, startAngle, totalAmountToRotate, numberOfBlobsToPlace):
    blobX = startX
    blobY = startY
    numberOfStepsLeftInSlip = 0
    
    # Drop all the blobs
    for blobIndex in range(numberOfBlobsToPlace):
      # Calculate this blob's properties based on the previous blobs
      blobRadius = self.blobRadiusFluctuator.getNext()
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
