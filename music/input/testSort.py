import csv
import numpy as np
from   numpy import *
from operator import itemgetter, attrgetter, methodcaller

a = ['wocoa', '1', 'made']
b = ['fc', '9', 'date']
c = ['rile', '4', 'ck']

d = vstack((a, b, c))
print d
print '\n'

b = np.array(d).tolist()
c = sorted(b, key=lambda b: b[1])
print b
print c