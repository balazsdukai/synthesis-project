import psycopg2
import matplotlib.pyplot as plt
from matplotlib.dates import *
import numpy as np
import math
import numpy as np
import datetime
import time

# Create a connection object
try:
    conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!", host="wifitracking.bk.tudelft.nl", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"
# This routine creates a cursor which will be used throughout of your database programming with Python.
cur = conn.cursor()

apname = 'A-08-J-005'

def startCounts():

    startCounts = []
    times = []
    time = datetime.time(0,0,0)
        
    for i in range(0,60*24/5): #iterate over time, every 5 min
        if i%100 == 0:
            print time
        SQL =  "select count(*) \
            from groupedall \
            where ap_start = '{}' \
            and not (extract(month from te) = 4 and extract(day from te) = 22) \
            and not (extract(month from te) = 4 and extract(day from te) = 23) \
            and ts::time  > '{}' - interval '10 minutes' \
            and ts::time < '{}' + interval '10 minutes'".format(apname, str(time),str(time))
            
        cur.execute(SQL)
        count = cur.fetchall()
        print count
        if count == []:
            startCounts.append(0.0)
        else:
            startCounts.append(float(count[0][0]))
        times.append(time)
        time = addMins(time,5)
        print time
    #print type(times)
    #print times[0]
    #print times
    #print type(times[0])
    #print len(times)
    #print ''
    #print type(startCounts)
    #print startCounts[0]
    #print type(startCounts[0])
    #print len(startCounts)
    #print startCounts
    print 'ja?'



    plt.plot(times, startCounts, color='b')
    print 'reach?'
    lectureStart = addLectureStart()
    print 'ja maat'
    plt.title('Frequency of access point: {}'.format(apname))
    #plt.legend(handles=[start])
    styleGraph()
         
             
def addMins(tm, mins):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    #print fulldate
    fulldate = fulldate + datetime.timedelta(minutes=mins)
    #print fulldate
    return fulldate.time()

def addLectureStart():
    # add the start of each lecture as a vertical line
    lectureStart = plt.axvline((60*60*8)+(45*60),color='k',linestyle='--',label='start lecture')
    plt.axvline((60*60*10)+(45*60),color='k',linestyle='--')
    plt.axvline((60*60*12)+(45*60),color='k',linestyle='--')
    plt.axvline((60*60*13)+(45*60),color='k',linestyle='--')
    plt.axvline((60*60*15)+(45*60),color='k',linestyle='--')
    plt.axvline((60*60*17)+(45*60),color='k',linestyle='--')
    return lectureStart

def styleGraph():
    plt.xlim((60*60*6,24*60*60))
    plt.ylabel('Frequency')
    plt.xlabel('Time')
    min45 = 45*60
    hour = 60*60
    lectureTimes = [6*hour+min45,8*hour+min45,10*hour+min45,12*hour+min45,13*hour+min45,15*hour+min45,17*hour+min45,19*hour+min45,21*hour+min45,23*hour+min45]
    plt.xticks( lectureTimes )
    plt.gca().set_xticklabels(['6:45','8:45','10:45','12:45','13:45','15:45','17:45','19:45','21:45','23:45'])
    print 'whatsup'
    plt.show()


def main():
    print 'start main'
    startCounts()
    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()

# NOTE!!!
#connection.commit()
#This method commits the current transaction. 
#If you don't call this method, anything you did since the last call to commit() 
#is not visible from other database connections.
