# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
GUI testing with pytest-qt
How to run? pytest this.py or python -m pytest this.py
"""

from qtpy.QtCore import Qt
from ezcad.tests.automate import launch, quit, MS_BETWEEN_CLICKS
from .funs.covid19_colorbar import new_ticks


def test_polygon(qtbot):
    window = launch()
    # For recording screen on my 1920x1080 laptop, leave bottom for terminal.
    width, height = 1920, 900  # pixels
    anchorx, anchory = 0, 0
    window.setFixedSize(width, height)
    window.move(anchorx, anchory)
    # window.showFullScreen()
    qtbot.wait(2*MS_BETWEEN_CLICKS)

    # Switch to polygon menubar
    idx = window.menubar_plus.toolbar.cb_mode.findText("Polygon Menubar")
    window.menubar_plus.toolbar.cb_mode.setCurrentIndex(idx)
    qtbot.wait(MS_BETWEEN_CLICKS)

    pm = window.plugins_manager.getPluginByName("Polygon Menubar",
        category="PluginMenuBar")
    # dialog = pm.plugin_object.bartender.new_from_coord()
    dialog = pm.plugin_object.bartender.covid19_global_spread()
    qtbot.addWidget(dialog)
    qtbot.waitForWindowShown(dialog)
    dialog.move((width+anchorx)*0.5, anchory)

    # qtbot.keyClicks(dialog.new_polygon.edit, 'test')
    # qtbot.wait(MS_BETWEEN_CLICKS)

    qtbot.mouseClick(dialog.btn_ok, Qt.LeftButton)
    # qtbot.wait(10*MS_BETWEEN_CLICKS)

    name = 'covid-19'
    while name not in window.database:
        print('waiting for object', name)
        qtbot.wait(MS_BETWEEN_CLICKS)

    # check if the tree has the item
    while name not in window.treebase.object_items:
        qtbot.wait(MS_BETWEEN_CLICKS)
    window.treebase.expandAll()

    # check object in tree - turn on in viewer
    dob_item = window.treebase.object_items[name]
    dob_item.setCheckState(0, Qt.Checked)
    qtbot.wait(2*MS_BETWEEN_CLICKS)

    # check on property
    prop_name = 'Confirmed'
    props_item = window.treebase.find_child(dob_item, 'properties')
    prop_item = window.treebase.find_child(props_item, prop_name)
    prop_item.setCheckState(0, Qt.Checked)
    qtbot.wait(2*MS_BETWEEN_CLICKS)

    # view all in viewer
    while len(window.current_viewer.canvas.visuals) == 0:
        print('waiting for visuals to viewer')
        qtbot.wait(MS_BETWEEN_CLICKS)
    window.current_viewer.set_view_all()
    qtbot.wait(2*MS_BETWEEN_CLICKS)

    # zoom in
    window.current_viewer.distance = 230
    qtbot.wait(2*MS_BETWEEN_CLICKS)

    # change color map
    dob = window.database[name]
    clip = (-1, 1000000)
    ticks, _, _ = new_ticks()
    gradient = dob.prop[prop_name]['colorGradient']
    gradient['ticks'] = ticks
    dob.style['coloring'] = 2
    dob.current_property = prop_name
    dob.set_clip(prop_name, clip=clip)
    dob.set_gradient(prop_name, gradient=gradient)
    dob.make_colormap(prop_name)
    dob.update_visuals()
    qtbot.wait(2*MS_BETWEEN_CLICKS)

    # set border color to gray
    dob.style['border_color'] = (180, 180, 180, 255)
    dob.update_visuals()
    qtbot.wait(2*MS_BETWEEN_CLICKS)

    # open colorbar
    dialog = pm.plugin_object.bartender.covid19_global_cmap()
    qtbot.addWidget(dialog)
    qtbot.waitForWindowShown(dialog)
    dialog.move(anchorx+50, anchory+height*0.6)

    # time player
    dialog = pm.plugin_object.bartender.open_time_player()
    qtbot.addWidget(dialog)
    qtbot.waitForWindowShown(dialog)
    dialog.move((width+anchorx)*0.5, anchory)

    qtbot.keyClicks(dialog.le_polygon, name)
    dialog.load_polygon()
    qtbot.wait(MS_BETWEEN_CLICKS)

    # dialog.sp_tm.clear()
    # qtbot.keyClicks(dialog.sp_tm, '10')
    # vals = [10, 50, 100, 120]
    vals = range(0, dob.n_times, 5)
    for val in vals:
        dialog.sp_tm.setValue(val)  # not trigger slot
        dialog.spinbox_value_changed_tm(val)
        qtbot.wait(10*MS_BETWEEN_CLICKS)

    qtbot.wait(3600*MS_BETWEEN_CLICKS)

    quit(qtbot, window)
