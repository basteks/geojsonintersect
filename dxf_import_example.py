import ezdxf
from geojson import LineString, Feature, FeatureCollection
import geojsonintersect as geoJSInter

## Choose which dxf file to use
#dxfdoc = ezdxf.readfile('examples/test.dxf')
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
geoJSInter.plot_geometry(featuresCollection,junctions)