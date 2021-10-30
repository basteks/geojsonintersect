import ezdxf
from geojson import LineString, Feature, FeatureCollection
import geojsonintersect as geoJSInter
import shapely.geometry as shpGeom
import geopandas as gpd
import matplotlib.pyplot as plt

## Choose which dxf file to use
dxfdoc = ezdxf.readfile('examples/EN10077_H3_window_frame.dxf')
#dxfdoc = ezdxf.readfile('examples/roof_thermal_bridge.dxf')

my_features = []
for entity in dxfdoc.entities:
    # LwPolylines recovery
    if entity.dxftype() == "LWPOLYLINE":
        ptArray = []
        for pt in entity.get_points('xy'):
            ptArray.append(pt)
        if entity.closed:
            ptArray.append(entity.get_points('xy')[0])
        if entity.closed:
            my_line = LineString(ptArray)
        else:
            my_line = LineString(ptArray)
        my_features.append(Feature(properties={"Layer": entity.dxf.layer,
                                               "SubClasses": "AcDbEntity:AcDbPolyline",
                                               "EntityHandle": entity.dxf.handle}, geometry=my_line))
    # TODO : recovering other types of entity : circles, polylines, splines, etc.

featuresCollection = FeatureCollection(my_features)
junctions = geoJSInter.add_junctions(featuresCollection)

shapelyFeatures = shpGeom.GeometryCollection([shpGeom.shape(feature["geometry"]) for feature in featuresCollection.features])
gpdGeom = gpd.GeoDataFrame({'geometry':shapelyFeatures})

fig = plt.figure() 
ax = fig.gca()
for geom in gpdGeom.geometry:
    x, y = geom.xy
    ax.plot(x, y, color='#999999', linewidth=1, solid_capstyle='round', zorder=1)
for pt in junctions:
    plt.scatter(x=pt.coords[0][0], y=pt.coords[0][1], marker='o', c='red', s=10, zorder=2)
ax.axis('scaled')
plt.show()