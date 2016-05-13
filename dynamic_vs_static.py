import psycopg2
import matplotlib.pyplot as plt
import numpy as np
import math
import numpy as np

# Create a connection object
try:
    conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!", host="wifitracking.bk.tudelft.nl", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"

# This routine creates a cursor which will be used throughout of your database programming with Python.
cur = conn.cursor()


cur.execute("select * \
            from ( \
            SELECT mac, \
            count(distinct(apname)),\
            sum(sesdur) as joe, \
            count(distinct(apname)) / (extract(hour from sum(sesdur))*60 + extract(minute from sum(sesdur))) as ratio \
            from wifilog \
            group by mac \
            limit 1000) as sub \
            where joe > time '08:00:00'")
data = [x[3] for x in cur.fetchall()]
print data

plt.figure(facecolor='white')

bins = 10
plt.hist(data, bins, rwidth=0.9, facecolor = '#00A6D6', edgecolor = 'None')

plt.xlabel('ratio')
plt.ylabel('frequency')
plt.title('histogram')
plt.grid(True)


plt.show()

   
# Close the database connection
conn.close()
    




# NOTE!!!
#connection.commit()
#This method commits the current transaction. 
#If you don't call this method, anything you did since the last call to commit() 
#is not visible from other database connections.




