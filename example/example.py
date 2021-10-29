import json
from geojson import FeatureCollection
import geojsonintersect as geoJSInter

with open('example_input.geojson',encoding='utf-8-sig', errors='ignore') as f:
    features = json.load(f, strict=False)["features"]
featuresCollection = FeatureCollection(features)
geoJSInter.add_junctions(featuresCollection)