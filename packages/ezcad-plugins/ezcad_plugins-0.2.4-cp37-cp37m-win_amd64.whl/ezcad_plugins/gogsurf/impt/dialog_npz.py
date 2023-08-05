# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import Signal
from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog
from ezcad.utils.envars import FILTER_ALL_FILES


class Dialog(EasyDialog):
    NAME = _("Load NPZ file")
    HELP_BODY = _("<b>Example</b> <br>")
    sig_start = Signal(str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        filters = "NPZ files (*.npz)" + FILTER_ALL_FILES
        self.input = self.create_browsefile(_("NPZ file"), filters=filters)
        self.layout.addWidget(self.input)

        self.object_name = self.create_lineedit("Object name")
        self.layout.addWidget(self.object_name)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        fn = self.input.lineedit.edit.text()
        object_name = self.object_name.edit.text()
        self.sig_start.emit(fn, object_name)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = Dialog()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
