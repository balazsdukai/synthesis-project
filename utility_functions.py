import psycopg2

def connectDB():
    # Create a connection object
    try:
        conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!",
                                host="wifitracking.bk.tudelft.nl", port="5432")
        print("Opened database successfully")
    except:
        print("I'm unable to connect to the database")

    # This routine creates a cursor which will be used throughout of your database programming with Python.
    cur = conn.cursor()

    return conn, cur


def reconnectDB(conn):
    """
    Re-connects to the database
    :param conn: connection object
    :return: connection object, cursor object
    """
    # First close the database connection if it was open
    try:
        conn.close()
        print('Closed existing connection successfully')
    except:
        print('The connection object does not exist, create one first (HINT: use \'connectDB()\')')

    # Create a connection object
    try:
        conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!",
                                host="wifitracking.bk.tudelft.nl", port="5432")
        print("Opened database successfully")
    except:
        print("I'm unable to connect to the database")

    # This routine creates a cursor which will be used throughout of your database programming with Python.
    cur = conn.cursor()

    return conn, cur

def building_id2name(bld_id,cur):
    cur.execute('select name from buildings where id = {}'.format(bld_id))
    records = cur.fetchall()
    return records[0][0]

def buildingpart_id2name(buildingpart_id,cur):
    cur.execute('select name from buildingparts_bk where id = {}'.format(buildingpart_id))
    records = cur.fetchall()
    return records[0][0]

def apname2building_id(apname):
    #get the building id by getting the 2 characters before the second '-' in apname
    i = apname.find("-",2)
    bld_id = apname[(i-2):(i)]
    if bld_id == '12' and apname[7] == '1':
        bld_id = '13'
    if bld_id == '61':
        bld_id = '62'
    return bld_id

def apname2buildingpart_id(apname,cur):
    cur.execute('select buildingpart_id from building_part_bk where apname = {}'.format(apname))
    records = cur.fetchall()
    return records[0][0]

def getBuildingName(string):
    """
    Subsets building name from the 'maploc' field.
    :param string: the value of the 'maploc' field of a single record in the database
    :return: str - the buildingid of the respective building, parsed to be compliant with createBuildingset()
    """
    campus = 'System Campus > '
    to_replace = ["-", " ", "(", ")", "&"]

    i = string.find(campus)
    if i >= 0:
        string = string.replace(campus, '')
        e = string.find(' > ')
        string = string[:e]
    else:
        pass
    res = ''.join([i for i in string if not i.isdigit()])
    for ch in to_replace:
        if ch in res:
            res = res.replace(ch, "_")
            if "___" in res:
                res = res.replace("___", "_")
    if res[0] == "_":
        building = res[1:].lower()
        return building
    else:
        building = res.lower()
        return building

def parseBuildingId(cur, buildingTable, field):
    """
    Parses buildingnames to PostgreSQL compliant field names
    :param cur: database cursor object from psycopg2
    :param buildingTable: str - name of the table that contains the building names
    :param field: str - name of the field in the table that contains the building names
    :return: sorted list - PostgreSQL compliant field names, e.g. "50-TNW-RID" -> "tnw_rid"
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
    buildings = sorted(buildings)

    return buildings

# Example
# s0 = 'System Campus > 21-BTUD > 1e verdieping'
# s1 = 'Root Area'
# getBuildingName(s0)
# getBuildingName(s1)

