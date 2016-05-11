import utility_functions as uf
import time

start_time = time.time() # for measuring approx. execution time

#conn, cur = uf.reconnectDB(conn)

def main():
    # connect and reconnect database
    conn, cur = uf.connectDB()

    buildings = createBuildingsetTable(conn, cur, buildingsTable="buildings", field="buildingid", name="buildingset_v0504_test",\
                                       mac=True)

    createBuildingset(conn, cur, sequenceTable='group_rec', id_field='mac', building_field='building', \
                      buildingsetTable='buildingset_v0504_test', building_list=buildings, mac=True, limit=5000)

    # Close the database connection
    conn.close()


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



def createBuildingset(conn, cur, sequenceTable, id_field, building_field, buildingsetTable, building_list, mac=True, limit=None):
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
        if id_field == 'mac':
            identifier = 'mac'
            pass
        else:
            response = input(
                "The id_field does not resemble to \'mac\', are you sure that mac-addresses are stored in the id_field? (y/n): ")
            if response == 'y':
                identifier = 'mac'
                pass
            else:
                print('Returning from function...')
                return
    else:
        if id_field == 'username':
            identifier = 'username'
            pass
        else:
            response = input(
                "The id_field does not resemble to \'username\', are you sure that usernames are stored in the id_field? (y/n): ")
            if response == 'y':
                identifier = 'username'
                pass
            else:
                print('Returning from function...')
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

        # Parse insert query
        fieldnames = identifier
        for i in building_list:
            fieldnames += ',' + i

        values = '%('+identifier+')s'
        for i in building_list:
            values += ', ' + '%('+i+')s'

        value_dict = {}
        value_dict[identifier] = id
        for i in building_list:
            if i in b:
                value_dict[i] = 1
            else:
                value_dict[i] = None

        query = 'insert into '+buildingsetTable+' (' + fieldnames + ') values ('+values+')'
        cur.execute(query, value_dict)
        conn.commit()

    print('Values inserted into table \''+buildingsetTable+'\' successfully')


if __name__ == '__main__':
    main()

print(("%f seconds" % (time.time() - start_time)))
