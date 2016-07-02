import numpy as np
import random
import time
import copy
import sampleInput as sp
import sys
import csv

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
        outPutSet[:, 3] = np.linspace(1, numRows, num = numRows)

        trainSet = outPutSet[:int(numRows*percentage)]
        testSet = outPutSet[int(numRows*percentage):]

        for iitem in trainSet:
            itemBitArray[0, iitem[1]] += 1
            userBitArray[0, iitem[0]] += 1

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
        self.MAE = MAE
        print 'MAE:', MAE

def getRbar(bu, bi, userID, itemID, userMat, itemMat, userBitArray, itemBitArray, mu, maxRating, minRating):
    val = mu
    if userBitArray[0, userID] > 0:
        val = val + bu[0, userID]
    if itemBitArray[0, itemID] > 0:
        val = val + bi[0, itemID]
    if userBitArray[0, userID] > 0 and itemBitArray[0, itemID] > 0:
        val = val + np.vdot(userMat[userID, :], itemMat[itemID, :])
    if val > maxRating:
        return maxRating
    elif val < minRating:
        return minRating
    else:
        return val

def getCurPred(userID, numItem, userMat, itemMat, mu, bu, bi, userBitArray, itemBitArray):
    curPred = np.zeros((1, numItem))
    for i in xrange(0, numItem):
        curPred[0, i] = getRbar(bu, bi, userID, i, userMat, itemMat, userBitArray, itemBitArray, mu, maxRating, minRating)
    return curPred


if __name__ == '__main__':

    numEpoches = 50
    toffline = time.time()
    sgdMF = svdTrain()
    sgdMF.startTrain('u.data', 100000, 0.98, numEpoches)
    offlineTime = time.time()-toffline

    trainSet = copy.copy(sgdMF.trainSet)
    testSet = copy.copy(sgdMF.testSet)
    userMat = copy.copy(sgdMF.userMat)
    itemMat = copy.copy(sgdMF.itemMat)
    bu = copy.copy(sgdMF.bu)
    bi = copy.copy(sgdMF.bi)
    userBitArray = copy.copy(sgdMF.userBitArray)
    itemBitArray = copy.copy(sgdMF.itemBitArray)
    mu = copy.copy(sgdMF.mu)

    numUser = 943
    numItem = 1682
    M = 20
    numRows = 100000
    sampleRange = 100
    topN = 10
    T = int(sys.argv[1])
    numIn = 0
    sizeRsv = float(sys.argv[2])
    reservoir = np.zeros((0, 4))
    full = 0
    endTimestamp = trainSet[-1, 3]
    maxRating = 5
    minRating = 1
    alpha1 =  float(sys.argv[3])
    alphaList = np.zeros((numUser, 1)) + alpha1
    beta = float(sys.argv[4])
    memoValue = []
    reservoirChanged = 1
    er = 0
    maeEachUserNon = np.zeros((1, numUser))
    for i in xrange(0, testSet.shape[0]):
        pred = getRbar(bu, bi, testSet[i, 0], testSet[i, 1], userMat, itemMat, userBitArray, itemBitArray, mu, maxRating, minRating)
        er = er + abs(pred - float(testSet[i][2]))
        maeEachUserNon[0, int(testSet[i, 0])] += abs(pred - float(testSet[i, 2]))

    ratingMat = np.zeros((numUser, numItem))
    timeList = []
    memoListSNuIdx = []
    memoListSPuIdx = []
    memoList = []
    for i in xrange(0, trainSet.shape[0]):
        ratingMat[trainSet[i, 0], trainSet[i, 1]] = trainSet[i, 2]

    for i in xrange(0, testSet.shape[0]):
        userID = int(testSet[i, 0])
        itemID = int(testSet[i, 1])

        if i%100 == 0:
            print 'INFO: # of testing data:', i

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
                print '-------------testing details ------------'
                print 'In! Test point ID:', i
                print 'userID:%d, itemID:%d'%(userID, itemID)
                print 'added tuple is:', testSet[i, :]
                numIn += 1
                reservoirChanged = 1
                rsvTimeArray = reservoir[:, 3]
                thredArray1 = np.exp(1.0/(tmstp-rsvTimeArray))
                buffArray = -np.exp(-thredArray1)
                thredArray2 = 1 - np.exp(buffArray)
                probArry = np.random.uniform(0, 1, sizeRsv)
                right = thredArray2 - probArry
                rplcdIdx = np.where(right == right.max())[0][0]
                print 'removed tuple is:'
                print reservoir[rplcdIdx, :]
                outItedmIdx = reservoir[rplcdIdx, :]
                reservoir[rplcdIdx, :] = testSet[i, :]

        if full and reservoirChanged:
            reservoirChanged = 0
            bufIdx2 = np.where(reservoir[:, 0] == userID)[0]
            userPool2 = reservoir[bufIdx2, :]
            curPred = getCurPred(userID, numItem, userMat, itemMat, mu, bu, bi, userBitArray, itemBitArray)

            SPuIdx = sp.smpPosiInput(curPred, userPool1, numUser, numItem)
            if len(SPuIdx) > 10:
                SPuIdx = random.sample(SPuIdx, 10)
            SNuIdx = sp.smpNegaInput(curPred, userPool2, SPuIdx, numUser, numItem)
            if len(SNuIdx) > 10:
                SNuIdx = random.sample(SNuIdx, 10)

            # print 'SNuIdx=>', SNuIdx
            # print 'SPuIdx=>', SPuIdx
            memoListSPuIdx.append(len(SPuIdx))
            memoListSNuIdx.append(len(SNuIdx))
            memoList.append(len(SPuIdx)+len(SNuIdx))
            memoValue.append(sys.getsizeof(itemMat[1]) * (len(SPuIdx)+len(SNuIdx)))
            alpha2 = alphaList[userID, 0]
            t10 = time.time()
            for ii in xrange(0, len(SPuIdx)):
                for rnd in xrange(0, T):
                    alpha = alpha2/((1+rnd)**0.01)
                    rate_hat = curPred[0, SPuIdx[ii]]
                    if len(SNuIdx) == 0:
                        ita = 0
                    else:
						rate_avg = min(np.mean(curPred[0, SNuIdx[:]]), maxRating)
						ita = np.mean(np.maximum(np.zeros((1, len(SNuIdx))), ratingMat[userID, SNuIdx[:]]- curPred[0, SNuIdx[:]]))

                    e = ratingMat[userID, SPuIdx[ii]] - rate_hat
                    if len(SNuIdx) == 0:
                        nega_avg = np.zeros((1, M))
                    else:
                        idx = SNuIdx[:]
                        nega_sum = np.sum(itemMat[idx, :], axis=0)
                        nega_avg = nega_sum/len(SNuIdx)

                    userMat[userID, :] = userMat[userID, :] + alpha * e * itemMat[SPuIdx[ii], :] - alpha * ita * nega_avg - \
                                            alpha * beta * userMat[userID, :]
                    itemMat[SPuIdx[ii], :] = itemMat[SPuIdx[ii], :] + alpha * e * \
                                            userMat[userID, :] - alpha * beta * itemMat[SPuIdx[ii], :]

                    for j in xrange(0, len(SNuIdx)):
						itemMat[SNuIdx[j], :] = itemMat[SNuIdx[j], :] - alpha * ita * \
										userMat[userID, :] - alpha * beta * itemMat[SNuIdx[j], :]
                    curPred = getCurPred(userID, numItem, userMat, itemMat, mu, bu, bi, userBitArray, itemBitArray)
                    # print curPred[0, SPuIdx[ii]]
            alphaList[userID, 0] = alpha
            timeList.append(time.time()-t10)


    ''' Evalutating '''
    increMAEcount = 0
    increMAEsum = 0
    er = 0
    erRMSE = 0
    userBitArrayInTest = np.zeros((1, numUser))
    maeEachUser = np.zeros((1, numUser))
    for i in xrange(0, testSet.shape[0]):
        userBitArrayInTest[0, int(testSet[i, 0])] += 1
        pred = getRbar(bu, bi, testSet[i, 0], testSet[i, 1], userMat, itemMat, userBitArray, itemBitArray, mu, maxRating, minRating)
        er = er + abs(pred - float(testSet[i][2]))
        erRMSE = erRMSE + (pred - float(testSet[i][2]))**2
        maeEachUser[0, int(testSet[i, 0])] += abs(pred - float(testSet[i, 2]))

    print er
    print erRMSE
    erRMSE = erRMSE/testSet.shape[0]
    print '=========== Evaluation results ========'
    print 'the incremental MAE is :', er/testSet.shape[0]
    print 'the incremental RMSE is:', erRMSE
    print 'non-incremental MAE is :', sgdMF.MAE
    print 'the improvement is :%f'%(sgdMF.MAE-er/testSet.shape[0])
    print 'avg length of SPuIdx:', np.mean(memoListSPuIdx)
    print 'avg length of SNuIdx:', np.mean(memoListSNuIdx)
    print 'avg all length:', np.mean(memoList)
    print 'avg time', np.mean(timeList)
    print 'Size of storage in offline: %d'%(sys.getsizeof(userMat) + sys.getsizeof(itemMat) + sys.getsizeof(ratingMat))
    print 'Size of online:' , np.sum(memoList)*sys.getsizeof(userMat[1])/numUser
    print 'Offline train time:',offlineTime
    print '============ para list =============='
    print 'T:', T
    print 'Alpha (initial):', alpha1
    print 'Beta:', beta
    print 'reservoirSize:', sizeRsv
    print 'numEpoches:', numEpoches

    distriINFO = np.zeros((3, numUser))
    distriINFO[0, :] = userBitArray
    distriINFO[1, :] = userBitArrayInTest
    distriINFO[2, :] = maeEachUser

    with open('mae_distribution.txt', 'a') as f:
        writer = csv.writer(f)
        writer.writerows(distriINFO)
        writer.writerows(maeEachUserNon)

    f = open('performance.txt','a')
    f.write(str(alpha1))
    f.write(',')
    f.write(str(beta))
    f.write(',')
    f.write(str(sizeRsv))
    f.write(',')
    f.write(str(numEpoches))
    f.write(',')
    f.write(str(T))
    f.write(',')
    f.write(str(sgdMF.MAE)) #ORIGINAL MAE
    f.write(',')
    f.write(str(er/testSet.shape[0]))
    f.write(',')
    f.write(str(sgdMF.MAE-er/testSet.shape[0]))
    f.write('\n')
    f.close()


    f = open('resultTimeImpML.txt','a')
    for i in xrange(0, len(timeList)):
        f.write(str(timeList[i]))
        f.write('\t')
    f.write('\n')
    f.close()

    f = open('memoValueImpML.txt','a')
    for i in xrange(0, len(memoValue)):
        f.write(str(memoValue[i]))
        f.write('\t')
    f.write('\n')
    f.close()
