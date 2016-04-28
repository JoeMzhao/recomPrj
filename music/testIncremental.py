import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
import time
import csv
import random
import math
#from pudb import set_trace; set_trace()
import copy


def load_Nby3(filename, numRows):
    counts = np.zeros((numRows, 3))
    for i, line in enumerate(open(filename, 'r')):
        user, timestamp, item = line.strip().split(',')
        user = int(user)
        item = int(item)
        timestamp = int(timestamp)
        counts[i, 0] = user
        counts[i, 1] = item
        counts[i, 2] = timestamp
    print 'finish loading test N by 3 matrix'
    return counts

def load_matrix(filename, num_users, num_items):
    t0 = time.time()
    counts = np.zeros((num_users, num_items))
    total = 0.0 #number of none-zero entries
    num_zeros = num_users * num_items
    for i, line in enumerate(open(filename, 'r')):
        user, timestamp, item = line.strip().split(',')
        user = int(user)
        item = int(item)
        timestamp = int(timestamp)
        if user >= num_users:
            continue
        if item >= num_items:
            continue
        if item != 0:
            counts[user, item] = counts[user, item] + 1
            total += 1
            num_zeros -= 1
        if i % 1000 == 0:
            print 'loaded %i data points...' % i
    alpha = num_zeros / total
    print 'alpha is %.2f' % alpha
    # counts *= alpha
    counts = sparse.csr_matrix(counts)
    t1 = time.time()
    print 'Finished loading matrix in %f seconds' % (t1 - t0)
    return (counts, alpha)

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

def inOrnot(timestamp, poolSize):
    bound = 1 - poolSize * 0.9 /timestamp
    buff  = random.random()
    if buff < bound:
        print 'In!'
        return 1
    else:
        return 0

def whichOut(timeArry, timestamp):
    boundArry1 = np.exp(1/(timestamp - timeArry))
    buff = - np.exp( -boundArry1 )
    boundArry2 = 1 - np.exp(buff)
    probArry = np.random.uniform(0, 1, len(timeArry))
    right = boundArry2 - probArry
    index = np.where(right[:] == right.max())[0]
    return index

def SamplePositiveInput(curPred, userUpool1, newCome, numUser, numTrack):
    userID = newCome[0]
    posiTrackIdx = []
    userUpool1 = np.vstack([userUpool1, newCome])
    poolFreqMat = np.zeros((1, numTrack))

    for i in range (0, userUpool1.shape[0]):
        poolFreqMat[0, userUpool1[i, 1]] += 1

    for j in range (0, numTrack):
        if (poolFreqMat[0, j] >= 2) and (curPred[userID, j] > 1.1*np.mean(curPred[userID, :])):
            posiTrackIdx = posiTrackIdx = posiTrackIdx + [j]
        elif (poolFreqMat[0, j] < 2 and poolFreqMat[0, j] >= 1) and (curPred[userID, j] < 0.9*np.mean(curPred[userID, :])):
            posiTrackIdx = posiTrackIdx + [j]
        else:
            continue
    return posiTrackIdx

def SampleNegativeInput(curPred, userUpool2, SPuIdx, newCome, numUser, numTrack):
    userID = newCome[0]
    negaTrackIdx = []
    userUpool2 = np.vstack([userUpool2, newCome])
    poolFreqMat = np.zeros((1, numTrack))

    for i in range (0, userUpool2.shape[0]):
        poolFreqMat[0, userUpool2[i, 1]] += 1

    poolFreqMat[0, SPuIdx] = -1

    for j in range (0, numTrack):
        if (poolFreqMat[0, j] < 2 and poolFreqMat[0, j] >= 1) and (curPred[userID, j] > 1.1*np.mean(curPred[userID, :])):
            negaTrackIdx = negaTrackIdx + [j]
        elif (poolFreqMat[0, j] >= 2) and (curPred[userID, j] < 0.9*np.mean(curPred[userID, :])):
            negaTrackIdx = negaTrackIdx + [j]
        else:
            continue
    return negaTrackIdx

class testInitial():
    def __init__(self):
        self.user_vectors = np.random.rand(1000, 10)
        self.item_vectors = np.random.rand(298837, 10)


# ------------------------------------------------------

if __name__ == '__main__':

    (trainMat, alphaTrain) = load_matrix('fullTrainSet.csv', 1001, 298837)
    testMat = load_Nby3('partialTestSet.csv', 2000)
    auxilaryTrainMat = copy.copy(trainMat)
    # predVects = testInitial()
    m = ImplicitMF(trainMat, 10)
    predVects = m.train_model()
    curPred = (predVects.user_vectors).dot((predVects.item_vectors.T))

    N = 10 # top N tracks are recommended
    P10K = 10000
    num4test = 0
    num4hit  = 0

    for i in range(0, testMat.shape[0]):
        userID  = testMat[i, 0]
        trackID = testMat[i, 1]
        if trainMat[userID, trackID]>3:
            num4test += 1
        else:
            continue

        userVec = trainMat[userID]
        rowVec = userVec[0].todense()
        notListen = np.where(rowVec[0] == 0)[1]
        sampled = random.sample(notListen, P10K)
        oneKrate = np.zeros((1, len(sampled)))

        for j in range(0, len(sampled)):
            itemIdx = sampled[j]
            oneKrate[0, j] = curPred[userID-1, itemIdx]

        corresp = curPred[userID-1, trackID]
        thre = np.where(oneKrate > corresp)

        if len(thre[1]) <= (N-1):
            num4hit += 1
        if i % 100 == 0:
            print 'proccesed %i data points...' % i

    print num4hit
    print num4test
# ------ the incremental section --------------------------
    poolSize = 1230817
    trainSet = load_Nby3('fullTrainSet.csv', poolSize)
    counter1 = 0
    counter2 = 0
    numComing = 0
    numUser = 1000
    numTrack = 298837
    T = 5
    M = 10
    alpha = 3
    beta = 3
    numofZeros = 0


    for i in range(0, testMat.shape[0]):
        print i
        userID = testMat[i, 0]
        trackID = testMat[i, 1]
        correspIdx1 = np.where(trainSet[:, 0] == userID)[0]
        userPool1 = trainSet[correspIdx1, :]

        if inOrnot(testMat[i, 2], poolSize):
            numComing += 1
            trainMat[userID, trackID] = trainMat[userID, trackID]+1
            timeArry = trainSet[:, 2]

            kickIdx = whichOut(timeArry, testMat[i, 2])
            trainSet[kickIdx, :] = testMat[i, :]

            correspIdx2 = np.where(trainSet[:, 0] == userID)[0]
            userPool2 = trainSet[correspIdx2, :]

            SPuIdx = SamplePositiveInput(curPred, userPool1, testMat[i, :],
                                                             numUser, numTrack)
            SNuIdx = SampleNegativeInput(curPred, userPool2, SPuIdx, testMat[i, :],
                                                             numUser, numTrack)

            if len(SPuIdx) == 0:
                print 'In! but the length is 0!!!'
                numofZeros += 1;
            for round in range (0, T):
                for ii in range (0, len(SPuIdx)):
                    countHat = trainMat[userID, SPuIdx[ii]]
                    buffArray = trainMat[userID, SNuIdx[:]]
                    countAvg = np.mean(buffArray.todense())
                    ita = max(0, countHat - countAvg)

                    if  len(SNuIdx) == 0:
                        negaAvg = np.zeros((1, M))
                    else:
                        idx = SNuIdx[:]
                        negaSum = np.sum(predVects.item_vectors[idx, :], axis = 0)
                        negaAvg = negaSum/len(idx)


                    # print predVects.user_vectors[userID, :]

                    # print alpha * beta * predVects.user_vectors[userID, :]
                    # print alpha * ita * (predVects.item_vectors[SPuIdx[ii], :] - negaAvg)

                    predVects.user_vectors[userID, :] += (alpha * ita * (predVects.item_vectors[SPuIdx[ii], :] - negaAvg) - alpha * beta * predVects.user_vectors[userID, :]).reshape(M, )
                    # print predVects.user_vectors[userID, :]

                    predVects.item_vectors[SPuIdx[ii], :] += (alpha * ita * predVects.user_vectors[userID, :] - alpha * beta * predVects.item_vectors[SPuIdx[ii], :]).reshape(M, )

                    for j in range(0, len(SNuIdx)):
                        negaIdx = SNuIdx[j]
                        predVects.item_vectors[negaIdx, :] = predVects.item_vectors[negaIdx, :] - alpha * ita * predVects.user_vectors[userID, :] - alpha * beta * predVects.item_vectors[negaIdx, :]

        curPred = (predVects.user_vectors).dot((predVects.item_vectors.T))

        if auxilaryTrainMat[userID, trackID]>3:
            counter1 += 1
            userVec = trainMat[userID]
            rowVec = userVec[0].todense()
            notListen = np.where(rowVec[0] == 0)[1]
            sampled = random.sample(notListen, P10K)
            oneKrate = np.zeros((1, len(sampled)))

            for j in range(0, len(sampled)):
                itemIdx = sampled[j]
                oneKrate[0, j] = curPred[userID-1, itemIdx]

            corresp = curPred[userID-1, trackID]
            thre = np.where(oneKrate > corresp)

            if len(thre[1]) <= (N-1):
                counter2 += 1

    print '------- incremental results ------------'
    print counter2
    print counter1
    print '------- non-incremental results --------'
    print num4hit
    print num4test
    print '------- number of incoming -------------'
    print numComing
    print '------- number incoming but 0 length ---'
    print numofZeros
    print '------- parameters ---------------------'
    print 'T is %d, alpha and beta are %f' % (T, alpha)


#
