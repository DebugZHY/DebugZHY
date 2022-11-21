import csv
import os
import numpy as np
from collections import Counter

for i in range(2001, 2023):
    File = open('Chicago_Crimes_{}.csv'.format(i), 'r')
    RawData = csv.reader(File)
    Type = []
    Location = []
    Arrest = []
    Index = 0
    for Line in RawData:
        if Index >= 1:
            Type.append(Line[5])
            Location.append(Line[7])
            Arrest.append(Line[8])
        Index += 1
        print("{}: {}".format(i, Index))
    File.close()

    TypeCount = list(Counter(Type).items())
    TypeCount = sorted(TypeCount, key=lambda i: i[1], reverse=True)
    LocationCount = list(Counter(Location).items())
    LocationCount = sorted(LocationCount, key=lambda i: i[1], reverse=True)

    Path = os.getcwd()
    FileName = "{}\\Result-{}.txt".format(Path, i)
    File = open(FileName, 'w')
    File.write("\nType\n\n")
    for i in range(len(TypeCount)):
        File.write("{:<50}{}\n".format(TypeCount[i][0], TypeCount[i][1]))
    File.write("\nLocation\n\n")
    for i in range(len(LocationCount)):
        File.write("{:<50}{}\n".format(LocationCount[i][0], LocationCount[i][1]))
    File.close()