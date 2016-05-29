import numpy as np

def loadDataExplicit(filename, numRows, numUser, numItem, percentage, spliter, Sorted, step):
	outPutSet = np.zeros((numRows, 4))
	outPutMat = np.zeros((numUser, numItem))
	bitArray = np.zeros((1, numItem))

	for i, line in enumerate(open(filename, 'r')):
		user, item, rating, timeStamp = line.strip().split(spliter)
		userID = int(int(user)-1)
		# if Sorted:
		# 	if userID == 550 or userID == 188:
		# 		continue
		itemID = int(int(item)-1)
		bitArray[0, itemID] += 1

		outPutSet[i, 0] = userID
		outPutSet[i, 1] = itemID
		outPutSet[i, 2] = rating
		outPutSet[i, 3] = timeStamp

	if Sorted:
		outPutSet = sorted(outPutSet, key=lambda outPutSet: outPutSet[3])
		outPutSet = np.asarray(outPutSet)
	if step:
		outPutSet[:, 3] = np.linspace(1, numRows, num = numRows)

	trainSet = outPutSet[:int(numRows*percentage)]
	testSet = outPutSet[int(numRows*percentage):]

	for i in xrange(0, len(trainSet)):
		outPutMat[int(trainSet[i, 0]), int(trainSet[i, 1])] = trainSet[i, 2]

	return trainSet, testSet, outPutMat, bitArray

def loadDataImplicit(filename, numRows, numUser, numItem, percentage, spliter, Sorted, step):
	outPutSet = np.zeros((numRows, 3))
	outPutMat = np.zeros((numUser, numItem))

	for i, line in enumerate(open(filename, 'r')):
		user, item, rating, timeStamp = line.strip().split(spliter)
		userID = int(int(user)-1)
		itemID = int(int(item)-1)

		outPutSet[i, 0] = userID
		outPutSet[i, 1] = itemID
		outPutSet[i, 2] = timeStamp

	if Sorted:
		outPutSet = sorted(outPutSet, key=lambda outPutSet: outPutSet[2])
		outPutSet = np.asarray(outPutSet)
	if step:
		outPutSet[:, 2] = np.linspace(1, numRows, num = numRows)

	trainSet = outPutSet[:int(numRows*percentage)]
	testSet = outPutSet[int(numRows*percentage):]

	for i in xrange(0, len(trainSet)):
		outPutMat[int(trainSet[i, 0]), int(trainSet[i, 1])] += 1


	return trainSet, testSet, outPutMat
