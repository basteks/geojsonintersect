# geojsonintersect
Helps dealing with geoJSON self intersections for a good TopoJSON conversion

geojsonintersect is a very simple library intended to check the self-intersections of a GeoJSON geometry in order to achieve an acceptable conversion to TopoJSON topology. As explained by [Mike Bostock](https://bost.ocks.org/mike/topology/), the second step of the GeoJSON to TopoJSON conversion (the "join" step) actually consider junctions **only if they are shared by each of the intersecting geometries**.

From [Mike Bostock](https://bost.ocks.org/mike/topology/)

> For example, consider the line ABC, where A, B and C are distinct points. If there is another line DBE (fig. a), then B is a junction. Similarly, if there are two lines ABC and ABD (fig. b and c), then because the lines diverge at point B, B is a junction. A few simple examples: 

![Simple junctions from Mike Bostock](https://raw.githubusercontent.com/basteks/geojsonintersect/main/doc/mike_bostocks_simple_junctions.PNG)

>(Note: if two line segments intersect, but don’t share a point, this intersection is ignored. The topology only cares how points are connected, and whether they are distinct, not their positions.) 

Conversely, **if two lines crosses without sharing the intersecting point, the junction is ignored**. This is, for example, what happens if we consider the line ABE and the line DC on fig. a.

### Usage
---
The file `geojsonintersect.py` only contains two functions : 
- `cutAtPpoint` which enables to cut a geometry at a specified point. You don't need to call this function by yourself as it is called by the main function called `add_junctions`
- the main function `add_junctions`, which takes a GeoJSON `FeatureCollection` as parameter, and returns a list of the junction points as Shapely Points.

The file `simple_example.py` show a basic usage of the library, importing a GeoJSON from an input file `examples/simple_example_input.geojson` composed of four self-intersecting rectangles ABCH, DEFG, CDKJ and ILGH (see figure below).

![Geometry of example_input.geojson](https://raw.githubusercontent.com/basteks/geojsonintersect/main/examples/simple_example_geometry.PNG)

Using the `add_junctions` function adds the points I and J on the one hand, and K and L on the ther hand, respectively in the rectangles ABCH (which therefore becomes ABCJIH) and DEFG (which becomes DEFGLK)

The file `dxf_import_example.py` show a more consistent usage of the library, importing a DXF file (currently you can choose between a thermal bridge from the file `examples/roof_thermal_bridge.dxf` and a window frame from the EN 10077-2 standard from the file `EN10077_H3_window_frame.dxf`. In this example, the dxf entities (currently only LwPolynies) are converted to a GeoJSON `FeatureCollection` on which this algorithm is applied. Then, a simple visualization tool is provided to show the final geometry and the junction points identified.


### Credits
---
This library is based on the [amazing Shapely library](https://github.com/Toblerity/Shapely) for manipulation and analysis of planar geometric objects.

This idea came from [a reflexion with Facundo Ferrín](https://github.com/fferrin/pytopojson/issues/7), the creator of the great [pytopojson](https://github.com/fferrin/pytopojson) library.

Obvioulsy, it is also based on the work from [Mike Bostock](https://bost.ocks.org/mike/), the creator of [TopoJSON](https://github.com/topojson/)

The importation of a dxf file in the `dxf_import_example.py` file is achieved via the [ezdxf library](https://ezdxf.mozman.at/)

[Geopandas](https://geopandas.org/) and [Matplotlib](https://matplotlib.org/) are used for the vizualization
