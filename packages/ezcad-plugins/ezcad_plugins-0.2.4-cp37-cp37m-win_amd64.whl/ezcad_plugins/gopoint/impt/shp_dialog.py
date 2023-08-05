# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import Signal
from qtpy.QtWidgets import QTextBrowser, QPushButton, QHBoxLayout
from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog
from ezcad.utils.envars import FILTER_ALL_FILES
from .read_shapefile import preview_shapefile


class Dialog(EasyDialog):
    NAME = _("Load Shapefile")
    HELP_BODY = _("<b>Example</b> <br>")
    sig_start = Signal(str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        filters = "Shape files (*.shp)" + FILTER_ALL_FILES
        self.input = self.create_browsefile(_("Shape file"), filters=filters)
        self.layout.addWidget(self.input)

        self.object_name = self.create_lineedit("Object name")
        self.layout.addWidget(self.object_name)

        self.previewLines = self.create_lineedit("Preview shapes", default='5')
        btnLoad = QPushButton(_('Load'))
        btnLoad.clicked.connect(self.load_shapes)
        hbox = QHBoxLayout()
        hbox.addWidget(self.previewLines)
        hbox.addWidget(btnLoad)
        self.layout.addLayout(hbox)

        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setFontFamily("monospace")
        self.layout.addWidget(self.textBrowser)

        action = self.create_action()
        self.layout.addWidget(action)

    def load_shapes(self):
        filename = self.input.lineedit.edit.text()
        nr = int(self.previewLines.edit.text())
        text = preview_shapefile(filename, nr=nr)
        self.textBrowser.setText(text)

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
