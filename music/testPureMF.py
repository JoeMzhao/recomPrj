import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
import time
import csv
import random

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
        timestamp = float(timestamp)
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
    counts *= alpha
    counts = sparse.csr_matrix(counts)
    t1 = time.time()
    print 'Finished loading matrix in %f seconds' % (t1 - t0)
    return counts

class ImplicitMF():

    def __init__(self, counts, num_factors=10, num_iterations=1,
                 reg_param=0.8):
        self.counts = counts
        self.num_users = counts.shape[0]
        self.num_items = counts.shape[1]
        self.num_factors = num_factors
        self.num_iterations = num_iterations
        self.reg_param = reg_param

    def train_model(self):
        self.user_vectors = np.random.normal(size=(self.num_users,
                                                   self.num_factors))
        self.item_vectors = np.random.normal(size=(self.num_items,
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

# class perforEva():
#     def __init__(self, curPred, testMat):
#         self.

# if __name__ == '__main__':
trainMat = load_matrix('music50k', 1000, 298837)
testMat  = load_Nby3('music50k-test!', 1000)

m = ImplicitMF(trainMat)
predVects = m.train_model()
curPred = (predVects.user_vectors).dot((predVects.item_vectors.T))
print curPred.shape

with open('user_item_vectors.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerows(predVects.user_vectors)
    f_csv.writerows('\n\n\n')
    f_csv.writerows(predVects.item_vectors)

with open('curPred.csv','w') as cur:
    cur_csv = csv.writer(cur)
    cur_csv.writerows(curPred)


N = 5 # top 10 tracks are recommended
P10K = 100
num4test = 0
num4hit  = 0

for i in range(0, testMat.shape[0]):
    userID  = testMat[i, 0]
    trackID = testMat[i, 1]
    if trainMat[userID, trackID]:
        num4test += 1
    else:
        continue

    userVec   = trainMat[i]
    notListen = np.where(userVec == 0)
    sampled   = random.sample(notListen, 20)
    oneKrate  = np.zeros((1, len(sampled)))
    corresp   = curPred[userID, trackID]

    for j in range(0, len(sample)):
        itemIdx = sampled[j]
        oneKrate[j] = curPre[i, itemIdx]

    thre = np.where(oneKrate > corresp)

    if len(thre) <= (N-1):
        num4hit += 1

print num4hit
print num4test
