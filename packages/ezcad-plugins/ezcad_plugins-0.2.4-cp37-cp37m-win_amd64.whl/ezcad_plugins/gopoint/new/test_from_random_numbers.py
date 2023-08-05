# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
GUI testing with pytest-qt
How to run? pytest this.py or python -m pytest this.py
"""

from qtpy.QtCore import Qt
from tests.ezcad_window import launch, quit, MS_BETWEEN_CLICKS


def test_ezcad(qtbot):
    window = launch()

    idx = window.menubar_plus.toolbar.cb_mode.findText("Point Menubar")
    window.menubar_plus.toolbar.cb_mode.setCurrentIndex(idx)
    qtbot.wait(MS_BETWEEN_CLICKS)

    pm = window.plugins_manager.getPluginByName("Point Menubar",
        category="PluginMenuBar")
    dialog = pm.plugin_object.bartender.new_from_random_numbers()

    qtbot.addWidget(dialog)
    qtbot.waitForWindowShown(dialog)
    qtbot.wait(MS_BETWEEN_CLICKS)

    qtbot.keyClicks(dialog.new_point.edit, 'test')
    qtbot.wait(MS_BETWEEN_CLICKS)
    qtbot.keyClicks(dialog.n_vertex.edit, '10')
    qtbot.wait(MS_BETWEEN_CLICKS)

    qtbot.mouseClick(dialog.btn_apply, Qt.LeftButton)
    qtbot.wait(3*MS_BETWEEN_CLICKS)

    quit(qtbot, window)
