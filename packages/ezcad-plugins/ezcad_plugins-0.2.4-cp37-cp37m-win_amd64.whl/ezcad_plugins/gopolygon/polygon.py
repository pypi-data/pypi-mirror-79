# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
A set of polygons
"""

import copy
from datetime import datetime
import numpy as np
import qtawesome as qta

from ezcad.utils.logger import logger
from ezcad.utils.envars import LMT_LST_DELTA
from gopoint.funs.property_ops import add_property, set_clip, \
    set_gradient, make_colormap, set_current_property
from .utils import POLYGON_STYLE
from .dbsqlite import DBSQLite
from .visual import PolygonVisual
from .style_pages import GraphicsPage, DataInfoPage
from .funs.polygon_data import PolygonData


class Polygon:
    """Polygon data object.

    It is a set of 2D polygons with time-varying properties. An example is
    the Covid-19 cases of each country each day. This object has 200+ records.
    A record is a polygon or multi-polygon, representing the country borders.

    Attributes
    ----------
    name : str
        The name of the object.
    vertexes : dict
        The spatial XYs.
    """
    NAME = "Polygon"
    ICON = qta.icon('fa5s.draw-polygon')
    geometry_type = 'Polygon'
    prop_array_key = 'array2d'

    def __init__(self, name=None):
        """
        Initialize object.

        Parameters
        ----------
        name : str
            name of the object
        """
        self._name = name
        self.vertexes = {
            'xy': None,
            'xyLST': datetime.now(),  # LST = Last Saved Time
            'xyLMT': datetime.now()   # LMT = Last Modified Time
        }
        self.prop = {}  # each property array is ntimes by nrecords
        self.current_property = None
        self.current_time_index = 0
        self.db_sqlite = None
        self.survey = None
        self.style = None
        self.set_style()
        self.style_pages = [GraphicsPage, DataInfoPage]
        self.viewable_in_plot = True
        self.viewable_in_image = False
        self.viewable_in_volume = True
        self.visuals_in_plot = {}  # visual per viewer
        self.visuals_in_image = {}
        self.visuals_in_volume = {}
        self._times = []
        self._record_names = []

    @property
    def times(self):
        """list: get or set the times.
        """
        return self._times

    @times.setter
    def times(self, times):
        self._times = times

    @property
    def record_names(self):
        """list: get or set the record names.
        """
        return self._record_names

    @record_names.setter
    def record_names(self, record_names):
        self._record_names = record_names

    def set_style(self, style=None, update_plots=False):
        """Set the polygon style for plot.

        Parameters
        ----------
        style : dict
            polygon style
        update_plots : bool
            whether to update plots
        """
        if style is None:  # initialize
            style = copy.deepcopy(POLYGON_STYLE)
        self.style = style
        if update_plots:
            self.update_visuals()

    def update_visuals(self):
        colors, border_color, border_width = self.prepare_style()
        for viu, vis in self.visuals_in_volume.items():
            for i in range(self.n_records):
                polygon = vis[i]
                fill_color = colors[i]
                polygon.easy_update(fill_color=fill_color,
                    border_color=border_color, border_width=border_width)

    @property
    def n_records(self):
        """Number of records"""
        return len(self.vertexes['xy'])

    @property
    def n_properties(self):
        """Number of properties"""
        return len(self.prop)

    @property
    def n_times(self):
        """Number of times"""
        if len(self.prop) == 0:
            return 0
        else:
            name = self.current_property
            return self.prop[name]['array2d'].shape[0]

    @property
    def name(self):
        """str: get or set the object name.
        """
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def set_vertexes(self, vertexes=None, save=True):
        """Set spatial XY vertexes.

        1D list: point
            [x,y]
        2D list: polygon without hole
           [[x,y], [x,y], [x,y]]
        3D list: polygon with hole
          [[[x,y], [x,y], [x,y]],
           [[x,y], [x,y], [x,y]]]
        4D list: multi polygons
         [[[[x,y], [x,y], [x,y]],
           [[x,y], [x,y], [x,y]]],
          [[[x,y], [x,y], [x,y]]]]
        5D list: record e.g. a country with an island

        Parameters
        ----------
        vertexes : list
            XYs 5D list, ref. MultiPolygon in GeoJSON.
        save : bool
            whether save to database
        """
        self.vertexes['xy'] = vertexes
        timestamp = datetime.now()
        self.vertexes['xyLMT'] = timestamp
        if save:
            self.vertexes['xyLST'] = timestamp - LMT_LST_DELTA
        else:
            self.vertexes['xyLST'] = timestamp + LMT_LST_DELTA

    def get_vertexes(self):
        """Get the vertexes XYs list.

        Returns
        -------
        list
            XYs 4D list, ref. MultiPolygon in GeoJSON.
        """
        return self.vertexes['xy']

    def add_property(self, prop_name, array=None, clip=None, gradient=None,
        save=True):
        """

        Parameters
        ----------
        prop_name : str
            The name of the property.
        array : array
            The data array, n_times by n_records
        clip
        gradient
        save
        """
        if array is None:
            array = np.zeros((self.n_times, self.n_records))
        self.prop[prop_name] = {self.prop_array_key: array}
        timestamp = datetime.now()
        self.prop[prop_name]['arrayLMT'] = timestamp
        if save:
            self.prop[prop_name]['arrayLST'] = timestamp - LMT_LST_DELTA
        else:
            self.prop[prop_name]['arrayLST'] = timestamp + LMT_LST_DELTA
        self.set_clip(prop_name, clip=clip)
        self.set_gradient(prop_name, gradient=gradient)
        self.make_colormap(prop_name)

    def set_clip(self, prop_name, clip=None):
        """

        Parameters
        ----------
        prop_name
        clip
        """
        set_clip(self, prop_name, clip=clip)

    def set_gradient(self, prop_name, gradient=None):
        set_gradient(self, prop_name, gradient=gradient)

    def make_colormap(self, prop_name):
        make_colormap(self, prop_name)

    def update_plots_by_prop(self):
        """Update plots by property change.

        When switch click between properties in the data tree, the only thing
        changed for plots is the coloring property. This method comes in.
        """
        self.style['coloring'] = 2
        self.update_visuals()

    def change_time(self, index):
        self.current_time_index = index
        self.style['coloring'] = 2
        self.update_visuals()

    def prepare_style(self):
        fill_color = self.style['fill_color']
        border_color = self.style['border_color']
        border_width = self.style['border_width']
        coloring = self.style['coloring']
        fill_color = [x / 255. for x in fill_color]
        border_color = [x / 255. for x in border_color]
        if coloring == 1:
            colors = [fill_color] * self.n_records
        else:
            prop_name = self.current_property
            ti = self.current_time_index
            prop_array = self.prop[prop_name][self.prop_array_key][ti, :]
            cmap = self.prop[prop_name]['colormap']
            colors = cmap.map(prop_array, mode='float')
        return colors, border_color, border_width

    def make_visuals_in_volume(self, parent='viewer'):
        """Make visual for display in volume viewer.

        Parameters
        ----------
        parent : str
            The name of the viewer.
        """
        self.visuals_in_volume[parent] = self.make_visuals()

    def make_visuals(self):
        visuals = []
        colors, border_color, border_width = self.prepare_style()
        xy5d = self.vertexes['xy']
        for i in range(self.n_records):
            print('plotting', i, self.record_names[i])
            xy4d = xy5d[i]
            color = colors[0]
            nodes, edges = self.xys_list2edge(xy4d)
            # nodes, edges = self._test_polygons_and_holes()
            pdat = PolygonData(nodes, edges)
            pv = PolygonVisual(polygon_data=pdat, color=color,
                border_color=border_color, border_width=border_width)
            pv.queryable_in_3d = True
            pv.host_dob = self
            pv.dob_record_index = i
            visuals.append(pv)
        return visuals

    @staticmethod
    def remove_duplicate_node(xy4d):
        """Remove duplicate node from the 4D list"""
        nodes = set()
        xy4d_new = []
        for xy3d in xy4d:
            xy3d_new = []
            for xy2d in xy3d:
                # find and save the duplicates' indices in 2D
                dups = []
                for i in range(len(xy2d)):
                    xy1d = xy2d[i]
                    if xy1d not in nodes:
                        nodes.add(xy1d)
                    else:
                        dups.append(i)
                # xy2d may be a tuple, need convert to list for mutation
                xy2d_edit = list(xy2d)
                # remove elements by indices
                # https://stackoverflow.com/a/11303234/7269441
                for i in sorted(dups, reverse=True):
                    del xy2d_edit[i]
                xy3d_new.append(xy2d_edit)
            xy4d_new.append(xy3d_new)
        return xy4d_new

    @staticmethod
    def xys_list2edge(xy4d):
        # xy4d = Polygon.remove_duplicate_node(xy4d)
        nodes, edges = [], []
        i_node = 0
        for xy3d in xy4d:
            for xy2d in xy3d:
                # Remove tail node if it's the same as head node
                # first_node = xy2d[0]
                # last_node = xy2d[-1]
                # xy2d_edit = list(xy2d)
                # if first_node == last_node:
                #     del xy2d_edit[-1]
                # Remove duplicate nodes in 2D list
                # https://stackoverflow.com/a/7961390/7269441
                # xy2d_edit = list(set(xy2d))  # not preserve order
                xy2d_edit = list(dict.fromkeys(xy2d))  # keep order
                n_points = len(xy2d_edit)
                for i in range(n_points):
                    node = xy2d_edit[i]
                    if node in nodes:
                        print('WARNING: duplicate', i_node, node)
                    nodes.append(node)
                    # Create edge and add to list
                    edge = [i_node, i_node + 1]
                    if i == 0:
                        head_node_index = i_node
                    if i == n_points - 1:
                        edge = [i_node, head_node_index]
                    edges.append(edge)
                    i_node += 1
        return np.array(nodes), np.array(edges)

    @staticmethod
    def xys_list2edge_t2h(xy4d):
        """Convert polygon XYs from 4D list to node-edge arrays.

        Connect tail to head.

        Parameters
        ----------
        xy4d : list
            XYs 4D list, ref. MultiPolygon in GeoJSON

        Returns
        -------
        tuple
            An array of XY nodes and an array of edges.
        """
        nodes, edges, breaks = [], [], []
        i_node = 0
        for xy3d in xy4d:
            for xy2d in xy3d:
                first_node = xy2d[0]
                last_node = xy2d[-1]
                xy2d_edit = list(xy2d)
                if first_node != last_node:
                    xy2d_edit.append(first_node)
                for xy1d in xy2d_edit:
                    nodes.append(xy1d)
                    i_node += 1
                breaks.append(i_node)
        del breaks[-1]  # remove the last break
        for i in range(len(nodes) - 1):
            edge = [i, i + 1]
            edges.append(edge)
        for i in sorted(breaks, reverse=True):
            del edges[i - 1]
        return np.array(nodes), np.array(edges)

    @staticmethod
    def _test_polygons_and_holes():
        nodes = np.array([
            [1.0, 1.0], [1.0, 2.0], [2.0, 1.0],
            [1.1, 1.1], [1.3, 1.1], [1.0, 2.0],
            [3.0, 1.0], [4.0, 1.0], [3.0, 2.0],
        ])
        edges = np.array([
            [0, 1], [1, 2], [2, 0],
            [3, 4], [4, 5], [5, 3],
            [6, 7], [7, 8], [8, 6],
        ])
        # Require tail node NOT repeat head node
        # Caution: duplicate nodes get removed in edges
        # pdat = PolygonData(nodes, edges)
        # pv = PolygonVisual(polygon_data=pdat, color=color,
        #     border_color=border_color, border_width=border_width)
        return nodes, edges

    def make_visuals_slow(self):
        """This one is deprecated because it is slow making a separate
        visual for each polygon in the Vispy visual-scene system.
        For example, a world map with 246 countries has 3697 visuals,
        as many countries are multi-polygon for islands.
        The optimization is one visual per record. The record may be
        multi-polygon e.g. country with islands."""
        visuals = []
        colors, border_color, border_width = self.prepare_style()
        xy5d = self.vertexes['xy']
        for i in range(self.n_records):
            xy4d = xy5d[i]
            color = colors[i]
            record_visuals = []
            for j in range(len(xy4d)):
                xy3d = xy4d[j]
                # not support polygon with hole
                xy2d = np.array(xy3d[0])
                pv = PolygonVisual(pos=xy2d, color=color,
                    border_color=border_color, border_width=border_width)
                pv.queryable_in_3d = True
                pv.host_dob = self
                pv.dob_mpolygon_index = j
                pv.dob_record_index = i
                record_visuals.append(pv)
            visuals.append(record_visuals)
        return visuals

    def set_current_property(self, **kwargs):
        """Set the current property.

        Parameters
        ----------
        kwargs : dict
            key-word arguments, passed to prop-ops function
        """
        set_current_property(self, **kwargs)

    def set_database(self, file=None):
        """Set database.

        Parameters
        ----------
        file : str
            database filename
        """
        self.db_sqlite_file = file

    def commit_sqlite(self):
        """Commit SQLite."""
        self.db_sqlite.connect.commit()

    def open_sqlite(self):
        """Open SQLite."""
        self.db_sqlite = DBSQLite(file=self.db_sqlite_file)

    def create_sqlite_tables(self):
        """Create SQLite tables."""
        self.db_sqlite.create_tables()

    def remove_sqlite_tables(self):
        """Remove SQLite tables."""
        self.open_sqlite()
        self.db_sqlite.remove_tables(self.name)
        self.commit_sqlite()
        self.close_sqlite()

    def close_sqlite(self):
        """Close SQLite."""
        self.db_sqlite.connect.close()

    def save_to_sqlite(self, db_sqlite=None, to_project=True, to_object=False):
        """Save to SQLite.

        Parameters
        ----------
        db_sqlite : :class:`~dbsqlite.DBSQLite`
            The database.
        to_project : bool
            Whether save to project.
        to_object : bool
            Whether save to object.
        """
        logger.info('Start save object: {}'.format(self.name))
        if db_sqlite is None:
            db_sqlite = self.db_sqlite
        # db_sqlite.save_atom(self.name, self.atom_style)
        db_sqlite.save_geom(self.name, self.geometry_type)
        # db_sqlite.save_cprop(self.name, self.current_property)
        # db_sqlite.save_vtx(self.name, self.vertexes,
        #     to_project=to_project, to_object=to_object)
        # db_sqlite.save_props(self.name, self.prop, self.prop_array_key,
        #     to_project=to_project, to_object=to_object)
        logger.info('Done save object: {}'.format(self.name))
