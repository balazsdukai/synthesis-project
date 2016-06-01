
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.networkanalysis import *
from qgis.gui import *
import shapefile

paths_conn = "/var/nobackup/Google_Drive/TU-Delft_GEO1101_Group-2/data/bk_map/bk_bg_paths.shp"
b_parts_conn = "/var/nobackup/Google_Drive/TU-Delft_GEO1101_Group-2/data/bk_map/bk_bg_centroid.shp"

paths = shapefile.Reader(paths_conn)
b_parts = shapefile.Reader(b_parts_conn)
paths_geom = paths.shapes()
b_parts_geom = b_parts.shapes()

# for i in range(len(paths_geom)):
#     print paths_geom[i].points
#     print paths.record(i)
#     print paths_geom[i].shapeType
#     
# for i in range(len(b_parts_geom)):
#     print b_parts_geom[i].points
#     print b_parts.record(i)
#     print b_parts_geom[i].shapeType

# print and set the prefix path
print QgsApplication.showSettings()
QgsApplication.setPrefixPath("/usr", True)
# get the available providers for reading data
QgsApplication.initQgis()
providers = QgsProviderRegistry.instance().providerList()
for provider in providers:
    print provider

paths = QgsVectorLayer(paths_conn, 'bk_bg_paths', "ogr")
if not paths:
    print "Layer failed to load!"
if not paths.isValid():
    print "Layer is not valid!"
    

# don't use information about road direction from layer attributes,
# all roads are treated as two-way
director = QgsLineVectorLayerDirector(paths, -1, '', '', '', 3)

# It is necessary then to create a strategy for calculating edge properties
properter = QgsDistanceArcProperter()

# And tell the director about this strategy
director.addProperter(properter)

# only CRS is set, all other values are defaults
crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
builder = QgsGraphBuilder(crs, topologyTolerance = 0.5)

# set the start points
print b_parts.record(0)
pStart = QgsPoint(b_parts_geom[0].points[0][0], b_parts_geom[0].points[0][1])
print b_parts.record(10)
pStop = QgsPoint(b_parts_geom[10].points[0][0], b_parts_geom[10].points[0][1])

# build the graph with tied points
tiedPoints = director.makeGraph(builder, [pStart, pStop])
graph = builder.graph()

tStart = tiedPoints[0]
tStop = tiedPoints[1]
idStart = graph.findVertex(tStart)
idStop = graph.findVertex(tStop)

(tree, costs) = QgsGraphAnalyzer.dijkstra(graph, idStart, 0)

if tree[idStop] == -1:
    print "Path not found"
else:
    p = []
    curPos = idStop
    while curPos != idStart:
        p.append(graph.vertex(graph.arc(tree[curPos]).inVertex()).point())
        curPos = graph.arc(tree[curPos]).outVertex();
    
    p.append(tStart)
    
    rb = QgsRubberBand(qgis.utils.iface.mapCanvas())
    rb.setColor(Qt.red)
    
    for pnt in p:
        rb.addPoint(pnt)