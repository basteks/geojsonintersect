import shapely.geometry as shpGeom

def cutAtPoint(feature, cuttingPoint):
    print(f"cutting at point ({cuttingPoint.x},{cuttingPoint.y})")
    coords = list(feature.coords)
    found = False
    res = []
    for i, pt in enumerate(coords):
        if shpGeom.Point(pt)==cuttingPoint:
            found = True
            if i>0 and i<len(coords)-1:
                res =  [
                    shpGeom.LineString(coords[:i+1]),
                    shpGeom.LineString(coords[i:])
                    ]
                return res
            else:
                return [feature]
        elif not found:
            if i<len(coords)-1 and shpGeom.LineString((shpGeom.Point(pt),shpGeom.Point(coords[i+1]))).contains(cuttingPoint):
                res =  [
                    shpGeom.LineString(coords[:i+1] + [(cuttingPoint.x, cuttingPoint.y)]),
                    shpGeom.LineString( [(cuttingPoint.x, cuttingPoint.y)] + coords[i+1:])
                    ]
                return res

def add_junctions(featcol):
    shapelyFeatures = shpGeom.GeometryCollection([shpGeom.shape(feature["geometry"]) for feature in featcol.features])
    junctions = []
    for feature1 in shapelyFeatures:
        for feature2 in shapelyFeatures:
            if feature2!=feature1:
                featsIntersection = feature1.intersection(feature2)
                if isinstance(featsIntersection,shpGeom.multilinestring.MultiLineString):
                    if len(featsIntersection.geoms)>0:
                        for geom in list(featsIntersection.geoms):
                            for intersectionPoint in list(geom.coords):
                                try:
                                    junctions.index(shpGeom.Point(intersectionPoint))
                                except:
                                    junctions.append(shpGeom.Point(intersectionPoint))
                elif isinstance(featsIntersection,shpGeom.linestring.LineString):
                    if len(featsIntersection.coords)>0:
                        for intersectionPoint in list(featsIntersection.coords):
                            try:
                                junctions.index(shpGeom.Point(intersectionPoint))
                            except:
                                junctions.append(shpGeom.Point(intersectionPoint))
    shapelyJunctions = shpGeom.GeometryCollection(junctions)
    print(f"junctions : {shapelyJunctions}")
    newFeatures = []
    for feature in shapelyFeatures:
        tempFeatures = [feature]
        for junc in shapelyJunctions:
            for feat in tempFeatures:
                if feat.contains(junc):
                    a = cutAtPoint(feat, junc)
                    idx = tempFeatures.index(feat)
                    tempFeatures.remove(feat)
                    for elm in reversed(a):
                        tempFeatures.insert(idx, elm)
        newFeatures.append(tempFeatures)

    if len(featcol.features) == len(newFeatures):
        for elm in newFeatures:
            coords = []
            for elm2 in elm:
                for pt in list(elm2.coords):
                    try:
                        coords.index(pt)
                    except:
                        coords.append(pt)
            essai = shpGeom.LinearRing(coords)
            pts = []
            for pt in list(essai.coords):
                pts.append([pt[0],pt[1]])
            featcol.features[newFeatures.index(elm)]["geometry"]["coordinates"] = pts
            featcol.features[newFeatures.index(elm)]["geometry"]["type"] = "LineString"
            print(featcol.features[newFeatures.index(elm)])
    else:
        print('error !') # TODO : more explicit message and method to handle this case
    return junctions