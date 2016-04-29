import psycopg2

# Create a connection object
try:
    conn = psycopg2.connect(database="wifi", user="guest", password="welcome", host="wifitracking.bk.tudelft.nl", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"

# This routine creates a cursor which will be used throughout of your database programming with Python.
cur = conn.cursor()

cur.execute("SELECT distinct mac from wifilog")
macs = cur.fetchall()
print "macs fetched"

iterator = 0

cur.execute("select * from wifilog where mac='"+macs[iterator][0]+"';")
mac0 = cur.fetchall()

cur.execute("SELECT distinct username from wifilog")
users = cur.fetchall()
print "users fetched"

cur.execute("select * from wifilog where username='"+users[iterator][0]+"';")
user0 = cur.fetchall()


# Close the database connection
conn.close()

# NOTE!!!
#connection.commit()
#This method commits the current transaction.
#If you don't call this method, anything you did since the last call to commit()
#is not visible from other database connections.