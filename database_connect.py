import psycopg2

# Create a connection object
try:
    conn = psycopg2.connect(database="wifi", user="guest", password="welcome", host="wifitracking.bk.tudelft.nl", port="5432")
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






