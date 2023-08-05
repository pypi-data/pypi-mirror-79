# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from vispy.scene.visuals import create_visual_node
from .polygon_visual import PolygonVisual

Polygon = create_visual_node(PolygonVisual)
