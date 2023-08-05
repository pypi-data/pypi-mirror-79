# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import os
import sys
if os.path.realpath(os.path.dirname(__file__)) not in sys.path:
    sys.path.append(os.path.realpath(os.path.dirname(__file__)))

from ezcad.config.base import _
from ezcad.widgets.mode_switch import PluginMenuBar
from ezcad.utils.qthelpers import MENU_SEPARATOR, create_action, add_actions
from gopolygon.bartender import Bartender


class PolygonMenuBar(PluginMenuBar):
    NAME = "Polygon Menubar"

    def __init__(self):
        super().__init__()
        self.treebase = None
        self.bartender = None

        self.new_menu = self.addMenu(_("New"))
        self.edit_menu = self.addMenu(_("Edit"))
        self.tool_menu = self.addMenu(_("Tool"))
        self.gate_menu = self.addMenu(_("Gate"))

    def setup(self):
        # call bartender after set treebase
        self.bartender = Bartender(self.treebase)
        self.make_actions()
        self.new_menu_actions = [
            self.act_new_coord,
            self.act_covid19_spread,
        ]
        self.edit_menu_actions = [
        ]
        self.tool_menu_actions = [
            self.act_time_player,
        ]
        self.gate_menu_actions = [
        ]

        add_actions(self.new_menu, self.new_menu_actions)
        add_actions(self.edit_menu, self.edit_menu_actions)
        add_actions(self.tool_menu, self.tool_menu_actions)
        add_actions(self.gate_menu, self.gate_menu_actions)

    def make_actions(self):
        self.act_new_coord = create_action(self, _('From coordinates'),
            triggered=self.bartender.new_from_coord)
        self.act_covid19_spread = create_action(self,
            _('Covid-19 global spread'),
            triggered=self.bartender.covid19_global_spread)
        self.act_time_player = create_action(self, _('Time player'),
            triggered=self.bartender.open_time_player)
