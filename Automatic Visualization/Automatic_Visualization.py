import psycopg2
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import *
import numpy as np

def main ():
    ## INPUT ##
    # From Building
    bld_from = "21-BTUD"
    # To Building
    bld_to = "20-Aula"
    # Time interval
    start = datetime.datetime(2016,04,25,4,0,0)
    end = datetime.datetime(2016,04,26,4,0,0)
    
    # Create individual trajectories view
    cur.execute(open("individual_trajectories.sql", "r").read(),(start,end,bld_from,bld_to))
    conn.commit()

    
    
    '''start_interval = start
    # Create time series of movement
    times = []
    movements = []
    while start_interval < end:
        end_interval = start_interval + datetime.timedelta(0,60*60)
        # Count people moving from A to B at time
        SQL =  "select count(*) \
                from individual_trajectories \
                where end_time-((end_time-start_time)/2) < %s \
                and end_time-((end_time-start_time)/2) > %s"
        data =(start_interval,time)
        cur.execute(SQL,data)
        movement = cur.fetchall()
        times.append(time)
        movements.append(movement[0][0])
        start_interval = end_interval

    # Bar plot
    #plt.plot(times, movements)
    #plt.bar(times,movements)

    N = len(times)
    ind = np.arange(N)
    fig, ax = plt.subplots()
    width = 0.5
    bars = ax.bar(ind, movements, width)
    plt.show()'''

    

    # Drop individual trajectorie view
    #cur.execute("drop table individual_trajectories")
    #conn.commit()

    # Close the database connection
    conn.close()


if __name__ == '__main__':
    # Create a connection object
    try:
        conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!", host="wifitracking.bk.tudelft.nl", port="5432")
        print "Opened database successfully"
    except:
        print "I'm unable to connect to the database"

    # Create cursor used for database actions
    cur = conn.cursor()
    main()
