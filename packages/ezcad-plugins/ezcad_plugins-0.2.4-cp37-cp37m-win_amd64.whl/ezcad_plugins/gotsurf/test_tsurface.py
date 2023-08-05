# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
GUI testing with pytest-qt
How to run? pytest this.py or python -m pytest this.py
"""

from qtpy.QtCore import Qt
from ezcad.tests.automate import launch, quit, MS_BETWEEN_CLICKS


def test_polygon(qtbot):
    window = launch()
    # For recording screen on my 1920x1080 laptop, leave bottom for terminal.
    width, height = 1920, 900  # pixels
    # anchorx, anchory = 0, 0
    anchorx, anchory = -1920, 0
    window.setFixedSize(width, height)
    window.move(anchorx, anchory)
    # window.showFullScreen()
    qtbot.wait(2*MS_BETWEEN_CLICKS)

    # create a point object
    name = "testp"
    comment, delimiter, method = "#", "comma", "xy"
    text = "1,1,0 \n 2,1,0 \n 2,2,0 \n 1,2,0"
    pm = window.plugins_manager.getPluginByName("Point Menubar",
                                                category="PluginMenuBar")
    pm.plugin_object.bartender.new_from_coord_worker(
        name, comment, delimiter, method, text)

    # check if the tree has the item
    while name not in window.treebase.object_items:
        qtbot.wait(MS_BETWEEN_CLICKS)
    window.treebase.expandAll()

    # check object in tree - turn on in viewer
    dob_item = window.treebase.object_items[name]
    dob_item.setCheckState(0, Qt.Checked)
    qtbot.wait(2*MS_BETWEEN_CLICKS)

    # Switch menubar
    idx = window.menubar_plus.toolbar.cb_mode.findText("Tsurface Menubar")
    window.menubar_plus.toolbar.cb_mode.setCurrentIndex(idx)
    qtbot.wait(MS_BETWEEN_CLICKS)

    # create a tsurf from point
    tsurf_name = name + "_ts"
    pm = window.plugins_manager.getPluginByName("Tsurface Menubar",
        category="PluginMenuBar")
    pm.plugin_object.bartender.new_from_point_worker(name, tsurf_name)

    # check if the tree has the item
    while tsurf_name not in window.treebase.object_items:
        qtbot.wait(MS_BETWEEN_CLICKS)
    window.treebase.expandAll()

    # uncheck the point
    dob_item = window.treebase.object_items[name]
    dob_item.setCheckState(0, Qt.Unchecked)
    # check object in tree - turn on in viewer
    dob_item = window.treebase.object_items[tsurf_name]
    dob_item.setCheckState(0, Qt.Checked)
    qtbot.wait(2*MS_BETWEEN_CLICKS)

    qtbot.wait(3600*MS_BETWEEN_CLICKS)

    quit(qtbot, window)
