import os
import random
from src.fluctuating_value import FluctuatingValue
from src.artificial_artist import ArtificialArtist


# Fully Algorithmic and Completely Artificial Drawing Engine
class FACADE:
  def __init__(self, classPropertiesObjects,
  # Default settigs
  exportImageWidth=28,
  drawingSettings=ArtificialArtist.DrawingSettings(
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
    slipThreshold=random.uniform(0.005, 0.025),
    maxSlipPercentage=random.uniform(0.05, 0.15),
    finalGaussianNoiseAmount_min=0.0,
    finalGaussianNoiseAmount_max=0.02)):
    # Now apply the given settings
    self.classPropertiesObjects = classPropertiesObjects
    self.exportImageSize = (exportImageWidth, exportImageWidth)
    self.drawingSettings = drawingSettings
  

  # Generates and outputs the requested number of images
  def generateDataset(self, numOfImagesToGenerateForEachClass, outputDirectoryPath):
    # Setup the top level export directories
    FACADE.ensureDirectoryExists(outputDirectoryPath)
    imageOutputDirectoryPath = '%s/images'%(outputDirectoryPath)
    FACADE.ensureDirectoryExists(imageOutputDirectoryPath)
    blcOutputDirectoryPath = '%s/blcs'%(outputDirectoryPath)
    FACADE.ensureDirectoryExists(blcOutputDirectoryPath)

    # Generate the images for this class
    for classIndex in range(len(self.classPropertiesObjects)):
      # Get setup to generate and export images for this class
      classProps = self.classPropertiesObjects[classIndex]
      imageOutputDirectoryPathForClass = '%s/%s'%(imageOutputDirectoryPath, classProps.className)
      FACADE.ensureDirectoryExists(imageOutputDirectoryPathForClass)
      blcOutputDirectoryPathForClass = '%s/%s'%(blcOutputDirectoryPath, classProps.className)
      FACADE.ensureDirectoryExists(blcOutputDirectoryPathForClass)

      # Draw a bunch of images in this class
      for drawingIndex in range(numOfImagesToGenerateForEachClass):
        # Generate the drawing
        perfectBLC = classProps.generateAPerfectBLC()
        artist = ArtificialArtist.newWithRandomParams(self.drawingSettings)
        drawing, blcAfterDrawing = artist.drawBLC(perfectBLC)

        # Save the drawing
        outputImagePath = '%s/%s_%d.jpg'%(imageOutputDirectoryPathForClass, classProps.className, drawingIndex)
        outputImage = drawing.resize(self.exportImageSize)
        outputImage.save(outputImagePath)
        outputBLCPath = '%s/%s_%d.json'%(blcOutputDirectoryPathForClass, classProps.className, drawingIndex)
        blcAfterDrawing.save(outputBLCPath)


  # Contains all the nessecary data that FACADE needs to work with a class
  class ClassPropertiesObject:
    def __init__(self, className, generateAPerfectBLC):
      self.className = className
      self.generateAPerfectBLC = generateAPerfectBLC
  

  # Make a direcotry if it does not exists
  @staticmethod
  def ensureDirectoryExists(directoryPath):
    if (not os.path.exists(directoryPath)):
      os.mkdir(directoryPath)
