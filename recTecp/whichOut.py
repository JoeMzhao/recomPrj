import numpy as np
import math

def whichOut(timeArray, timestamp):
    threArray1 = np.exp(1/(timestamp - timeArray))
    buff = - np.exp(-threArray1)
    threArray2 = 1 - np.exp(buff)
    probArry = np.random.uniform(0, 1, len(timeArray))
    right = threArray2 - probArry
    index = np.where(right == right.max())
    return index[0][0]
