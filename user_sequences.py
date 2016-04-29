import psycopg2

# Create a connection object
try:
    conn = psycopg2.connect(database="wifi", user="guest", password="welcome", host="wifitracking.bk.tudelft.nl", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"

# This routine creates a cursor which will be used throughout of your database programming with Python.
cur = conn.cursor()

# Globals
ITERATOR = 0 # iterator used later in script
MAPLOC = 4 # location of the 'maploc' field

def getTime(item):
    return item[2] # location of the timestamp in a record


def getBuilding(string):
    s = string.find(">") + 2
    e = string.find(">", s) - 1
    return string[s:e]

# Get records by mac address
cur.execute("SELECT distinct mac from wifilog")
macs = cur.fetchall()
print "macs fetched"

cur.execute("select * from wifilog where mac='"+macs[ITERATOR][0]+"';")
mac0 = cur.fetchall()

# Get records by username
cur.execute("SELECT distinct username from wifilog")
users = cur.fetchall()
print "users fetched"

cur.execute("select * from wifilog where username='"+users[ITERATOR][0]+"';")
user0 = cur.fetchall()

user0_sorted = sorted(user0, key=getTime) # sort records by datetime
user0_seq = []
for i in user0_sorted:
    seq = getBuilding(i[MAPLOC])
    user0_seq.append(seq)

def sequenceUsers(users, limit=50):
    MAPLOC = 4 # location of the 'maploc' field
    sequences = []
    for i in users[ :limit]:
        username = i[0]
        cur.execute("select * from wifilog where username='" + username + "';")
        user = cur.fetchall()
        user_sorted = sorted(user, key=getTime)  # sort records by datetime
        seq = []
        for i in user0_sorted:
            s = getBuilding(i[MAPLOC])
            seq.append(s)
        u_seq = (username, seq)
        sequences.append(u_seq)

    return sequences

seqs = sequenceUsers(users, 20)








# Close the database connection
conn.close()

# NOTE!!!
#connection.commit()
#This method commits the current transaction.
#If you don't call this method, anything you did since the last call to commit()
#is not visible from other database connections.