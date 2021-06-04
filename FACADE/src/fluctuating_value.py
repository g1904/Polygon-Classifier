import random
import numpy as np

# Manages a single fluctuation value
class FluctuatingValue:
  @staticmethod
  def newWithRandomParams(randomFluctuatorConstraints):
    # "randomFluctuatorConstraints" is to long a name, internally let's use something simpler 
    limits = randomFluctuatorConstraints

    # Get random props within the given ranges
    averageValue = random.uniform(limits.averageValue_min, limits.averageValue_max)
    maxDeviationFromAverage = random.uniform(limits.maxDeviationFromAverage_min, limits.maxDeviationFromAverage_max)
    maxChangePercentage = random.uniform(limits.maxChangePercentage_min, limits.maxChangePercentage_max)

    # Use the random props from above to generate a new fluctuating value
    minValue = averageValue - maxDeviationFromAverage
    maxValue = averageValue + maxDeviationFromAverage
    maxChangeDelta = maxChangePercentage * (maxValue - minValue)
    return FluctuatingValue(minValue, maxValue, maxChangeDelta)
  

  # Define the randomizer constriants in a way that can be passed around
  class RandomFluctuatorConstraints:
    def __init__(self, 
      averageValue_min, averageValue_max,
      maxDeviationFromAverage_min, maxDeviationFromAverage_max,
      maxChangePercentage_min, maxChangePercentage_max):
      # Just hang onto everything for a bit
      self.averageValue_min = averageValue_min
      self.averageValue_max = averageValue_max
      self.maxDeviationFromAverage_min = maxDeviationFromAverage_min
      self.maxDeviationFromAverage_max = maxDeviationFromAverage_max
      self.maxChangePercentage_min = maxChangePercentage_min
      self.maxChangePercentage_max = maxChangePercentage_max
    

  # Create a new fluctuating value
  def __init__(self, minVal, maxVal, maxChangeDelta):
    self.mean = ((maxVal - minVal) / 2.0) + minVal
    self.minVal = minVal
    self.maxVal = maxVal
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
    if (newValue == self.minVal) or (newValue == self.maxVal):
      # If we've run into the bounds, then we don't want to continue accelerating outwards
      self.previousChange = -1.0 * self.previousChange
    else:
      self.previousChange = newValue - self.previousValue
    self.previousValue = newValue

    # Return the requested value
    return newValue


  # Get a positive or negative change delta in the right range
  def getRandomChangeDelta(self):
    return self.maxChangeDelta * random.uniform(-1.0, 1.0)
