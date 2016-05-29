import numpy as np
import random

def smpPosiInput(curPred, userPool1, newCome, numUser, numItem):
    userID = int(newCome[0])
    posiItemIdx = []
    userPool1 = np.vstack([userPool1, newCome])

    poolRateMat = np.zeros((1, numItem))

    for i in xrange (0, userPool1.shape[0]):
        poolRateMat[0, userPool1[i, 1]] = userPool1[i, 2]

    for j in xrange (0, numItem):
        if ((poolRateMat[0, j] > 3.5) and (curPred[userID, j] > 3.5)):
            posiItemIdx.append(j)
        elif ((poolRateMat[0, j] <= 3.5 and poolRateMat[0, j] > 0) and (curPred[userID, j] <= 3.5 and poolRateMat[0, j] > 0)):
            posiItemIdx.append(j)
        else:
            continue
    posiItemIdx = random.sample(posiItemIdx, len(posiItemIdx)/8)
    return posiItemIdx


def smpNegaInput(curPred, userPool2, SPuIdx, newCome, numUser, numItem):
    userID = int(newCome[0])
    negaItemIdx = []
    userPool2 = np.vstack([userPool2, newCome])

    poolRateMat = np.zeros((1, numItem))

    for i in xrange (0, userPool2.shape[0]):
        poolRateMat[0, userPool2[i, 1]] = userPool2[i, 2]

    poolRateMat[0, SPuIdx] = 0

    for j in range (0, numItem):
        if ((poolRateMat[0, j] < 3.5 and poolRateMat[0, j] > 0) and curPred[userID, j] > 3.5):
            negaItemIdx.append(j)
        # elif (poolRateMat[0, j] >= 3.5) and (curPred[userID, j] <= 3.5 and (poolRateMat[0, j] > 0)):
        #     negaItemIdx.append(j)
        else:
            continue
    return negaItemIdx
