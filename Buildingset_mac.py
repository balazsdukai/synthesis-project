import psycopg2
from collections import Counter
import csv
import pandas as pd
import utility_functions as uf



conn, cur = uf.connectDB()



conn,cur = uf.reconnectDB(conn)


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


def createBuildingsetTable(conn, cur, buildingsTable="buildings", field="buildingid", name="buildingset", mac=True):
    """
    Creates and empty table if not exists for the buildingsets in the database
    :param conn: database connection object from psycopg2
    :param cur: database cursor object from psycopg2
    :param buildingsTable: str - name of the table that contains the building names
    :param field: str - name of the field in the table that contains the building names
    :param name: str - name of the new BuildingsetTable, defaults to "buildingset
    :param mac: boolean - if True, the name of the field that contains the mac/user identifiers will be 'mac', if False it will be 'username'
    :return: list - of building names, which are also the table field names in the same order
    """
    buildings = parseBuildingId(cur, buildingsTable, field)

    #create a table with the identifier + buildingnames as fields
    if mac:
        id_field = "mac"
    else:
        id_field = "username"

    query = "create table if not exists "+name+" ("+id_field+" text,"
    for b in buildings:
        query +=  b + " smallint, "
    query = query[:-2] # remove the trailing comma from the last field name
    query += ");"
    cur.execute(query)
    cur.statusmessage
    conn.commit()

    return  buildings

buildings = createBuildingsetTable(conn, cur, buildingsTable="buildings", field="buildingid", name="buildingset", mac=True)



def createBuildingset(conn, cur, sequenceTable, id_field, building_field, buildingsetTable, mac=True, limit=None):
    """
    Loads the sequences into the database, so they can be directly used by Orange algorithms.
    :param conn: database connection object from psycopg2
    :param cur: database cursor object from psycopg2
    :param sequenceTable: str - name of the table containing the sequences
    :param id_field: str - name of the field in the sequenceTable that contains the mac/user identifiers
    :param building_field: str - name of th field in the sequenceTable that contains the building ids
    :param buildingsetTable: str - name of the empty buildingsetTable
    :param mac: boolean - if True, id_field contains mac addresses, if False the id_field contains usernames
    :param limit: int - limit the number of mac/users to be processed, defaults to no limit
    :return: nothing
    """
    # Testing for potential id_field name confusions
    if mac:
        if id_field is 'mac':
            pass
        else:
            response = raw_input(
                "The id_field does not resemble to \'mac\', are you sure that mac-addresses are stored in the id_field? (y/n): ")
            if response == 'y':
                pass
            else:
                print 'Returning from function...'
                return
    else:
        if id_field is 'username':
            pass
        else:
            response = raw_input(
                "The id_field does not resemble to \'username\', are you sure that usernames are stored in the id_field? (y/n): ")
            if response == 'y':
                pass
            else:
                print 'Returning from function...'
                return

    # Get id_field list
    cur.execute('select distinct '+id_field+' from '+sequenceTable+';')
    ids = cur.fetchall()

    # Get the visited buildings per id
    for id in ids[:limit]:
        id = id[0]
        cur.execute('select distinct '+building_field+' from '+sequenceTable+' where '+id_field+'=\''+id+'\';')
        b = cur.fetchall()
        b = [uf.getBuildingName(i[0]) for i in b]
        print b








createBuildingset(conn, cur, sequenceTable='group_rec_test', id_field='mac', building_field='building',\
                  buildingsetTable='buildingset', mac=True, limit=50)



def createBuildingset(, conn, cur, sequenceTable, buildingsetTable="buildingset",limit=50):

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
