# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import Signal
from qtpy.QtWidgets import QHBoxLayout
from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog


class Dialog(EasyDialog):
    NAME = _("New point from random numbers")
    sig_start = Signal(str, int, float, float)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("New point")
        self.new_point = self.create_lineedit(text)
        self.layout.addWidget(self.new_point)

        text = _("Number of vertexes")
        self.n_vertex = self.create_lineedit(text)
        self.n_vertex.label.setWordWrap(False)
        self.layout.addWidget(self.n_vertex)

        text = _("Mean")
        default = '0.0'
        self.mean = self.create_lineedit(text, default=default)

        text = _("Standard deviation")
        default = '1.0'
        self.std = self.create_lineedit(text, default=default)

        hbox = QHBoxLayout()
        hbox.addWidget(self.mean)
        hbox.addWidget(self.std)
        self.layout.addLayout(hbox)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        object_name = self.new_point.edit.text()
        n_vertex = int(self.n_vertex.edit.text())
        mean = float(self.mean.edit.text())
        std = float(self.std.edit.text())
        self.sig_start.emit(object_name, n_vertex, mean, std)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = Dialog()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
