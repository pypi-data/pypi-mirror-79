# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
This module creates polygons object.
"""
import numpy as np
from ezcad.utils.functions import table2array
from ezcad.utils.convert_grid import ln2xy
from gopolygon.polygon import Polygon
from gopolygon.funs.world_borders import world_borders
from gopolygon.funs.covid19 import covid19


def from_coordinate(name, comment, delimiter, method, text, survey=None):
    """Create polygon from coordinates.

    Parameters
    ----------
    name : str
        name of the new object
    comment : char
        character denoting comment line
    delimiter : str
        delimiter for columns
    method : str
        coordinate method, xy or ln
    text : str
        text of the data table, usually from GUI text box
    survey : object
        survey, used to convert LN to XY

    Returns
    -------
    object
        a polygon object
    """
    data_raw = table2array(text, comment, delimiter)
    nrow = data_raw.shape[0]
    ncol = 2
    data_array = np.zeros((nrow, ncol))
    if method == 'xy':
        for j in range(ncol):
            data_array[:, j] = data_raw[:, j]
    elif method == 'ln':
        if survey is None:
            raise ValueError("Need survey to get line numbers to XYs")
        data_xy = ln2xy(data_raw, survey=survey)
        for j in range(ncol):
            data_array[:, j] = data_xy[:, j]

    # pos = data_array
    # props = {'aprop': np.array([[[]]])}
    # dob = from_data_array(data_array, props, name)
    dob = -1
    return dob


def init_dob(object_name, pos, props, times, record_names):
    """Initialize polygon, base function.

    Parameters
    ----------
    object_name : str
        The name of the object.
    pos : list
        XYs 5D list, ref. MultiPolygon in GeoJSON.
    props : dict
        The properties, key is property name, value is 2D array.
    times : list
        The time stamps of property.
    record_names : list
        The name of each record.

    Returns
    -------
    object
        a polygon object
    """
    dob = Polygon(object_name)
    dob.set_vertexes(pos)
    for key, value in props.items():
        dob.add_property(key, array=value)
    dob.set_current_property()
    dob.times = times
    dob.record_names = record_names
    return dob


def covid19_pandemic(object_name, covid19_fn, map_fn, survey=None):
    # Get borders for each country from world map shp file
    countries = world_borders(fn=map_fn)

    record_names = []
    pos = []
    for key, val in countries.items():
        country_name = val['NAME']
        record_names.append(country_name)
        pos.append(val['BORDER'])

    df = covid19(fn=covid19_fn)
    times = df['Date'].unique().tolist()
    n_times = len(times)

    props = {}
    prop_names = ['Confirmed', 'Recovered', 'Deaths']
    for prop_name in prop_names:
        arrays = []
        for key, val in countries.items():
            c = df[df['iso_alpha3'] == key][prop_name]
            arr = c.values
            if len(arr) == 0:
                arr = np.full(n_times, -1)
            # if arr.shape[0] != n_times:
            #     print('check...', key, arr.shape)
            #     print(df[df.iso_alpha3 == key]['Country'].unique())
            assert arr.shape[0] == n_times
            arrays.append(arr)
        arr2d = np.stack(arrays, axis=0).T  # n_times by n_records
        props[prop_name] = arr2d

    dob = init_dob(object_name, pos, props, times, record_names)
    return dob


def dummy_dob():
    name = "polygon"
    # pos = [[[[[0, 0], [2, 0], [1, 1]]]]]
    pos = [
        # [[[[0, 0], [2, 0], [1, 1]]]],
        # [[[[0, 0], [0, 2], [1, 1]]]],
        [[[[0, 0], [2, 0], [1, 1], [0, 0]]]],
        [[[[0, 0], [0, 2], [1, 1], [0, 0]]]],
    ]
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[0, 0], [1, 2]])
    props = {'infected': arr1, 'death': arr2}
    times = []
    record_names = []
    dob = init_dob(name, pos, props, times, record_names)
    return dob


def main():
    dob = dummy_dob()
    # print('test', dob.n_records, dob.n_times, dob.n_properties)


if __name__ == '__main__':
    main()
