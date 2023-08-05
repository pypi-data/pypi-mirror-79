# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import numpy as np
try:
    import shapefile
except ImportError:
    print("WARNING cannot import pyshp shapefile")


def read_shapefile(filename):
    """Read ESRI shapefile

    :param filename: the input file name
    :type filename: str
    :return: XYZC of a Line
    :rtype: array
    """
    shape = shapefile.Reader(filename)
    # print(shape)
    # print(vars(shape))
    print("Shape type:", shapefile.SHAPETYPE_LOOKUP[shape.shapeType])
    if shape.shapeType not in [3, 5]:
        raise ValueError("Shape type must be Polyline or Polygon")
    print("Number of records:", shape.numRecords)
    print("Number of fields:", len(shape.fields))
    records = shape.shapeRecords()
    # fixed_type = records[0].shape.__geo_interface__['type']
    # if fixed_type is not 'MultiPolygon':
    #     raise NotImplementedError
    xyzc = []
    for record in records:
        geojson = record.shape.__geo_interface__
        if geojson['type'] is 'Polygon':
            polygon = geojson['coordinates']
            polygon2line(polygon, xyzc)
        elif geojson['type'] is 'MultiPolygon':
            multi_polygon = geojson['coordinates']
            for polygon in multi_polygon:
                polygon2line(polygon, xyzc)
        else:
            raise NotImplementedError
    return np.array(xyzc)


def polygon2line(polygon, xyzc):
    """Convert GeoJSON polygon to XYZC nx4 list.

    https://en.wikipedia.org/wiki/GeoJSON
    A simple polygon without hole
    {
        "type": "Polygon",
        "coordinates": [
            [[30, 10], [40, 40], [20, 40], [10, 20], [30, 10]]
        ]
    }
    A polygon with a hole
    {
        "type": "Polygon",
        "coordinates": [
            [[35, 10], [45, 45], [15, 40], [10, 20], [35, 10]],
            [[20, 30], [35, 35], [30, 20], [20, 30]]
        ]
    }

    :param polygon: the coordinates of GeoJSON type Polygon
    :param xyzc: XYZC values of points
    :type xyzc: list
    """
    # A polygon with hole has an outer edge and inner edge.
    for edge in polygon:
        npt = len(edge)
        ipt = 0
        for point in edge:
            x, y = point
            cv = 1 if ipt < npt - 1 else 0
            xyzc.append((x, y, 0, cv))
            ipt += 1


def main():
    fn = "C:\\Users\\xinfa\\Downloads\\ne_110m_admin_0_countries\\ne_110m_admin_0_countries.shp"
    xyzc = read_shapefile(fn)
    print(xyzc.shape)


if __name__ == '__main__':
    main()
