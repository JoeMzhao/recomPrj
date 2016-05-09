import numpy as np
import random
import math
import loadMatrix
import inORnot as io
import whichOut as wo
import sampleInput as sp
import time
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
import copy
# from pudb import set_trace; set_trace()

class ImplicitMF():

    def __init__(self, counts, alpha, num_factors=20, num_iterations=1,
                 reg_param=0.2):
        self.counts = counts
        self.num_users = counts.shape[0]
        self.num_items = counts.shape[1]
        self.num_factors = num_factors
        self.num_iterations = num_iterations
        self.reg_param = reg_param
        self.alpha = alpha

    def train_model(self):
        self.userMat = self.alpha * np.random.normal(size=(self.num_users,
                                                   self.num_factors))
        self.trackMat = self.alpha * np.random.normal(size=(self.num_items,
                                                   self.num_factors))

        for i in xrange(self.num_iterations):
            t0 = time.time()
            print 'Solving for user vectors...'
            self.userMat = self.iteration(True, sparse.csr_matrix(self.trackMat))
            print 'Solving for item vectors...'
            self.trackMat = self.iteration(False, sparse.csr_matrix(self.userMat))
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
                counts_i = self.counts[i]#.toarray()
            else:
                counts_i = self.counts[:, i].T#.toarray()
            CuI = sparse.diags(counts_i, 0)
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


def serverSamplePositiveInput(curPred, userPool1, newCome, numUsers, numTracks):
    SPuIdx = sp.SamplePositiveInput(curPred, userPool1, newCome, numUsers, numTracks)
    return SPuIdx

def serverSampleNegativeInput(curPred, userPool2, SPuIdx, newCome, numUsers, numTracks):
    SNuIdx = sp.SampleNegativeInput(curPred, userPool2, SPuIdx, newCome, numUsers, numTracks)
    return SNuIdx


'''--------------------- >>>> main section <<<< -----------------------------'''

if __name__ == '__main__':
    '''  >>> the none incremental model <<< '''
    numUsers = 1000
    numTracks = 298837
    poolSize = 1230815
    M = 20
    trainAlpha = 5

    trainCountMat = loadMatrix.loadData2matrix('trainSetLF.csv', numUsers, numTracks)
    trainSet = loadMatrix.loadData2Set('trainSetLF.csv', poolSize)
    testSet = loadMatrix.loadData2Set('oneKtestSetLF.csv', 1000)
    auxilaryMat = copy.copy(trainCountMat)

    # vectors = testVectors(numUsers, numTracks, M)
    m = ImplicitMF(trainCountMat, trainAlpha)
    vectors = m.train_model()

    userMat = vectors.userMat
    trackMat = vectors.trackMat
    # userMat = loadMatrix.loadLatentVectors('userVectors.csv', numUsers, M)
    # trackMat = loadMatrix.loadLatentVectors('trackVectors.csv', numTracks, M)

    curPred = np.dot(userMat, trackMat.transpose())

    N = 10
    P10K = 20000
    num4test = 0
    num4hit = 0

    for i in range(0, testSet.shape[0]):
        print '------------ This is %dth testing data point ----------' %i
        userID = int(testSet[i, 0])
        trackID = int(testSet[i, 1])
        if trainCountMat[userID, trackID] > 4:
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

    alpha = 1
    beta = 1
    counter1 = 0
    counter2 = 0
    numIn = 0
    T = 1
    inBlis0 = 0
    regu_para = 0.2
    confiMat = trainAlpha * trainCountMat
    lbd_eye = sparse.eye(M) * regu_para

    for i in range(0, testSet.shape[0]):
        print '------------ This is %dth testing data point ----------' %i
        userID = int(testSet[i, 0])
        trackID = int(testSet[i, 1])
        bufIdx1 = np.where(trainSet[:, 0] == userID)
        userPool1 = trainSet[bufIdx1[0], :]

        if io.inORnot(testSet[i, 2], poolSize):
            print 'In!'
            # confiMat[userID, trackID] += trainAlpha
            # Cui = sparse.diags(confiMat[userID, :], 0)
            # eye = sparse.eye(numTracks)
            # pui = copy.copy(confiMat[userID, :])
            # pui[np.where(pui != 0)] = 1
            # yTy = trackMat.transpose().dot(trackMat)
            # yTCuiy = np.dot(trackMat.transpose() * Cui.tocsc(), trackMat)
            # yTCupu = np.dot(trackMat.transpose() * (Cui + eye), pui.transpose())
            # # print '-----------------<><><><><><><><><>----------------'
            # # print userMat[userID, :]
            # userMat[userID, :] = spsolve(sparse.csr_matrix(yTy + yTCuiy + lbd_eye), sparse.csr_matrix(yTCupu.reshape((M, 1))))
            # # print userMat[userID, :]
            # # print '-----------------<><><><><><><><><>----------------'
            Cii = sparse.diags(confiMat[:, trackID], 0)
            eye = sparse.eye(numUsers)
            pii = copy.copy(confiMat[:, trackID])
            pii[np.where(pii != 0)] = 1
            xTx = userMat.transpose().dot(userMat)
            xTCuix = np.dot(userMat.transpose() * Cii.tocsc(), userMat)
            yTCipi = np.dot(userMat.transpose() * (Cii + eye), pii.transpose())
            trackMat[trackID, :] = spsolve(sparse.csr_matrix(xTx + xTCuix + lbd_eye), sparse.csr_matrix(yTCipi.reshape((M, 1))))

            numIn += 1
            trainCountMat[userID, trackID] += 1
            timeArray = trainSet[:, 2]
            kickIdx = wo.whichOut(timeArray, testSet[i, 2])
            trainSet[kickIdx, :] = testSet[i, :]

            bufIdx2 = np.where(trainSet[:, 0] == userID)
            userPool2 = trainSet[bufIdx2[0], :]

            SPuIdx = serverSamplePositiveInput(curPred, userPool1, testSet[i, :], numUsers, numTracks)
            SNuIdx = serverSampleNegativeInput(curPred, userPool2, SPuIdx, testSet[i, :], numUsers, numTracks)

            print '----->>>>>> length of SPuIdx is %d <<<<<<-----', len(SPuIdx)
            print '----->>>>>> length of SNuIdx is %d <<<<<<-----', len(SNuIdx)

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
                        negaSum = np.sum(trackMat[idx, :], axis = 0)
                        negaAvg = negaSum/len(idx)

                    userMat[userID, :] = userMat[userID, :] + alpha * ita * \
                                        (trackMat[SPuIdx[ii]] - negaAvg) - alpha * beta * \
                                        userMat[userID, :]
                    trackMat[SPuIdx[ii], :] = trackMat[SPuIdx[ii], :] + alpha * ita * \
                                        userMat[userID, :] - alpha * beta * trackMat[SPuIdx[ii], :]


                    for j in range(0, len(SNuIdx)):
                        trackMat[SNuIdx[j], :] = trackMat[SNuIdx[j], :] - alpha * ita *\
                                        userMat[userID, :] - alpha * beta * trackMat[SNuIdx[j], :]

        curPred = np.dot(userMat, trackMat.transpose())

        if auxilaryMat[userID, trackID] > 4:
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

    print '---------------- None incremental results --------------------------'
    print 'number of hits %d' %num4hit
    print 'number of test %d' %num4test

    print '--------------------- incremental results --------------------------'
    print 'number of hits %d' %counter1
    print 'number of test %d' %counter2

    print '--------------------- incomed points -------------------------------'
    print numIn

    print '--------------------- incomed points but length is 0----------------'
    print inBlis0

    print '--------------------- list of parameters ---------------------------'
    print 'M = %d, alpha and beta = %f, T = %d, topN = %d'% (M, alpha, T, N)
    print 'regu_para = %f, confident_alpha = %d'%(0.2, trainAlpha)



