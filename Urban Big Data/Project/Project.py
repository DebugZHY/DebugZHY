import csv
import os
import numpy as np
from collections import Counter
from datetime import datetime

for i in range(2001, 2023):
    File = open('Chicago_Crimes_{}.csv'.format(i), 'r')
    RawData = csv.reader(File)
    Type = []
    Location = []
    Arrest = []
    Time = []
    Month = []
    Hour = []
    Weekday = []
    Index = 0
    for Line in RawData:
        if Index >= 1:
            Type.append(Line[5])
            Location.append(Line[7])
            Arrest.append(Line[8])
            tMonth = int(Line[2][0:2])
            tDay = int(Line[2][3:5])
            tYear = int(Line[2][6:10])
            tHour = int(Line[2][11:13])
            if Line[2][-2] == "P":
                tHour += 12
            tDate = datetime(tYear, tMonth, tDay)
            tWeekday = tDate.weekday()
            Month.append(tMonth)
            Hour.append(tHour)
            Weekday.append(tWeekday)
        Index += 1
        print("{}: {}".format(i, Index))
    File.close()

    TypeCount = list(Counter(Type).items())
    TypeCount = sorted(TypeCount, key=lambda i: i[1], reverse=True)
    LocationCount = list(Counter(Location).items())
    LocationCount = sorted(LocationCount, key=lambda i: i[1], reverse=True)
    MonthCount = list(Counter(Month).items())
    MonthCount = sorted(MonthCount, key=lambda i: i[0])
    HourCount = list(Counter(Hour).items())
    HourCount = sorted(HourCount, key=lambda i: i[0])
    WeekdayCount = list(Counter(Weekday).items())
    WeekdayCount = sorted(WeekdayCount, key=lambda i: i[0])

    Path = os.getcwd()
    FileName = "{}\\Result-{}.txt".format(Path, i)
    File = open(FileName, 'w')
    File.write("\nType\n\n")
    for i in range(len(TypeCount)):
        File.write("{:<50}{}\n".format(TypeCount[i][0], TypeCount[i][1]))
    File.write("\nLocation\n\n")
    for i in range(len(LocationCount)):
        File.write("{:<50}{}\n".format(LocationCount[i][0], LocationCount[i][1]))
    File.write("\nMonth\n\n")
    for i in range(len(MonthCount)):
        File.write("{:<50}{}\n".format(MonthCount[i][0], MonthCount[i][1]))
    File.write("\nHour\n\n")
    for i in range(len(HourCount)):
        File.write("{:<50}{}\n".format(HourCount[i][0], HourCount[i][1]))
    File.write("\nWeekday\n\n")
    for i in range(len(WeekdayCount)):
        File.write("{:<50}{}\n".format(WeekdayCount[i][0], WeekdayCount[i][1]))
    File.close()