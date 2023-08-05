# -*- coding: utf-8 -*-
# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

"""
Simple polygon visual based on MeshVisual and LineVisual
https://groups.google.com/forum/#!topic/vispy/lQf0Pn2D6XY
https://github.com/vispy/vispy/pull/1481
https://github.com/campagnola/vispy/tree/polygon-data
"""

from __future__ import division

import numpy as np

from vispy.visuals.visual import CompoundVisual
from vispy.visuals.mesh import MeshVisual
from vispy.visuals.line import LineVisual
from vispy.color import Color
# from vispy.geometry import PolygonData
from .polygon_data import PolygonData
from vispy.gloo import set_state


class PolygonVisual(CompoundVisual):
    """
    Displays a 2D polygon

    Parameters
    ----------

    pos : array
        Set of vertices defining the polygon.
    color : str | tuple | list of colors
        Fill color of the polygon.
    border_color : str | tuple | list of colors
        Border color of the polygon.
    border_width : int
        Border width in pixels.
        Line widths > 1px are only
        guaranteed to work when using `border_method='agg'` method.
    border_method : str
        Mode to use for drawing the border line (see `LineVisual`).

            * "agg" uses anti-grain geometry to draw nicely antialiased lines
              with proper joins and endcaps.
            * "gl" uses OpenGL's built-in line rendering. This is much faster,
              but produces much lower-quality results and is not guaranteed to
              obey the requested line width or join/endcap styles.

    triangulate : boolean
        Triangulate the set of vertices
    **kwargs : dict
        Keyword arguments to pass to `CompoundVisual`.
    """
    def __init__(self, pos=None, color='black',
                 border_color=None, border_width=1, border_method='gl',
                 triangulate=True, polygon_data=None, **kwargs):
        self._mesh = MeshVisual()
        self._border = LineVisual(method=border_method)
        self._polygon_data = polygon_data
        self._pos = None
        self._color = Color(color)
        self._border_width = border_width
        self._border_color = Color(border_color)
        self._triangulate = triangulate
        self._raw_pdat_nodes = np.copy(polygon_data.vertices)
        self._raw_pdat_edges = np.copy(polygon_data.edges)

        if pos is not None:
            self.pos = pos

        self._update()
        CompoundVisual.__init__(self, [self._mesh, self._border], **kwargs)
        self._mesh.set_gl_state(polygon_offset_fill=True,
                                polygon_offset=(1, 1), cull_face=False)
        self.freeze()

    def _update(self):
        if self._polygon_data is None:
            return
        # Set border before mesh (not work), need save copy at init,
        # because the edges are changed after
        # the polygon data get faces via triangulation if the vertices
        # have duplicates. The change may be duplicates removed and edges
        # shifted causing corruption.
        if not self._border_color.is_blank:
            self._border.set_data(
                # pos=self.polygon_data.vertices,
                # connect=self.polygon_data.edges,
                pos=self._raw_pdat_nodes,
                connect=self._raw_pdat_edges,
                color=self._border_color.rgba,
                width=self._border_width
            )
            self._border.update()

        if not self._color.is_blank and self._triangulate:
            pts, tris = self._polygon_data.faces
            set_state(polygon_offset_fill=False)
            self._mesh.set_data(vertices=pts, faces=tris.astype(np.uint32),
                                color=self._color.rgba)
        elif not self._color.is_blank:
            self.mesh.set_data(vertices=self.pos,
                               color=self._color.rgba)

    @property
    def pos(self):
        """ The vertex position of the polygon.
        """
        pdata = self._polygon_data
        if pdata is None:
            return None
        return pdata.vertices

    @pos.setter
    def pos(self, pos):
        self.polygon_data = PolygonData(vertices=np.array(pos, dtype=np.float32))
        
    @property
    def polygon_data(self):
        return self._polygon_data
    
    @polygon_data.setter
    def polygon_data(self, polygon_data):
        self._polygon_data = polygon_data
        self._update()

    @property
    def color(self):
        """ The color of the polygon.
        """
        return self._color

    @color.setter
    def color(self, color):
        self._color = Color(color, clip=True)
        self._update()

    @property
    def border_color(self):
        """ The border color of the polygon.
        """
        return self._border_color

    @border_color.setter
    def border_color(self, border_color):
        self._border_color = Color(border_color)
        self._update()

    @property
    def mesh(self):
        """The vispy.visuals.MeshVisual that is owned by the PolygonVisual.
           It is used to fill in the polygon
        """
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh
        self._update()

    @property
    def border(self):
        """The vispy.visuals.LineVisual that is owned by the PolygonVisual.
           It is used to draw the border of the polygon
        """
        return self._border

    @border.setter
    def border(self, border):
        self._border = border
        self._update()
