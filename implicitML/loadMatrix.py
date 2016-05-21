import numpy as np
import time
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve

def loadData2matrix(filename, numUsers, numTracks):
    matrix = np.zeros((numUsers, numTracks))
    for i, line in enumerate(open(filename, 'r')):
        user, track, timestamp = line.strip().split(',')
        userID = int(user)
        trackID = int(track)
        timestamp = int(timestamp)
        matrix[userID, trackID] += 1
    print '------------- finish loading data to rating matrix! ----------------'
    return matrix


def loadData2Set(filename, numRows):
    Set = np.zeros((numRows, 4))
    for i, line in enumerate(open(filename, 'r')):
        user, track, ratings, timestamp = line.strip().split(',')
        userID = int(user)
        trackID = int(track)
        ratings = int(ratings)
        timestamp = int(timestamp)

        Set[i, 0] = userID
        Set[i, 1] = trackID
        Set[i, 2] = ratings
        Set[i, 3] = timestamp

    print '---------------- finish loading data to Set! -----------------------'
    return Set
