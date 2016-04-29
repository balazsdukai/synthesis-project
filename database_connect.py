import psycopg2

# Create a connection object
try:
    conn = psycopg2.connect(database="wifi", user="guest", password="welcome", host="wifitracking.bk.tudelft.nl", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"

# This routine creates a cursor which will be used throughout of your database programming with Python.
cur = conn.cursor()

<<<<<<< HEAD
## Get all table names in DB
#cur.execute("SELECT table_name FROM information_schema.tables\
#       WHERE table_schema = 'public'")
#for table in cur.fetchall():
#    print(table)

## Get all column names in 'wifilog' table
#cur.execute("SELECT * FROM wifilog LIMIT 0")
#colnames = [desc[0] for desc in cur.description]
#print colnames

## Nr. of rows in the table
#cur.execute("SELECT count(*) FROM wifilog")
#rows = cur.fetchall()
#print rows
#print rows[0]
#print rows[0][0] # to access the value

cur.execute("SELECT distinct mac from wifilog")
macs = cur.fetchall()
print "macs fetched"

for mac in range(len(macs)):
    
    print mac

# Close the database connection
conn.close()

# NOTE!!!
#connection.commit()
#This method commits the current transaction. 
#If you don't call this method, anything you did since the last call to commit() 
#is not visible from other database connections.
=======
# Get all table names in DB
cur.execute("SELECT table_name FROM information_schema.tables\
       WHERE table_schema = 'public'")
for table in cur.fetchall():
    print(table)

# Get all column names in 'wifilog' table
cur.execute("SELECT * FROM wifilog LIMIT 0")
colnames = [desc[0] for desc in cur.description]
print colnames




<<<<<<< HEAD
>>>>>>> parent of a85286b... update with simple SQL query
=======
>>>>>>> parent of a85286b... update with simple SQL query


