import csv
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
from math import radians, sin, cos, atan2, sqrt
from distfit import distfit

def Haversine(Lat1, Long1, Lat2, Long2):
    Lat1, Long1, Lat2, Long2 = map(radians, [Lat1, Long1, Lat2, Long2])
    K = sin((Lat1 - Lat2) / 2) ** 2 + cos(Lat1) * cos(Lat2) * (sin((Long1 - Long2) / 2) ** 2)
    Dist = 2 * atan2(sqrt(K), sqrt(1 - K))
    return 6371 * Dist


IntersectionCoords = {}
File = open('intersections.csv', 'r')
RawData = csv.reader(File)
for Line in RawData:
    IntersectionCoords[Line[0]] = [float(Line[1]), float(Line[2])]
File.close()

File = open('taxi_id.csv', 'r')
RawData = csv.reader(File)
Taxi_id = []
TripYear = []
TripMonth = []
TripDay = []
DayNum = []
Trips = 0
Departure = []
Arrival = []
TripDistance = []
TripTime = []
Index = 0
Date1 = {"Month": 3, "Day": 11}
Date2 = {"Month": 4, "Day": 7}
Date3 = {"Month": 11, "Day": 28}
Date1TripsHour = []
Date2TripsHour = []
Date3TripsHour = []
for Line in RawData:
    Taxi_id.append(int(Line[0]))
    Trips += 1
    tDate = datetime.fromtimestamp(int(Line[1]) - 46800)
    if tDate.month == Date1["Month"] and tDate.day == Date1["Day"]:
        Date1TripsHour.append(tDate.hour)
    elif tDate.month == Date2["Month"] and tDate.day == Date2["Day"]:
        Date2TripsHour.append(tDate.hour)
    elif tDate.month == Date3["Month"] and tDate.day == Date3["Day"]:
        Date3TripsHour.append(tDate.hour)
    TripYear.append(tDate.year)
    TripMonth.append(tDate.month)
    TripDay.append(tDate.day)
    FirstDay = date(TripYear[0], 1, 1)
    DayNum.append(((date(TripYear[Index], TripMonth[Index], TripDay[Index]) - FirstDay).days + 1))
    Departure.append(int(Line[3]))
    Arrival.append(int(Line[4]))
    Lat1 = IntersectionCoords[Line[3]][0]
    Long1 = IntersectionCoords[Line[3]][1]
    Lat2 = IntersectionCoords[Line[4]][0]
    Long2 = IntersectionCoords[Line[4]][1]
    Dist = 1000 * Haversine(Lat1, Long1, Lat2, Long2)
    TripDistance.append(int(Dist))
    TripTime.append(int(Line[2]) - int(Line[1]))
    Index += 1
    print(Index)
File.close()

plt.rc('font', size=20)  # controls default text sizes
plt.rc('axes', titlesize=20)  # fontsize of the axes title
plt.rc('axes', labelsize=20)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)  # fontsize of the tick labels
plt.rc('ytick', labelsize=20)  # fontsize of the tick labels
plt.rc('legend', fontsize=20)  # legend fontsize
plt.rc('figure', titlesize=20)  # fontsize of the figure title
plt.rcParams["font.family"] = "Times New Roman"

#Q1
TripsPerTaxi = list(Counter(Taxi_id).items())
print("Unique Taxis:")
print(len(TripsPerTaxi))
print("Trips:")
print(Trips)

#Q2
TripsPerTaxi_ID = [_[0] for _ in TripsPerTaxi]
TripsPerTaxi_Num = [_[1] for _ in TripsPerTaxi]
MaxTrips = max(TripsPerTaxi_Num)
TopPerformers = [_[1] for _ in list(enumerate(TripsPerTaxi_ID)) if TripsPerTaxi_Num[_[0]] == MaxTrips]
plt.bar(TripsPerTaxi_ID, TripsPerTaxi_Num, width=2)
plt.xlabel("Taxi ID")
plt.ylabel("Trips")
plt.title("Trips per Taxi")
plt.show()
print("Top Performers:")
print(TopPerformers)

#Q3
DailyTrips = list(Counter(DayNum).items())
DailyTrips_DayNum = [_[0] for _ in DailyTrips]
DailyTrips_Trips = [_[1] for _ in DailyTrips]
DailyTrips_Date = [datetime.strftime(FirstDay + timedelta(_ - 1), "%m-%d") for _ in DailyTrips_DayNum]
plt.bar(DailyTrips_DayNum, DailyTrips_Trips, width=1)
plt.xlabel("Day in The Year")
plt.ylabel("Daily Trips")
plt.title("Daily Trip Count")
plt.show()

#Q4
DepartureTripNum = list(Counter(Departure).items())
ArrivalTripNum = list(Counter(Arrival).items())
DepartureTripNum_ID = [_[0] for _ in DepartureTripNum]
DepartureTripNum_Num = [_[1] for _ in DepartureTripNum]
ArrivalTripNum_ID = [_[0] for _ in ArrivalTripNum]
ArrivalTripNum_Num = [_[1] for _ in ArrivalTripNum]
Index = sorted(range(len(DepartureTripNum_ID)), key=lambda i: DepartureTripNum_ID[i])
DepartureTripNum_ID = sorted(DepartureTripNum_ID)
DepartureTripNum_Num = [DepartureTripNum_Num[_] for _ in Index]
Index = sorted(range(len(ArrivalTripNum_ID)), key=lambda i: ArrivalTripNum_ID[i])
ArrivalTripNum_ID = sorted(ArrivalTripNum_ID)
ArrivalTripNum_Num = [ArrivalTripNum_Num[_] for _ in Index]
plt.bar(DepartureTripNum_ID, DepartureTripNum_Num, width=2)
plt.xlabel("Intersection ID")
plt.ylabel("Depature Trips")
plt.title("Depature Trip Distribution among Intersections")
plt.show()
plt.bar(ArrivalTripNum_ID, ArrivalTripNum_Num, width=2)
plt.xlabel("Intersection ID")
plt.ylabel("Arrival Trips")
plt.title("Arrival Trip Distribution among Intersections")
plt.show()

#Q5
Date1Trips = list(Counter(Date1TripsHour).items())
Date1Trips_Hour = [_[0] for _ in Date1Trips]
Date1Trips_Num = [_[1] for _ in Date1Trips]
Date2Trips = list(Counter(Date2TripsHour).items())
Date2Trips_Hour = [_[0] for _ in Date2Trips]
Date2Trips_Num = [_[1] for _ in Date2Trips]
Date3Trips = list(Counter(Date3TripsHour).items())
Date3Trips_Hour = [_[0] for _ in Date3Trips]
Date3Trips_Num = [_[1] for _ in Date3Trips]
plt.bar(Date1Trips_Hour, Date1Trips_Num, width=1)
plt.xlabel("Hour")
plt.ylabel("Trips")
plt.title("Trip Distribution in Mar. 11")
plt.show()
plt.bar(Date2Trips_Hour, Date2Trips_Num, width=1)
plt.xlabel("Hour")
plt.ylabel("Trips")
plt.title("Trip Distribution in Apr. 7")
plt.show()
plt.bar(Date3Trips_Hour, Date3Trips_Num, width=1)
plt.xlabel("Hour")
plt.ylabel("Trips")
plt.title("Trip Distribution in Nov. 28")
plt.show()

#Q6
Dist = distfit(todf=True)
Dist.fit_transform(np.array(TripDistance))
print(Dist.model)
Dist.plot()
plt.show()
TripDistance = list(Counter(TripDistance).items())
TripDistance_Dist = [_[0] for _ in TripDistance]
TripDistance_Trips = [_[1] for _ in TripDistance]
plt.bar(TripDistance_Dist, TripDistance_Trips, width=10)
plt.xlabel("Distance (m)")
plt.ylabel("Trips")
plt.title("Trip Distance Distribution")
plt.show()

TripTime = [int(i / 60) for i in TripTime]
Dist = distfit(todf=True)
Dist.fit_transform(np.array(TripTime))
print(Dist.model)
Dist.plot()
plt.show()
TripTime = list(Counter(TripTime).items())
TripTime_Time = [_[0] for _ in TripTime]
TripTime_Trips = [_[1] for _ in TripTime]
plt.bar(TripTime_Time, TripTime_Trips, width=10)
plt.xlabel("Trip Time (min)")
plt.ylabel("Trips")
plt.title("Trip Distance Distribution")
plt.show()