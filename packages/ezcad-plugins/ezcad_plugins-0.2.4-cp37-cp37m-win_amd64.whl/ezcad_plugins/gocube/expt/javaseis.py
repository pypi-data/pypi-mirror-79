# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import Signal
from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog
from ezcad.utils.envars import NCORE


class Dialog(EasyDialog):
    NAME = _("Export cube to JavaSeis dataset")
    sig_start = Signal(str, str, str, int)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("Output cube")
        geom = ['Cube']
        self.grabob = self.create_grabob(text, geom=geom)
        self.layout.addWidget(self.grabob)

        text = _("Property")
        self.property = self.create_combobox(text)
        self.property.combobox.setMinimumContentsLength(20)
        self.layout.addWidget(self.property)

        text = _("JavaSeis name")
        self.jsname = self.create_browsedir(text)
        self.layout.addWidget(self.jsname)

        nth = str(NCORE - 1)
        self.threads = self.create_lineedit("Number of threads", default=nth)
        self.layout.addWidget(self.threads)

        action = self.create_action()
        self.layout.addWidget(action)

    def apply(self):
        cube_name = self.grabob.lineedit.edit.text()
        prop_name = self.property.combobox.currentText()
        file_name = self.jsname.lineedit.edit.text()
        threads = int(self.threads.edit.text())
        self.sig_start.emit(cube_name, prop_name, file_name, threads)

    def load_object(self):
        cube = self.object # assigned by grab object
        propList = list(cube.prop.keys())
        self.property.combobox.clear()
        self.property.combobox.addItems(propList)
        prop_name = cube.current_property
        index = propList.index(prop_name)
        self.property.combobox.setCurrentIndex(index)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = Dialog()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
