# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import Signal
from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog
from ezcad.utils.envars import FILTER_ALL_FILES


class Dialog(EasyDialog):
    NAME = _("Load Numpy memmap")
    sig_start = Signal(str, str, str, str, tuple)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Numpy memmap")
        filters = "DAT files (*.dat)" + FILTER_ALL_FILES
        self.input = self.create_browsefile(text, filters=filters)
        self.layout.addWidget(self.input)
        self.object_name = self.create_lineedit(_("Object name"))
        self.layout.addWidget(self.object_name)
        self.prop_name = self.create_lineedit(_("Property name"))
        self.layout.addWidget(self.prop_name)
        self.shape = self.create_lineedit(_("Shape"), default="10, 10, 10")
        self.layout.addWidget(self.shape)
        self.dtype = self.create_lineedit(_("Data type"), default="float32")
        self.layout.addWidget(self.dtype)
        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        fn = self.input.lineedit.edit.text()
        object_name = self.object_name.edit.text()
        prop_name = self.prop_name.edit.text()
        shape = self.shape.edit.text()
        dtype = self.dtype.edit.text()
        shape = [int(x) for x in shape.split(',')]
        shape = (shape[0], shape[1], shape[2])
        self.sig_start.emit(fn, object_name, prop_name, dtype, shape)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = Dialog()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
