from . import classify
from classify import classify
import numpy as np


def getData(client, action, filePath):

    inputs, outputs, timestamps = classify(client, filePath)

    if action == "train":
        inp = []
        outp = []

        for input in inputs:
            for i in range(0, len(inputs[input])):
                inp.append(inputs[input][i])

        for output in outputs:
            for i in range(0, len(outputs[output])):
                outp.append(outputs[output][i])

        inp = np.array(inp)
        outp = np.array(outp)

        inp_max, inp = normalize(inp)
        outp_max, outp = normalize(outp)

        return inp, outp, timestamps

    if action == "predict":

        inp = {}
        outp = {}
        inp_max = {}
        outp_max = {}

        for input in inputs:
            i = inputs[input]
            i = np.array(i)
            i_max, i = normalize(i)
            inp_max[input] = i_max
            inp[input] = i

        for output in outputs:
            o = outputs[output]
            o = np.array(o)
            o_max, o = normalize(o)
            outp_max[output] = o_max
            outp[output] = o

        return inp_max, inp, outp_max, outp, timestamps


def normalize(data):

    maximums = np.amax(abs(data), axis=0)

    if hasattr(maximums, "__len__"):
        for i in range (0, len(maximums)):
            if maximums[i]==0 :
                maximums[i]=1
        return maximums, data/maximums
    else:
        if maximums == 0:
            maximums = 1
        return maximums, data/maximums