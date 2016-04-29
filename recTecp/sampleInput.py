import numpy as np

def SamplePositiveInput(curPred, userPool1, newCome, numUsers, numMovies):
    userID = int(newCome[0])
    posiMovieIdx = []
    userPool1 = np.vstack([userPool1, newCome])

    poolRateMat = np.zeros((1, numMovies))

    for i in range (0, userPool1.shape[0]):
        poolRateMat[0, userPool1[i, 1]] = userPool1[i, 2]

    for j in range (0, numMovies):
        if ((poolRateMat[0, j] > 3.5) and (curPred[userID, j] > 3.5)):
            posiMovieIdx = posiMovieIdx = posiMovieIdx + [j]
        elif ((poolRateMat[0, j] <= 3.5 and poolRateMat[0, j] > 0) and ((curPred[userID, j] <= 3.5) and (poolRateMat[0, j] > 0))):
            posiMovieIdx = posiMovieIdx + [j]
        else:
            continue
    return posiMovieIdx


def SampleNegativeInput(curPred, userPool2, SPuIdx, newCome, numUsers, numMovies):
    userID = int(newCome[0])
    negaMovieIdx = []
    userPool2 = np.vstack([userPool2, newCome])

    poolRateMat = np.zeros((1, numMovies))

    for i in range (0, userPool2.shape[0]):
        poolRateMat[0, userPool2[i, 1]] = userPool2[i, 2]

    poolRateMat[0, SPuIdx] = 0

    for j in range (0, numMovies):
        if (((poolRateMat[0, j] < 3.5) and (poolRateMat[0, j] > 0)) and (curPred[userID, j] > 3.5)):
            negaMovieIdx = negaMovieIdx + [j]
        elif ((poolRateMat[0, j] >= 3.5) and ((curPred[userID, j] <= 3.5) and (poolRateMat[0, j] > 0))):
            negaMovieIdx = negaMovieIdx + [j]
        else:
            continue
    return negaMovieIdx
