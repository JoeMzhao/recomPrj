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

	numUser = 943
	numItem = 1682
	regular_u = 0.4
	regular_v = 0.4
	M = 20
	tolerence = 1e-5
	maxIter = 500
	numRows = 100000
	percentage = 0.98
	sampleRange = 210
	topN = 10
																#Sorted, step/stamp
	trainSet, testSet, ratingMat, bitArray = \
				LD.loadDataExplicit('u.data', numRows, numUser, numItem, percentage, '\t', 1, 1)

	prediction = mfExplicit(numUser, numItem, regular_u, regular_v, M, tolerence, maxIter, trainSet, testSet, ratingMat)
	prediction.startMF()
	MAE = EVA.computeMAE(testSet, prediction.curPred)
	num4hit, num4Test = EVA.computeRecallNonIncre(testSet, ratingMat, prediction.curPred, topN, sampleRange)
	RECALL = num4hit/num4Test
	print 'MAE of pure MF is: %f'%MAE
	print 'RECALL of pure MF is: %.3f, num4hit is %d, num4Test is %d'%\
							((float(num4hit)/num4Test), num4hit, num4Test)


	''' ----->>>  Incremental Model  <<<-----'''
	numIncome = 0
	spuLen = []
	snuLen = []
	curPred = copy.copy(prediction.curPred)
	userMat = copy.copy(prediction.userMat)
	itemMat = copy.copy(prediction.itemMat)
	poolSize = trainSet.shape[0]
	T = 3
	alpha = 0.0001
	beta = 0.01
	incre4test = 0
	incre4hit = 0

	for i in xrange(0, testSet.shape[0]):
		if i%500 == 0:
			print '---- %dth testing dataset ----'%i
		userID = int(testSet[i, 0])
		itemID = int(testSet[i, 1])
		bufIdx1 = np.where(trainSet[:, 0] == userID)[0]
		userPool1 = trainSet[bufIdx1, :]
		if io.inORnot(testSet[i, 3], poolSize):
			printed1 = 1
			printed2 = 1
			numIncome += 1
			ratingMat[userID, itemID] = testSet[i, 2]
			timeArray = trainSet[:, 3]
			kickIdx = wo.whichOut(timeArray, testSet[i, 3])
			trainSet[kickIdx, :] = testSet[i, :]

			bufIdx2 = np.where(trainSet[:, 0] == userID)[0]
			userPool2 = trainSet[bufIdx2, :]

			SPuIdx = sp.smpPosiInput(curPred, userPool1, testSet[i, :], numUser, numItem)
			SNuIdx = sp.smpNegaInput(curPred, userPool2, SPuIdx, testSet[i, :], numUser, numItem)

			spuLen.append(len(SPuIdx))
			snuLen.append(len(SNuIdx))
			# if userID == 550:
			# 	time.sleep(0.1)
			# 	print 'SPuIdx is following:'
			# 	print SPuIdx
			# 	print 'SNuIdx is following:'
			# 	print SNuIdx
			# 	print userMat[550, :]

			# if printed1:
			# 	print ':::::::::Original usermat:::::::'
			# 	print userMat[userID, :]
			# 	printed1 = 0
			for rnd in xrange(0, T):
				for ii in xrange(0, len(SPuIdx)):
					rate_hat = curPred[userID, SPuIdx[ii]]
					if len(SNuIdx) == 0:
						rate_avg = 0
					else:
						rate_avg = np.mean(curPred[userID, SNuIdx[:]])
					ita = max(0.0, rate_hat - rate_avg)
					# if printed1:
					# 	print 'ce la ita %f:'%ita
					# 	print 'length of SPuIdx and SNuIdx%d, %d'%(len(SPuIdx), len(SNuIdx))
					# 	printed1 = 0
					if len(SNuIdx) == 0:
						nega_avg = np.zeros((1, M))
					else:
						idx = SNuIdx[:]
						nega_sum = np.sum(itemMat[idx, :], axis=0)
						nega_avg = nega_sum/len(SNuIdx)
					# print 'This is the reduction:'
					# print itemMat[SPuIdx[ii], :] - nega_avg

					userMat[userID, :] = userMat[userID, :] + alpha * ita * \
										(itemMat[SPuIdx[ii], :] - nega_avg) - \
										alpha * beta * userMat[userID, :]
					itemMat[SPuIdx[ii], :] = itemMat[SPuIdx[ii], :] + alpha * ita * \
									userMat[userID, :] - alpha * beta * itemMat[SPuIdx[ii], :]
					for j in xrange(0, len(SNuIdx)):
						itemMat[SNuIdx[j], :] = itemMat[SNuIdx[j], :] - alpha * ita * \
										userMat[userID, :] - alpha * beta * itemMat[SNuIdx[j], :]
			# if printed2:
			# 	print '::::::::After usermat:::::::'
			# 	print userMat[userID, :]
			# 	printed2 = 0
			curPred = np.dot(userMat, itemMat.T)

		if testSet[i, 2] >= 4 and bitArray[0, itemID] > 0:
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
	print 'MAE of pure MF is: %f'%MAE
	print 'RECALL of pure MF is: %.3f, num4hit is %d, num4Test is %d'%\
							((float(num4hit)/num4Test), num4hit, num4Test)
	print '--------- Incremental ---------'
	MAE2 = EVA.computeMAE(testSet, curPred)
	print 'MAE =  %f'%MAE2
	print 'RECALL = %f, incre4hit = %d, incre4test = %d'%\
						((float(incre4hit)/incre4test), incre4hit, incre4test)


	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	# #
