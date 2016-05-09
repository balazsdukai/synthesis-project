import psycopg2
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import *
import numpy as np
from Tkinter import *
import createmaps as CM



# Create a connection object
try:
    conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!", host="wifitracking.bk.tudelft.nl", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"

# Create cursor used for database actions
cur = conn.cursor()


def main (blds_from,blds_to,dates):
    
    createTable(blds_from,blds_to,dates)
    CM.main(dates, blds_from, blds_to)
    barPlot(blds_from,blds_to,dates)
    dropTable()
    # Close the database connection
    conn.close()


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


def dropTable():
    # Drop individual trajectorie table
    cur.execute("drop table individual_trajectories")
    conn.commit()

def test():
    dates = [datetime.date(2016,04,25),datetime.date(2016,04,26),datetime.date(2016,04,27),datetime.date(2016,04,28),datetime.date(2016,04,29)]
    # all buildings: ['50-TNW-RID','64-HSL','66-OGZ','60-LMS','38-Cultureel Centrum','37-Sportcentrum','26-Bouwcampus','23-CITG','22-TNW-TN','VLL-LAB(TNO)','21-BTUD','20-Aula','46-P&E lab','35-Drebbelweg','45-LSL','43-EGM','34-OCP-3ME','32-OCP-IO','30-O&S','30-IKC ISD-FMVG','31-TBM','08-BK-City','03-Science Center','05-TNW-BIO','36-EWI-LB','36-EWI-HB','19-Studuitzendbureau','12-TNW-DCT','12-Kramerslab & Proeffabriek','62-LR','62-Simona']
    
    blds_from = ['50-TNW-RID','64-HSL','66-OGZ','60-LMS','38-Cultureel Centrum','37-Sportcentrum','26-Bouwcampus','23-CITG','22-TNW-TN','VLL-LAB(TNO)','21-BTUD','20-Aula','46-P&E lab','35-Drebbelweg','45-LSL','43-EGM','34-OCP-3ME','32-OCP-IO','30-O&S','30-IKC ISD-FMVG','31-TBM','08-BK-City','03-Science Center','05-TNW-BIO','36-EWI-LB','36-EWI-HB','19-Studuitzendbureau','12-TNW-DCT','12-Kramerslab & Proeffabriek','62-LR','62-Simona']
    blds_to = ['50-TNW-RID','64-HSL','66-OGZ','60-LMS','38-Cultureel Centrum','37-Sportcentrum','26-Bouwcampus','23-CITG','22-TNW-TN','VLL-LAB(TNO)','21-BTUD','20-Aula','46-P&E lab','35-Drebbelweg','45-LSL','43-EGM','34-OCP-3ME','32-OCP-IO','30-O&S','30-IKC ISD-FMVG','31-TBM','08-BK-City','03-Science Center','05-TNW-BIO','36-EWI-LB','36-EWI-HB','19-Studuitzendbureau','12-TNW-DCT','12-Kramerslab & Proeffabriek','62-LR','62-Simona']
    main(blds_from,blds_to,dates)


if __name__ == '__main__':
    test()
    
