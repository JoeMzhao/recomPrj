import csv
import numpy as np
from   numpy import *

with open('top25.csv') as f:
    cf    = csv.reader(f, delimiter = '\t')
    traid = [row[2] for row in cf]

with open('top25.csv') as f:
    cf        = csv.reader(f, delimiter = '\t')
    timestamp = [row[1] for row in cf]

with open('top25.csv') as f:
    cf     = csv.reader(f, delimiter = '\t')
    userID = [row[0] for row in cf]

traid     = mat(traid).T
timestamp = mat(timestamp).T
userID    = mat(userID).T
rawTable  = hstack((userID, timestamp, traid))

print rawTable.shape[0]
print rawTable

for i in range(0, rawTable.shape[0]):
    print i
    if len(rawTable[i, 2]) < 5:
        rawTable[i, :] = [0]
        
print '\n\n'
print rawTable

        

