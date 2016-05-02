import psycopg2
from collections import Counter
import csv
import pandas as pd

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

def getBuildingInt(string):
    """
    Selects the id_seq of the building, or gives 0 if the building is not in the 'buildings' table
    :param string: the value of the 'maploc' field of a single record in the database
    :return: int - the seq_id of the respective building
    """
    s = string.find(">") + 2
    e = string.find(">", s) - 1
    building = string[s:e]
    cur.execute("SELECT id_seq FROM buildings WHERE buildingid LIKE '%"+building+"%';")
    id_seq = cur.fetchall()
    if id_seq:
        id_seq = id_seq[0][0]
    else:
        id_seq = 0
    return id_seq

def getBuilding(string):
    """
    Selects the buildingid of the building
    :param string: the value of the 'maploc' field of a single record in the database
    :return: str - the buildingid of the respective building
    """
    s = string.find(">") + 2
    e = string.find(">", s) - 1
    building = string[s:e]
    return building

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
        u_seq = []
        #u_seq.append(username)
        #seq = ""
        for i in user_sorted:
            s = getBuilding(i[maploc])
            #seq += str(s)+','
            u_seq.append(s)
        sequences.append((username,u_seq))

    return sequences


seqs = sequenceUsers(users, 20)


def createBuildingset(users, limit=50):
    """
    Create sequences of unique usernames from WiFi record.
    :param users: unique usernames returned by getUsers()
    :param limit: limit the nr. of users to  sequence
    :return: [(username,[sequence of buildings]), ...]
    """
    cur.execute("select buildingid from buildings;")
    header = cur.fetchall()
    header = [i[0] for i in header] # list of buildingid
    header.insert(0,'username') # create header for the data frame
    buildingset_df = []
    buildingset_df.append(header) # header for the data frame

    # Extract the sequence for each user
    maploc = 4 # location of the 'maploc' field
    for i in users[ :limit]:
        username = i[0]
        cur.execute("select * from wifilog where username='" + username + "';")
        user = cur.fetchall()
        user_sorted = sorted(user, key=getTime)  # sort records by datetime
        b_seq = []
        # gets the sequence of buildings for the user
        for i in user_sorted:
            s = getBuilding(i[maploc])
            #seq += str(s)+','
            b_seq.append(s)
        # create count for each building and construct the buildingset data frame
        count = Counter(b_seq)
        user_sequence = []
        user_sequence.append(username)
        for b in header[:-1]:
            if b in count:
                user_sequence.append(int(count[b]))
            else:
                user_sequence.append(0)
        buildingset_df.append(user_sequence)

    return buildingset_df


buildingset = createBuildingset(users, 100)
buildingset_df = pd.DataFrame(buildingset[1:], columns=buildingset[0])

cur.execute("select buildingid from buildings;")
buildingid = cur.fetchall()
buildingid = [i[0] for i in buildingid]  # list of buildingid
buildingid.insert(0, 'username')

for i,n in enumerate(buildingid):
    s = 'D#'+ n
    buildingid[i] = s
buildingid[0] = 'username'
buildingset_df.columns = buildingid


# write buildingset_df into csv
buildingset_df.to_csv('buildingset.csv', index=False)


# write the test sequences into a csv
with open("seqs.csv", "wb") as f:
    fieldnames = ['username', 'sequence']
    writer = csv.writer(f)
    writer.writerow(fieldnames)
    writer.writerows(seqs)

# Close the database connection
conn.close()

# NOTE!!!
#connection.commit()
#This method commits the current transaction.
#If you don't call this method, anything you did since the last call to commit()
#is not visible from other database connections.