import numpy as np
import csv
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta


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
Index = 0
for Line in RawData:
    TripsPerTaxi = list(Counter(Taxi_id).items())
    Taxi_id.append(int(Line[0]))
    Trips += 1
    TripYear.append(datetime.fromtimestamp(int(Line[1])).year)
    TripMonth.append(datetime.fromtimestamp(int(Line[1])).month)
    TripDay.append(datetime.fromtimestamp(int(Line[1])).day)
    FirstDay = date(TripYear[0], 1, 1)
    DayNum.append(((date(TripYear[Index], TripMonth[Index], TripDay[Index]) - FirstDay).days + 1))
    Departure.append(int(Line[3]))
    Arrival.append(int(Line[4]))
    Index += 1
    print(Index)
    if Index >= 10000:
        break
TripsPerTaxi = list(Counter(Taxi_id).items())
TripsPerTaxi_ID = [_[0] for _ in TripsPerTaxi]
TripsPerTaxi_Num = [_[1] for _ in TripsPerTaxi]
MaxTrips = max(TripsPerTaxi_Num)
TopPerformers = [_[1] for _ in list(enumerate(TripsPerTaxi_ID)) if TripsPerTaxi_Num[_[0]] == MaxTrips]
plt.bar(TripsPerTaxi_ID, TripsPerTaxi_Num, width=1)
plt.show()
DailyTrips = list(Counter(DayNum).items())
DailyTrips_DayNum = [_[0] for _ in DailyTrips]
DailyTrips_Trips = [_[1] for _ in DailyTrips]
DailyTrips_Date = [datetime.strftime(FirstDay + timedelta(_ - 1), "%m-%d") for _ in DailyTrips_DayNum]
plt.bar(DailyTrips_DayNum, DailyTrips_Trips, width=1)
plt.show()
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
print("Unique Taxis:")
print(len(TripsPerTaxi))
print("Trips:")
print(Trips)
print("Top Performers:")
print(TopPerformers)


test = 1