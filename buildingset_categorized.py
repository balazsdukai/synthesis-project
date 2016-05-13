import utility_functions as uf
import buildingset as bs
import time
import datetime as dt

start_time = time.time() # for measuring approx. execution time

#conn, cur = uf.reconnectDB(conn)

def main():
    # connect and reconnect database
    conn, cur = uf.connectDB()

    buildings = bs.createBuildingsetTable(conn, cur, buildingsTable="buildings", field="buildingid",\
                                          name="buildingset_v0513_test", mac=True)

    createBs_categorized(conn, cur, sequenceTable='group_rec_test', id_field='mac', starttime='ts', endtime='te',\
                         building_field='building', buildingsetTable='buildingset_v0513_test',\
                         building_list=buildings, mac=True, limit=5000)

    # Close the database connection
    conn.close()


def createBs_categorized(conn, cur, sequenceTable, id_field, starttime, endtime, building_field, buildingsetTable, building_list, mac=True, limit=None):
    """
    Loads the sequences into the database, so they can be directly used by Orange algorithms.
    :param conn: database connection object from psycopg2
    :param cur: database cursor object from psycopg2
    :param sequenceTable: str - name of the table containing the sequences
    :param id_field: str - name of the field in the sequenceTable that contains the mac/user identifiers
    :param starttime: str - name of the field in the sequenceTable that contains the start time of a record
    :param endtime: str - name of the field in the sequenceTable that contains the end time of a record
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
    # define time categories
    occasional = dt.timedelta(minutes=30)
    often = dt.timedelta(hours=5)

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

    # Parse fix part of the insert query
    fieldnames = identifier
    for i in building_list:
        fieldnames += ',' + i

    values = '%(' + identifier + ')s'
    for i in building_list:
        values += ', ' + '%(' + i + ')s'

    # Get the visited buildings per id
    for id in ids[:limit]:
        id = id[0]
        # select the average time spent in a building per week
        cur.execute('SELECT '+building_field+', AVG(B.avg_time) FROM (SELECT '\
                    +building_field+', AVG(A.duration) As avg_time, nr_week FROM (SELECT '\
                    +building_field+', '+endtime+'-'+starttime+' as duration, EXTRACT(WEEK FROM '+starttime+\
                    ')::smallint as nr_week FROM '+sequenceTable+' where '+id_field+'=\''+id+'\') as A GROUP BY '\
                    +building_field+', nr_week) As B GROUP BY '+building_field+';')

        b = cur.fetchall()
        buildingname = [uf.getBuildingName(i[0]) for i in b] #TODO: add switch for getBuildingName in case the buildingnames are already converted
        buildingset = [(uf.getBuildingName(i[0]),i[1]) for i in b]

        value_dict = {}
        value_dict[identifier] = id
        for i in building_list:
            if i in buildingname:
                for k in buildingset:
                    if k[0] == i:
                        if k[1] <= occasional: # occasionally at the building
                            value_dict[i] = 1
                        elif occasional < k[1] <= often: # regularly at the building
                            value_dict[i] = 2
                        elif often < k[1]: # often at the building
                            value_dict[i] = 3
                    else:
                        pass
            else:
                value_dict[i] = None

        query = 'insert into '+buildingsetTable+' (' + fieldnames + ') values ('+values+')'
        cur.execute(query, value_dict)
        conn.commit()

    print 'Values inserted into table \''+buildingsetTable+'\' successfully'


if __name__ == '__main__':
    main()

print("%f seconds" % (time.time() - start_time))
