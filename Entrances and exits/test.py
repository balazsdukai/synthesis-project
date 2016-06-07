import psycopg2
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import *
import numpy as np
import csv
import time
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))
import utility_functions as uf



times = []
time = datetime.time(0,0,0)

def addMins(tm, mins):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    print fulldate
    fulldate = fulldate + datetime.timedelta(minutes=mins)
    print fulldate
    print type(fulldate)
    print fulldate.time()
    return fulldate.time()

for i in range(12):
    times.append(time)
    time = addMins(time,120)
    #print time
#print len(times)
#print type(times[0])




#times = [0.0,2.0,4.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0,22.0]
#print len(times)
startCounts = [0.0,0.0,0.0,10.0,10.0,10.0,10.0,20.0,20.0,20.0,10.0,0.0]
print len(startCounts)
plt.plot(times, startCounts, color='b')
plt.show()
