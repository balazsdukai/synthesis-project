import psycopg2
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import *
import numpy as np
from Tkinter import *
import createmaps as CM
import csv

import os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))
import utility_functions as uf



# Create a connection object
try:
    conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!", host="wifitracking.bk.tudelft.nl", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"

# Create cursor used for database actions
cur = conn.cursor()


def main (blds_from,blds_to,dates):



    str_dates = list2string(dates)
    # Create filtered table
    cur.execute(open("filtered2.sql", "r").read().format(str_dates,str_dates))
    records = cur.fetchall()
    print 'filtered records selected'



    
    #createFiltered(dates)
    #fillAndGroup()
    
    # createTable(blds_from,blds_to,dates)
    # CM.main(dates, blds_from, blds_to)
    # barPlot(blds_from,blds_to,dates)
    # dropTable('filtered')
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
    cur.execute(open("grouped.sql", "r").read())
    conn.commit()

def insertRecord(mac,record):
    i_bld,i_start,i_end, i_aps, i_apt = 0,1,2,3,4
    t_s = "'{}'::timestamp".format(record[i_start])
    t_e = "'{}'::timestamp".format(record[i_end])
    mac = "'{}'".format(mac)
    bld = "'{}'".format(record[i_bld])
    ap_s = "'{}'".format(record[i_aps])
    ap_e = "'{}'".format(record[i_apt])
    #with open('insertGrouped.csv', 'ab') as f:
    #    writer = csv.writer(f)
    #    writer.writerow([mac, bld, t_s, t_e, ap_s, ap_e])

    #cur.execute("insert into grouped values ({},{},{},{},{},{})".format(mac,bld,t_s,t_e,ap_s,ap_e))
    #conn.commit()
    

def fillAndGroup():
    macs = getMacs()
    createGrouped()



    i_bld,i_start,i_end,i_ap = 0,1,2,3 # location of the 'maploc' field
    sequences = []
    count = 0
    for mac in macs:
        print count
        cur.execute("select maploc,start_time,end_time,apname from filtered where mac='{}'".format(mac))
        records = cur.fetchall()
        
        cur_bld = uf.getBuildingName(records[0][i_bld])
        cur_rec = (cur_bld,records[0][i_start],records[0][i_end],records[0][i_ap],records[0][i_ap])
        
        for i in range(len(records)-2):
            next_bld = uf.getBuildingName(records[i+1][i_bld])
            next_rec = (next_bld,records[i+1][i_start],records[i+1][i_end],records[i+1][i_ap],records[i+1][i_ap])
            
            
            gap = next_rec[i_start] - cur_rec[i_end]
            if gap > datetime.timedelta(0,60*60):
                gap_rec = ('world',cur_rec[i_end],next_rec[i_start],None,None)
                insertRecord(mac,gap_rec)
            
            if gap < datetime.timedelta(0,17*60) and cur_bld == next_bld:
                cur_rec = (cur_rec[i_bld],cur_rec[i_start],next_rec[i_end],cur_rec[i_ap],next_rec[i_ap])
            else:
                if cur_rec[i_end]-cur_rec[i_start] > datetime.timedelta(0,15*60):
                    insertRecord(mac,cur_rec)
                cur_rec = next_rec
                cur_bld = cur_rec[i_bld]

        if cur_rec[i_end]-cur_rec[i_start] > datetime.timedelta(0,15*60):
            insertRecord(mac,cur_rec)
        count += 1

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

def createFiltered(dates):
    str_dates = list2string(dates)
    # Create filtered table
    print str_dates
    cur.execute(open("filtered.sql", "r").read().format(str_dates,str_dates))
    conn.commit()
    print 'table filtered created'

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
