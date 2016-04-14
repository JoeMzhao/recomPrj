import csv
import numpy as np
from numpy import *
from operator import itemgetter, attrgetter, methodcaller

with open('newfile.data') as f:
	cf    = csv.reader(f, delimiter = '\t')
	traid = [row[2] for row in cf]

with open('newfile.data') as f:
	cf        = csv.reader(f, delimiter = '\t')
	timestamp = [row[1] for row in cf]

with open('newfile.data') as f:
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

#for i in range(0, len(c)):
#	print c[i]

with open('stocks.csv','w') as f:
	f_csv = csv.writer(f)
	f_csv.writerows(c)
		

