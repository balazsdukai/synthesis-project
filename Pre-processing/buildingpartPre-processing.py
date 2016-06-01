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

try:
    conn = psycopg2.connect(database="wifi", user="postgres", password="M1jnwachtw00rd", host="localhost", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"
cur = conn.cursor()


def getMinTime():
    cur.execute('select min(asstime) from wifilog')
    min_time = cur.fetchall()
    return min_time[0][0] - datetime.timedelta(1)


## GLOBALS ##

# Connect to DB
#conn,cur = uf.connectDB()
# min and max time
min_time = getMinTime()
max_time = datetime.datetime.now()

sqlPath = os.getcwd() + '/sql/'

def main ():

    # Create raw states
    #createBuildingpartRawStates()

    # Create preprocessed states for buildingpart level
    createBuildingpartStates()

    # Create movements for buildingpart level
    createBuildingpartMovements()

    # Close the database connection
    conn.close()
    


def createBuildingpartRawStates():
    # Create filtered table
    print 'start creating raw buildingpart states'
    cur.execute(open(sqlPath + "buildingpartRawStates.sql", "r").read())
    conn.commit()
    print 'raw states created'

def createBuildingpartStatesEmpty():
    cur.execute(open(sqlPath + "buildingpartStatesEmpty.sql", "r").read())
    conn.commit()

def getMacs():
    cur.execute('select distinct mac from buildingpartRawStates ')
    records = cur.fetchall()
    macs = []
    for record in records:
        macs.append(record[0])
    print 'retrieved distinct mac adresses'
    
    return macs

def insertRecord(record):
    i_mac,i_bldpart,i_start,i_end = 0,1,2,3
    mac = "'{}'".format(record[i_mac])
    t_s = "'{}'::timestamp".format(record[i_start])
    t_e = "'{}'::timestamp".format(record[i_end])
    bldpart = "'{}'".format(record[i_bldpart])

    cur.execute("insert into buildingpartStates values ({},{},{},{})".format(mac,bldpart,t_s,t_e))
    conn.commit()
    
def updateBuildingField(record):
    i_mac,i_start,i_end,i_ap = 0,1,2,3 # location of columns
    cur_bldpart = uf.apname2buildingpart_id(record[i_ap],cur)
    return (record[i_mac],cur_bldpart,record[i_start],record[i_end])
    
def insertWorld(cur_rec,next_rec,gap):
    i_mac,i_bldpart,i_start,i_end = 0,1,2,3 # location of columns
    
    if gap > datetime.timedelta(0,60*60) :
        world_rec = (cur_rec[i_mac],0,cur_rec[i_end],next_rec[i_start])
        insertRecord(world_rec)

def createBuildingpartStates():
    # retrieve distinct macs
    macs = getMacs()
    # create empty table for building states
    createBuildingpartStatesEmpty()
    
    count = 0
    i_mac,i_bldpart,i_start,i_end = 0,1,2,3 # location of columns
    
    for mac in macs:
        if count%100 == 0:
            print count
        count += 1
        cur.execute("select mac,start_time,end_time,apname from buildingpartRawStates where mac='{}'".format(mac))
        records = cur.fetchall()
        cur_rec = updateBuildingField(records[0])
        
        # insert world at start
        insertRecord((cur_rec[i_mac],0,min_time,cur_rec[i_start]))

        for next_rec in records[1:-1]:
            next_rec = updateBuildingField(next_rec)
            gap = next_rec[i_start] - cur_rec[i_end]
            # insert world in the middle
            insertWorld(cur_rec,next_rec,gap)
            # grouping and inserting records
            if gap < datetime.timedelta(0,60*60) and cur_rec[i_bldpart] == next_rec[i_bldpart]:
                # group records
                cur_rec = (cur_rec[i_mac],cur_rec[i_bldpart],cur_rec[i_start],next_rec[i_end])
            else:
                # check if current record should be inserted
                if cur_rec[i_end]-cur_rec[i_start] > datetime.timedelta(0,6*60):
                    insertRecord(cur_rec)
                cur_rec = next_rec
        
        # check if last record should be inserted
        if cur_rec[i_end]-cur_rec[i_start] > datetime.timedelta(0,6*60):
            insertRecord(cur_rec)

        # insert world at end
        insertRecord((cur_rec[i_mac],0,cur_rec[i_end],max_time))
        
def createBuildingpartMovements():
    print 'start creating movements'
    cur.execute(open(sqlPath + "buildingpartMovements.sql", "r").read())
    conn.commit()
    print 'movements created'

def test():
    main()

if __name__ == '__main__':
    test()
