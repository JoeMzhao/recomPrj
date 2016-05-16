import numpy as np
import scipy.io
import nimfa
import loadMatrix
import random
import inORnot as io
import whichOut as wo
import sampleInput as sp

''' the movieLens 100k data set contains 943 users and 1682 movies '''

if __name__ == '__main__':
    mat = scipy.io.loadmat('movielens100k.mat')
    V = mat['ratings']
    lsnmf = nimfa.Lsnmf(V, seed="random_vcol", rank=20, max_iter=12, sub_iter=10,
                    inner_sub_iter=10, beta=0.1)
    lsnmf_fit = lsnmf()

    userMat = lsnmf_fit.coef().todense().T
    moviMat = lsnmf_fit.basis().todense()

    print '<><><><><>--- latent matrices shapes ---<><><><><><><>'
    print userMat.shape
    print moviMat.shape
    print '<><><><><>------------------------------<><><><><><><>'

    curPred = np.dot(userMat, moviMat.T)
    numUsers = 943
    numMovies = 1682
    poolSize = 95000
    M = 20

    trainRateMat = loadMatrix.loadData2matrix('trainSetML.csv', numUsers, numMovies)
    trainSet = loadMatrix.loadData2Set('trainSetML.csv', poolSize)
    testSet = loadMatrix.loadData2Set('testSetML.csv', 5000)

    N = 10 # recommend top N movies
    P10K = 200
    num4test = 0
    num4hit = 0

    for i in range(0, testSet.shape[0]):
        if i%1000 == 0:
            print i
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
    print ' -------------- >>> results list <<< -------------'
    print num4hit
    print num4test


    '''  >>> the incremental model <<< '''
    alpha = 1
    beta = 1

    counter1 = 0
    counter2 = 0
    numIn = 0
    T = 3

    for i in range(0, testSet.shape[0]):
        if i%1000 == 0:
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
                        negaSum = np.sum(moviMat[idx, :], axis = 0)
                        negaAvg = negaSum/len(idx)

                    #print vectors.userMat[userID, :]
                    userMat[userID, :] = userMat[userID, :] + alpha * ita * \
                                        (moviMat[SPuIdx[ii]] - negaAvg) - alpha * beta * \
                                        userMat[userID, :]
                    moviMat[SPuIdx[ii], :] = moviMat[SPuIdx[ii], :] + alpha * ita * \
                                        userMat[userID, :] - alpha * beta * moviMat[SPuIdx[ii], :]

                    for j in range(0, len(SNuIdx)):
                        moviMat[SNuIdx[j], :] = moviMat[SNuIdx[j], :] - alpha * ita *\
                                        userMat[userID, :] - alpha * beta * moviMat[SNuIdx[j], :]

        curPred = np.dot(userMat, moviMat.T)

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
            # print 'the length of thre is %d, corresp is %f' %(len(thre[0]), corresp)

            if (len(thre[0]) <= (N-1)):
                counter2 += 1

    print '---------------- None incremental results -------------------------'
    print 'number of hits %d' %num4hit
    print 'number of test %d' %num4test

    print '---------------- Incremental results ------------------------------'
    print 'number of hits %d' %counter2
    print 'number of test %d' %counter1
    print 'number of incoming points in testset %d' %numIn
