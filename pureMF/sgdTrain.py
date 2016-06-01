import numpy as np
import random
import time

class svdTrain():
    def __init__(self, M=20, maxRating=5, minRating=1, lambdaval=0.1, gamma=0.05,
                        topN=10, numUser=943, numItem=1682):
        self.maxRating = maxRating
        self.minRating = minRating
        self.lambdaval = lambdaval
        self.gamma = gamma
        self.topN = topN
        self.M = M
        self.bu = np.random.rand(1, numUser)
        self.bi = np.random.rand(1, numItem)
        self.userMat = np.random.rand(numUser, M)
        self.itemMat = np.random.rand(numItem, M)
        self.numUser = numUser
        self.numItem = numItem

    def rBar(self, u, i):
        val = self.mu
        if self.userBitArray[0, u] > 0:
            val = val + self.bu[0, u]
        if self.itemBitArray[0, i] > 0:
            val = val + self.bi[0, i]
        if self.userBitArray[0, u] > 0 and self.itemBitArray[0, i] > 0:
            val = val + np.vdot(self.userMat[u, :], self.itemMat[i, :])
        if val > self.maxRating:
            return self.maxRating
        elif val < self.minRating:
            return self.minRating
        else:
            return val


    def startTrain(self, filename, numRows, percentage, numEpoch):
        outPutSet = np.zeros((numRows, 4))
        outPutMat = np.zeros((self.numUser, self.numItem))
        itemBitArray = np.zeros((1, self.numItem))
        userBitArray = np.zeros((1, self.numUser))
        muCount = 0
        mu = 0

        for i, line in enumerate(open(filename, 'r')):
            user, item, rating, timeStamp = line.strip().split('\t')
            userID = int(int(user)-1)
            itemID = int(int(item)-1)

            outPutSet[i, 0] = userID
            outPutSet[i, 1] = itemID
            outPutSet[i, 2] = rating
            outPutSet[i, 3] = timeStamp
            muCount += 1
            mu = mu + float(rating)

        mu = mu/muCount
        outPutSet = sorted(outPutSet, key=lambda outPutSet: outPutSet[3])
        outPutSet = np.asarray(outPutSet)

        trainSet = outPutSet[:int(numRows*percentage)]
        testSet = outPutSet[int(numRows*percentage):]

        for iitem in trainSet:
            itemBitArray[0, iitem[1]] = 1
            userBitArray[0, iitem[0]] = 1

        for i in xrange(0, len(trainSet)):
            outPutMat[int(trainSet[i, 0]), int(trainSet[i, 1])] = trainSet[i, 2]

        self.ratingMat = outPutMat
        self.trainSet = trainSet
        self.testSet = testSet
        self.mu = mu
        self.itemBitArray = itemBitArray
        self.userBitArray = userBitArray
        self.go(numEpoch)

    def go(self, numEpoch):
        l = 0
        while l < numEpoch:
            l += 1
            for item in self.trainSet:
                error = float(item[2]) - self.rBar(item[0], item[1])
                self.bu[0, item[0]]=self.bu[0, item[0]]+self.gamma*(error-self.lambdaval*self.bu[0, item[0]])
                self.bi[0, item[1]]=self.bi[0, item[1]]+self.gamma*(error-self.lambdaval*self.bi[0, item[1]])
                self.itemMat[item[1]]=np.add(self.itemMat[item[1]],np.multiply(self.gamma,np.add(np.multiply(error, self.userMat[item[0]]),np.multiply(-self.lambdaval,self.itemMat[item[1]]))))
                self.userMat[item[0]]=np.add(self.userMat[item[0]],np.multiply(self.gamma,np.add(np.multiply(error, self.itemMat[item[1]]),np.multiply(-self.lambdaval,self.userMat[item[0]]))))
            print 'Epoch',l,'finished!'

        self.eva()

    def eva(self):
        MAECount = 0
        MAESum = 0
        for item in self.testSet:
            MAECount += 1
            # print self.rBar(item[0],item[1])
            MAESum = MAESum + abs(self.rBar(item[0],item[1])-float(item[2]))

        print 'finished testing!'
        MAE = MAESum/MAECount
        print 'MAE:', MAE


if __name__ == '__main__':
    sgdMF = svdTrain()
    sgdMF.startTrain('u.data', 100000, 0.98, 5)


















#
