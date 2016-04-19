import csv
import numpy as np
from numpy import *
from operator import itemgetter, attrgetter, methodcaller
import random
import ctypes
import time
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve

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

    # alpha = num_zeros / total
    # print 'alpha is %.2f' % alpha
    # counts *= alpha

    counts = sparse.csr_matrix(counts)
    t1 = time.time()
    print 'Finished loading matrix in %f seconds' % (t1 - t0)
    return counts


trainMat = load_matrix('music30k.csv', 1001, 298837)
testMat = load_Nby3('music30k-test!.csv',2000)
curPred = mat(np.random.rand(1000,298837))
N = 5 # top N tracks are recommended
P10K = 20
num4test = 0
num4hit  = 0

for i in range(0, testMat.shape[0]):
	userID  = testMat[i, 0]
	trackID = testMat[i, 1]
	if trainMat[userID, trackID]>0:
		num4test += 1
	else:
	    continue
	userVec = trainMat[userID+1]
	rowVec = userVec[0].todense()
	notListen = np.where(rowVec[0] == 0)[1]
	sampled = random.sample(notListen, 20)
	oneKrate = np.zeros((1, len(sampled)))

	for j in range(0, len(sampled)):
		itemIdx = sampled[j]
		oneKrate[0, j] = curPred[userID-1, itemIdx]

	corresp = curPred[userID-1, trackID]
	thre = np.where(oneKrate > corresp)

	print oneKrate[0]
	print corresp
	print thre

	if len(thre[1]) <= (N-1):
		num4hit += 1
#		if i % 100 == 0:
#			print 'proccesed %i data points...' % i
print num4hit
print num4test

# print trainMat
# print trainMat[1000]
# userVec = trainMat[1]
# print userVec[0].todense()
# rowVec = userVec[0].todense()
# print rowVec
# notListen = np.where(rowVec[0] == 0)[1]
#
# sampled   = random.sample(notListen, 20)
# print sampled
