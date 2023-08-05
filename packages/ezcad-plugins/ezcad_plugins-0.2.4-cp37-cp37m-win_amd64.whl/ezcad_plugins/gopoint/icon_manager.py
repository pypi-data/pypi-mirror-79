# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import os.path as osp
import qtawesome as qta

icondir = osp.join(osp.dirname(osp.realpath(__file__)), 'fonts')

_qtaargs = {
    'gopoint': [('ezcad.point',), {}],
    'goline': [('ezcad.line',), {}],
    'gotsurf': [('ezcad.tsurf',), {}],
    'gogsurf': [('ezcad.gsurf',), {}],
    'gocube': [('ezcad.cube',), {}],
    # 'golabel': [('ezcad.label',), {}],
    'golabel': [('fa.tag',), {}],
}


def icon(name):
    qta.load_font('ezcad', 'ezcad.ttf', 'ezcad-charmap.json',
        directory=icondir)
    args, kwargs = _qtaargs[name]
    return qta.icon(*args, **kwargs)
