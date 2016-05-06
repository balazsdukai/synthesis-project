import psycopg2
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import *
import numpy as np
from Tkinter import *



# Create a connection object
try:
    conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!", host="wifitracking.bk.tudelft.nl", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"

# Create cursor used for database actions
cur = conn.cursor()


def main (dates):
    ## INPUT ##
    # From Building
    bld_from = "21-BTUD"
    # To Building
    bld_to = "20-Aula"
    # Time interval
    start = datetime.datetime(2016,04,25,0,0,0)
    end = datetime.datetime(2016,04,26,0,0,0)
    
    
    
    createTable(bld_from,bld_to,dates)
    barPlot(bld_from,bld_to,dates)
    dropTable()

def barPlot(bld_from,bld_to,dates):
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
        movements.append(int(movement[0][0])/n_days)

    # Bar plot
    fig, ax = plt.subplots()
    width = 0.9
    bars = ax.bar(hours, movements, width,color = '#00a6d6',edgecolor = 'none')
    ax.set_ylabel('People')
    ax.set_ylabel('Hour of the day')
    ax.set_title('Movement from %s to %s on %s' % (bld_from,bld_to,datenum2string(dates)))
    ax.set_xticks(hours + (width/2))
    ax.set_xticklabels(hours, rotation=45, ha='center')
    plt.show()

   

def createTable(bld_from,bld_to,dates):
    str_dates = datenum2string(dates)
    
    # Create individual trajectories table
    cur.execute(open("individual_trajectories.sql", "r").read().format(str_dates,str_dates,str_dates,bld_from,bld_to))
    conn.commit()
    
def datenum2string(dates):
    # Convert dates list to single string
    str_dates = "'{}'".format(dates[0])
    for date in dates[1:]:
        str_dates = str_dates + ",'" +str(date) +"'" 
    return str_dates


def dropTable():
    # Drop individual trajectorie table
    cur.execute("drop table individual_trajectories")
    conn.commit()

def test():
    dates = [datetime.date(2016,04,25),datetime.date(2016,04,26),datetime.date(2016,04,27),datetime.date(2016,04,28)]
    main(dates)


if __name__ == '__main__':
    test()
    
# Close the database connection
conn.close()
