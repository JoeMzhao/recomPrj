import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
import time
import csv
import random
import math
# from pudb import set_trace; set_trace()

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
            num_zeros -= 1 #should not reduce 1 everytime, computed by hand
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

    def __init__(self, counts, alpha, num_factors=10, num_iterations=2,
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
    bound = 1 - poolSize/timestamp
    buff  = random.random
    if buff < bound:
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
    userID = newComep[0]
    posiTrackIdx = []
    userUpool1 = np.vstack([userUpool1, newCome])
    poolFreqMat = np.zeros((1, numTrack))

    for i in range (0, userUpool1.shape[0]):
        poolFreqMat[0, userPool1[i, 1]] += 1

    for j in range (0, numTrack):
        if (poolFreqMat[0, j] >= 1) and (curPred[userID, j] > 1.2 * np.mean(curPred[userID, :])):
            posiTrackIdx = np.vstack([posiTrackIdx, j])
        elif:






# ------------------------------------------------------

if __name__ == '__main__':
    (trainMat, alpha) = load_matrix('music30k.csv', 1001, 298837)
    testMat = load_Nby3('music30k-test!.csv',2000)

    m = ImplicitMF(trainMat, alpha)
    predVects = m.train_model()
    curPred = (predVects.user_vectors).dot((predVects.item_vectors.T))
    print curPred.shape

    # with open('user_item_vectors.csv','w') as f:
    #     f_csv = csv.writer(f)
    #     f_csv.writerows(predVects.user_vectors)
    #     f_csv.writerows('\n\n\n')
    #     f_csv.writerows(predVects.item_vectors)
    #
    # with open('curPred.csv','w') as cur:
    #     cur_csv = csv.writer(cur)
    #     cur_csv.writerows(curPred)

    N = 10 # top N tracks are recommended
    P10K = 10000
    num4test = 0
    num4hit  = 0

    for i in range(0, testMat.shape[0]):
        userID  = testMat[i, 0]
        trackID = testMat[i, 1]
        if trainMat[userID, trackID]>0:
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
    trainSet = load_Nby3('music30k.csv', 30000)
    counter1 = 0
    counter2 = 0
    poolSize = 30000
    numComing = 0
    numUser = 1000
    numTrack = 298837

    for i in range(0, testMat.shape[0]):
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









        #
