import folium
import psycopg2
import datetime
#from IPython.display import HTML
import random
from math import *
import os

def getCount(bld_nr,next_bld_nr,rows):
    for i in range(len(rows)):
        if bld_nr==rows[i][0] and next_bld_nr==rows[i][1]:
            return (i,rows[i][2])
    return None
def intersect(k1,b1,k2,b2):
    x=(b2-b1)/(k1-k2)
    y=k1*x+b1
    return (x,y)
def perpendicular(k,x0,y0):
    km=-1.0/k
    b=y0+x0/k
    return (km,b)

def list2string(lst):
    # Convert dates list to single string
    string = "'{}'".format(lst[0])
    for value in lst[1:]:
        string = string + ",'" +str(value) +"'" 
    return string
def getCoordinate(startpoint,endpoint,offset):
    x0=startpoint[0]
    y0=startpoint[1]
    x1=endpoint[0]
    y1=endpoint[1]
    k= (y1-y0)/(x1-x0)
    b=y0-k*x0
    bnew=b+offset*sqrt(1+k**2)
    knew=k
    kp1=perpendicular(k,x0,y0)[0]
    bp1=perpendicular(k,x0,y0)[1]
    kp2=perpendicular(k,x1,y1)[0]
    bp2=perpendicular(k,x1,y1)[1]
    (x1,y1)=intersect(knew,bnew,kp1,bp1)
    (x2,y2)=intersect(knew,bnew,kp2,bp2)
    return [(x1,y1),(x2,y2)]

def getBuildings(rows):
    buildings={}
    for i in range(len(rows)):
        lon=rows[i][0]
        lat=rows[i][1]
        building_name=rows[i][2]
        buildings[building_name]=(lat,lon)
    return buildings
def drawBuildings(buildings,blds_from,blds_to,Map):
    for building_name in buildings:
        if building_name in blds_from or building_name in blds_to:
            marker=folium.Marker(buildings[building_name],
                  popup=building_name
                 )
            marker.add_to(Map)

def drawLines(rows,buildings,Map):
    # Line style :
    thick=35.0
    thin=5.0
    diff=rows[0][2]-rows[-1][2]
    times= (thick-thin)/(float(diff))
    coe=400000.0
    finished=[]
    # Draw lines :
    for i in range(len(rows)):
        if i in finished:
            continue
        r =random.randint(0,255)
        g = random.randint(0,255)
        b =random.randint(0,255)
        bld_nr=rows[i][0]
        next_bld_nr=rows[i][1]
        thickness=(rows[i][2]-rows[-1][2])*times+thin
        polyline=folium.PolyLine([
            [buildings[bld_nr][0],buildings[bld_nr][1]],
            [buildings[next_bld_nr][0],buildings[next_bld_nr][1]]],
        popup=bld_nr+' To '+next_bld_nr+": "+str(rows[i][2]),
        weight=thickness,
        color='rgb('+str(r)+','+str(g)+','+str(b)+')'
        ,opacity=1)
        polyline.add_to(Map)
        finished.append(i)
        if(getCount(next_bld_nr,bld_nr,rows)!=None):
            (index,count)=getCount(next_bld_nr,bld_nr,rows)
            thickness=(count-rows[-1][2])*times+thin
            newCoords=getCoordinate(buildings[next_bld_nr],buildings[bld_nr],0.00005+thickness/coe)
            polyline=folium.PolyLine([
                [newCoords[0][0],newCoords[0][1]],
                [newCoords[1][0],newCoords[1][1]]],
            popup=next_bld_nr+' To '+bld_nr+": "+str(count),
            weight=thickness,
            color='rgb('+str(r)+','+str(g)+','+str(b)+')'
            ,opacity=1)
            polyline.add_to(Map)
            finished.append(index)

def createMap(dates,blds_from,blds_to):
    
    # Connect to database
    try:
        conn = psycopg2.connect("dbname='wifi' user='team2' host='wifitracking.bk.tudelft.nl' password='AlsoSprachZ!'")
        print 'successful'
    except:
        print "I am unable to connect to the database"
    # Initialise map view
    map_osm = folium.Map(location=[51.9979838316019, 4.37410721256426],zoom_start=15)

    # Get all building locations
    cur= conn.cursor()
    cur.execute("SELECT * FROM buildings;")
    rows = cur.fetchall()
    buildings=getBuildings(rows)
    drawBuildings(buildings,blds_from,blds_to,map_osm)
        
    # Format SQL statement
    SQL="""select bld_nr,next_bld_nr,count(*)
        from individual_trajectories
        group by bld_nr,next_bld_nr
        order by count desc
        """
    cur.execute(SQL)
    rows = cur.fetchall()
    # Draw lines
    drawLines(rows,buildings,map_osm)
    # Close connection
    cur.close()
    conn.close()
    # Save the map
    map_osm.save('map.html')
    os.system('map.html')

def test():
    bld_from = ["23-CITG","21-BTUD","30-O&S","20-Aula"]
    bld_to = ["23-CITG","21-BTUD","30-O&S","20-Aula"]
    start = datetime.date(2016,04,20)
    end = datetime.date(2016,04,26)
    date=[]
    date.append(start)
    date.append(end)
    createMap(date,bld_from,bld_to)

def main(dates, bld_from, bld_to):
    createMap(dates, bld_from, bld_to)
    
    
if __name__=='__main__':
    test()
