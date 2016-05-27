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



'''try:
    conn = psycopg2.connect(database="wifi", user="postgres", password="geomatics", host="localhost", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"
cur = conn.cursor()'''


def getMinTime():
    cur.execute('select min(asstime) from wifilog')
    min_time = cur.fetchall()
    return min_time[0][0] - datetime.timedelta(1)


## GLOBALS ##

# Connect to DB
conn,cur = uf.connectDB()
# min and max time
min_time = getMinTime()
max_time = datetime.datetime.now()

sqlPath = os.getcwd() + '/sql/'

def main (blds_from,blds_to,dates):
    createRawStates()

    createBuildingStates(dates)

    #createMovements(blds_from,blds_to,dates)

    #CM.main(dates, blds_from, blds_to)
    #barPlot(blds_from,blds_to,dates)

    # Close the database connection
    conn.close()
    


def createRawStates():
    # Create filtered table
    print 'start creating raw states'
    cur.execute(open(sqlPath + "rawStates.sql", "r").read())
    conn.commit()
    print 'raw states created'

def createBuildingStatesEmpty():
    cur.execute(open(sqlPath + "buildingStatesEmpty.sql", "r").read())
    conn.commit()

def getMacs():
    cur.execute('select distinct mac from rawStates')
    records = cur.fetchall()
    macs = []
    for record in records:
        macs.append(record[0])
    print 'retrieved distinct mac adresses'
    
    return macs

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

    cur.execute("insert into buildingStates values ({},{},{},{},{},{})".format(mac,bld,t_s,t_e,ap_s,ap_e))
    conn.commit()


    
def updateBuildingField(record):
    i_mac,i_start,i_end,i_ap = 0,1,2,3 # location of columns
    cur_bld = uf.apname2id(record[i_ap])
    return (record[i_mac],cur_bld,record[i_start],record[i_end],record[i_ap],record[i_ap])
    
def insertWorld(cur_rec,next_rec,gap):
    i_mac,i_bld,i_start,i_end,i_aps,i_ape = 0,1,2,3,4,5 # location of columns
    
    if gap > datetime.timedelta(0,60*60) :
        world_rec = (cur_rec[i_mac],0,cur_rec[i_end],next_rec[i_start],'NULL','NULL')
        insertRecord(world_rec)

def createBuildingStates(dates):
    # retrieve distinct macs
    macs = getMacs()
    # create empty table for building states
    createBuildingStatesEmpty()
    
    count = 0
    i_mac,i_bld,i_start,i_end,i_aps,i_ape = 0,1,2,3,4,5 # location of columns
    
    for mac in macs:
        #if count%100 == 0:
        print count
        count += 1
        cur.execute("select mac,start_time,end_time,apname from rawStates where mac='{}'".format(mac))
        records = cur.fetchall()
        cur_rec = updateBuildingField(records[0])
        
        # insert world at start
        insertRecord((cur_rec[i_mac],0,min_time,cur_rec[i_start],'NULL','NULL'))

        for next_rec in records[1:-1]:
            next_rec = updateBuildingField(next_rec)
            gap = next_rec[i_start] - cur_rec[i_end]
            # insert world in the middle
            insertWorld(cur_rec,next_rec,gap)
            # grouping and inserting records
            if gap < datetime.timedelta(0,60*60) and cur_rec[i_bld] == next_rec[i_bld]:
                # group records
                cur_rec = (cur_rec[i_mac],cur_rec[i_bld],cur_rec[i_start],next_rec[i_end],cur_rec[i_aps],next_rec[i_aps])
            else:
                # check if current record should be inserted
                if cur_rec[i_end]-cur_rec[i_start] > datetime.timedelta(0,6*60):
                    insertRecord(cur_rec)
                cur_rec = next_rec
        
        # check if last record should be inserted
        if cur_rec[i_end]-cur_rec[i_start] > datetime.timedelta(0,6*60):
            insertRecord(cur_rec)

        # insert world at end
        insertRecord((cur_rec[i_mac],0,cur_rec[i_end],max_time,'NULL','NULL'))
        


def barPlot(blds_from,blds_to,dates):
    n_days = len(dates)
    movements = []
    mov_from_to_world = []
    n_hours = 24
    hours = np.arange(n_hours)
    for hour in hours:
        SQL =  "select count(*) \
                from trajectories \
                where from_bld != 0 and to_bld != 0 and extract(hour from end_time-(end_time-start_time)/2) = {}".format(str(hour))
        cur.execute(SQL,str(hour))
        movementb = cur.fetchall()
        movements.append(float(movementb[0][0])/n_days)
        SQL = "select count(*) \
                from trajectories \
                where (from_bld = 0 or to_bld = 0) and extract(hour from end_time-(end_time-start_time)/2) = {}".format(str(hour))
        cur.execute(SQL, str(hour))
        movementw = cur.fetchall()
        mov_from_to_world.append(float(movementw[0][0])/n_days)
    #print n_days
    #print movements
    #print mov_from_to_world
    # Bar plot
    fig, ax = plt.subplots()
    width = 0.9
    bar1 = ax.bar(hours, movements, width,color = '#00a6d6',edgecolor = 'none')
    bar2 = ax.bar(hours, mov_from_to_world, width,color = '#6ebbd5',edgecolor = 'none', bottom=movements)

    #ax.set_ylim((0,4000))
    ax.set_ylabel('People')
    ax.set_xlabel('Hour of the day')
    ax.set_title('Movement from %s to %s on %s' % (list2string(blds_from),list2string(blds_to),list2string(dates)))
    ax.set_xticks(hours + (width/2))
    ax.set_xticklabels(hours, rotation=45, ha='center')
    plt.show()

   
def createMovements():
    print 'start creating movements'
    # Create individual trajectories table
    cur.execute(open(fpath + "buildingMovements.sql", "r").read())
    conn.commit()
    print 'movements created'
    
def list2string(lst):
    # Convert dates list to single string
    string = "'{}'".format(lst[0])
    for value in lst[1:]:
        string = string + ",'" +str(value) +"'" 
    return string

def test():
    dates = [datetime.date(2016,04,25),datetime.date(2016,04,26)]
    # all buildings: ['50-TNW-RID','64-HSL','66-OGZ','60-LMS','38-Cultureel Centrum','37-Sportcentrum','26-Bouwcampus','23-CITG','22-TNW-TN','VLL-LAB(TNO)','21-BTUD','20-Aula','46-P&E lab','35-Drebbelweg','45-LSL','43-EGM','34-OCP-3ME','32-OCP-IO','30-O&S','30-IKC ISD-FMVG','31-TBM','08-BK-City','03-Science Center','05-TNW-BIO','36-EWI-LB','36-EWI-HB','19-Studuitzendbureau','12-TNW-DCT','12-Kramerslab & Proeffabriek','62-LR','62-Simona']
    # all buildings: ['drebbelweg','cultureel_centrum','tnw_bio','ocp_me','me','studuitzendbureau','tnw_tn','world','tnw_dct','vliegtuighal','lms','ewi_hb','aula','o_s','btud','ogz','kramerslab_proeffabriek','tbm','bk_city','egm','sportcentrum','tnw_rid','vll_lab_tno_','citg','science_center','lr','ocp_me_old','bouwcampus','ikc_isd_fmvg','ocp_io','simona','hsl','ewi_lb','lsl','p_e_lab']
    # all buildings: [0, 3, 5, 8, 12, 12, 19, 20, 21, 22, 23, 26, 30, 30, 31, 32, 34, 35, 36, 36, 37, 38, 43, 45, 46, 50, 60, 62, 62, 64, 66, 99]
    blds_from = [0, 3, 5, 8, 12, 12, 19, 20, 21, 22, 23, 26, 30, 30, 31, 32, 34, 35, 36, 36, 37, 38, 43, 45, 46, 50, 60, 62, 62, 64, 66, 99]
    blds_to = [0, 3, 5, 8, 12, 12, 19, 20, 21, 22, 23, 26, 30, 30, 31, 32, 34, 35, 36, 36, 37, 38, 43, 45, 46, 50, 60, 62, 62, 64, 66, 99]
    main(blds_from,blds_to,dates)


if __name__ == '__main__':
    test()
