import psycopg2
import datetime

def main ():
    ## INPUT ##
    # From Building
    bld_from = "21-BTUD"
    # To Building
    bld_to = "08-BK-City"
    # Time interval

    

    # Create individual trajectorie view
    cur.execute(open("individual_trajectories.txt", "r").read())
    conn.commit()

    # Select records from specified input
    SQL =  "select * \
            from individual_trajectories \
            where bld_nr = %s \
            and next_bld_nr = %s \
            limit 10"
    data =(bld_from,bld_to,)
    cur.execute(SQL,data)
    print cur.query
    records = cur.fetchall()
    print records

    # Drop individual trajectorie view
    cur.execute("drop view individual_trajectories")
    conn.commit()

    # Close the database connection
    conn.close()


if __name__ == '__main__':
    # Create a connection object
    try:
        conn = psycopg2.connect(database="wifi", user="team2", password="AlsoSprachZ!", host="wifitracking.bk.tudelft.nl", port="5432")
        print "Opened database successfully"
    except:
        print "I'm unable to connect to the database"

    # Create cursor used for database actions
    cur = conn.cursor()
    main()
