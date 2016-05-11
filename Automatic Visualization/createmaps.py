import folium
import vincent
import psycopg2
import datetime
import json
import shutil
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

def getPopup(bld_nr,next_bld_nr,count1,count2,path):
    data={bld_nr+' To '+next_bld_nr:count1,next_bld_nr+' To '+bld_nr:count2}
    vis = vincent.Pie(data,outer_radius=70,width=50,height=50)
    vis.legend(title=bld_nr+' To '+next_bld_nr+': '+str(count1)+' , '+next_bld_nr+' To '+bld_nr+': '+str(count2))
    vis.to_json(path)

def drawBuildings(newBuildingList,buildings,Map):
    for building_name in buildings:
        if building_name in newBuildingList:
            marker=folium.Marker(buildings[building_name],
                  popup=building_name
                 )
            marker.add_to(Map)

def checkFolder(path):
    if os.path.isdir(path)==True:
        shutil.rmtree(path)
        os.makedirs(path)
    else:
        os.makedirs(path)

def drawLines(dates,rows,buildings,newBuildingList,Map):
    # Line style :
    thick=50.0
    thin=2.0
    maxCount=max(rows[0][2]*2,len(dates)*500.0)
    minCount=maxCount*0.01
    print minCount
    times= (thick-thin)/(maxCount-minCount)
    finished=[]
    # Draw lines :
    path=os.path.join(os.path.dirname(__file__), 'charts', '')
    checkFolder(path)
    for i in range(len(rows)):
        if i in finished:
            continue
        bld_nr=rows[i][0]
        next_bld_nr=rows[i][1]
        if(getCount(next_bld_nr,bld_nr,rows)!=None):
            (index,count)=getCount(next_bld_nr,bld_nr,rows)
            total=rows[i][2]+count
            if total<minCount:
                continue
            if bld_nr not in newBuildingList:
                newBuildingList.append(bld_nr)
            if next_bld_nr not in newBuildingList:
                newBuildingList.append(next_bld_nr)
            thickness=total*times+thin
            sym= fabs(rows[i][2]-count)/(rows[i][2]+count)
            r= int(255/1.0*sym)
            g= int(-200/1.0*sym)+200
            b=0
            chartPath=path+'vis'+str(i)+'.json'
            pop= getPopup(bld_nr,next_bld_nr,rows[i][2],count,chartPath)
            polyline=folium.PolyLine([
                [buildings[bld_nr][0],buildings[bld_nr][1]],
            [buildings[next_bld_nr][0],buildings[next_bld_nr][1]]],
            popup=folium.Popup(max_width=450).add_child(
            folium.Vega(json.load(open(chartPath)), width=450, height=150)),
            weight=thickness,
            color='rgb('+str(r)+','+str(g)+','+str(b)+')'
            ,opacity=1)
            polyline.add_to(Map)
            finished.append(index)
        else:
            if rows[i][2]<minCount:
                continue
            if bld_nr not in newBuildingList:
                newBuildingList.append(bld_nr)
            if next_bld_nr not in newBuildingList:
                newBuildingList.append(next_bld_nr)
            thickness=rows[i][2]*times+thin
            r =0
            g =126
            b =229
            polyline=folium.PolyLine([
            [buildings[bld_nr][0],buildings[bld_nr][1]],
            [buildings[next_bld_nr][0],buildings[next_bld_nr][1]]],
            popup=bld_nr+' To '+next_bld_nr+": "+str(rows[i][2]),
            weight=thickness,
            color='rgb('+str(r)+','+str(g)+','+str(b)+')'
            ,opacity=1)
            polyline.add_to(Map)
            finished.append(i)
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
        
    # Format SQL statement
    SQL="""select bld_nr,next_bld_nr,count(*)
        from individual_trajactories
        group by bld_nr,next_bld_nr
        order by count desc
        """
    cur.execute(SQL)
    rows = cur.fetchall()
    # Draw lines and buildings
    newBuildingList=[]
    drawLines(dates,rows,buildings,newBuildingList,map_osm)
    drawBuildings(newBuildingList,buildings,map_osm)
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
def main(dates,blds_from,blds_to):
    createMap(dates,blds_from,blds_to)
    
if __name__=='__main__':
    test()
