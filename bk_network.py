"""
Reference: http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/network_analysis.html
"""
from qgis.core import *
from qgis.networkanalysis import *

# paths = 
# b_parts =

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
pStart = points of the buildingparts come here
tiedPoint = director.makeGraph(builder, [pStart])
pStart = tiedPoint[0]

# build the graph
graph = builder.graph()

idStart = graph.findVertex(pStart)

(tree, costs) = QgsGraphAnalyzer.dijkstra(graph, idStart, 0)

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