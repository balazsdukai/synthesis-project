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

def main (blds_from,blds_to,dates, types):
    data = filterMovements(blds_from,blds_to,dates, types)
    CM.main(dates, blds_from, blds_to)
    barPlot(blds_from,blds_to,dates, types)
    # Close the database connection
    conn.close()

def filterMovements(blds_from,blds_to,dates, types):
    cur.execute(open(sqlPath + "buildingMovements.sql", "r").read().format(list2string(blds_from), list2string(blds_to), list2string(dates), list2string(types)))
    conn.commit()

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

def test():
    dates = [datetime.date(2016,04,25),datetime.date(2016,04,26)]
    # all buildings: ['50-TNW-RID','64-HSL','66-OGZ','60-LMS','38-Cultureel Centrum','37-Sportcentrum','26-Bouwcampus','23-CITG','22-TNW-TN','VLL-LAB(TNO)','21-BTUD','20-Aula','46-P&E lab','35-Drebbelweg','45-LSL','43-EGM','34-OCP-3ME','32-OCP-IO','30-O&S','30-IKC ISD-FMVG','31-TBM','08-BK-City','03-Science Center','05-TNW-BIO','36-EWI-LB','36-EWI-HB','19-Studuitzendbureau','12-TNW-DCT','12-Kramerslab & Proeffabriek','62-LR','62-Simona']
    # all buildings: ['drebbelweg','cultureel_centrum','tnw_bio','ocp_me','me','studuitzendbureau','tnw_tn','world','tnw_dct','vliegtuighal','lms','ewi_hb','aula','o_s','btud','ogz','kramerslab_proeffabriek','tbm','bk_city','egm','sportcentrum','tnw_rid','vll_lab_tno_','citg','science_center','lr','ocp_me_old','bouwcampus','ikc_isd_fmvg','ocp_io','simona','hsl','ewi_lb','lsl','p_e_lab']
    # all buildings: [0, 3, 5, 8, 12, 12, 19, 20, 21, 22, 23, 26, 30, 30, 31, 32, 34, 35, 36, 36, 37, 38, 43, 45, 46, 50, 60, 62, 62, 64, 66, 99]
    blds_from = [0, 3, 5, 8]#, 12, 12, 19, 20, 21, 22, 23, 26, 30, 30, 31, 32, 34, 35, 36, 36, 37, 38, 43, 45, 46, 50, 60, 62, 62, 64, 66, 99]
    blds_to = [0, 3, 5, 8]#, 12, 12, 19, 20, 21, 22, 23, 26, 30, 30, 31, 32, 34, 35, 36, 36, 37, 38, 43, 45, 46, 50, 60, 62, 62, 64, 66, 99]
    types = ["mobile"]
    main(blds_from,blds_to,dates, types)


if __name__ == '__main__':
    test()
