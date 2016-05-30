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
    conn = psycopg2.connect(database="postgres", user="postgres", password="204138Koanui", host="localhost", port="5432")
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

def main ():

    # Create raw states
    createBuildingRawStates()

    # Create preprocessed states for building level
    createBuildingStates()

    # Create movements for building level
    createBuildingMovements()

    # Close the database connection
    conn.close()
    


def createBuildingRawStates():
    # Create filtered table
    print 'start creating raw states'
    cur.execute(open(sqlPath + "buildingRawStates.sql", "r").read())
    conn.commit()
    print 'raw states created'

def createBuildingStatesEmpty():
    cur.execute(open(sqlPath + "buildingStatesEmpty.sql", "r").read())
    conn.commit()

def getMacs():
    cur.execute('select distinct mac from buildingRawStates')
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

def createBuildingStates():
    # retrieve distinct macs
    macs = getMacs()
    # create empty table for building states
    createBuildingStatesEmpty()
    
    count = 0
    i_mac,i_bld,i_start,i_end,i_aps,i_ape = 0,1,2,3,4,5 # location of columns
    
    for mac in macs:
        if count%100 == 0:
            print count
        count += 1
        cur.execute("select mac,start_time,end_time,apname from buildingRawStates where mac='{}'".format(mac))
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
        
def createBuildingMovements():
    print 'start creating movements'
    cur.execute(open(fpath + "buildingMovements.sql", "r").read())
    conn.commit()
    print 'movements created'

def test():
    main()

if __name__ == '__main__':
    test()
