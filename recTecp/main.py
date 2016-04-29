import numpy as np
import random
import math
import loadMatrix
import inORnot as io
import whichOut as wo
import sampleInput as sp

class testVectors():
    def __init__(self, numUsers, numMovies, M):
        self.userMat = np.random.rand(numUsers, M)
        self.moviMat = np.random.rand(numMovies, M)



if __name__ == '__main__':
    '''  >>> the none incremental model <<< '''
    numUsers = 943
    numMovies = 1682
    poolSize = 95000
    M = 20

    trainRateMat = loadMatrix.loadData2matrix('trainSetML.csv', numUsers, numMovies)
    trainSet = loadMatrix.loadData2Set('trainSetML.csv', poolSize)
    testSet = loadMatrix.loadData2Set('testSetML.csv', 5000)

    vectors = testVectors(numUsers, numMovies, M)
    curPred = np.dot(vectors.userMat, vectors.moviMat.transpose())

    N = 10 # recommend top N movies
    P10K = 200
    num4test = 0
    num4hit = 0

    for i in range(0, testSet.shape[0]):
        if testSet[i, 2] == 5:
            num4test += 1
        else:
            continue
        userID = int(testSet[i, 0])
        movieID = int(testSet[i, 1])

        userArry = trainRateMat[userID, :]
        notListen = np.where(userArry == 0)
        sampled = random.sample(notListen[0], P10K)
        candiRate = np.zeros((1, len(sampled)))
        for j in range(0, len(sampled)):
            bufIdx = sampled[j]
            candiRate[0, j] = curPred[userID, bufIdx]
        corresp = curPred[userID, movieID]
        thre = np.where(candiRate[0] > corresp)

        if (len(thre[0]) <= (N-1)):
            num4hit += 1

    '''  >>> the incremental model <<< '''
    alpha = 0.1
    beta = 0.1

    counter1 = 0
    counter2 = 0
    numIn = 0
    T = 10

    for i in range(0, testSet.shape[0]):
        print '------------ This is %dth testing data point ----------' %i
        userID = testSet[i, 0]
        movieID = testSet[i, 1]
        bufIdx1 = np.where(trainSet[:, 0] == userID)
        userPool1 = trainSet[bufIdx1[0], :]

        if io.inORnot(testSet[i, 3], poolSize):
            numIn += 1
            trainRateMat[userID, movieID] = testSet[i, 2]
            timeArray = trainSet[:, 3]
            kickIdx = wo.whichOut(timeArray, testSet[i, 3])
            trainSet[kickIdx, :] = testSet[i, :]

            bufIdx2 = np.where(trainSet[:, 0] == userID)
            userPool2 = trainSet[bufIdx2[0], :]

            SPuIdx = sp.SamplePositiveInput(curPred, userPool1, testSet[i, :], numUsers, numMovies)
            SNuIdx = sp.SampleNegativeInput(curPred, userPool2, SPuIdx, testSet[i, :], numUsers, numMovies)

            for roud in range(0, T):
                for ii in range(0, len(SPuIdx)):
                    rateHat = trainRateMat[userID, SPuIdx[ii]]
                    rateAvg = np.mean(trainRateMat[userID, SNuIdx[:]])
                    ita = max(0, rateHat - rateAvg)

                    if len(SNuIdx) == 0:
                        negaAvg = np.zeros((1, M))
                    else:
                        idx = SNuIdx[:]
                        negaSum = np.sum(vectors.moviMat[idx, :], axis = 0)
                        negaAvg = negaSum/len(idx)

                    vectors.userMat[userID, :] = vectors.userMat[userID, :] + alpha * ita * \
                                        (vectors.moviMat[SPuIdx[ii]] - negaAvg) - alpha * beta * \
                                        vectors.userMat[userID, :]
                    vectors.moviMat[SPuIdx[ii], :] = vectors.moviMat[SPuIdx[ii], :] + alpha * ita * \
                                        vectors.userMat[userID, :] - alpha * beta * vectors.moviMat[SPuIdx[ii], :]

                    for j in range(0, len(SNuIdx)):
                        vectors.moviMat[SNuIdx[j], :] = vectors.moviMat[SNuIdx[j], :] - alpha * ita *\
                                        vectors.userMat[userID, :] - alpha * beta * vectors.moviMat[SNuIdx[j], :]

        curPred = np.dot(vectors.userMat, vectors.moviMat.transpose())

        if testSet[i, 2] == 5:
            counter1 += 1
            userArry = trainRateMat[userID, :]
            notListen = np.where(userArry == 0)
            sampled = random.sample(notListen[0], P10K)
            candiRate = np.zeros((1, len(sampled)))
            for j in range(0, len(sampled)):
                bufIdx = sampled[j]
                candiRate[0, j] = curPred[userID, bufIdx]
            corresp = curPred[userID, movieID]
            thre = np.where(candiRate[0] > corresp)

            if (len(thre[0]) <= (N-1)):
                counter2 += 1

    print '---------------- None incremental results -------------------------'
    print 'number of hits %d' %num4hit
    print 'number of test %d' %num4test

    print '---------------- Incremental results ------------------------------'
    print 'number of hits %d' %counter2
    print 'number of test %d' %counter1
