# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import Signal
from qtpy.QtWidgets import QTextEdit, QLabel, QRadioButton, QButtonGroup, \
    QHBoxLayout
from ezcad.config.base import _
from ezcad.widgets.ezdialog import EasyDialog


class Dialog(EasyDialog):
    NAME = _("New polygon from coordinates")
    sig_start = Signal(str, str, str, str, str)

    def __init__(self, parent=None):
        EasyDialog.__init__(self, parent)
        self.setup_page()

    def setup_page(self):
        text = _("New polygon")
        self.new_polygon = self.create_lineedit(text)
        self.layout.addWidget(self.new_polygon)

        text = _("Comment")
        self.comment = self.create_lineedit(text, default='#')
        self.layout.addWidget(self.comment)
        
        text = _("Delimiter")
        self.delimiter = self.create_lineedit(text, default='comma')
        self.layout.addWidget(self.delimiter)
        
        lblSystem = QLabel(_("Coordinate system"))
        self.rb_xy = QRadioButton(_("X,Y"))
        self.rb_ln = QRadioButton(_("ILNO,XLNO"))
        bgSystem = QButtonGroup()
        bgSystem.addButton(self.rb_xy)
        bgSystem.addButton(self.rb_ln)
        hbox = QHBoxLayout()
        hbox.addWidget(lblSystem)
        hbox.addWidget(self.rb_xy)
        hbox.addWidget(self.rb_ln)
        self.layout.addLayout(hbox)

        text = _("# Insert X, Y, Z")
        self.textbox = QTextEdit(text, self)
        self.layout.addWidget(self.textbox)

        action = self.create_action()
        self.layout.addWidget(action)

        self.rb_xy.toggled.connect(lambda: self.set_method(self.rb_xy))
        self.rb_ln.toggled.connect(lambda: self.set_method(self.rb_ln))
        self.rb_xy.setChecked(True)
        
    def set_method(self, rb):
        if rb.isChecked():
            if rb.text() == _("X,Y"):
                self.method = 'xy'
            elif rb.text() == _("ILNO,XLNO"):
                self.method = 'ln'
            else:
                raise ValueError("unknown value {}".format(rb.text()))

    def apply(self):
        object_name = self.new_polygon.edit.text()
        comment = self.comment.edit.text()
        delimiter = self.delimiter.edit.text().lower()
        method = self.method
        text = self.textbox.toPlainText()
        self.sig_start.emit(object_name, comment, delimiter, method, text)
        

def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = Dialog()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
