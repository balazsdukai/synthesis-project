import psycopg2
import matplotlib.pyplot as plt
import numpy as np

# Create a connection object
try:
    conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!", host="wifitracking.bk.tudelft.nl", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"

# This routine creates a cursor which will be used throughout of your database programming with Python.
cur = conn.cursor()

# Get all table names in DB
cur.execute("SELECT table_name FROM information_schema.tables\
      WHERE table_schema = 'public'")
for table in cur.fetchall():
   print(table)

# Get all column names in 'wifilog' table
cur.execute("SELECT * FROM wifilog LIMIT 0")
colnames = [desc[0] for desc in cur.description]
print colnames

# Nr. of rows in the table
cur.execute("SELECT * FROM temp where next_bld_nr = '08-BK-City'")
test = cur.fetchall() #list of tuples (bld name, apname, nr of scans)
values = []
for item in test:
    #print item[2]
    values.append(item[2])
print values[0]
#print test[0][2]

plt.hist(values)
plt.show()
#print rows[0]
#print rows[0][0] # to access the value

# Close the database connection
conn.close()

# NOTE!!!
#connection.commit()
#This method commits the current transaction. 
#If you don't call this method, anything you did since the last call to commit() 
#is not visible from other database connections.


