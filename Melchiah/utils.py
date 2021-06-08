from tensorflow.keras.preprocessing.image import load_img, img_to_array, array_to_img
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random as random
import math as math
import copy
from PIL import Image
from os import listdir, mkdir
from os.path import isdir, isfile, join


def emptyFile(filePath):
  fileToEmpty = open(filePath, 'w')
  fileToEmpty.write('')
  fileToEmpty.close()


def getPrecentText(subCount, totalCount):
  return "{:.2f}%".format(100 * (subCount / totalCount))


tempOutputFile = None
def saveModelSummary(model, outputFilePath):
  def writeLineToOutputFile(line):
    tempOutputFile.write(line + '\n')
  emptyFile(outputFilePath)
  tempOutputFile = open(outputFilePath, 'a')
  model.summary(print_fn=writeLineToOutputFile)
  tempOutputFile.close()


def getNoisyVariants(originalImages, directoryPath):
  noisyImages = []
  # Either load from a file, or create new ones
  if (isdir(directoryPath) and isfile(join(directoryPath, 'image_0.jpg'))):
    print('\nUsing saved noisy images from: ' + directoryPath)
    fileNames = [fileName for fileName in listdir(directoryPath) if isfile(join(directoryPath, fileName))]
    for fileName in fileNames:
      filePath = directoryPath + '/' + fileName
      image = img_to_array(load_img(filePath, color_mode="grayscale"))
      noisyImages.append(image)
  else: # If no save images were found, then generate new ones
    #mkdir(directoryPath)
    print('\nAdding noise and saving to: ' + directoryPath)
    imageCount = len(originalImages)
    imageIndex = 0
    # Copy the images so we don't overwrite anything
    copiesOfOriginalImages = []
    for originalImage in originalImages:
      copiesOfOriginalImages.append(copy.deepcopy(originalImage))
    # Add gaussian noise to each image
    for originalImage in copiesOfOriginalImages:
      image = originalImage.reshape((28, 28))
      gaussianMask = np.random.normal(0.0, 1.0, (28, 28))
      for x in range(28):
        for y in range(28):
          image[x, y] = np.average([image[x, y], gaussianMask[x][y]], weights=[1, 1])
      image = image.reshape((28, 28, 1))
      array_to_img(image).save(directoryPath + '/image_' + str(imageIndex) + '.jpg')
      noisyImages.append(image)
      imageIndex += 1
      if (imageIndex % math.floor(imageCount / 20) == 0):
        print('Completed ' + str(imageIndex) + ' of ' + str(imageCount) + ' images.')
  return np.array(noisyImages)


def plotTrainAndTestLoss(trainLoss, testLoss, filePath):
  plt.figure()
  plt.xlabel('epochs')
  plt.ylabel('loss')
  plt.ylim([0, 1])
  plt.plot(trainLoss, color='#FF0000', label='Trainning Data')
  plt.plot(testLoss, color='#0000FF', label='Test Data')
  plt.legend()
  plt.savefig(filePath)


def printSomeAutoencoderSamples(autoencoder, testImages, expectedImages=None, filePath='output/autoencoder_samples.jpg'):
  # Figure out the plot configuration
  subplotRowCount = 2
  if (expectedImages is not None):
    subplotRowCount = 3
  fig, subplots = plt.subplots(subplotRowCount, 4)

  # Print a few images
  for sampleIndex in range(4):
    # Get the input image
    imageIndex = random.randint(0, len(testImages) - 1)
    rawInputImage = testImages[imageIndex]
    printableInputImage = rawInputImage.reshape((28, 28))

    # Get the output image
    rawOutputImage = autoencoder.predict(np.array([rawInputImage]))[0]
    printableOutputImage = rawOutputImage.reshape((28, 28))

    # Add the input and output images to the figure
    subplots[0, sampleIndex].axis('off')
    subplots[0, sampleIndex].title.set_text('Input ' + str(sampleIndex + 1))
    subplots[0, sampleIndex].imshow(printableInputImage, cmap=plt.get_cmap('gray'))
    subplots[1, sampleIndex].axis('off')
    subplots[1, sampleIndex].title.set_text('Output ' + str(sampleIndex + 1))
    subplots[1, sampleIndex].imshow(printableOutputImage, cmap=plt.get_cmap('gray'))
    if (expectedImages is not None):
      printableExpectedImage = expectedImages[imageIndex].reshape((28, 28))
      subplots[2, sampleIndex].axis('off')
      subplots[2, sampleIndex].title.set_text('Expected ' + str(sampleIndex + 1))
      subplots[2, sampleIndex].imshow(printableExpectedImage, cmap=plt.get_cmap('gray'))
  plt.savefig(filePath)


def plotABunchOfEncoderSamplesForEachFashionClass(encode, testImages, testClassLabels, filePath):
  plt.figure()
  colorsByClass = getADiverseSetOfColor(10)
  maxX = 0.1
  maxY = 0.1

  # Sort the test images by class
  testImagesByClass = [[] for _ in range(10)]
  for testImageIndex in range(len(testImages)):
    testImage = testImages[testImageIndex]
    classIndex = testClassLabels[testImageIndex]
    testImagesByClass[classIndex].append(testImage)

  # Pick a few hundered random images from each class
  imagesToPlotByClass = [[] for _ in range(10)]
  for classIndex in range(10):
    imagesInThisClass = testImagesByClass[classIndex]
    numberOfImagesInThisClass = len(imagesInThisClass)
    for _ in range(250):
      imageIndex = random.randint(0, numberOfImagesInThisClass - 1)
      imagesToPlotByClass[classIndex].append(imagesInThisClass[imageIndex])

  # Encode the images
  pointsByClass = encode(np.array(imagesToPlotByClass))
  
  # Plot a bunch of samples for each class
  for classIndex in range(10):
    points = pointsByClass[classIndex]
    pointsX = [point[0] for point in points]
    pointsY = [point[1] for point in points]
    maxX = np.max([maxX, np.max(pointsX)])
    maxY = np.max([maxY, np.max(pointsY)])
    plt.scatter(pointsX, pointsY, color=colorsByClass[classIndex], s=3)

  # Add some extra configuration to the plot
  plt.xlim([0, 0.1 + (maxX * 1.5)]) # Leave some space for the legend
  plt.ylim([0, 0.1 + (maxY * 1.1)])
  print('max x: ' + str(maxX) + ', max y: ' + str(maxY))
  plt.legend(
    handles=[
      mpatches.Patch(color=colorsByClass[0], label='T-shirt/top'),
      mpatches.Patch(color=colorsByClass[1], label='Trouser'),
      mpatches.Patch(color=colorsByClass[2], label='Pullover'),
      mpatches.Patch(color=colorsByClass[3], label='Dress'),
      mpatches.Patch(color=colorsByClass[4], label='Coat'),
      mpatches.Patch(color=colorsByClass[5], label='Sandal'),
      mpatches.Patch(color=colorsByClass[6], label='Shirt'),
      mpatches.Patch(color=colorsByClass[7], label='Sneaker'),
      mpatches.Patch(color=colorsByClass[8], label='Bag'),
      mpatches.Patch(color=colorsByClass[9], label='Ankle boot'),
    ],
    loc='upper right')
  plt.savefig(filePath)


def getADiverseSetOfColor(colorCount):
  BRIGHTNESS = 200
  RED_THRESHOLD = BRIGHTNESS
  GREEN_THRESHOLD = BRIGHTNESS * 2
  BLUE_THRESHOLD = BRIGHTNESS * 3
  COLOR_STEP = (BRIGHTNESS * 3) / colorCount

  # Spread out the colors
  colors = [None for i in range(colorCount)]
  for i in range(colorCount):
    colorAsNumber = math.floor(i * COLOR_STEP)
    if (0 <= colorAsNumber < RED_THRESHOLD):
      colorTuple = (RED_THRESHOLD - colorAsNumber, colorAsNumber, 0)
    elif (RED_THRESHOLD <= colorAsNumber < GREEN_THRESHOLD):
      colorTuple = (0, GREEN_THRESHOLD - colorAsNumber, colorAsNumber - RED_THRESHOLD)
    else:
      colorTuple = (colorAsNumber - GREEN_THRESHOLD, 0, BLUE_THRESHOLD - colorAsNumber)
    # Convert to hexcode
    colors[i] = '#%02x%02x%02x' % colorTuple

  return colors
