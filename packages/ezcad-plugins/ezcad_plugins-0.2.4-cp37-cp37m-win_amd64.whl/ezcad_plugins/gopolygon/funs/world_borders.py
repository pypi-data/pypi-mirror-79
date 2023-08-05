# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
http://andrewgaidus.com/Reading_Zipped_Shapefiles/
https://gis.stackexchange.com/questions/250092/using-pyshp-to-read-a-file-like-object-from-a-zipped-archive
http://thematicmapping.org/downloads/world_borders.php
"""

from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO
try:
    import shapefile
except ImportError:
    print("WARNING cannot import pyshp shapefile")
# from shapely.geometry import shape


def world_borders(fn=None):
    if fn is None or fn == 'default':
        # Specify zipped shapefile url
        wb_url = 'http://thematicmapping.org/downloads/TM_WORLD_BORDERS_SIMPL-0.3.zip'
        zip_file = ZipFile(BytesIO(urlopen(wb_url).read()))
    else:
        # Read local zip file
        # fn = r"C:\Users\xinfa\Downloads\TM_WORLD_BORDERS_SIMPL-0.3.zip"
        # fn = r"C:\Users\xinfa\Downloads\TM_WORLD_BORDERS-0.3.zip"
        zip_file = ZipFile(open(fn, 'rb'))

    filenames = [y for y in sorted(zip_file.namelist()) for ending in
                 ['dbf', 'prj', 'shp', 'shx'] if y.endswith(ending)]
    # print(filenames)

    dbf, prj, shp, shx = [BytesIO(zip_file.read(filename)) for filename in
                          filenames]
    r = shapefile.Reader(shp=shp, shx=shx, dbf=dbf, encoding='ISO8859-1')
    # print(r.bbox)
    # print(r.numRecords)

    # attributes, geometry = [], []
    # field_names = [field[0] for field in r.fields[1:]]
    # print(field_names)
    # for row in r.shapeRecords():
    #     geometry.append(shape(row.shape.__geo_interface__))
    #     attributes.append(dict(zip(field_names, row.record)))
    # print(row.shape.__geo_interface__)
    # print(len(attributes))
    # print(attributes[0])
    # print(geometry[0])
    # print(r.shapeRecord(0).shape.__geo_interface__)
    # print(r.shapeRecord(0).record[4])

    countries = {}
    field_names = [field[0] for field in r.fields[1:]]
    for row in r.shapeRecords():
        shape = row.shape.__geo_interface__
        # Make border of each country a 4D list
        if shape['type'] == 'MultiPolygon':
            coords = shape['coordinates']
        elif shape['type'] == 'Polygon':
            coords = [shape['coordinates']]
        else:
            raise ValueError("Unsupported type: {}".format(shape['type']))
        country = dict(zip(field_names, row.record))
        country['BORDER'] = coords
        alpha3 = country['ISO3']
        countries[alpha3] = country
    return countries


def zip_extract():
    # https://medium.com/@loldja/reading-shapefile-zips-from-a-url-in-python-3-93ea8d727856
    import geopandas as gpd
    import requests
    import zipfile
    import io
    url = 'http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_us_county_500k.zip'
    local_path = 'tmp/'
    print('Downloading shapefile...')
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    print("Download is done")
    z.extractall(path=local_path)  # extract to local folder
    filenames = [y for y in sorted(z.namelist()) for ending in
                 ['dbf', 'prj', 'shp', 'shx'] if y.endswith(ending)]
    dbf, prj, shp, shx = [filename for filename in filenames]
    usa = gpd.read_file(local_path + shp)
    print("Shape of the dataframe: {}".format(usa.shape))
    print("Projection of dataframe: {}".format(usa.crs))
    usa.tail()  # last 5 records in dataframe
    print(filenames)
    ax = usa.plot()
    ax.set_title("USA Counties. Default view)")


def main():
    countries = world_borders()
    # print(list(countries.keys()))
    print(len(countries))
    # print(countries['CHN'])
    i = 0
    j = 0
    for key in countries:
        xy4d = countries[key]
        j += 1
        for xy3d in xy4d:
            for xy2d in xy3d:
                i += 1
    print("Number of polygons", i, j)


if __name__ == '__main__':
    main()
