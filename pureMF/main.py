import numpy as np
import loadData as LD
import math
import evaluating as EVA
import ALS
import time
import copy
import random
import inORnot as io
import whichOut as wo
import sampleInput as sp

class mfExplicit():
	def __init__(self, numUser, numItem, regular_u, regular_v, M, tolerence,\
								maxIter, trainSet, testSet, ratingMat):
		self.numUser = numUser
		self.numItem = numItem
		self.regular_u = regular_u
		self.regular_v = regular_v
		self.maxIter = maxIter
		self.M = M
		self.tolerence = tolerence
		self.trainSet = trainSet
		self.testSet = testSet
		self.ratingMat = ratingMat

	def startMF(self):
		nonZeroItem = []
		nonZeroUser = []
		for i in xrange(0, self.numUser):
			nonZeroItem.append(i)
			nonZeroItem.append(np.where(self.ratingMat[i, :] > 0))

		for i in xrange(0, self.numItem):
			nonZeroUser.append(i)
			nonZeroUser.append(np.where(self.ratingMat[:, i] > 0))

		userMatO = np.random.rand(self.numUser, M)
		itemMatO = np.random.rand(self.numItem, M)

		for i in xrange(0, self.numItem):
			if len(nonZeroUser[2 * i + 1][0]) > 0:
				idx = nonZeroUser[2 * i + 1][0]
				itemMatO[i, 0] = np.mean(self.ratingMat[idx, i])

		self.iteration(userMatO, itemMatO, nonZeroItem, nonZeroUser)

	def iteration(self, userMatO, itemMatO, nonZeroItem, nonZeroUser):
		tolerBuffer = np.zeros((1, self.maxIter))
		noZeroEntri = self.trainSet.shape[0]

		for i in xrange(0, self.maxIter):
			if i%20 == 0:
				print '=== %dth iteration ==='%i
			userMat, itemMat = ALS.ALS(self.ratingMat, userMatO, itemMatO,\
								nonZeroItem, nonZeroUser, self.M, self.regular_v, self.regular_u)

			tolerBuffer[0, i] = EVA.computeRMSE(self.trainSet, userMat, itemMat)
			if i > 0 and math.fabs(tolerBuffer[0, i] - tolerBuffer[0, i-1])<tolerence:
				break
			userMatO = userMat
			itemMatO = itemMat
			if i == maxIter-1:
				print 'max iteration reached!'
		self.userMat = userMat
		self.itemMat = itemMat
		self.curPred = np.dot(self.userMat, self.itemMat.T)

if __name__ == '__main__':

	numUser = 943  #6040
	numItem = 1682 #3952
	regular_u = 0.4
	regular_v = 0.4
	M = 20
	tolerence = 1e-2
	maxIter = 500
	numRows = 100000 #100000 #
	percentage = 0.98
	sampleRange = 210
	topN = 10
																#Sorted, step/stamp
	trainSet, testSet, ratingMat, bitArray = \
				LD.loadDataExplicit('u.data', numRows, numUser, numItem, percentage, '\t', 0, 1)

	prediction = mfExplicit(numUser, numItem, regular_u, regular_v, M, tolerence, maxIter, trainSet, testSet, ratingMat)
	prediction.startMF()



	''' ----->>>  Incremental Model  <<<-----'''
	numIncome = 0
	curPred = copy.copy(prediction.curPred)
	userMat = copy.copy(prediction.userMat)
	itemMat = copy.copy(prediction.itemMat)
	poolSize = trainSet.shape[0]
	T = 7
	alpha1 = 0.0006
	beta = 0.001
	incre4test = 0
	incre4hit = 0
	sizeRsv = 800.0
	reservoir = np.zeros((0, 4))
	flag = 0
	full = 0
	reservoirChanged = 1
	endTimestamp = trainSet[-1, 3]

	for i in xrange(0, testSet.shape[0]):

		userID = int(testSet[i, 0])
		itemID = int(testSet[i, 1])
		ratingMat[userID, itemID] = testSet[i, 2]
		testSet[i, 3] = testSet[i, 3] - endTimestamp
		tmstp = testSet[i, 3]

		if reservoir.shape[0] <= sizeRsv-1:
			reservoir = np.vstack([reservoir, testSet[i, :]])
		else:
			full = 1
			bufIdx1 = np.where(reservoir[:, 0] == userID)[0]
			userPool1 = np.vstack([reservoir[bufIdx1, :], testSet[i, :]])
			intoProb = 1 - sizeRsv/tmstp
			seed = random.random()
			if seed <= intoProb:
				# print 'Added to reservoir! ID is %d'%testSet[i, 1]
				numIncome += 1
				reservoirChanged = 1
				rsvTimeArray = reservoir[:, 3]
				thredArray1 = np.exp(1.0/(tmstp - rsvTimeArray))
				buffArray = -np.exp(-thredArray1)
				thredArray2 = 1 - np.exp(buffArray)
				probArry = np.random.uniform(0, 1, sizeRsv)
				right = thredArray2 - probArry
				rplcdIdx = np.where(right == right.max())[0][0]
				reservoir[rplcdIdx, :] = testSet[i, :]

		if full and reservoirChanged:
			reservoirChanged = 0
			bufIdx2 = np.where(reservoir[:, 0] == userID)[0]
			userPool2 = reservoir[bufIdx2, :]

			SPuIdx = sp.smpPosiInput(curPred, userPool1, userID, numUser, numItem)
			SPuIdx = random.sample(SPuIdx, int(len(SPuIdx) * 0.2))
			SNuIdx = sp.smpNegaInput(curPred, userPool2, SPuIdx, userID, numUser, numItem)
			SNuIdx = random.sample(SNuIdx, int(len(SNuIdx) * 0.2))

			for rnd in xrange(0, T):
				alpha = alpha1/((1+rnd)**0.1)
				for ii in xrange(0, len(SPuIdx)):
					flag = 1
					rate_hat = curPred[userID, SPuIdx[ii]]
					if len(SNuIdx) == 0:
						rate_avg = 0
					else:
						rate_avg = np.mean(curPred[userID, SNuIdx[:]])
					ita = max(0.0, rate_hat - rate_avg)

					if len(SNuIdx) == 0:
						nega_avg = np.zeros((1, M))
					else:
						idx = SNuIdx[:]
						nega_sum = np.sum(itemMat[idx, :], axis=0)
						nega_avg = nega_sum/len(SNuIdx)

					userMat[userID, :] = userMat[userID, :] + alpha * ita * \
										(itemMat[SPuIdx[ii], :] - nega_avg) - \
										alpha * beta * userMat[userID, :]
					itemMat[SPuIdx[ii], :] = itemMat[SPuIdx[ii], :] + alpha * ita * \
									userMat[userID, :] - alpha * beta * itemMat[SPuIdx[ii], :]
					for j in xrange(0, len(SNuIdx)):
						itemMat[SNuIdx[j], :] = itemMat[SNuIdx[j], :] - alpha * ita * \
										userMat[userID, :] - alpha * beta * itemMat[SNuIdx[j], :]
		if flag:
			curPred = np.dot(userMat, itemMat.T)
			flag = 0

		if testSet[i, 2] >= 4 and bitArray[0, itemID] > 0 and full:
			print '------- Evaluating details -------'
			print ' %dth testing point'%i
			print 'userID : %d       itemID : %d'%(userID, itemID)
			incre4test += 1
			userArry = ratingMat[userID, :]
			notRated = np.where(userArry == 0)
			sampled = random.sample(notRated[0], sampleRange)
			selectedRate = np.zeros((1, sampleRange))

			for j in xrange(0, sampleRange):
				bufIdx = sampled[j]
				selectedRate[0, j] = curPred[userID, bufIdx]
			corresp = curPred[userID, itemID]
			print 'Maximum in the selected items: %.5e'%(max(selectedRate[0]))
			print 'Our prediction is: %.5e'%corresp
			thre = np.where(selectedRate[0] > corresp)
			if (len(thre[0]) <= (topN-1)):
				print '!!! This is a hit !!!'
				incre4hit += 1
			print '----------------------------------'

	print '========== results list ==========='
	print '-------- None incremental -----'
	MAE = EVA.computeMAE(testSet, prediction.curPred)
	num4hit, num4Test = EVA.computeRecallNonIncre(testSet[sizeRsv:], ratingMat, prediction.curPred, topN, sampleRange)
	RECALL = num4hit/num4Test
	print 'MAE of pure MF is: %f'%MAE
	print 'RECALL of pure MF is: %.3f, num4hit is %d, num4Test is %d'%\
							((float(num4hit)/num4Test), num4hit, num4Test)

	print '--------- Incremental ---------'
	MAE2 = EVA.computeMAE(testSet, curPred)
	print 'MAE =  %f'%MAE2
	print 'RECALL = %f, incre4hit = %d, incre4test = %d'%\
						((float(incre4hit)/incre4test), incre4hit, incre4test)

	print '--------- Parameter list -----------'
	print 'num of incoming point: %d '%numIncome


	#
