import math
import numpy as np
from scipy.stats import norm
from PIL import Image
from numpy.lib.type_check import imag
import random
from src.fluctuating_value import FluctuatingValue
#from scipy.stats import multivariate_normal

def placeInkBlob(blobX, blobY, blobRadius, blobPressure, pixels, pixelToBlobDistanceMap):
  for x in range(math.floor(currentX - (currentPenRadius + 1)), math.ceil(currentX + (currentPenRadius + 2))):
    for y in range(math.floor(currentY - (currentPenRadius + 1)), math.ceil(currentY + (currentPenRadius + 2))):
      if (x in range(0, imageWidth)) and (y in range(0, imageWidth)):
        distanceFromPixelToInkBlob = math.dist([x + 0.5, y + 0.5], [currentX, currentY])
        if (distanceFromPixelToInkBlob < currentPenRadius) and (distanceFromPixelToInkBlob < blah[x][y]):
          value = math.floor(255.0 * (1.0 - (currentPenPressure * (1.0 - math.pow(distanceFromPixelToInkBlob / currentPenRadius, 2.0)))))
          noise = math.floor(255.0 * ((random.random() * 2.0) - 1.0) * noiseAmount)
          if slipCount > 0 :
            noise = noise * noiseMutlipleOnSlip
          value += noise
          value = math.floor(np.max([0, value]))
          value = math.floor(np.min([255, value]))
          canvasPixels[x, y] = value
          blah[x][y] = distanceFromPixelToInkBlob

# Control
x1 = 0.1
y1 = 0.25
xPeak = 0.3
yPeak = 0.65
x2 = 0.6
y2 = 0.8
imageWidth = 256
penRadius = FluctuatingValue(3.0, 1.5, 0.15)
penPressure = FluctuatingValue(1.0, 0.6, 0.05)
angleOffset = FluctuatingValue(15, -15, 4)
noiseAmount = 0.15
stepSize = 0.25
slipThreshold = 0.015
noiseMutlipleOnSlip = 0.6
maxSlipPercentage = 0.1

# Create a new canvas
canvas = Image.new('L', (imageWidth, imageWidth), color=255)
canvasPixels = canvas.load()

# Calcualte initial plot stats
startingX = x1 * imageWidth
startingY = y1 * imageWidth
endingX = x2 * imageWidth
endingY = y2 * imageWidth
peakX = xPeak * imageWidth
peakY = yPeak * imageWidth
targetX = peakX
targetY = peakY
#distanceFromStartToEnd = math.dist([startingX, startingY], [peakX, peakY])

# Draw the line
blah = [[math.inf for y in range(imageWidth)] for x in range(imageWidth)]
currentX = startingX
currentY = startingY
slipCount = 0
distanceFromLastCheckpointToTarget = math.dist([startingX, startingY], [peakX, peakY])
angleFromStartToEnd = np.arctan((endingY - startingY) / (endingX - startingX))
angleFromStartToPeak = np.arctan((peakY - startingY) / (peakX - startingX))
angleFromLastCheckpoint = angleFromStartToPeak - (angleFromStartToEnd - angleFromStartToPeak)
print("angleFromStartToEnd: " + str(angleFromStartToEnd))
print("angleFromStartToPeak: " + str(angleFromStartToPeak))
print("angleFromLastCheckpoint: " + str(angleFromLastCheckpoint))
while ((math.dist([currentX, currentY], [endingX, endingY]) > stepSize) and ((np.abs(endingX - startingX) > np.abs(currentX - startingX)) or (np.abs(endingY - startingY) > np.abs(currentY - startingY)))):
  print("Expected Horizontal Distance: " + str(np.abs(endingX - startingX)))
  print("Current Horizontal Distance: " + str(np.abs(currentX - startingX)))
  # If trag
  if targetX == peakX and (np.abs(targetX - startingX) < np.abs(currentX - startingX)) and (np.abs(targetY - startingY) < np.abs(currentY - startingY)):
    targetX = endingX
    targetY = endingY
    distanceFromLastCheckpointToTarget = math.dist([peakX, peakY], [endingX, endingY])
    angleFromLastCheckpoint = angleFromStartToEnd
    print("Hit pivot point!")

  # Get the intital random values
  distanceToTarget = math.dist([currentX, currentY], [targetX, targetY])
  percentOfDistanceDone = 1.0 - (distanceToTarget / distanceFromLastCheckpointToTarget)
  print('percentOfDistanceDone: ' + str(percentOfDistanceDone))
  angleOffsetWeight = 0.0#1.0 - math.pow((2.0 * percentOfDistanceDone) - 1.0, 2.0) + 0.2
  angleToTarget = np.arctan((targetY - currentY) / (targetX - currentX))
  optimalAngle = (percentOfDistanceDone * (angleToTarget - angleFromLastCheckpoint)) + angleFromLastCheckpoint
  currentAngle = optimalAngle + math.radians(angleOffset.getNext() * angleOffsetWeight)
  currentPenRadius = penRadius.getNext()
  currentPenPressure = penPressure.getNext()

  # Calculate slip
  if (slipCount > 0):
    currentPenPressure = currentPenPressure * 0.2
    slipCount -= 1
  elif (random.random() < slipThreshold):
    slipCount = random.random() * maxSlipPercentage * imageWidth

  # Drop this blob
  placeInkBlob()
  
  # Update the position
  currentX = currentX + (stepSize * math.cos(currentAngle))
  currentY = currentY + (stepSize * math.sin(currentAngle))

# Temp
for x in range(math.floor(startingX - 3), math.floor(startingX + 4)):
  for y in range(math.floor(startingY - 3), math.floor(startingY + 4)):
    canvasPixels[x,y] = 0
#for x in range(math.floor(peakX - 2), math.floor(peakX + 3)):
#  for y in range(math.floor(peakY - 2), math.floor(peakY + 3)):
#    canvasPixels[x,y] = 0
for x in range(math.floor(endingX - 3), math.floor(endingX + 4)):
  for y in range(math.floor(endingY - 3), math.floor(endingY + 4)):
    canvasPixels[x,y] = 0
#for x in range(math.floor(currentX - 4), math.floor(currentX + 5)):
#  for y in range(math.floor(currentY - 4), math.floor(currentY + 5)):
#    canvasPixels[x,y] = 0

canvas.show()
canvas.save('outputs/sample-artificial-line.png')