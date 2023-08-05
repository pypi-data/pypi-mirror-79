# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
Cube IO from Numpy memmap file.
"""

import os
import numpy as np
from gocube.new.new import DEFAULT_VIDX
from gosurvey.new.new import new_survey_from_vidx


def load_cube(fufn, shape, dtype='float32', vidx=None, survey=None,
    object_name=None, prop_name='amp'):
    """Load numpy memmap file and setup cube.

    :param fufn: full-path filename
    :type fufn: str
    :param shape: number of samples, (NIL, NXL, NDP)
    :type shape: tuple
    :param dtype: data type
    :type dtype: str
    :param vidx: volume indexes
    :type vidx: dict
    :param survey: survey, used to convert LN to XY
    :type survey: :class:`~ezcad.gosurvey.survey.Survey`
    :param object_name: name of the new object
    :type object_name: str
    :param prop_name: name of the property
    :type prop_name: str
    :return: a cube object
    :rtype: :class:`~ezcad.gocube.cube.Cube`
    """
    if vidx is None:
        vidx = DEFAULT_VIDX
        vidx['IL_AMNT'] = shape[0]
        vidx['XL_AMNT'] = shape[1]
        vidx['DP_AMNT'] = shape[2]
        vidx['IL_LAST'] = vidx['IL_FRST'] + vidx['IL_AMNT'] - 1
        vidx['XL_LAST'] = vidx['XL_FRST'] + vidx['XL_AMNT'] - 1
        vidx['DP_LAST'] = vidx['DP_FRST'] + vidx['DP_AMNT'] - 1
    if survey is None:
        survey = new_survey_from_vidx(vidx)

    if object_name is None:
        path, fn = os.path.split(fufn)
        object_name = os.path.splitext(fn)[0]
    from gocube.cube import Cube
    array3d = np.memmap(fufn, dtype=dtype, mode='r', shape=shape)
    cube = Cube(object_name)
    cube.make_from_vidx(vidx, survey, array3d, dataVelType=prop_name)
    cube.calc_prop_percentile()
    cube.init_xyz_range()
    cube.set_section_number()
    cube.init_colormap()
    cube.set_current_property()
    return cube
