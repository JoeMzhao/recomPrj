import random

def inORnot(timestamp, poolSize):
    thre = 1 - poolSize*0.2/timestamp
    buff = random.random()
    if buff < thre:
        return 1
    else:
        return 0
