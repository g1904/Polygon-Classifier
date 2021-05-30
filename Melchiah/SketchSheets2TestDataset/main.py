import math
from PIL import Image

# Controls
inputImageBasePath = 'inputs/neat-set-'
outputBasePath = 'outputs/NeatSet/neat-set-'
authorName = 'patrick'
indexToSheetName = [ '', 'example', 'line', 'triangle', 'rectangle', 'diamond', 'hexagon', 'octagon', 'circle' ]
cellCountH = 4
cellCountV = 5
offsetHRatio = 1.0 / 14.5
offsetVRatio = 1.0 / 8.75#1.0 / 8.5
cellMarginRatio = 1.0 / 6.0

for i in range(2, 9):
  # Load and stretch the sheet
  inputImagePath = inputImageBasePath + authorName + '-sheets-' + str(i) + '.jpg'
  outputPathStub = outputBasePath + indexToSheetName[i] + "-" + authorName + '-'
  sheet = Image.open(inputImagePath)
  sheedImageWidth, _ = sheet.size
  sheetImageHeight = math.floor((sheedImageWidth * 11.0) / 8.5)
  sheet = sheet.resize((sheedImageWidth, sheetImageHeight))
  sheetOutputImageName = outputPathStub + 'sheet.jpg'
  sheet.save(sheetOutputImageName)

  # Calcualte values
  offsetH = sheedImageWidth * offsetHRatio
  offsetV = sheetImageHeight * offsetVRatio
  cellWidth = (sheedImageWidth - (2.0 * offsetH)) / cellCountH
  cellMargin = cellWidth * cellMarginRatio

  # Punch out the individual cells
  for x in range(cellCountH):
    for y in range(cellCountV):
      left = math.floor(offsetH + (x * cellWidth) + cellMargin)
      top = math.floor(offsetV + (y * cellWidth) + cellMargin)
      right = math.floor(offsetH + ((x + 1) * cellWidth) - cellMargin)
      bottom = math.floor(offsetV + ((y + 1) * cellWidth) - cellMargin)

      cellImageName = outputPathStub + str(x + (y * cellCountV)) + '.jpg'
      cellImage = sheet.crop((left, top, right, bottom))
      cellImage = cellImage.convert('L') # Convert to black and white
      cellImage.save(cellImageName)
