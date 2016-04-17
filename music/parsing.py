# -*- coding: utf-8 -*-
#
# parsing the text.

import re
import os
from itertools import groupby


def read_data(path):
    with open(path, "r") as r:
        return [re.split(",", l.strip("\n")) for l in r.readlines()]

# by groupby
def groupby_data(data, path):
    try:
        os.remove(path)
    except OSError:
        pass

    # really crucial, otherwise the code will be wrong
    data = sorted(data, key=lambda x: x[2])

    with open(path, "a") as w:
        count = 0
        mapping = []
        for key, group in groupby(data, lambda x: x[2]):
            mapping.append([key, str(count)])
            for d in group:
                w.write(d[0] + "," + d[1] + "," + str(count) + "\n")
            count += 1

    with open(path + "_mapping", "w") as toFile:
        out = "\n".join(map(lambda m: m[0] + "\t" + m[1], mapping))
        toFile.write(out)


# by dictionary
def map_to_unique(data, path):
    try:
        os.remove(path)
    except OSError:
        pass

    mydict = {}
    with open(path, "a") as w:
        for line in data:
            if line[2] not in mydict:
                mydict[line[2]] = str(len(mydict) + 1)
            w.write(line[0] + "," + line[1] + "," + mydict[line[2]])

    with open(path + "_mapping", "w") as toFile:
        out = "\n".join(map(lambda m: m[0] + "\t" + m[1], mydict.items()))
        toFile.write(out)

if __name__ == '__main__':
    in_path = "trimed.csv"
    out_path = "parsed"
    data = read_data(in_path)
    groupby_data(data, out_path)
