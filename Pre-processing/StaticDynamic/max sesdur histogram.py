import psycopg2
import datetime
import csv
import matplotlib.pyplot as plt
import numpy as np

def main ():
    # Get distinct mac addresses
    cur.execute("select mac,count(*), max(sesdur) \
                from wifilog \
                group by mac \
                having count(*) > 20")
                
    records = cur.fetchall()
    print "macs fetched"


    # Group records on building level and time
    data = maxSesdur(records)
    
    # Close the database connection
    conn.close()

def maxSesdur(records):
    data = []
    for record in records:
        maxSes = record[2]
        maxHour = maxSes.seconds / 3600.0
        if maxHour < 7:
            data.append(maxHour)
    histogram(data)

def histogram(data):
    plt.hist(data)
    plt.title("Histogram")
    plt.xlabel("max sesdur (hour)")
    plt.ylabel("Frequency")
    plt.show()
    #fig = plt.gcf()
    
    
    




if __name__ == '__main__':
    # Create a connection object

    try:
        conn = psycopg2.connect(database="wifi", user="postgres", password="geomatics", host="localhost", port="5432")
        print "Opened database successfully"
    except:
        print "I'm unable to connect to the database"

    # This routine creates a cursor which will be used throughout of your database programming with Python.
    cur = conn.cursor()
    main()
