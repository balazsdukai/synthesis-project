import psycopg2
import matplotlib.pyplot as plt
import numpy as np
import math
import numpy as np
from Tkinter import *

# Create a connection object
try:
    conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!", host="wifitracking.bk.tudelft.nl", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"

# This routine creates a cursor which will be used throughout of your database programming with Python.
cur = conn.cursor()

###DROPDOWN MENU####
cur.execute("SELECT distinct(bld_nr) FROM exit_count")
options = [x[0] for x in cur.fetchall()] #list of buildings)

master = Tk()
master.geometry("%dx%d+%d+%d" % (250, 80, 200, 150))
master.title("Select a building")

var = StringVar(master)
var.set(options[0]) # initial value
option = OptionMenu(master, var, *options)
option.pack(side = 'left',padx=10, pady=10)
#option.pack(side='left', padx=10, pady=10)



def ok():
    plt.close() #close plot if open
    bld = var.get()
    
    width = 0.9
    limit = 10

    ###   ENTRANCE   ###
    
    cur.execute("SELECT * FROM entrance_cnt where next_bld_nr = '{}'".format(bld))
    entr_result = cur.fetchall() #list of tuples (bld name, apname, nr of scans)

    entr_values = [x[2] for x in entr_result] #list of tuples (bld name, apname, nr of scans)
    entr_labels = [x[1] for x in entr_result] #list of tuples (bld name, apname, nr of scans)
    N = len(entr_values)
    x = np.arange(N)

    plt.figure(figsize=(15,12),facecolor='white')
    
    ax = plt.subplot(2,1,1)

    rects1 = ax.bar(x[0:limit], entr_values[0:limit], width, color='r', edgecolor='none')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Number of scans')
    ax.set_xlabel('Name of access point')
    ax.set_title('Number of entrance scans {}'.format(bld))
    
    ax.set_xticks(x[0:limit] + (0.5*width))
    ax.set_xticklabels(entr_labels[0:limit], rotation=30, ha='right')


    ###   EXIT   ###

    cur.execute("SELECT * FROM exit_count where bld_nr = '{}'".format(bld))
    exit_result = cur.fetchall() #list of tuples (bld name, apname, nr of scans)

    exit_values = []
    exit_labels = []
    for item in exit_result:
        exit_values.append(item[2])
        exit_labels.append(item[1])

    N = len(exit_values)
    exit_array = np.arange(N)

    ax = plt.subplot(2,1,2) #axes and figure

    rects2 = ax.bar(exit_array[0:limit], exit_values[0:limit], width, color='b', edgecolor='none')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Number of scans')
    ax.set_xlabel('Name of access point')
    ax.set_title('Number of exit scans {}'.format(bld))
    
    ax.set_xticks(x[0:limit] + (0.5*width))
    ax.set_xticklabels(exit_labels[0:limit], rotation=30, ha='right')

    plt.tight_layout()
    plt.show()

    master.quit()
    # Close the database connection
    conn.close()
    
# use button to run def ok()    
button = Button(master, text="Go!", command=ok)
button.pack(side='right', padx=10, pady=10)



# NOTE!!!
#connection.commit()
#This method commits the current transaction. 
#If you don't call this method, anything you did since the last call to commit() 
#is not visible from other database connections.


mainloop()


