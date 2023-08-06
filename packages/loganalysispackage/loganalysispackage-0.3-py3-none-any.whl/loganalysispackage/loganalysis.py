import logging

from . import average, datasource, model, prediction
from average import getAverage
from datasource import getData
from model import buildModel
from prediction import getPrediction
import math


class LogAnalysis:

    def traincontroller(self, client, filePath, modelPath):

        try:
            input_data, output_data, timestamp = getData(client, "train", filePath)
            buildModel(input_data, output_data, modelPath)
            return True
        except Exception as e:
            logging.exception(e)
            return False


    def predictcontroller(self, client, filePath, modelPath):

        try:
            input_max, inputs, output_max, outputs, timestamps = getData(client, "predict", filePath)

            predictions = {}

            for key in inputs:
                input = inputs[key]
                output = outputs[key]
                predict = getPrediction(input, output, modelPath)
                predict_list = []
                for i in range(0, len(predict)):
                    predict_list.append(math.floor(predict[i][0] + 0.5))
                predictions[key] = predict_list

            averages = getAverage(predictions, timestamps)

            return averages
        except Exception as e:
            logging.exception(e)
            return None