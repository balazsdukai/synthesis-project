import psycopg2
import datetime
import csv
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))
import utility_functions as uf



def main():
    cur.execute("select distinct mac from g2_buildingstates")
    macs = cur.fetchall()
    print "macs fetched"
    t_split = 5.5 # hours
    createTraject(macs,t_split)

    conn.close()

def createTraject(macs, t):
    iMac, iBld, iTs, iTe = 0,1,2,3 # location of items in records table
    trajectories = []
    count = 0
    for mac in macs:
        count += 1
        print count
        mac = mac[0]
        cur.execute(
            "select * \
            from g2_buildingstates \
            where mac='{}' \
            order by ts".format(mac))
        records = cur.fetchall()

        traject = []
        threshold = datetime.timedelta(0,t*3600) # i.e in this case: 5.5 hours
        for i in range(len(records)-1):
            seq_nr = records[i][iBld]
            traject.append(seq_nr)
            if records[i+1][iBld] == 0:
                te = records[i+1][iTe]
                ts = records[i+1][iTs]
                td = te - ts
                if td > threshold:
                    traject.append(records[i+1][iBld])
                    writeTraject(traject)
                    trajectories.append(traject)
                    traject = []
                
                    


def writeTraject(traject):
    with open('trajectories.txt', 'a') as f:
        for i in traject:
            f.write(str(i)+' ')
        f.write('\n') 
        
        


if __name__ == '__main__':
    # Create a connection object
    conn, cur = uf.connectDB()
    main()
