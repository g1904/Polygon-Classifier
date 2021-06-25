import math
from PIL import Image

# Controls
inputImageBasePath = 'data/neat-set-'
outputBasePath = 'NeatSet/'
authorName = ['a', 'b', 'c', 'd', 'e']
indexToSheetName = ['line', 'triangle', 'rectangle', 'diamond', 'hexagon', 'octagon', 'circle' ]
cellCountH = 4
cellCountV = 5
cellMarginRatio = 0
sheetImageWidth = 1382
sheetImageHeight = 1727

for j in range(5):
    for i in range(7):
        # Load and stretch the sheet
        inputImagePath = inputImageBasePath + authorName[j] + '-sheets-' + str(i) + '.jpg'
        outputPathStub = outputBasePath + indexToSheetName[i] + '/neat-set-' + indexToSheetName[i] + "-" + authorName[j] + '-'
        sheet = Image.open(inputImagePath)
        sheet = sheet.resize((sheetImageWidth, sheetImageHeight))
        sheetOutputImageName = outputPathStub + 'sheet.jpg'

        # Calcualte values
        cellWidth = sheetImageWidth / cellCountH
        cellMargin = cellWidth * cellMarginRatio

        # Punch out the individual cells
        for x in range(cellCountH):
            for y in range(cellCountV):
                left = math.floor(x * cellWidth + cellMargin)
                top = math.floor(y * cellWidth + cellMargin)
                right = math.floor((x + 1) * cellWidth - cellMargin)
                bottom = math.floor((y + 1) * cellWidth - cellMargin)

                cellImageName = outputPathStub + str(x + (y * cellCountV)) + '.jpg'
                cellImage = sheet.crop((left, top, right, bottom))
                cellImage = cellImage.convert('L').resize((100,100)) # Convert to black and white
                cellImage.save(cellImageName)