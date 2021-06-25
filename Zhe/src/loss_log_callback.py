from tensorflow import keras
from src.utils import emptyFile, getPrecentText, plotTrainAndTestAccuracy, plotTrainAndTestLoss
from sklearn.metrics import classification_report, confusion_matrix

# Loosely based on https://www.tensorflow.org/guide/keras/custom_callback
class LossLogCallback(keras.callbacks.Callback):
  def __init__(self, testData, testLabels, lossLogFilePath, lossPlotFilePath, accuracyPlotFilePath, patience=5):
    super(LossLogCallback, self).__init__()
    self.testData = testData
    self.testLabels = testLabels
    self.lossLogFilePath = lossLogFilePath
    self.lossPlotFilePath = lossPlotFilePath
    self.accuracyPlotFilePath = accuracyPlotFilePath
    self.patience = patience
    self.trainningLossHistory = []
    self.testLossHistory = []
    self.trainningAccuracyHistory = []
    self.testAccuracyHistory = []
    self.bestTestEpochIndex = None
    self.bestTestLoss = None
    self.bestWeights = None


  def on_train_begin(self, logs=None):
    # Setup the loss log file
    emptyFile(self.lossLogFilePath)
    self.lossLogFile = open(self.lossLogFilePath, 'a')

    # Use the initial model as a bassline
    (testLoss, testAccuracy) = self.test_model()
    self.log_loss('Initial Test', testLoss, testAccuracy)
    self.bestTestEpochIndex = -1
    self.bestTestLoss = testLoss
    self.bestWeights = self.model.get_weights()


  def on_epoch_end(self, epoch, logs=None):
    # Log the results from this epoch
    self.log_loss('\nEpoch: '+ str(epoch) + '\nTrainning', logs.get('loss'), logs.get('accuracy'))
    self.trainningLossHistory.append(logs.get('loss'))
    self.trainningAccuracyHistory.append(logs.get('accuracy'))
    (testLoss, testAccuracy) = self.test_model()
    self.log_loss('Test', testLoss, testAccuracy)
    self.testLossHistory.append(testLoss)
    self.testAccuracyHistory.append(testAccuracy)

    # If this is our best test yet, then record the model's current state
    if (testLoss < self.bestTestLoss):
      self.bestTestEpochIndex = epoch
      self.bestTestLoss = testLoss
      self.bestWeights = self.model.get_weights()
    # If we've passed the threshold and have run out of patience, then we have probably started overfitting
    elif (self.bestTestEpochIndex + self.patience == epoch):
      self.model.stop_training = True
      self.model.set_weights(self.bestWeights)


  def on_train_end(self, logs=None):
    self.model.set_weights(self.bestWeights)
    plotTrainAndTestLoss(self.trainningLossHistory, self.testLossHistory, self.lossPlotFilePath)
    plotTrainAndTestAccuracy(self.trainningAccuracyHistory, self.testAccuracyHistory, self.accuracyPlotFilePath)
    # Announce the selected weights
    (testLoss, testAccuracy) = self.test_model()
    self.log_loss('\nTrainning finished! Used weights from epoch ' + str(self.bestTestEpochIndex) + '.\nFinal Test', testLoss, testAccuracy)
    self.lossLogFile.close()
  

  # The following are some helper functions to make tracking loss easier

  def test_model(self):
    (testLoss, testAccuracy) = self.model.evaluate(self.testData, self.testLabels, verbose=0)
    return (testLoss, testAccuracy)


  def log_loss(self, label, loss, accuracy):
    #(testLoss, testAccuracy, _, _, _, _) = self.model.evaluate(self.testDataset, verbose=0)
    lossLogLineText = label + ' - Loss: ' + "{:.4f}".format(loss) + ', Accuracy: ' + getPrecentText(accuracy, 1)
    print(lossLogLineText)
    self.lossLogFile.write(lossLogLineText + '\n')
    #return loss