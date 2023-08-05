# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import numpy as np
from ezcad.utils.convert_grid import ln2xy
from ..new.new import init_dob


def update_target_line(treebase, points):
    points = ln2xy(points, survey=treebase.survey)
    object_name = 'TARGET_LINE'
    x, y = points[:, 0], points[:, 1]
    z = np.zeros(x.shape[0])
    xyz = np.stack((x, y, z), axis=-1)
    if object_name not in treebase.object_data:
        props = ['X', 'Y', 'Z']
        dob = init_dob(object_name, props, xyz)
        treebase.add_item(dob, check=True)
    else:
        dob = treebase.object_data[object_name]
        dob.set_vertexes(vertexes=xyz)
        connect = dob.make_connect()
        dob.set_connect(connect)
        segment = dob.make_segment()
        dob.set_segment(segment)
        dob.update_visuals_in_plot()
        dob.update_visuals_in_volume()
