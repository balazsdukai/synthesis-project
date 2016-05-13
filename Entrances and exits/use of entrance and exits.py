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

SQL =  "select extract(hour from asstime), count(*) \
        from wifilog \
        where apname = 'A-20-0-045' \
        group by extract(hour from asstime) \
        order by extract(hour from asstime);"
cur.execute(SQL)
result = [x[1] for x in cur.fetchall()]
print result

plt.figure(facecolor='white')

n_hours = 24
hours = np.arange(n_hours)


# Bar plot
ax = plt.subplot()
width = 0.9
bars = ax.bar(hours, result, width,color = '#00a6d6',edgecolor = 'none')
ax.set_ylabel('Frequency')
ax.set_xlabel('Hour of the day')
ax.set_title('Bar chart')
ax.set_xticks(hours + (width/2))
ax.set_xticklabels(hours, rotation=45, ha='center')


plt.show()

   
# Close the database connection
conn.close()
    




# NOTE!!!
#connection.commit()
#This method commits the current transaction. 
#If you don't call this method, anything you did since the last call to commit() 
#is not visible from other database connections.




