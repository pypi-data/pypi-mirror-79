# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

# from vispy import scene
from vispy.color import Color
from .funs.scene_visuals import Polygon as PolygonNode


# class PolygonVisual(scene.visuals.Polygon):
class PolygonVisual(PolygonNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_gl_state(depth_test=True)
        self.interactive = True
        self.unfreeze()
        self._queryable_in_3d = True
        self._host_dob = None
        self.dob_record_index = 0
        self.freeze()

    @property
    def queryable_in_3d(self):
        """bool: get or set if queryable in 3D.
        """
        return self._queryable_in_3d

    @queryable_in_3d.setter
    def queryable_in_3d(self, boolean):
        self._queryable_in_3d = boolean

    @property
    def host_dob(self):
        """object: get or set the host DOB.
        """
        return self._host_dob

    @host_dob.setter
    def host_dob(self, dob):
        self._host_dob = dob

    def easy_update(self, pos=None, fill_color=None, border_color=None,
                    border_width=None):
        """The idea is to keep it unchanged if none given."""
        if pos is not None:
            self._pos = pos
        if fill_color is not None:
            self._color = Color(fill_color, clip=True)
        if border_color is not None:
            self._border_color = Color(border_color)
        if border_width is not None:
            self._border_width = border_width
        self._update()
