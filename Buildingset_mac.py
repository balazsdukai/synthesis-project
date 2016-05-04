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

def parseBuildingId(cur, buildingTable, field):
    """
    Parses buildingnames to PostgreSQL compliant field names
    :param cur: database cursor object from psycopg2
    :param buildingTable: str - name of the table that contains the building names
    :param field: str - name of the field in the table that contains the building names
    :return: list - PostgreSQL compliant field names
    """
    # get the buildingnames without the building numbers on the front (e.g. "50-TNW-RID" -> "TNW_RID")
    cur.execute("select " + field + " from " + buildingTable + ";")
    x = cur.fetchall()
    # buildings = [i[0] for i in buildings]
    buildings = []
    for b in x:
        res = ''.join([i for i in b[0] if not i.isdigit()])
        for ch in ["-", " ", "(", ")", "&"]:
            if ch in res:
                res = res.replace(ch, "_")
                if "___" in res:
                    res = res.replace("___", "_")
        if res[0] == "_":
            buildings.append(res[1:].lower())
        else:
            buildings.append(res.lower())

    return buildings


def createBuildingsetTable(conn, cur, buildingTable="buildings", field="buildingid", name="buildingset"):
    """
    Creates and empty table if not exists for the buildingsets in the database
    :param conn: database connection object from psycopg2
    :param cur: database cursor object from psycopg2
    :param buildingTable: str - name of the table that contains the building names
    :param field: str - name of the field in the table that contains the building names
    :param name: str - name of the new BuildingsetTable, defaults to "buildingset
    :return: list - of building names, which are also the table field names in the same order
    """
    buildings = parseBuildingId(cur, buildingTable, field)

    #create a table with the mac + buildingnames as fields
    query = "create table if not exists "+name+" (mac text,"
    for b in buildings:
        query +=  b + " smallint, "
    query = query[:-2] # remove the trailing comma from the last field name
    query += ");"
    cur.execute(query)
    conn.commit()

    return  buildings

buildings = createBuildingsetTable(conn, cur, buildingTable="buildings", field="buildingid", name="buildingset")


def createBuildingset(macs, limit=50):
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
                #user_sequence.append(int(count[b]))
                user_sequence.append(1)
            else:
                user_sequence.append('?')
        buildingset_df.append(user_sequence)

    return buildingset_df


# create index on mac addresses
cur.execute("create index i_" + name + "_mac on " + name + " (mac);")
conn.commit()


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
