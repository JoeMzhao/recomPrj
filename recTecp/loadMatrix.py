import numpy as np

def loadData2matrix(filename, numUsers, numMovies):
    matrix = np.zeros((numUsers, numMovies))
    for i, line in enumerate(open(filename, 'r')):
        user, movie, ratings, timestamp = line.strip().split(',')
        userID = int(user)
        movieID = int(movie)
        rate = int(ratings)
        matrix[userID, movieID] = rate
    print 'finish loading data to rating matrix!'
    return matrix


def loadData2Set(filename, numRows):
    Set = np.zeros((numRows, 4))
    for i, line in enumerate(open(filename, 'r')):
        user, movie, rating, timestamp = line.strip().split(',')
        userID = int(user)
        movieID = int(movie)
        rate = int(rating)
        timeStamp = int(timestamp)

        Set[i, 0] = userID
        Set[i, 1] = movieID
        Set[i, 2] = rate
        Set[i, 3] = timeStamp

    print 'finish loading data to Set!'
    return Set
