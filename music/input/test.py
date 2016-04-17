import csv
import numpy as np
from numpy import *
from operator import itemgetter, attrgetter, methodcaller

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

for i in range(0, rawTable.shape[0]):
	if len(rawTable[i, 2]) < 5:
		rawTable[i, :] = [0]

b = np.array(rawTable).tolist()
c = sorted(b, key=lambda b: b[1])


for i in range(0, len(c)):
	c[i][1] = int(c[i][1]) - 1230989282000
	print c[i]

		

