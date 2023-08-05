# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import Signal
from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog


class Dialog(EasyDialog):
    NAME = _("Covid-19 global pandemic")
    sig_start = Signal(str, str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Object name")
        self.new_polygon = self.create_lineedit(text, default='covid-19')
        self.layout.addWidget(self.new_polygon)

        text = _("Covid-19 dataset")
        self.covid19 = self.create_lineedit(text, default='default')
        self.layout.addWidget(self.covid19)

        text = _("Worldmap shapefile")
        self.map = self.create_lineedit(text, default='default')
        self.layout.addWidget(self.map)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        object_name = self.new_polygon.edit.text()
        covid19 = self.covid19.edit.text()
        map = self.map.edit.text()
        self.sig_start.emit(object_name, covid19, map)
        

def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = Dialog()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
