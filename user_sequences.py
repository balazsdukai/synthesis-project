import psycopg2

# Create a connection object
try:
    conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!", host="wifitracking.bk.tudelft.nl", port="5432")
    print "Opened database successfully"
except:
    print "I'm unable to connect to the database"

# This routine creates a cursor which will be used throughout of your database programming with Python.
cur = conn.cursor()


def getTime(item):
    return item[2] # location of the timestamp in a record

def getBuilding(string):
    s = string.find(">") + 2
    e = string.find(">", s) - 1
    return string[s:e]

# # Get records by unique username
# def getUsers():
#     cur.execute("SELECT distinct username from wifilog")
#     users = cur.fetchall()
#     print "Users fetched"
#     return users

cur.execute("select * from usernames;")
users = cur.fetchall()

def sequenceUsers(users, limit=50):
    """
    Create sequences of unique usernames from WiFi record.
    :param users: unique usernames returned by getUsers()
    :param limit: limit the nr. of users to  sequence
    :return: [(username,[sequence of buildings]), ...]
    """
    maploc = 4 # location of the 'maploc' field
    sequences = []
    for i in users[ :limit]:
        username = i[0]
        cur.execute("select * from wifilog where username='" + username + "';")
        user = cur.fetchall()
        user_sorted = sorted(user, key=getTime)  # sort records by datetime
        seq = []
        for i in user:
            s = getBuilding(i[maploc])
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