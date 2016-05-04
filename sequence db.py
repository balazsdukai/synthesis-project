import psycopg2
import datetime
import csv

def main ():
    # Get distinct mac addresses
    cur.execute("select distinct mac from wifilog")
    macs = cur.fetchall()
    print "macs fetched"

    # Create a table for the grouped records
    createTable('group_rec')

    # Group records on building level and time
    seqs = groupRecords(macs)
    
    # Close the database connection
    conn.close()

def createTable(name):
    cur.execute(
                "create table if not exists group_rec(mac text NOT NULL,building text NOT NULL,\
ts timestamp without time zone NOT NULL,te timestamp without time zone NOT NULL, \
PRIMARY KEY(mac, ts));"
                )
    conn.commit()
    

def groupRecords(macs):
    i_bld,i_start,i_end = 0,1,2 # location of the 'maploc' field
    sequences = []
    for mac in macs:
        mac = mac[0]
        cur.execute("select maploc,asstime,asstime + sesdur as end_time from wifilog where mac='{}'".format(mac))
        records = cur.fetchall()

        seq = []

        cur_bld = getBuilding(records[0][i_bld])
        cur_rec = (cur_bld,records[0][i_start],records[0][i_end])
        
        for i in range(len(records)-2):
            next_bld = getBuilding(records[i+1][i_bld])
            next_rec = (next_bld,records[i+1][i_start],records[i+1][i_end])
            
            
            gap = next_rec[i_start] - cur_rec[i_end]
            if gap < datetime.timedelta(0,17*60) and cur_bld == next_bld:
                cur_rec = (cur_rec[i_bld],cur_rec[i_start],next_rec[i_end])
            else:
                if cur_rec[i_end]-cur_rec[i_start] > datetime.timedelta(0,15*60):
                    insertRecord(mac,cur_rec)
                cur_rec = next_rec
                cur_bld = cur_rec[i_bld]
        if cur_rec[i_end]-cur_rec[i_start] > datetime.timedelta(0,15*60):
            insertRecord(mac,cur_rec)



def getBuilding(string):
    """
    Selects the id_seq of the building, or gives 0 if the building is not in the 'buildings' table
    :param string: the value of the 'maploc' field of a single record in the database
    :return: int - the seq_id of the respective building
    """
    s = string.find(">") + 2
    e = string.find(">", s) - 1
    building = string[s:e]
    return building
    #cur.execute("SELECT id_seq FROM buildings WHERE buildingid LIKE '%"+building+"';")
    #id_seq = cur.fetchall()
    #if id_seq:
    #    id_seq = id_seq[0][0]
    #else:
    #    id_seq = 0
    #return id_seq

def insertRecord(mac,record):
    i_bld,i_start,i_end = 0,1,2
    t_s = "'{}'::timestamp".format(record[i_start])
    t_e = "'{}'::timestamp".format(record[i_end])
    mc = "'{}'".format(mac)
    bld = "'{}'".format(record[i_bld])
    with open('insertGroupRec.csv', 'ab') as f:
        #fieldnames = ['mac', 'building','ts','te']
        #writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer = csv.writer(f)
        #writer.writeheader()
        #writer.writerow({'mac':mc,'building':bld,'ts':t_s,'te':t_e})
        writer.writerow([mc, bld, t_s, t_e])
        
    #cur.execute("insert into group_rec values ('{}',{},'{}'::timestamp,'{}'::timestamp)".format(mac,int(record[i_bld]),record[i_start],record[i_end]))
    #cur.execute("insert into group_rec values ({},{},{},{})".format(mc,bld,ts,te))
    #conn.commit()
# NOTE!!!
#connection.commit()
#This method commits the current transaction.
#If you don't call this method, anything you did since the last call to commit()
#is not visible from other database connections.


if __name__ == '__main__':
    # Create a connection object

    try:
        conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!", host="wifitracking.bk.tudelft.nl", port="5432")
        print "Opened database successfully"
    except:
        print "I'm unable to connect to the database"

    # This routine creates a cursor which will be used throughout of your database programming with Python.
    cur = conn.cursor()
    main()
