# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
GUI, from three corner points
"""

from qtpy.QtCore import Signal
from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog


class Dialog(EasyDialog):
    NAME = _("New survey from PT3")
    sig_start = Signal(str, tuple, tuple, tuple)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        self.name = self.create_lineedit(_("Name"))
        self.p1_ilno = self.create_lineedit("P1 ILNO", wrap=False)
        self.p1_xlno = self.create_lineedit("P1 XLNO", wrap=False)
        self.p1_crsx = self.create_lineedit("P1 CRSX", wrap=False)
        self.p1_crsy = self.create_lineedit("P1 CRSY", wrap=False)
        self.p2_ilno = self.create_lineedit("P2 ILNO", wrap=False)
        self.p2_xlno = self.create_lineedit("P2 XLNO", wrap=False)
        self.p2_crsx = self.create_lineedit("P2 CRSX", wrap=False)
        self.p2_crsy = self.create_lineedit("P2 CRSY", wrap=False)
        self.p3_ilno = self.create_lineedit("P3 ILNO", wrap=False)
        self.p3_xlno = self.create_lineedit("P3 XLNO", wrap=False)
        self.p3_crsx = self.create_lineedit("P3 CRSX", wrap=False)
        self.p3_crsy = self.create_lineedit("P3 CRSY", wrap=False)

        self.layout.addWidget(self.name)
        self.layout.addWidget(self.p1_ilno)
        self.layout.addWidget(self.p1_xlno)
        self.layout.addWidget(self.p1_crsx)
        self.layout.addWidget(self.p1_crsy)
        self.layout.addWidget(self.p2_ilno)
        self.layout.addWidget(self.p2_xlno)
        self.layout.addWidget(self.p2_crsx)
        self.layout.addWidget(self.p2_crsy)
        self.layout.addWidget(self.p3_ilno)
        self.layout.addWidget(self.p3_xlno)
        self.layout.addWidget(self.p3_crsx)
        self.layout.addWidget(self.p3_crsy)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        name = self.name.edit.text()
        p1_ilno = int(self.p1_ilno.edit.text())
        p1_xlno = int(self.p1_xlno.edit.text())
        p1_crsx = float(self.p1_crsx.edit.text())
        p1_crsy = float(self.p1_crsy.edit.text())
        p2_ilno = int(self.p2_ilno.edit.text())
        p2_xlno = int(self.p2_xlno.edit.text())
        p2_crsx = float(self.p2_crsx.edit.text())
        p2_crsy = float(self.p2_crsy.edit.text())
        p3_ilno = int(self.p3_ilno.edit.text())
        p3_xlno = int(self.p3_xlno.edit.text())
        p3_crsx = float(self.p3_crsx.edit.text())
        p3_crsy = float(self.p3_crsy.edit.text())
        p1 = p1_ilno, p1_xlno, p1_crsx, p1_crsy
        p2 = p2_ilno, p2_xlno, p2_crsx, p2_crsy
        p3 = p3_ilno, p3_xlno, p3_crsx, p3_crsy
        self.sig_start.emit(name, p1, p2, p3)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = Dialog()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
