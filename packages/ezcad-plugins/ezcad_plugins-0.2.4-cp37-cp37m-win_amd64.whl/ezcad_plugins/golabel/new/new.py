# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import numpy as np
from ezcad.utils.envars import DELIMITER2CHAR
from ezcad.utils.convert_grid import ln2xy
from ..label import Label


def from_coordinate(name, comment, delimiter, method, text, survey=None):
    """Create line from coordinate.

    :param name: name of the new object
    :type name: str
    :param comment: character denoting comment line
    :type comment: char
    :param delimiter: delimiter for columns
    :type delimiter: str
    :param method: coordinate method, xy or ln
    :type method: str
    :param text: text of the data table, usually from GUI text box
    :type text: str
    :param survey: survey, used to convert LN to XY
    :type survey: :class:`~ezcad.gosurvey.survey.Survey`
    :return: a label object
    :rtype: :class:`~ezcad.golabel.label.Label`
    """
    xyz, labels = table2array(text, comment, delimiter)
    if method == 'ln':
        if survey is None:
            raise ValueError("Need survey to get line numbers to XYs")
        xy = ln2xy(xyz, survey=survey)
        xyz[:, 0] = xy[:, 0]
        xyz[:, 1] = xy[:, 1]
    dob = init_dob(name, xyz, labels)
    return dob


def init_dob_from_dframe(name, dataframe):
    """Create label from dataframe.
    It calls function :func:`~ezcad.golabel.new.new.init_dob`.

    :param name: name of the new object
    :type name: str
    :param dataframe: a Pandas dataframe
    :type dataframe: dataframe
    :return: a label object
    :rtype: :class:`~ezcad.golabel.label.Label`
    """
    # prop_list = dataframe.columns
    data_array = dataframe.values
    # print(type(data_array))  # <class 'numpy.ndarray'>
    # print(data_array.dtype)  # object
    vertexes = data_array[:, :3]
    labels = data_array[:, 3]
    vertexes = vertexes.astype(float)
    labels = labels.astype(str)
    dob = init_dob(name, vertexes, labels)
    return dob


def init_dob(object_name, vertexes, labels):
    """Create label, base function.

    :param object_name: name of the new object
    :type object_name: str
    :param vertexes: vertexes XYZ
    :type vertexes: array
    :param labels: label for each vertex
    :type labels: array
    :return: a label object
    :rtype: :class:`~ezcad.golabel.label.Label`
    """
    dob = Label(object_name)
    dob.set_text_style()
    dob.set_font()
    dob.set_vertexes(vertexes)
    dob.set_labels(labels)
    # dob.make_pg2d()
    # dob.make_pg3d()
    dob.set_xyz_range()
    return dob


def table2array(table, comment, delimiter):
    """Convert textual table to numeric array.

    :param table: textual table, usually from GUI text box
    :type table: str
    :param comment: character denoting comment line, such as #, !
    :type comment: char
    :param delimiter: delimiter for columns
    :type delimiter: str
    :returns: numeric data array
    :rtype: array
    """
    delim = DELIMITER2CHAR[delimiter]
    xyz_list = []
    text_list = []
    lines = table.split('\n')
    for line in lines:
        line = line.strip()  # remove heading/tailing spaces
        if len(line) == 0:  # skip blank line
            continue
        if line[0] == comment:  # skip comment line
            continue
        p = line.split(delim)
        pxyz = [float(v) for v in p[:3]]
        xyz_list.append(pxyz)
        text_list.append(p[3].strip())
    return np.array(xyz_list), np.array(text_list)
