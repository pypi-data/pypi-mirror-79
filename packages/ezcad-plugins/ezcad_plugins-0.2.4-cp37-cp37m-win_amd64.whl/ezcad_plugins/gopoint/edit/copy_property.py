# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import Signal
from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog
from ..utils import GEOMETRY_TYPES


class Dialog(EasyDialog):
    NAME = _("Copy property between objects")
    HELP_BODY = _("From and to objects should have the same geometry type.<br>"
    "The vertex number and order should be the same for both objects.<br>")
    sig_start = Signal(str, str, str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("From object")
        self.fromObject = self.create_grabob(text, geom=GEOMETRY_TYPES)
        self.layout.addWidget(self.fromObject)

        text = _("From Property")
        self.fromProperty = self.create_lineedit(text)
        self.layout.addWidget(self.fromProperty)

        text = _("To object")
        self.toObject = self.create_grabob(text, geom=GEOMETRY_TYPES)
        self.layout.addWidget(self.toObject)

        text = _("To Property")
        self.toProperty = self.create_lineedit(text)
        self.layout.addWidget(self.toProperty)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        fromName = self.fromObject.lineedit.edit.text()
        toName = self.toObject.lineedit.edit.text()
        fromPropName = self.fromProperty.edit.text()
        toPropName = self.toProperty.edit.text()
        self.sig_start.emit(fromName, fromPropName, toName, toPropName)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = Dialog()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
