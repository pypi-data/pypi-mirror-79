# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import Signal
from qtpy.QtWidgets import QLabel, QLineEdit, QHBoxLayout
from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog
from ..utils import GEOMETRY_TYPES


class Dialog(EasyDialog):
    NAME = _("Translate XYZ")
    sig_start = Signal(str, float, float, float, float, float, float)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Object")
        self.grabob = self.create_grabob(text, geom=GEOMETRY_TYPES)
        self.layout.addWidget(self.grabob)

        lbl_x = QLabel("AX")
        lbl_y = QLabel("AY")
        lbl_z = QLabel("AZ")
        self.le_x = QLineEdit("0")
        self.le_y = QLineEdit("0")
        self.le_z = QLineEdit("0")
        lbl_mx = QLabel("MX")
        lbl_my = QLabel("MY")
        lbl_mz = QLabel("MZ")
        self.le_mx = QLineEdit("1")
        self.le_my = QLineEdit("1")
        self.le_mz = QLineEdit("1")

        hbox = QHBoxLayout()
        hbox.addWidget(lbl_x)
        hbox.addWidget(self.le_x)
        hbox.addWidget(lbl_y)
        hbox.addWidget(self.le_y)
        hbox.addWidget(lbl_z)
        hbox.addWidget(self.le_z)
        self.layout.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(lbl_mx)
        hbox.addWidget(self.le_mx)
        hbox.addWidget(lbl_my)
        hbox.addWidget(self.le_my)
        hbox.addWidget(lbl_mz)
        hbox.addWidget(self.le_mz)
        self.layout.addLayout(hbox)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        object_name = self.grabob.lineedit.edit.text()
        x = float(self.le_x.text())
        y = float(self.le_y.text())
        z = float(self.le_z.text())
        mx = float(self.le_mx.text())
        my = float(self.le_my.text())
        mz = float(self.le_mz.text())
        self.sig_start.emit(object_name, x, y, z, mx, my, mz)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = Dialog()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
