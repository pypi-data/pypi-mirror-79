# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

#: Default text style.
TEXT_STYLE = {
    'color': (255, 0, 0, 255),
    'opacity': 255,
    'angle': 0,
    'anchor': (0.5, 0.5),
    'font_size': 8,
    'scale': (0.05, 0.05),
    'font': None,
    # QFont() Qt Object cannot be copied or pickled
    # TODO how to save QFont with Sqlite
}
