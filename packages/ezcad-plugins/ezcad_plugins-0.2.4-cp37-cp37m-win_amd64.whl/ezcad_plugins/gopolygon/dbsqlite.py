# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import copy
import sqlite3
from datetime import datetime
from ezcad.utils.dbsqlite import DBSQLite as DataBase
from ezcad.utils.dbsqlite import native_scalar
from ezcad.utils.logger import logger
from .utils import POLYGON_STYLE


class DBSQLite(DataBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_tables(self):
        self.ct_geometry_type()
        # self.ct_atom_style()
        # self.ct_current_property()
        # self.ct_point_vertexes()
        # self.ct_property_arrays()
        # self.ct_properties()
        # self.ct_color_gradient_ticks()

    def ct_polygon_style(self):
        logger.info('Creating table atom_style (if not exists)')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS atom_style
            (object_name TEXT PRIMARY KEY, symbol TEXT, size INTEGER,
            edge_width INTEGER, coloring INTEGER,
            colorR INTEGER, colorG INTEGER, colorB INTEGER, colorA INTEGER)
            ''')

    def ct_geometry_type(self):
        logger.info('Creating table geometry_type (if not exists)')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS geometry_type
            (object_name TEXT PRIMARY KEY, geometry_type TEXT)
            ''')


