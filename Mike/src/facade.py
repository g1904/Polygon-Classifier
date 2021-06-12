import os
import random
import multiprocessing
from src.fluctuating_value import FluctuatingValue
from src.artificial_artist import ArtificialArtist


# Fully Algorithmic and Completely Artificial Drawing Engine
class FACADE:
  def __init__(self, classPropertiesObjects,
  # Default settigs
  exportImageWidth=28,
  drawingSettings=ArtificialArtist.DrawingSettings(
    imageWidth=32,
    blobRadiusFluctuatorConstraints=FluctuatingValue.RandomFluctuatorConstraints(
      averageValue_min=2.0, averageValue_max=12.0,
      maxDeviationFromAverage_min=0.1, maxDeviationFromAverage_max=2.5,
      maxPercentChangePerPercent_min=0.0001, maxPercentChangePerPercent_max=0.0075),
    #blobPressureFluctuatorConstraints=FluctuatingValue.RandomFluctuatorConstraints(
    #  averageValue_min=0.6, averageValue_max=0.95,
    #  maxDeviationFromAverage_min=0.015, maxDeviationFromAverage_max=0.4,
    #  maxPercentChangePerPercent_min=0.00025, maxPercentChangePerPercent_max=0.006),
    blobPressureFluctuatorConstraints=FluctuatingValue.RandomFluctuatorConstraints(
      averageValue_min=0.85, averageValue_max=0.95,
      maxDeviationFromAverage_min=0.015, maxDeviationFromAverage_max=0.05,
      maxPercentChangePerPercent_min=0.00025, maxPercentChangePerPercent_max=0.006),
    angleOffsetFluctuatorConstraints=FluctuatingValue.RandomFluctuatorConstraints(
      averageValue_min=0.0, averageValue_max=0.0,
      maxDeviationFromAverage_min=5.0, maxDeviationFromAverage_max=25.0,
      maxPercentChangePerPercent_min=0.00025, maxPercentChangePerPercent_max=0.006),
    maxTexturingNoise=random.uniform(0.1, 0.2),
    #slipThreshold=random.uniform(0.0, 0.05),
    slipThreshold=0.0,
    maxSlipPercentage=random.uniform(0.025, 0.075),
    finalGaussianNoiseAmount_min=0.0,
    finalGaussianNoiseAmount_max=0.02)):
    # Now apply the given settings
    self.classPropertiesObjects = classPropertiesObjects
    self.exportImageSize = (exportImageWidth, exportImageWidth)
    self.drawingSettings = drawingSettings


  # Contains all the nessecary data that FACADE needs to work with a class
  class ClassPropertiesObject:
    def __init__(self, className, generateAPerfectBLC):
      self.className = className
      self.generateAPerfectBLC = generateAPerfectBLC
  

  # Generates and outputs the requested number of images
  def generateDataset(self, numOfImagesToGenerateForEachClass, outputDirectoryPath):
    # Setup the top level export directories
    FACADE.ensureDirectoryExists(outputDirectoryPath)
    imageOutputDirectoryPath = '%s/images'%(outputDirectoryPath)
    FACADE.ensureDirectoryExists(imageOutputDirectoryPath)
    blcOutputDirectoryPath = '%s/blcs'%(outputDirectoryPath)
    FACADE.ensureDirectoryExists(blcOutputDirectoryPath)

    # Spin up a process for each class
    processes = []
    for classIndex in range(len(self.classPropertiesObjects)):
      classArgs = (
        self.classPropertiesObjects[classIndex],
        numOfImagesToGenerateForEachClass,
        self.drawingSettings,
        self.exportImageSize,
        imageOutputDirectoryPath,
        blcOutputDirectoryPath)
      classProcess = multiprocessing.Process(target=FACADE.generateImagesForClass, args=classArgs)
      processes.append(classProcess)
      classProcess.start()
        
    for process in processes:
        process.join()
    

  # Generate all the images for a given class
  @staticmethod
  def generateImagesForClass(classProps, imageCount, drawingSettings, exportImageSize, imageOutputDirectoryPath, blcOutputDirectoryPath):
    # Get setup to generate and export images for this class
    imageOutputDirectoryPathForClass = '%s/%s'%(imageOutputDirectoryPath, classProps.className)
    FACADE.ensureDirectoryExists(imageOutputDirectoryPathForClass)
    blcOutputDirectoryPathForClass = '%s/%s'%(blcOutputDirectoryPath, classProps.className)
    FACADE.ensureDirectoryExists(blcOutputDirectoryPathForClass)

    # Draw a bunch of images in this class
    for drawingIndex in range(imageCount):
      wasSuccessful = False
      while not wasSuccessful:
        # Generate the inital BLC
        blcCreatioWasSuccessful = True
        perfectBLC = classProps.generateAPerfectBLC()
        # Determine whether or not we've accidentally gone out of bounds
        for connectedSet in perfectBLC.connectedSets:
          for point in connectedSet.points:
            if point.x < 0.025 or point.x > 0.975 or point.y < 0.025 or point.y > 0.975:
              blcCreatioWasSuccessful = False
              break
          if not blcCreatioWasSuccessful:
            break
        if not blcCreatioWasSuccessful:
          break

        # Draw the shape
        artist = ArtificialArtist.newWithRandomParams(drawingSettings)
        wasSuccessful, drawing, blcAfterDrawing = artist.drawBLC(perfectBLC)

        if wasSuccessful:
          # Save the drawing
          outputImagePath = '%s/%s_%d.jpg'%(imageOutputDirectoryPathForClass, classProps.className, drawingIndex)
          outputImage = drawing.resize(exportImageSize)
          outputImage.save(outputImagePath)
          outputBLCPath = '%s/%s_%d.json'%(blcOutputDirectoryPathForClass, classProps.className, drawingIndex)
          blcAfterDrawing.save(outputBLCPath)
  

  # Make a direcotry if it does not exists
  @staticmethod
  def ensureDirectoryExists(directoryPath):
    if (not os.path.exists(directoryPath)):
      os.mkdir(directoryPath)
