"""
Reference: http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/network_analysis.html
"""
# import sys
# from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.networkanalysis import *
# from qgis.gui import *

from utility_functions_sdss import *

app = QApplication([])
QgsApplication.setPrefixPath("/usr", True)
QgsApplication.initQgis()

# # Prepare processing framework 
# sys.path.append('/home/user/.qgis2/python/plugins')
# from processing.core.Processing import Processing
# Processing.initialize()
# from processing.tools import *

# import shapefile

paths_conn = "/var/nobackup/Google_Drive/TU-Delft_GEO1101_Group-2/data/bk_map/bk_bg_paths.shp"
b_parts_conn = "/var/nobackup/Google_Drive/TU-Delft_GEO1101_Group-2/data/bk_map/bk_bg_centroid.shp"

# paths = shapefile.Reader(paths_conn)
# b_parts = shapefile.Reader(b_parts_conn)
# paths_geom = paths.shapes()
# b_parts_geom = b_parts.shapes()

# for i in range(len(paths_geom)):
#     print paths_geom[i].points
#     print paths.record(i)
#     print paths_geom[i].shapeType
#     
# for i in range(len(b_parts_geom)):
#     print b_parts_geom[i].points
#     print b_parts.record(i)
#     print b_parts_geom[i].shapeType

paths = QgsVectorLayer(paths_conn, 'bk_bg_paths', "ogr")
if not paths:
    print "Layer failed to load!"
if not paths.isValid():
    print "Layer is not valid!"

b_parts = QgsVectorLayer(b_parts_conn, 'bk_bg_parts', "ogr")
if not b_parts:
    print "Layer failed to load!"
if not b_parts.isValid():
    print "Layer is not valid!"

# Get origins
origins = []
for i in b_parts.getFeatures():
    geom = i.geometry().asPoint()
    origins.append(geom)

# # don't use information about road direction from layer attributes,
# # all roads are treated as two-way
# director = QgsLineVectorLayerDirector(paths, -1, '', '', '', 3)
# 
# # It is necessary then to create a strategy for calculating edge properties
# properter = QgsDistanceArcProperter()
# 
# # And tell the director about this strategy
# director.addProperter(properter)
# 
# # only CRS is set, all other values are defaults
# crs = paths.crs()
# epsg = crs.authid()
# builder = QgsGraphBuilder(crs, False, 0.1, epsg)
# 
# # # set the start points
# # print b_parts.record(8)
# # pStart = QgsPoint(b_parts_geom[8].points[0][0], b_parts_geom[8].points[0][1])
# # print b_parts.record(10)
# # pStop = QgsPoint(b_parts_geom[10].points[0][0], b_parts_geom[10].points[0][1])
# 
# # build the graph with tied points
# tiedPoints = director.makeGraph(builder, origins)
# graph = builder.graph()
# 
# tStart = tiedPoints[6]
# tStop = tiedPoints[1]
# idStart = graph.findVertex(tStart)
# idStop = graph.findVertex(tStop)

graph, tiedPoints = makeUndirectedGraph(paths, origins)

pts = calculateRouteDijkstra(graph, tiedPoints, 0, 10, 0)

# (tree, costs) = QgsGraphAnalyzer.dijkstra(graph, 22, 0)
# 
# if tree[idStop] == -1:
#     print "Path not found"
# else:
#     p = []
#     curPos = idStop
#     while curPos != idStart:
#         p.append(graph.vertex(graph.arc(tree[curPos]).inVertex()).point())
#         curPos = graph.arc(tree[curPos]).outVertex();
#     
#     p.append(tStart)
#     
#     rb = QgsRubberBand(qgis.utils.iface.mapCanvas())
#     rb.setColor(Qt.red)
#     
#     for pnt in p:
#         rb.addPoint(pnt)
#         
# QgsApplication.exitQgis()
# QApplication.exit()


#===============================================================================
# Algorithm for shortest route network
#===============================================================================
for part in building parts:
    calculate the shortest route through the network to every other building Part
    return the routes from each part as a connection-matrix(dictionary/nested list)

def make_network (paths, startPoints, crs):
    """
    Creates a bidirectional graph from a set of connected or overlapping polylines.
    Input:
        paths: shapefile - layer with the polylines loaded into python object
        crs: int - crs for the graph, should be equal to the crs of paths. 
            Given as the crs ids in PostGIS.
        startPoints: list - start point coordinates created as [QgsPoint(x,y), ...]
    Returns:
        graph,
        tiedPoints 
    Requires:
        qgis.core, qgis.networkanalysis
    """
    # No direction is taken into consideration
    director = QgsLineVectorLayerDirector(paths, -1, '', '', '', 3)
    
    # It is necessary then to create a strategy for calculating edge properties
    properter = QgsDistanceArcProperter()
    
    # And tell the director about this strategy
    director.addProperter(properter)
    
    # only CRS is set, all other values are defaults
    CRS = QgsCoordinateReferenceSystem(crs, QgsCoordinateReferenceSystem.EpsgCrsId)
    builder = QgsGraphBuilder(CRS)
    
    # tie startPoints to the graph
    tiedPoints = director.makeGraph(builder, startPoints)
    
    # build the graph
    graph = builder.graph()
    
    return graph, tiedPoints

for part in b_parts:
    calculate the shortest route through the network to every other building Part
    return the routes from each part as a connection-matrix(dictionary/nested list)