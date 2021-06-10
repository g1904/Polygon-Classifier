import os
import json
import math
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array


# Variant of the Line class that stores information in a way more condusive to training the parser
class TrainLine:
  @staticmethod
  def fromTwoPointsAndPeak(aX, aY, peakX, peakY, bX, bY):
    # Total Magnitude
    totalMagnitude = math.dist([aX, aY], [bX, bY])

    # Angle
    angle = None
    horizontalVector = bX - aX
    if bY > aY:
      angle = np.arccos(horizontalVector / totalMagnitude)
    else:
      angle = (2.0 * np.pi) - np.arccos(horizontalVector / totalMagnitude)
    
    # Center Point
    centerX = aX - ((aX - bX) / 2.0)
    centerY = aY - ((aY - bY) / 2.0)
    
    # Projection Magnitudes
    magnitudeX = np.abs(np.cos(angle)) * totalMagnitude
    magnitudeY = np.abs(np.sin(angle)) * totalMagnitude
    magnitudeH = np.abs(np.cos(angle + (np.pi / 4.0))) * totalMagnitude

    # Create and return the line
    return TrainLine(centerX, centerY, peakX, peakY, magnitudeX, magnitudeY, magnitudeH)


  # Create a standard TrainLine
  def __init__(self, centerX, centerY, peakX, peakY, magnitudeX, magnitudeY, magnitudeH):
    self.centerX = centerX
    self.centerY = centerY
    self.peakX = peakX
    self.peakY = peakY
    self.magnitudeX = magnitudeX
    self.magnitudeY = magnitudeY
    self.magnitudeH = magnitudeH


  # Calculate the position of the two end-points and the peak of this line. Returns: (a, peak, b)
  def getEndpointsAndPeak(self):
    # Total Magnitude
    totalMagnitude = math.sqrt(math.pow(self.magnitudeX, 2.0) + math.pow(self.magnitudeY, 2.0))

    # Angle
    angle = None
    predictedAngleBasedOnX = np.arccos(self.magnitudeX / totalMagnitude)
    if self.magnitudeH / totalMagnitude <= np.cos(np.pi / 4.0):
      angle = predictedAngleBasedOnX
    else:
      angle = np.pi - predictedAngleBasedOnX
    
    # We don't yet know which x goes with which y
    xMin = self.centerX - (self.magnitudeX / 2.0)
    xMax = self.centerX + (self.magnitudeX / 2.0)
    yMin = self.centerY - (self.magnitudeY / 2.0)
    yMax = self.centerY + (self.magnitudeY / 2.0)

    # Now we can find the points
    pointA = None
    peakPoint = (self.peakX, self.peakY)
    pointB = None
    if angle < (np.pi / 2.0):
      pointA = (xMin, yMin)
      pointB = (xMax, yMax)
    else:
      pointA = (xMin, yMax)
      pointB = (xMax, yMin)
    
    # Now return the key points in this line
    return (pointA, peakPoint, pointB)
    



# Variant of the BLC class that stores information in a way more condusive to training the parser
class TrainBLC:
  @staticmethod
  def fromJson(jsonAsText):
    blcAsJson = json.loads(jsonAsText)
    lines = []

    # Parse all the lines
    for setAsJson in blcAsJson['connectedSets']:
      pointsAsJson = setAsJson['points']
      for startPointIndex in range(0, len(pointsAsJson) - 2, 2):
        startX = pointsAsJson[startPointIndex]['x']
        startY = pointsAsJson[startPointIndex]['y']
        peakX = pointsAsJson[startPointIndex + 1]['x']
        peakY = pointsAsJson[startPointIndex + 1]['y']
        endX = pointsAsJson[startPointIndex + 2]['x']
        endY = pointsAsJson[startPointIndex + 2]['y']

        if startX != endX or startY != endY:
          line = TrainLine.fromTwoPointsAndPeak(startX, startY, peakX, peakY, endX, endY)
          lines.append(line)
          line.getEndpointsAndPeak()
    
    # Now create and return the TrainBLC
    return TrainBLC(lines)

  def __init__(self, lines):
    self.lines = lines




# Loads the images and blcs from a dataset directory 
def loadBLCDatasetFromDirectory(datasetDirectory):
  imageArrays = []
  blcs = []

  # Find all the ifles
  imagesDirectory = datasetDirectory + '/images'
  blcsDirectory = datasetDirectory + '/blcs'
  for directory in os.scandir(imagesDirectory):
    className = directory.name
    if directory.is_dir():
      for imageFile in os.scandir(directory.path):
        # Load the image
        image = load_img(imageFile.path, color_mode="grayscale")
        imageArray = img_to_array(image)
        imageArrays.append(imageArray)

        # Load the BLC
        imageFileNameWithoutExtension = os.path.splitext(imageFile.name)[0]
        blcFilePath = blcsDirectory + '/' + className + '/' + imageFileNameWithoutExtension + '.json'
        print('')
        print(imageFileNameWithoutExtension)
        blc = TrainBLC.fromJson(open(blcFilePath, "r").read())
        blcs.append(blc)
  
  # Return the training data and labels
  return (np.array(imageArrays), blcs)


# Example Use
#loadBLCDatasetFromDirectory('datasets/artificial_polygons')
