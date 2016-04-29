import csv
import copy
import numpy as np
import scipy.sparse as sparse
import scipy.linalg
from scipy.sparse.linalg import spsolve
from multiprocessing import Process, Queue
import time
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
    total = 0.0
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
            print 'loaded %i counts...' % i
    alpha = num_zeros / total
    print 'alpha %.2f' % alpha
    # counts *= alpha
    counts = sparse.csr_matrix(counts)
    t1 = time.time()
    print 'Finished loading matrix in %f seconds' % (t1 - t0)
    return (counts, alpha)


class ImplicitMF():

    def __init__(self, counts, alpha, num_factors=10, num_iterations=5,
                 reg_param=0.8, num_threads=1):
        self.counts = counts
        self.num_users = counts.shape[0]
        self.num_items = counts.shape[1]
        self.num_factors = num_factors
        self.num_iterations = num_iterations
        self.reg_param = reg_param
        self.num_threads = num_threads
        self.alpha = alpha

    def train_model(self):
        self.user_vectors = self.alpha * np.random.normal(size=(self.num_users,
                                                   self.num_factors))
        self.item_vectors = self.alpha * np.random.normal(size=(self.num_items,
                                                   self.num_factors))

        for i in xrange(self.num_iterations):
            t0 = time.time()

            user_vectors_old = copy.deepcopy(self.user_vectors)
            item_vectors_old = copy.deepcopy(self.item_vectors)

            print 'Solving for user vectors...'
            self.user_vectors = self.iteration(True, sparse.csr_matrix(self.item_vectors))
            print 'Solving for item vectors...'
            self.item_vectors = self.iteration(False, sparse.csr_matrix(self.user_vectors))
            t1 = time.time()
            print 'iteration %i finished in %f seconds' % (i + 1, t1 - t0)
            norm_diff = scipy.linalg.norm(user_vectors_old - self.user_vectors) + scipy.linalg.norm(item_vectors_old - self.item_vectors)
            print 'norm difference:', norm_diff

        return self

    def iteration(self, user, fixed_vecs):
        num_solve = self.num_users if user else self.num_items
        num_fixed = fixed_vecs.shape[0]
        YTY = fixed_vecs.T.dot(fixed_vecs)
        eye = sparse.eye(num_fixed)
        lambda_eye = self.reg_param * sparse.eye(self.num_factors)
        solve_vecs = np.zeros((num_solve, self.num_factors))

        batch_size = int(np.ceil(num_solve * 1. / self.num_threads))
        print 'batch_size per thread is: %d' % batch_size
        idx = 0
        processes = []
        done_queue = Queue()
        while idx < num_solve:
            min_i = idx
            max_i = min(idx + batch_size, num_solve)
            p = Process(target=self.iteration_one_vec,
                        args=(user, YTY, eye, lambda_eye, fixed_vecs, min_i, max_i, done_queue))
            p.start()
            processes.append(p)
            idx += batch_size

        cnt_vecs = 0
        while True:
            is_alive = False
            for p in processes:
                if p.is_alive():
                    is_alive = True
                    break
            if not is_alive and done_queue.empty():
                break
            time.sleep(.1)
            while not done_queue.empty():
                res = done_queue.get()
                i, xu = res
                solve_vecs[i] = xu
                cnt_vecs += 1
        assert cnt_vecs == len(solve_vecs)

        done_queue.close()
        for p in processes:
            p.join()

        print 'All processes completed.'
        return solve_vecs

    def iteration_one_vec(self, user, YTY, eye, lambda_eye, fixed_vecs, min_i, max_i, output):
        t = time.time()
        cnt = 0
        for i in xrange(min_i, max_i):
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
            output.put((i, list(xu)))
            cnt += 1
            if cnt % 1000 == 0:
                print 'Solved %d vecs in %d seconds (one thread)' % (cnt, time.time() - t)
        output.close()
        print 'Process done.'

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
