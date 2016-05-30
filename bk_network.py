"""
Reference: http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/network_analysis.html
"""

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

for i in range(len(b_parts_geom)):
    print b_parts_geom[i].points
    print b_parts.record(i)
    print b_parts_geom[i].shapeType

# paths = 
# b_parts =

paths = QgsVectorLayer(paths_conn, 'bk_bg_paths', "ogr")

# don't use information about road direction from layer attributes,
# all roads are treated as two-way
director = QgsLineVectorLayerDirector(paths, -1, '', '', '', 3)

# It is necessary then to create a strategy for calculating edge properties
properter = QgsDistanceArcProperter()

# And tell the director about this strategy
director.addProperter(properter)

# only CRS is set, all other values are defaults
crs = QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem.EpsgCrsId)
builder = QgsGraphBuilder(crs)

# set the start points
pStart = QgsPoint(b_parts_geom[0].points[0][0], b_parts_geom[0].points[0][1])
tiedPoint = director.makeGraph(builder, [pStart])
pStart = tiedPoint[0]

# build the graph
graph = builder.graph()

idStart = graph.findVertex(pStart)

(tree, costs) = QgsGraphAnalyzer.dijkstra(graph, idStart, 0)

tree = QgsGraphAnalyzer.shortestTree(graph, idStart, 0)

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