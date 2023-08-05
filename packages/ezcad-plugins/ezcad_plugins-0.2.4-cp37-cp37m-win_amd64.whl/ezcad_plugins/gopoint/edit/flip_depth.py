# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import Signal
from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog
from ..utils import GEOMETRY_TYPES


class Dialog(EasyDialog):
    NAME = _("Object flip depth")
    sig_start = Signal(str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Input object")
        self.grabob = self.create_grabob(text, geom=GEOMETRY_TYPES)
        self.layout.addWidget(self.grabob)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        object_name = self.grabob.lineedit.edit.text()
        self.sig_start.emit(object_name)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = Dialog()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
