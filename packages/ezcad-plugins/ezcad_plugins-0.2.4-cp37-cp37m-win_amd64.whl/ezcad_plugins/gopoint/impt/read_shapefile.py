# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import os
import numpy as np
try:
    import shapefile
except ImportError:
    print("WARNING cannot import pyshp shapefile")


def read_shapefile(filename):
    """Read ESRI shapefile

    :param filename: the input file name
    :type filename: str
    :return: XYZ of the Point
    :rtype: array
    """
    shape = shapefile.Reader(filename)
    # print(shape)
    # print(vars(shape))
    if shape.shapeType != 1:
        raise ValueError("Shape type must be Point")
    print("Shape type:", shapefile.SHAPETYPE_LOOKUP[shape.shapeType])
    print("Number of records:", shape.numRecords)
    print("Number of fields:", len(shape.fields))
    records = shape.shapeRecords()
    fixed_type = records[0].shape.__geo_interface__['type']
    xyz = []
    for record in records:
        geojson = record.shape.__geo_interface__
        if geojson['type'] != fixed_type:
            continue
        x, y = geojson['coordinates']
        xyz.append((x, y, 0))
    return np.array(xyz)


def preview_shapefile(filename, nr=1):
    """Read ESRI shapefile

    :param filename: the input file name
    :type filename: str
    :param nr: number of records to preview
    :type nr: int
    :return: message for preview
    :rtype: str
    """
    shape = shapefile.Reader(filename)
    message = "Shape type: {}\n".format(SHAPETYPE_LOOKUP[shape.shapeType])
    message += "Number of records: {}\n".format(shape.numRecords)
    message += "Number of fields: {}\n".format(len(shape.fields))
    message += "Projection file content:\n"
    path, fn = os.path.split(filename)
    fn_base = os.path.splitext(fn)[0]
    fn_prj = fn_base + '.prj'
    fn_prj = os.path.join(path, fn_prj)
    with open(fn_prj, mode='r') as f:
        line = f.readline()
    message += line
    message += '\n'
    records = shape.shapeRecords()
    nre = nr if nr < shape.numRecords else shape.numRecords
    message += "The first {} records:\n".format(nre)
    for record in records[:nre]:
        geojson = record.shape.__geo_interface__
        message += str(geojson)
        message += '\n'
    return message


def main():
    fn = "C:\\Users\\xinfa\\Downloads\\CoalMines_US_EIA\\CoalMines_US_2018.shp"
    # xyz = read_shapefile(fn)
    # print(xyz.shape)
    message = preview_shapefile(fn, nr=4)
    print(message)


if __name__ == '__main__':
    main()
