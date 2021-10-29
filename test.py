import json
from geojson import FeatureCollection
import geojsonintersect as geoJSInter

with open('input.geo.json',encoding='utf-8-sig', errors='ignore') as f:
    features = json.load(f, strict=False)["features"]
featuresCollection = FeatureCollection(features)
geoJSInter.add_junctions(featuresCollection)