"""GeoJSONIntersect

This module allows the user to deal with the conversion between
GeoJSON and TopoJSON. It helps the user to manage the points of
self-intersection of his geometry, ensuring that they will be
identified as junctions for the GeoJSON to TopoJSON conversion.

Requirements
------------
This module requires that `shapely`, `geojson`, `geopandas` and
`matplotlib` be installed within the Python environment you are
importing this module into.

It contains the following functions:

    * cut_at_point - splits a feature at the cuttingPoint
    * add_junctions - the main function of the script
"""

import shapely.geometry as shpGeom
import geopandas as gpd
import matplotlib.pyplot as plt

verbose = False

def cut_at_point(feature, cuttingPoint):
    """Split a feature at the cuttingPoint

    Parameters
    ----------
    feature : shapely.geometry.linestring.LineString
        The object you would like to split at the junction point 
    cuttingPoint : shapely.geometry.point.Point
        The junction point

    Returns
    -------
    res : [shapely.geometry.linestring.LineString]
        The list of features obtained once feature as been split-
        ted at the junction point
    """
    if verbose:
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
    """Modify a complete geometry to integrate every junction
    points in each feature

    Parameters
    ----------
    featcol : geojson.feature.FeatureCollection
        The feature collection containing the whole geometry

    Returns
    -------
    junctions : [shapely.geometry.point.Point]
        The list of identified junction points
    """
    def append_junction(junctions,junc):
        """Add the points of junc to junctions, depending on the
        type of the junc object

        Parameters
        ----------
        junctions : [shapely.geometry.point.Point]
            The list of junction points to complete
        junc : shapely.geometry. ...
            A shapely geometry to decompose into a list of points

        Returns
        -------
        junctions : [shapely.geometry.point.Point]
            The list of identified junction points
        """
        if isinstance(junc,shpGeom.multilinestring.MultiLineString):
            if len(junc.geoms)>0:
                for geom in list(junc.geoms):
                    for intersectionPoint in list(geom.coords):
                        try:
                            junctions.index(shpGeom.Point(intersectionPoint))
                        except:
                            junctions.append(shpGeom.Point(intersectionPoint))
        elif isinstance(junc,shpGeom.linestring.LineString):
                    if len(junc.coords)>0:
                        for intersectionPoint in list(junc.coords):
                            try:
                                junctions.index(shpGeom.Point(intersectionPoint))
                            except:
                                junctions.append(shpGeom.Point(intersectionPoint))
        elif isinstance(junc,shpGeom.point.Point):
                    try:
                        junctions.index(junc)
                    except:
                        junctions.append(junc)
        elif isinstance(junc,shpGeom.collection.GeometryCollection):
                    for geom in junc:
                        append_junction(junctions,geom)
        
    shapelyFeatures = shpGeom.GeometryCollection([shpGeom.shape(feature["geometry"]) for feature in featcol.features])
    junctions = []
    for feature1 in shapelyFeatures:
        for feature2 in shapelyFeatures:
            if feature2!=feature1:
                featsIntersection = feature1.intersection(feature2)
                append_junction(junctions,featsIntersection)
    shapelyJunctions = shpGeom.GeometryCollection(junctions)
    if verbose:
        print(f"junctions : {shapelyJunctions}")
    newFeatures = []
    for feature in shapelyFeatures:
        tempFeatures = [feature]
        for junc in shapelyJunctions:
            for feat in tempFeatures:
                if feat.contains(junc):
                    a = cut_at_point(feat, junc)
                    idx = tempFeatures.index(feat)
                    tempFeatures.remove(feat)
                    for elm in reversed(a):
                        tempFeatures.insert(idx, elm)
        newFeatures.append(tempFeatures)

    if len(featcol.features) == len(newFeatures): # Need to handle the else case ?
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
            if verbose :
                print(featcol.features[newFeatures.index(elm)])
    return junctions

def plot_geometry(featcol, junctions):
    """Plot the whole geometry with the junction points visible

    Parameters
    ----------
    featcol : geojson.feature.FeatureCollection
        The feature collection containing the whole geometry
    junctions : [shapely.geometry.point.Point]
        A list of junction points
    """
    shapelyFeatures = shpGeom.GeometryCollection([shpGeom.shape(feature["geometry"]) for feature in featcol.features])
    
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
