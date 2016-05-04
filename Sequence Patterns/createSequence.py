import psycopg2
import datetime
import csv

def main ():
    # Get distinct mac addresses
    cur.execute("select distinct mac from group_rec")
    macs = cur.fetchall()
    print "macs fetched"
    # time threshold to define when to split a sequence; in hours
    t_split = 5.5 # hours
    sequences = createSequence(macs,t_split)
    
    # Close the database connection
    conn.close()

    
def createSequence(macs,t):
    """
    this function creates sequences from the group_rec table in the database;
    for every unique mac a sequence is created;
    if the time difference between two locations >= time threshold, a new sequence is created
    """
    threshold = datetime.timedelta(0,t*3600) # i.e in this case: 5.5 hours
    sequences = []
    i_bld,i_ts,i_te = 0,1,2 # location of items in record
    count = 0
    for mac in macs:
        print count
        mac = mac[0]
        cur.execute("select building,ts,te \
from group_rec where mac='{}'".format(mac))
        records = cur.fetchall()
        sequence = []
        for i in range(len(records)-1):
            seq_nr = getBuilding(records[i][i_bld])
            sequence.append(seq_nr)
            te1 = records[i][i_te]
            ts2 = records[i+1][i_ts]
            td = ts2 - te1
            if td > threshold:
                writeSequence(sequence)
                sequences.append(sequence)
                sequence=[]
        if len(sequence) != 0:
            writeSequence(sequence)
            sequences.append(sequence)
        count+=1

    
def getBuilding(building):
    """
    Selects the id_seq of the building, or gives 0 if the building is not in the 'buildings' table
    :param string: the value of the 'maploc' field of a single record in the database
    :return: int - the seq_id of the respective building
    """
    cur.execute("SELECT id_seq FROM buildings WHERE buildingid LIKE '%"+building+"';")
    id_seq = cur.fetchall()
    if id_seq:
        id_seq = id_seq[0][0]
    else:
        id_seq = 0
    return id_seq

def writeSequence(seq):
    i_bld,i_start,i_end = 0,1,2
    with open('sequences.txt', 'a') as f:
        for i in seq:
            f.write(str(i)+' ')
        f.write('\n') 
        

        
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
