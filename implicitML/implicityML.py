import numpy as np
import nimfa
import time
import random
import matplotlib.pyplot as plt
import pylab
import csv
import loadMatrix

def loadData2matrix(filename, numUsers = 943, numMovie = 1682):
    matrix = np.zeros((numUsers, numMovie))
    for i, line in enumerate(open(filename, 'r')):
        user, movie, rating, timestamp = line.strip().split(',')
        userID = int(user)
        movieID = int(movie)
        timestamp = int(timestamp)
        if timestamp < 31000:
            timestamp = 1
        elif timestamp < 62000:
            timestamp = 2
        else:
            timestamp = 3
        matrix[userID, movieID] = timestamp
        if i%15000 == 0:
            print 'finished load %d points to matrix' %i
    print 'finished loading data to time matrix!'
    return matrix

def moviReleaseTime(filename, numMovie = 1682):
    bitArray = np.ones((numMovie, 1))
    timeArray = np.zeros((numMovie, 1))
    for i, line in enumerate(open(filename, 'r')):
        user, movie, rating, timestamp = line.strip().split(',')
        movieID = int(movie)
        timestamp = int(timestamp)
        if timestamp < 31000:
            timestamp = 1
        elif timestamp < 62000:
            timestamp = 2
        else:
            timestamp = 3
        if bitArray[movieID, 0] == 1:
            timeArray[movieID, 0] = timestamp
            bitArray[movieID, 0] = 0
        if i%15000 == 0:
            print 'loaded %d temporal informaiton' %i
    print 'finished checking release date of movie!'
    return (timeArray, bitArray)

def pseudoRating(a):
    return{ '1+1': 0.5,
            '1+2': 1,
            '1+3': 1.5,
            '2+1': 1,
            '2+2': 2.5,
            '2+3': 3,
            '3+1': 1.5,
            '3+2': 3,
            '3+3': 5,
    }.get(a, 0)

def processTestSet(filename, numRows, trainMovieRlsTime, bitArray):
    testSet = np.zeros((numRows, 4))
    for i, line in enumerate(open(filename, 'r')):
        userID, movie, rating, purChasetimestamp1 = line.strip().split(',')
        movieID = int(movie)
        purChasetimestamp = int(purChasetimestamp1)
        if purChasetimestamp < 31000:
            purChasetimestamp = 1
        elif purChasetimestamp < 62000:
            purChasetimestamp = 2
        else:
            purChasetimestamp = 3
        if bitArray[movieID, 0] == 0:
            bitArray[movieID, 0] = 0
            releaseTime = purChasetimestamp
        else:
            releaseTime = trainMovieRlsTime[movieID, 0]

        para = str(int(purChasetimestamp)) + '+' + str(int(releaseTime))
        psedTestRate = pseudoRating(para)

        testSet[i, 0] = int(userID)
        testSet[i, 1] = movieID
        testSet[i, 2] = psedTestRate
        testSet[i, 3] = purChasetimestamp1
        if i%15000 == 0:
            print 'loaded %d temporal informaiton' %i
    print 'finished checking release date of movie!'
    return testSet




if __name__ == '__main__':
    numUser = 943
    numMovie = 1682

    trainTimeMatrix = loadData2matrix('trainSection.csv')
    (trainMovieRlsTime, bitArray) = moviReleaseTime('trainSection.csv')
    testSet = processTestSet('testSection.csv', 5000, trainMovieRlsTime, bitArray)
    print testSet

    pseduRatingMat = np.zeros((numUser, numMovie))

    for i in range(0, numUser):
        for j in range(0, numMovie):
            if trainTimeMatrix[i, j] > 0:
                para = str(int(trainTimeMatrix[i, j])) + '+' + str(int(trainMovieRlsTime[j, 0]))
                pseduRatingMat[i, j] = pseudoRating(para)

    t0 = time.time()
    lsnmf = nimfa.Lsnmf(pseduRatingMat, seed="random_vcol", rank=20, max_iter=12, sub_iter=10,
                    inner_sub_iter=10, beta=0.1)
    lsnmf_fit = lsnmf()
    print 'finish training process in %f seconds.' %(time.time()-t0)

    moviMat = lsnmf_fit.coef().T
    userMat = lsnmf_fit.basis()

    curPred = np.dot(userMat, moviMat.T)
    print curPred

    N = 10 # recommend top N movies
    P10K = 200
    num4test = 0
    num4hit = 0

    for i in range(0, testSet.shape[0]):
        if i%1000 == 0:
            print i
        if testSet[i, 2] >= 4.5:
            num4test += 1
        else:
            continue
        userID = int(testSet[i, 0])
        movieID = int(testSet[i, 1])

        userArry = pseduRatingMat[userID, :]
        notListen = np.where(userArry == 0)
        sampled = random.sample(notListen[0], P10K)
        candiRate = np.zeros((1, len(sampled)))

        for j in range(0, len(sampled)):
            bufIdx = sampled[j]
            candiRate[0, j] = curPred[userID, bufIdx]
        corresp = curPred[userID, movieID]
        thre = np.where(candiRate[0] > corresp)

        if (len(thre[0]) <= (N-1)):
            num4hit += 1
    print ' -------------- >>> results list <<< -------------'
    print num4hit
    print num4test


    # with open('pseudoRating.csv','w') as f:
    #     f_csv = csv.writer(f)
    #     f_csv.writerows(pseduRatingMat)








    #
