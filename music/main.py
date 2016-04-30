import numpy as np
import random
import math
import loadMatrix
import inORnot as io
import whichOut as wo
import sampleInput as sp

class ImplicitMF():

    def __init__(self, counts, alpha, num_factors=10, num_iterations=1,
                 reg_param=0.8):
        self.counts = counts
        self.num_users = counts.shape[0]
        self.num_items = counts.shape[1]
        self.num_factors = num_factors
        self.num_iterations = num_iterations
        self.reg_param = reg_param
        self.alpha = alpha

    def train_model(self):
        self.user_vectors = self.alpha * np.random.normal(size=(self.num_users,
                                                   self.num_factors))
        self.item_vectors = self.alpha * np.random.normal(size=(self.num_items,
                                                   self.num_factors))

        for i in xrange(self.num_iterations):
            t0 = time.time()
            print 'Solving for user vectors...'
            self.user_vectors = self.iteration(True, sparse.csr_matrix(self.item_vectors))
            print 'Solving for item vectors...'
            self.item_vectors = self.iteration(False, sparse.csr_matrix(self.user_vectors))
            t1 = time.time()
            print 'iteration %i finished in %f seconds' % (i + 1, t1 - t0)

        return self

    def iteration(self, user, fixed_vecs):
        num_solve = self.num_users if user else self.num_items
        num_fixed = fixed_vecs.shape[0]
        YTY = fixed_vecs.T.dot(fixed_vecs)
        eye = sparse.eye(num_fixed, num_fixed)
        lambda_eye = self.reg_param * sparse.eye(self.num_factors)
        solve_vecs = np.zeros((num_solve, self.num_factors))

        t = time.time()
        for i in xrange(num_solve):
            if user:
                counts_i = self.counts[i].toarray()
            else:
                counts_i = self.counts[:, i].T.toarray()
            CuI = sparse.diags(counts_i, [0])
            pu = counts_i.copy()
            pu[np.where(pu != 0)] = 1.0
            YTCuIY = fixed_vecs.T.dot(CuI).dot(fixed_vecs)
            YTCupu = fixed_vecs.T.dot(CuI + eye).dot(sparse.csr_matrix(pu).T)
            xu = spsolve(YTY + YTCuIY + lambda_eye, YTCupu)
            solve_vecs[i] = xu
            if i % 500 == 0:
                 print 'Solved %i vecs in %d seconds' % (i, time.time() - t)
            t = time.time()

        return solve_vecs

class testVectors():
    def __init__(self, numUsers, numTracks, M):
        self.userMat = np.random.rand(numUsers, M)
        self.trackMat = np.random.rand(numTracks, M)

if __name__ == '__main__':
    '''  >>> the none incremental model <<< '''
    numUsers = 1000
    numTracks = 298837
    poolSize = 1230815
    M = 20

    trainCountMat = loadMatrix.loadData2matrix('trainSetLF.csv', numUsers, numTracks)
    trainSet = loadMatrix.loadData2Set('trainSetLF.csv', poolSize)
    testSet = loadMatrix.loadData2Set('oneKtestSetLF.csv', 1000)

    # vectors = testVectors(numUsers, numTracks, M)
    m = ImplicitMF(trainCountMat, 10)
    vectors = m.train_model()

    curPred = np.dot(vectors.userMat, vectors.trackMat.transpose())

    N = 10
    P10K = 200
    num4test = 0
    num4hit = 0

    for i in range(0, testSet.shape[0]):
        print '------------ This is %dth testing data point ----------' %i
        userID = int(testSet[i, 0])
        trackID = int(testSet[i, 1])
        if trainCountMat[userID, trackID] >= 3:
            num4test += 1
        else:
            continue

        userArry = trainCountMat[userID, :]
        notListen = np.where(userArry == 0)
        sampled = random.sample(notListen[0], P10K)
        candiCount = np.zeros((1, len(sampled)))
        for j in range(0, len(sampled)):
            bufIdx = sampled[j]
            candiCount[0, j] = curPred[userID, bufIdx]
        corresp = curPred[userID, trackID]
        thre = np.where(candiCount[0] > corresp)
        if (len(thre[0]) <= (N-1)):
            num4hit += 1

    # print '---------------- None incremental results -------------------------'
    # print 'number of hits %d' %num4hit
    # print 'number of test %d' %num4test
    '''  >>> the incremental model <<< '''

    alpha = 0.1
    beta = 0.1
    counter1 = 0
    counter2 = 0
    numIn = 0
    T = 10
    inBlis0 = 0

    for i in range(0, testSet.shape[0]):
        print '------------ This is %dth testing data point ----------' %i
        userID = int(testSet[i, 0])
        trackID = int(testSet[i, 1])
        bufIdx1 = np.where(trainSet[:, 0] == userID)
        userPool1 = trainSet[bufIdx1[0], :]

        if io.inORnot(testSet[i, 2], poolSize):
            numIn += 1
            trainCountMat[userID, trackID] += 1
            timeArray = trainSet[:, 2]
            kickIdx = wo.whichOut(timeArray, testSet[i, 2])
            trainSet[kickIdx, :] = testSet[i, :]

            bufIdx2 = np.where(trainSet[:, 0] == userID)
            userPool2 = trainSet[bufIdx2[0], :]

            SPuIdx = sp.SamplePositiveInput(curPred, userPool1, testSet[i, :], numUsers, numTracks)
            SNuIdx = sp.SampleNegativeInput(curPred, userPool2, SPuIdx, testSet[i, :], numUsers, numTracks)

            if len(SPuIdx) == 0:
                inBlis0 += 1

            for roud in range(0, T):
                for ii in range(0, len(SPuIdx)):
                    countHat = trainCountMat[userID, SPuIdx[ii]]
                    countAvg = np.mean(trainCountMat[userID, SNuIdx[:]])
                    ita = max(0, countHat - countAvg)

                    if len(SNuIdx) == 0:
                        negaAvg = np.zeros((1, M))
                    else:
                        idx = SNuIdx[:]
                        negaSum = np.sum(vectors.trackMat[idx, :], axis = 0)
                        negaAvg = negaSum/len(idx)

                    vectors.userMat[userID, :] = vectors.userMat[userID, :] + alpha * ita * \
                                        (vectors.trackMat[SPuIdx[ii]] - negaAvg) - alpha * beta * \
                                        vectors.userMat[userID, :]
                    vectors.trackMat[SPuIdx[ii], :] = vectors.trackMat[SPuIdx[ii], :] + alpha * ita * \
                                        vectors.userMat[userID, :] - alpha * beta * vectors.trackMat[SPuIdx[ii], :]

                    for j in range(0, len(SNuIdx)):
                        vectors.trackMat[SNuIdx[j], :] = vectors.trackMat[SNuIdx[j], :] - alpha * ita *\
                                        vectors.userMat[userID, :] - alpha * beta * vectors.trackMat[SNuIdx[j], :]

        curPred = np.dot(vectors.userMat, vectors.trackMat.transpose())

        if trainCountMat[userID, trackID] >= 3:
            counter2 += 1
            userArry = trainCountMat[userID, :]
            notListen = np.where(userArry == 0)
            sampled = random.sample(notListen[0], P10K)
            candiCount = np.zeros((1, len(sampled)))
            for j in range(0, len(sampled)):
                bufIdx = sampled[j]
                candiCount[0, j] = curPred[userID, bufIdx]
            corresp = curPred[userID, trackID]
            thre = np.where(candiCount[0] > corresp)
            if (len(thre[0]) <= (N-1)):
                counter1 += 1

    print '---------------- None incremental results -------------------------'
    print 'number of hits %d' %num4hit
    print 'number of test %d' %num4test

    print '--------------------- incremental results --------------------------'
    print 'number of hits %d' %counter1
    print 'number of test %d' %counter2

    print '--------------------- incomed points -------------------------------'
    print numIn

    print '--------------------- incomed points but length is 0----------------'
    print inBlis0






















#















        #
