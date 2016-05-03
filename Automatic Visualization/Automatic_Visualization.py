import psycopg2
import datetime

def main ():
    ## INPUT ##
    # From Building
    
    # To Building

    # Time interval
    


    
    # Get distinct mac addresses
    cur.execute("SELECT distinct mac \
                FROM wifilog \
                WHERE extract(day from(asstime))=19")

    # Create individual trajectorie view
    cur.execute(open("individual_trajectories.sql", "r").read())
    records = cur.fetchall()
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
