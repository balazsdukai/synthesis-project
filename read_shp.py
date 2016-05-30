import shapefile

sf = shapefile.Reader("C:/Users/KEVIN3/Downloads/bk_bg_centroid.shp")
shapes = sf.shapes()

for i in range(len(shapes)):
    
    print shapes[i].points
    print sf.record(i)
    print shapes[i].shapeType


