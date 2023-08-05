# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
https://github.com/pytest-dev/pytest-qt/issues/254
"""

import pyautogui
from minimal_shortcut import Window


def test_shortcut(qtbot):
    window = Window()
    assert window.var == 0
    window.show()
    qtbot.waitUntil(lambda: window.isVisible())
    qtbot.wait(1000)
    pyautogui.hotkey("ctrl", "up")
    qtbot.wait(1000)
    assert window.var == 1
