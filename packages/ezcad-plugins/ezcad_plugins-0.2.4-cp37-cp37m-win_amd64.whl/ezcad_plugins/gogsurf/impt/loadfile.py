# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import os
import numpy as np
from ..surface import Gsurface
from ezcad.utils.envars import COORDINATE_PROPERTY_NAMES


def load_gsurf_npzfile(fufn, gsurf_name, survey):
    """Locad gsurface from numpy.savez file.

    :param fufn: full-path filename
    :type fufn: str
    :return: a gsurface object
    :rtype: :class:`~ezcad.gogsurf.surface.Gsurface`
    """
    # x = np.linspace(-8, 8, 50)
    # y = np.linspace(-8, 8, 50)
    # z = 0.1 * ((x.reshape(50,1) ** 2) - (y.reshape(1,50) ** 2))
    # print(x.shape, y.shape, z.shape)
    # outfile = '/home/joe/code/ezcad/data/gsurf_saddle'
    # np.savez(outfile, x=x, y=y, z=z)

    # infile = '/home/joe/code/ezcad/data/gsurf_saddle.npz'
    npzfile = np.load(fufn)
    # print(type(npzfile))  # <class 'numpy.lib.npyio.NpzFile'>
    # print(npzfile.files)  # ['x', 'y', 'z']
    # print(npzfile['x'])   # numpy array x
    x, y, z = npzfile['x'], npzfile['y'], npzfile['z']

    # path, fn = os.path.split(fufn)
    # gsurf_name = os.path.splitext(fn)[0]
    dob = Gsurface(gsurf_name, z)
    zname = COORDINATE_PROPERTY_NAMES[2]
    dob.add_property(zname, array=z)

    sidx_ln = {
        'IL_FRST': x[0],
        'IL_LAST': x[-1] * 100,
        'IL_NCRT': (x[-1] - x[0]) / (x.shape[0] - 1),
        'IL_AMNT': x.shape[0],
        'XL_FRST': y[0],
        'XL_LAST': y[-1] * 100,
        'XL_NCRT': (y[-1] - y[0]) / (y.shape[0] - 1),
        'XL_AMNT': y.shape[0],
    }

    # w, h = z.shape
    # random = np.random.randn(w, h)
    # dob.add_property('random', array=random)
    dob.set_current_property()
    dob.survey = survey
    dob.set_dict_sidx(sidx_ln)
    dob.init_corners()
    dob.set_xyz_range()
    return dob
