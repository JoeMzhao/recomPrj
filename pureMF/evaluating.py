import numpy as np
import math
import time
import random

def computeRMSE(trainSet, userMat, itemMat):
	e = 0
	curPred = np.dot(userMat, itemMat.T)
	for i in xrange(0, trainSet.shape[0]):
		userID = trainSet[i, 0]
		itemID = trainSet[i, 1]
		actualRate = trainSet[i, 2]
		e = e + (curPred[userID, itemID] - actualRate)**2

	RMSE = math.sqrt(2 * e/trainSet.shape[0])
	return RMSE

def computeMAE(testSet, curPred):
	e = 0
	for i in xrange(0, testSet.shape[0]):
		userID = testSet[i, 0]
		itemID = testSet[i, 1]
		actualRate = testSet[i, 2]
		e = e + np.absolute(actualRate - curPred[userID, itemID])

	e = e/testSet.shape[0]
	return e

def computeRecallNonIncre(testSet, ratingMat, curPred, topN, sampleRange):
	num4hit = 0
	num4Test = 0
	for i in xrange(0, testSet.shape[0]):
		if testSet[i, 2] >= 4:
			num4Test += 1
		else:
			continue
		userID = int(testSet[i, 0])
		itemID = int(testSet[i, 1])
		userArray = ratingMat[userID, :]
		notRated = np.where(userArray == 0)
		sampled = random.sample(notRated[0], sampleRange)
		selectedRate = np.zeros((1, sampleRange))
		for j in xrange(0, sampleRange):
			bufIdx = sampled[j]
			selectedRate[0, j] = curPred[userID, bufIdx]

		corresp = curPred[userID, itemID]
		thre = np.where(selectedRate[0] > corresp)
		if len(thre[0]) <= (topN-1):
			num4hit += 1
	return num4hit, num4Test
