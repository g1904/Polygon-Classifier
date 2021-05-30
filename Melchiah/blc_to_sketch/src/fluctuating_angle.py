import random
import numpy as np

# Manages a single fluctuation value
class FluctuatingAngle:
  def __init__(self, maxVal, minVal, maxChangeDelta):
    self.mean = (maxVal - minVal) / 2.0 + minVal
    self.maxVal = maxVal
    self.minVal = minVal
    self.maxChangeDelta = maxChangeDelta
    self.previousValue = self.mean
    self.previousChange = self.getRandomChangeDelta()
  

  # Randomly generate the next value
  def getNext(self):
    # Generate the new value
    newChangeDelta = self.getRandomChangeDelta()
    newChange = self.previousChange + newChangeDelta
    newValue = self.previousValue + newChange

    # Clamp the new value
    newValue = np.max([newValue, self.minVal])
    newValue = np.min([newValue, self.maxVal])

    # Update the records
    self.previousValue = newValue
    if (newValue == self.minVal) or (newValue == self.maxVal):
      # If we've run into the bounds, then we don't want to continue accelerating outwards
      self.previousChange = -1.0 * self.previousChange
    else:
      self.previousChange = newValue - self.previousValue

    # Return the requested value
    return newValue


  # Get a positive or negative change delta in the right range
  def getRandomChangeDelta(self):
    randomUnitVector = ((random.random() * 2.0) - 1.0)
    return self.maxChangeDelta * randomUnitVector