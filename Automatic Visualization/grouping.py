import psycopg2
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import *
import numpy as np
from Tkinter import *
#import createmaps as CM
import csv
import folium

import os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))
import utility_functions as uf
import time




# Create a connection object

try:
    conn = psycopg2.connect(database="wifi", user="postgres", password="geomatics", host="localhost", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"

"""
try:
    conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!", host="wifitracking.bk.tudelft.nl", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"
"""
# Create cursor used for database actions
cur = conn.cursor()

## GLOBAlS ##
START = time.time()
cur.execute('select min(asstime) from wifilog')
min_time = cur.fetchall()
min_time = min_time[0][0] - datetime.timedelta(1)
max_time = datetime.datetime.now()


def main (blds_from,blds_to,dates):

    createFiltered(dates)
    fillAndGroup(dates)


    # createTable(blds_from,blds_to,dates)
    # CM.main(dates, blds_from, blds_to)
    # barPlot(blds_from,blds_to,dates)
    #dropTable('filtered')
    # Close the database connection
    conn.close()

def getMacs():
    cur.execute('select distinct mac from filtered')
    records = cur.fetchall()
    macs = []
    for record in records:
        macs.append(record[0])
    print 'retrieved distinct mac adresses'
    
    return macs

def createGrouped():
    cur.execute(open("groupedAll.sql", "r").read())
    conn.commit()

def insertRecord(record):
    i_mac,i_bld,i_start,i_end, i_aps, i_ape = 0,1,2,3,4,5
    mac = "'{}'".format(record[i_mac])
    t_s = "'{}'::timestamp".format(record[i_start])
    t_e = "'{}'::timestamp".format(record[i_end])
    bld = "'{}'".format(record[i_bld])
    ap_s = "'{}'".format(record[i_aps])
    ap_e = "'{}'".format(record[i_ape])
    #with open('insertGrouped.csv', 'ab') as f:
        #writer = csv.writer(f)
        #writer.writerow([mac, bld, t_s, t_e, ap_s, ap_e])

    cur.execute("insert into groupedAll values ({},{},{},{},{},{})".format(mac,bld,t_s,t_e,ap_s,ap_e))
    conn.commit()

def createFiltered(dates):
    str_dates = list2string(dates)
    # Create filtered table
    cur.execute(open("filterAll.sql", "r").read().format(str_dates,str_dates))
    conn.commit()
    print 'filtered table created'
    
def updateBuildingField(record):
    i_mac,i_bld,i_start,i_end,i_ap = 0,1,2,3,4 # location of columns
    cur_bld = uf.getBuildingName(record[i_bld])
    return (record[i_mac],cur_bld,record[i_start],record[i_end],record[i_ap],record[i_ap],record[i_ap])
    
def insertWorld(cur_rec,next_rec,gap):
    
    i_mac,i_bld,i_start,i_end,i_aps,i_ape = 0,1,2,3,4,5 # location of columns
    
    if gap > datetime.timedelta(0,60*50) :
        world_rec = (cur_rec[i_mac],'world',cur_rec[i_end],next_rec[i_start],'NULL','NULL')
        insertRecord(world_rec)

def fillAndGroup(dates):
    macs = getMacs()
    createGrouped()
    

    
    
    count = 0
    i_mac,i_bld,i_start,i_end,i_aps,i_ape = 0,1,2,3,4,5 # location of columns
    
    for mac in macs:
        if count%100 == 0:
            print count
        count += 1
        cur.execute("select mac,maploc,start_time,end_time,apname from filtered where mac='{}'".format(mac))
        records = cur.fetchall()
        cur_rec = updateBuildingField(records[0])
        
        # insert world at start
        insertRecord((cur_rec[i_mac],'world',min_time,cur_rec[i_start],'NULL','NULL'))

        
        for next_rec in records[1:-1]:
            next_rec = updateBuildingField(next_rec)
            gap = next_rec[i_start] - cur_rec[i_end]

            # insert world in the middle
            insertWorld(cur_rec,next_rec,gap)

            # grouping and inserting records
            if gap < datetime.timedelta(0,17*60) and cur_rec[i_bld] == next_rec[i_bld]:
                # group records
                cur_rec = (cur_rec[i_mac],cur_rec[i_bld],cur_rec[i_start],next_rec[i_end],cur_rec[i_aps],next_rec[i_aps])
            else:
                # check if current record should be inserted
                if cur_rec[i_end]-cur_rec[i_start] > datetime.timedelta(0,15*60):
                    insertRecord(cur_rec)
                cur_rec = next_rec
        

        # check if last record should be inserted
        if cur_rec[i_end]-cur_rec[i_start] > datetime.timedelta(0,15*60):
            insertRecord(cur_rec)

        # insert world at end
        insertRecord((cur_rec[i_mac],'world',cur_rec[i_end],max_time,'NULL','NULL'))
        


def barPlot(blds_from,blds_to,dates):
    n_days = len(dates)
    movements = []
    n_hours = 24
    hours = np.arange(n_hours)
    for hour in hours:
        SQL =  "select count(*) \
                from individual_trajectories \
                where extract(hour from end_time-(end_time-start_time)/2) = {}".format(str(hour))
        cur.execute(SQL,str(hour))
        movement = cur.fetchall()
        movements.append(float(movement[0][0])/n_days)

    # Bar plot
    fig, ax = plt.subplots()
    width = 0.9
    bars = ax.bar(hours, movements, width,color = '#00a6d6',edgecolor = 'none')
    ax.set_ylabel('People')
    ax.set_xlabel('Hour of the day')
    ax.set_title('Movement from %s to %s on %s' % (list2string(blds_from),list2string(blds_to),list2string(dates)))
    ax.set_xticks(hours + (width/2))
    ax.set_xticklabels(hours, rotation=45, ha='center')
    plt.show()
    

def dropTable(name):
    # Drop filtered table
    cur.execute("drop table {}".format(name))
    conn.commit()
    print 'table {} dropped'.format(name)

   
def createTable(blds_from,blds_to,dates):
    str_dates = list2string(dates)
    str_blds_from = list2string(blds_from)
    str_blds_to = list2string(blds_to)
    
    # Create individual trajectories table
    cur.execute(open("individual_trajectories.sql", "r").read().format(str_dates,str_dates,str_dates,str_blds_from,str_blds_to))
    conn.commit()
    
def list2string(lst):
    # Convert dates list to single string
    string = "'{}'".format(lst[0])
    for value in lst[1:]:
        string = string + ",'" +str(value) +"'" 
    return string

def test():
    dates = [datetime.date(2016,04,25),datetime.date(2016,04,26)]
    # all buildings: ['50-TNW-RID','64-HSL','66-OGZ','60-LMS','38-Cultureel Centrum','37-Sportcentrum','26-Bouwcampus','23-CITG','22-TNW-TN','VLL-LAB(TNO)','21-BTUD','20-Aula','46-P&E lab','35-Drebbelweg','45-LSL','43-EGM','34-OCP-3ME','32-OCP-IO','30-O&S','30-IKC ISD-FMVG','31-TBM','08-BK-City','03-Science Center','05-TNW-BIO','36-EWI-LB','36-EWI-HB','19-Studuitzendbureau','12-TNW-DCT','12-Kramerslab & Proeffabriek','62-LR','62-Simona']
    
    blds_from = ['50-TNW-RID','64-HSL','66-OGZ','60-LMS','38-Cultureel Centrum','37-Sportcentrum','26-Bouwcampus','23-CITG','22-TNW-TN','VLL-LAB(TNO)','21-BTUD','20-Aula','46-P&E lab','35-Drebbelweg','45-LSL','43-EGM','34-OCP-3ME','32-OCP-IO','30-O&S','30-IKC ISD-FMVG','31-TBM','08-BK-City','03-Science Center','05-TNW-BIO','36-EWI-LB','36-EWI-HB','19-Studuitzendbureau','12-TNW-DCT','12-Kramerslab & Proeffabriek','62-LR','62-Simona']
    blds_to = ['50-TNW-RID','64-HSL','66-OGZ','60-LMS','38-Cultureel Centrum','37-Sportcentrum','26-Bouwcampus','23-CITG','22-TNW-TN','VLL-LAB(TNO)','21-BTUD','20-Aula','46-P&E lab','35-Drebbelweg','45-LSL','43-EGM','34-OCP-3ME','32-OCP-IO','30-O&S','30-IKC ISD-FMVG','31-TBM','08-BK-City','03-Science Center','05-TNW-BIO','36-EWI-LB','36-EWI-HB','19-Studuitzendbureau','12-TNW-DCT','12-Kramerslab & Proeffabriek','62-LR','62-Simona']
    main(blds_from,blds_to,dates)


if __name__ == '__main__':
    test()
