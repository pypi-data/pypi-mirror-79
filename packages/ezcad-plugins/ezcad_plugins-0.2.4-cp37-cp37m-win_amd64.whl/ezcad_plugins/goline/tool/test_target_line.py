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

    # create a survey object
    name = "tests"
    floats = 0, 0, 10, 10, -10, 10  # x0, y0, x1, y1, x2, y2
    ints = 1, 10, 1, 10  # i1, i2, j1, j2
    pm = window.plugins_manager.getPluginByName("Survey Menubar",
                                                category="PluginMenuBar")
    pm.plugin_object.bartender.new_from_vt3_worker(
        name, floats, ints)
    qtbot.wait(2*MS_BETWEEN_CLICKS)

    # check object in tree - turn on in viewer
    names = ["SURVEY_BOX_LINE", "SURVEY_BOX_LABEL"]
    for name in names:
        dob_item = window.treebase.object_items[name]
        dob_item.setCheckState(0, Qt.Checked)
        qtbot.wait(MS_BETWEEN_CLICKS)

    while len(window.current_viewer.canvas.visuals) == 0:
        print('waiting for visuals to viewer')
        qtbot.wait(MS_BETWEEN_CLICKS)
    # Orthogonal view to see survey box label properly
    window.current_viewer.set_view_orthogonal()
    # view all in viewer
    window.current_viewer.set_view_all()
    qtbot.wait(MS_BETWEEN_CLICKS)

    # Switch to polygon menubar
    idx = window.menubar_plus.toolbar.cb_mode.findText("Line Menubar")
    window.menubar_plus.toolbar.cb_mode.setCurrentIndex(idx)
    qtbot.wait(MS_BETWEEN_CLICKS)

    pm = window.plugins_manager.getPluginByName("Line Menubar",
        category="PluginMenuBar")
    dialog = pm.plugin_object.bartender.select_target_line()
    qtbot.addWidget(dialog)
    qtbot.waitForWindowShown(dialog)
    dialog.move((width+anchorx)*0.5, anchory)

    qtbot.wait(3600*MS_BETWEEN_CLICKS)

    quit(qtbot, window)
