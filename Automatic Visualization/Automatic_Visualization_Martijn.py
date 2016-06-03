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
import createmaps as CM

conn,cur = uf.connectDB()

## GLOBALS ##
START = time.time()
cur.execute('select min(asstime) from wifilog')
min_time = cur.fetchall()
min_time = min_time[0][0] - datetime.timedelta(1)
max_time = datetime.datetime.now()
useGroupedAll = True
sqlPath = os.getcwd() + '/sql/'

def main (blds_from,blds_to,dates,types):
    #weekWeekend()
    mobileStatic()
    #fromAndToBuilding(0)
    
    # CM.main(dates, blds_from, blds_to)
    # barPlot(blds_from,blds_to,dates, types)
    # Close the database connection   
    conn.close()

def mobileStatic():
    blds_from = [0]
    blds_to = getAllBlds()
    dates = getDates('week')
    

    # get data
    types = ['mobile']
    data = filterMovements(blds_from,blds_to,dates,types,True)
    movements,times = countMovements(blds_from,blds_to,dates, types)

    types = ['static'] 
    data = filterMovements(blds_to,blds_from,dates,types,True)
    movements2,times2 = countMovements(blds_to,blds_from,dates, types)

    # plot data
    mobile, = plt.plot(times,movements,color='b',label='mobile')
    static, = plt.plot(times2,movements2,color='r',label='static')
    lectureStart = addLectureStart()

    plt.title('Mobile vs static movement')
    plt.legend(handles=[mobile,static,lectureStart])
    styleGraph()

def weekWeekend():
    blds_from = getAllBlds()
    blds_to = getAllBlds()
    types = ['mobile']

    # get data
    dates = getDates('week')
    data = filterMovements(blds_from,blds_to,dates,types,True)
    movements,times = countMovements(blds_from,blds_to,dates, types)

    dates = getDates('weekend')    
    data = filterMovements(blds_to,blds_from,dates,types,True)
    movements2,times2 = countMovements(blds_to,blds_from,dates, types)

    # plot data
    week, = plt.plot(times,movements,color='b',label='week')
    weekend, = plt.plot(times2,movements2,color='r',label='weekend')
    lectureStart = addLectureStart()

    plt.title('Movement during week and weekend')
    plt.legend(handles=[week,weekend,lectureStart])
    styleGraph()

def styleGraph():
    plt.xlim((60*60*6,24*60*60))
    plt.ylabel('Devices/hour')
    plt.xlabel('Time')
    min45 = 45*60
    hour = 60*60
    lectureTimes = [6*hour+min45,8*hour+min45,10*hour+min45,12*hour+min45,13*hour+min45,15*hour+min45,17*hour+min45,19*hour+min45,21*hour+min45,23*hour+min45]
    plt.xticks( lectureTimes )
    plt.gca().set_xticklabels(['6:45','8:45','10:45','12:45','13:45','15:45','17:45','19:45','21:45','23:45'])
    plt.show()

def fromAndToBuilding(bld_id):
    blds_from = [bld_id]
    blds_to = getAllBlds()
    dates = getDates('week')
    types = ['mobile']
    name = uf.building_id2name(bld_id,cur)
    if name == 'world':
        name = 'campus'
    fromAndToMovement(blds_from,blds_to,dates,types,name)

def fromAndToMovement(blds_from,blds_to,dates,types,name):
    # get data
    data = filterMovements(blds_from,blds_to,dates,types,False)
    movements,times = countMovements(blds_from,blds_to,dates, types)

    data = filterMovements(blds_to,blds_from,dates,types,False)
    movements2,times2 = countMovements(blds_to,blds_from,dates, types)

    # plot data
    to_campus, = plt.plot(times,movements,color='b',label='to {}'.format(name))
    from_campus, = plt.plot(times2,movements2,color='r',label='from {}'.format(name))
    lectureStart = addLectureStart()

    # style graph
    plt.title('Movement from and to {}'.format(name))
    plt.legend(handles=[to_campus,from_campus,lectureStart])
    styleGraph()
    

def filterMovements(blds_from,blds_to,dates, types,twoDirections):
    directions = '(from_bld in ({}) and to_bld in ({}))'.format(list2string(blds_from), list2string(blds_to))
    if twoDirections:
        directions = directions + 'or' + '(to_bld in ({}) and from_bld in ({}))'.format(list2string(blds_from), list2string(blds_to))
    cur.execute(open(sqlPath + "buildingMovements.sql", "r").read().format(directions, list2string(dates), list2string(types)))
    conn.commit()

def countMovements(blds_from,blds_to,dates, types):
    n_days = len(dates)
    movements = []
    times = []
    time = datetime.time(0,0,0)
    
    for i in range(0,60*24/5):
        if i%100 == 0:
            print time
        SQL =  "select count(*) \
            from buildingmovements_temp \
            where (end_time-(end_time-start_time)/2)::time  > '{}' - interval '10 minutes' \
            and (end_time-(end_time-start_time)/2)::time < '{}' + interval '10 minutes'".format(str(time),str(time))
        cur.execute(SQL)
        movement = cur.fetchall()
        if movement == []:
            movements.append(0.0)
        else:
            movements.append(float(movement[0][0])/n_days)  
        times.append(time)
        time = addMins(time,5)

    return movements,times


def addLectureStart():
    # add the start of each lecture as a vertical line
    lectureStart = plt.axvline((60*60*8)+(45*60),color='k',linestyle='--',label='start lecture')
    plt.axvline((60*60*10)+(45*60),color='k',linestyle='--')
    plt.axvline((60*60*12)+(45*60),color='k',linestyle='--')
    plt.axvline((60*60*13)+(45*60),color='k',linestyle='--')
    plt.axvline((60*60*15)+(45*60),color='k',linestyle='--')
    plt.axvline((60*60*17)+(45*60),color='k',linestyle='--')
    return lectureStart
    

def addMins(tm, mins):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(minutes=mins)
    return fulldate.time()
    

def barPlot(blds_from,blds_to,dates, types):
    n_days = len(dates)
    movements = []
    mov_from_to_world = []
    n_hours = 24
    hours = np.arange(n_hours)
    types = list2string(types)
    for hour in hours:
        # Count movements twice, once for between buildings only and once between buildings and world
        SQL =  "select count(*) \
                from buildingmovements_temp \
                where from_bld != 0 and to_bld != 0 and extract(hour from end_time-(end_time-start_time)/2) = {}".format(str(hour))
        cur.execute(SQL,str(hour))
        movementb = cur.fetchall()
        movements.append(float(movementb[0][0])/n_days)
        SQL = "select count(*) \
               from buildingmovements_temp \
               where (from_bld = 0 or to_bld = 0) and extract(hour from end_time-(end_time-start_time)/2) = {}".format(str(hour))
        cur.execute(SQL, str(hour))
        movementw = cur.fetchall()
        mov_from_to_world.append(float(movementw[0][0])/n_days)

    # Bar plot
    fig, ax = plt.subplots()
    width = 0.9
    bar1 = ax.bar(hours, movements, width,color = '#00a6d6',edgecolor = 'none')
    bar2 = ax.bar(hours, mov_from_to_world, width,color = '#6ebbd5',edgecolor = 'none', bottom=movements)

    # Change this value to set limits on the y axis
    ax.set_ylim((0,1400))
    ax.set_ylabel('People')
    ax.set_xlabel('Hour of the day')
    ax.set_title('Movement from %s to %s on %s' % (list2string(blds_from),list2string(blds_to),list2string(dates)))
    ax.set_xticks(hours + (width/2))
    ax.set_xticklabels(hours, rotation=45, ha='center')
    plt.show()
    
def list2string(lst):
    # Convert dates list to single string
    string = "'{}'".format(lst[0])
    for value in lst[1:]:
        string = string + ",'" +str(value) +"'" 
    return string

def getDates(requestedDates):
    if requestedDates == 'week':
        return [datetime.date(2016, 4, 4), datetime.date(2016, 4, 11), datetime.date(2016, 4, 18), datetime.date(2016, 4, 25), datetime.date(2016, 5, 2), datetime.date(2016, 5, 9), datetime.date(2016, 5, 16), datetime.date(2016, 5, 23), datetime.date(2016, 5, 30), datetime.date(2016, 4, 5), datetime.date(2016, 4, 12), datetime.date(2016, 4, 19), datetime.date(2016, 4, 26), datetime.date(2016, 5, 3), datetime.date(2016, 5, 10), datetime.date(2016, 5, 17), datetime.date(2016, 5, 24), datetime.date(2016, 5, 31), datetime.date(2016, 4, 6), datetime.date(2016, 4, 13), datetime.date(2016, 4, 20), datetime.date(2016, 4, 27), datetime.date(2016, 5, 4), datetime.date(2016, 5, 11), datetime.date(2016, 5, 18), datetime.date(2016, 5, 25), datetime.date(2016, 6, 1), datetime.date(2016, 3, 31), datetime.date(2016, 4, 7), datetime.date(2016, 4, 14), datetime.date(2016, 4, 21), datetime.date(2016, 4, 28), datetime.date(2016, 5, 5), datetime.date(2016, 5, 12), datetime.date(2016, 5, 19), datetime.date(2016, 5, 26), datetime.date(2016, 6, 2), datetime.date(2016, 4, 4), datetime.date(2016, 4, 11), datetime.date(2016, 4, 18), datetime.date(2016, 4, 25), datetime.date(2016, 5, 2), datetime.date(2016, 5, 9), datetime.date(2016, 5, 16), datetime.date(2016, 5, 23), datetime.date(2016, 5, 30), datetime.date(2016, 4, 5), datetime.date(2016, 4, 12), datetime.date(2016, 4, 19), datetime.date(2016, 4, 26), datetime.date(2016, 5, 3), datetime.date(2016, 5, 10), datetime.date(2016, 5, 17), datetime.date(2016, 5, 24), datetime.date(2016, 5, 31), datetime.date(2016, 4, 6), datetime.date(2016, 4, 13), datetime.date(2016, 4, 20), datetime.date(2016, 4, 27), datetime.date(2016, 5, 4), datetime.date(2016, 5, 11), datetime.date(2016, 5, 18), datetime.date(2016, 5, 25), datetime.date(2016, 6, 1), datetime.date(2016, 4, 6), datetime.date(2016, 4, 13), datetime.date(2016, 4, 20), datetime.date(2016, 4, 27), datetime.date(2016, 5, 4), datetime.date(2016, 5, 11), datetime.date(2016, 5, 18), datetime.date(2016, 5, 25), datetime.date(2016, 6, 1), datetime.date(2016, 3, 31), datetime.date(2016, 4, 7), datetime.date(2016, 4, 14), datetime.date(2016, 4, 21), datetime.date(2016, 4, 28), datetime.date(2016, 5, 5), datetime.date(2016, 5, 12), datetime.date(2016, 5, 19), datetime.date(2016, 5, 26), datetime.date(2016, 6, 2), datetime.date(2016, 4, 1), datetime.date(2016, 4, 8), datetime.date(2016, 4, 15), datetime.date(2016, 4, 22), datetime.date(2016, 4, 29), datetime.date(2016, 5, 6), datetime.date(2016, 5, 13), datetime.date(2016, 5, 20), datetime.date(2016, 5, 27)]
    elif requestedDates == 'weekend':
        return [datetime.date(2016, 4, 2), datetime.date(2016, 4, 9), datetime.date(2016, 4, 16), datetime.date(2016, 4, 23), datetime.date(2016, 4, 30), datetime.date(2016, 5, 7), datetime.date(2016, 5, 14), datetime.date(2016, 5, 21), datetime.date(2016, 5, 28), datetime.date(2016, 4, 3), datetime.date(2016, 4, 10), datetime.date(2016, 4, 17), datetime.date(2016, 4, 24), datetime.date(2016, 5, 1), datetime.date(2016, 5, 8), datetime.date(2016, 5, 15), datetime.date(2016, 5, 22), datetime.date(2016, 5, 29)]
    else:
        print 'dates not found'

def getAllBlds():
    cur.execute('select distinct id from buildings order by id')
    records = cur.fetchall()
    blds = []
    for record in records:
        blds.append(record[0])
    return blds
        

def test():
    dates = [datetime.date(2016,04,25),datetime.date(2016,04,26),datetime.date(2016,04,27),datetime.date(2016,04,28)]
    # all buildings: ['50-TNW-RID','64-HSL','66-OGZ','60-LMS','38-Cultureel Centrum','37-Sportcentrum','26-Bouwcampus','23-CITG','22-TNW-TN','VLL-LAB(TNO)','21-BTUD','20-Aula','46-P&E lab','35-Drebbelweg','45-LSL','43-EGM','34-OCP-3ME','32-OCP-IO','30-O&S','30-IKC ISD-FMVG','31-TBM','08-BK-City','03-Science Center','05-TNW-BIO','36-EWI-LB','36-EWI-HB','19-Studuitzendbureau','12-TNW-DCT','12-Kramerslab & Proeffabriek','62-LR','62-Simona']
    # all buildings: ['drebbelweg','cultureel_centrum','tnw_bio','ocp_me','me','studuitzendbureau','tnw_tn','world','tnw_dct','vliegtuighal','lms','ewi_hb','aula','o_s','btud','ogz','kramerslab_proeffabriek','tbm','bk_city','egm','sportcentrum','tnw_rid','vll_lab_tno_','citg','science_center','lr','ocp_me_old','bouwcampus','ikc_isd_fmvg','ocp_io','simona','hsl','ewi_lb','lsl','p_e_lab']
    # all buildings: [0, 3, 5, 8, 12, 12, 19, 20, 21, 22, 23, 26, 30, 30, 31, 32, 34, 35, 36, 36, 37, 38, 43, 45, 46, 50, 60, 62, 62, 64, 66, 99]
    blds_from = [0]
    blds_to = [0,3, 5, 8, 12, 12, 19, 20, 21, 22, 23, 26, 30, 30, 31, 32, 34, 35, 36, 36, 37, 38, 43, 45, 46, 50, 60, 62, 62, 64, 66, 99]
    types = ["mobile"]
    main(blds_from,blds_to,dates, types)


if __name__ == '__main__':
    test()
