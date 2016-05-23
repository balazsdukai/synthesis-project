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
apname = 'A-08-J-005'

###EXIT###
SQL =  "select extract(hour from te), count(*) \
        from groupedall \
        where ap_start = '{}' \
        and not (extract(month from te) = 4 and extract(day from te) = 22) \
        and not (extract(month from te) = 4 and extract(day from te) = 23) \
        group by extract(hour from te) \
        order by extract(hour from te);".format(apname)
cur.execute(SQL)

result = cur.fetchall()

for i in range(24):
    if i not in [x[0] for x in result]:
        item = i,0
        result.insert(i,item)

values = [x[1] for x in result]
print values


fig,ax = plt.subplots()
fig.patch.set_facecolor('white')
width = 0.35

n_hours = 24
hours = np.arange(n_hours)
print hours

# Bar plot #1
bars = ax.bar(hours+width, values, width,color = 'red',edgecolor = 'none')
#6ebbe5

###ENTRANCE###
SQL =  "select extract(hour from ts), count(*) \
        from groupedall \
        where ap_start = '{}' \
        and not (extract(month from ts) = 4 and extract(day from ts) = 22) \
        and not (extract(month from ts) = 4 and extract(day from ts) = 23) \
        group by extract(hour from ts) \
        order by extract(hour from ts);".format(apname)
cur.execute(SQL)

result1 = cur.fetchall()

for i in range(24):
    print i
    if i not in [x[0] for x in result1]:
        item = i,0
        print 'yes'
        result1.insert(i,item)

values1 = [x[1] for x in result1]

# Bar plot #2
bars1 = ax.bar(hours, values1, width,color = '#00a6d6',edgecolor = 'none')










ax.set_ylabel('Frequency')
ax.set_xlabel('Hour of the day')
ax.set_title('Frequency of access point: {}'.format(apname))
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




