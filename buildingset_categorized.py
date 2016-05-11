import utility_functions as uf
import buildingset as bs
import time

start_time = time.time() # for measuring approx. execution time

#conn, cur = uf.reconnectDB(conn)

def main():
    # connect and reconnect database
    conn, cur = uf.connectDB()

    buildings = bs.createBuildingsetTable(conn, cur, buildingsTable="buildings", field="buildingid", name="buildingset_v0511_test",\
                                       mac=True)

    createBs_categorized(conn, cur, sequenceTable='group_rec', id_field='mac', building_field='building', \
                      buildingsetTable='buildingset_v0504_test', building_list=buildings, mac=True, limit=5000)

    # Close the database connection
    conn.close()


def createBs_categorized(conn, cur, sequenceTable, id_field, building_field, buildingsetTable, building_list, mac=True, limit=None):
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

    Categorize the buildings based on time spent in building.
    The categories represent:
        1 = <=0.5 h/week
        2 = >0.5>=5 h/week
        3 = >5 h/week
    """
    # Testing for potential id_field name confusions
    if mac:
        if id_field == 'mac':
            identifier = 'mac'
            pass
        else:
            response = raw_input(
                "The id_field does not resemble to \'mac\', are you sure that mac-addresses are stored in the id_field? (y/n): ")
            if response == 'y':
                identifier = 'mac'
                pass
            else:
                print 'Returning from function...'
                return
    else:
        if id_field == 'username':
            identifier = 'username'
            pass
        else:
            response = raw_input(
                "The id_field does not resemble to \'username\', are you sure that usernames are stored in the id_field? (y/n): ")
            if response == 'y':
                identifier = 'username'
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

    print 'Values inserted into table \''+buildingsetTable+'\' successfully'


if __name__ == '__main__':
    main()

print("%f seconds" % (time.time() - start_time))
