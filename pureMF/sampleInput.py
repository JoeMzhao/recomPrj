import numpy as np
import random

def smpPosiInput(curPred, userPool1, userID, numUser, numItem):
    posiItemIdx = []
    poolRateMat = np.zeros((1, numItem))

    for i in xrange (0, userPool1.shape[0]):
        poolRateMat[0, userPool1[i, 1]] = userPool1[i, 2]

    meanScore = np.mean(userPool1[:, 2])

    for j in xrange (0, numItem):
        if ((poolRateMat[0, j] > meanScore) and (curPred[userID, j] >  meanScore)):
            posiItemIdx.append(j)
        elif ((poolRateMat[0, j] <= meanScore and poolRateMat[0, j] > 0) and (curPred[userID, j] <= meanScore and poolRateMat[0, j] > 0)):
            posiItemIdx.append(j)
        else:
            continue

    return posiItemIdx


def smpNegaInput(curPred, userPool2, SPuIdx, userID, numUser, numItem):
    negaItemIdx=[]
    poolRateMat = np.zeros((1, numItem))

    for i in xrange (0, userPool2.shape[0]):
        poolRateMat[0, userPool2[i, 1]] = userPool2[i, 2]

    poolRateMat[0, SPuIdx] = 0
    meanScore = np.mean(userPool2[:, 2])
    for j in range (0, numItem):
        if ((poolRateMat[0, j] < meanScore and poolRateMat[0, j] > 0) and curPred[userID, j] > meanScore):
            negaItemIdx.append(j)
        elif (poolRateMat[0, j] >= meanScore) and (curPred[userID, j] <= meanScore and (poolRateMat[0, j] > 0)):
            negaItemIdx.append(j)
        else:
            continue
    return negaItemIdx
