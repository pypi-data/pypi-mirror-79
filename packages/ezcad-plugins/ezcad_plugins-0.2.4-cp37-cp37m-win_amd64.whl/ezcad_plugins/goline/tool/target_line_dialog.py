# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
Dialog for select target lines on map view.
"""

import numpy as np
from qtpy.QtCore import Signal
from qtpy.QtWidgets import (QDialog, QLabel, QSpinBox, QFormLayout,
    QPushButton, QRadioButton, QVBoxLayout, QHBoxLayout, QGroupBox, QMessageBox)

from ezcad.config.base import _


class Dialog(QDialog):
    sig_start = Signal(object)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.survey = None
        self.setup_page()
        if self.parent is not None:
            self.survey = self.parent.survey
        if self.survey is not None:
            if not hasattr(self.survey, 'geometry'):
                QMessageBox.critical(self, _("Error"),
                    _("No survey geometry has been loaded yet."))
                return
            else:
                self.load()

    def setup_page(self):
        self.setWindowTitle(_("Select target lines"))
        vbox = QVBoxLayout()

        lbl_select = QLabel(_('Select method:'))
        self.rb_iline = QRadioButton(_('Inline'))
        self.rb_xline = QRadioButton(_('Crossline'))
        self.rb_rect = QRadioButton(_('Rectangle'))

        hbox = QHBoxLayout()
        hbox.addWidget(self.rb_iline)
        hbox.addWidget(self.rb_xline)
        hbox.addWidget(self.rb_rect)

        vbox.addWidget(lbl_select)
        vbox.addLayout(hbox)

        self.iline_group = QGroupBox(_('Select inline'))
        lbl_il_iline = QLabel(_('Inline number'))
        lbl_il_xline_bgn = QLabel(_('Crossline start'))
        lbl_il_xline_end = QLabel(_('Crossline end'))
        self.sp_il_iline = QSpinBox()
        self.sp_il_xline_bgn = QSpinBox()
        self.sp_il_xline_end = QSpinBox()
        iline_layout = QFormLayout()
        iline_layout.addRow(lbl_il_iline, self.sp_il_iline)
        iline_layout.addRow(lbl_il_xline_bgn, self.sp_il_xline_bgn)
        iline_layout.addRow(lbl_il_xline_end, self.sp_il_xline_end)
        self.iline_group.setLayout(iline_layout)

        self.xline_group = QGroupBox(_('Select crossline'))
        lbl_xl_xline = QLabel(_('Crossline number'))
        lbl_xl_iline_bgn = QLabel(_('Inline start'))
        lbl_xl_iline_end = QLabel(_('Inline end'))
        self.sp_xl_xline = QSpinBox()
        self.sp_xl_iline_bgn = QSpinBox()
        self.sp_xl_iline_end = QSpinBox()
        xline_layout = QFormLayout()
        xline_layout.addRow(lbl_xl_xline, self.sp_xl_xline)
        xline_layout.addRow(lbl_xl_iline_bgn, self.sp_xl_iline_bgn)
        xline_layout.addRow(lbl_xl_iline_end, self.sp_xl_iline_end)
        self.xline_group.setLayout(xline_layout)

        self.rect_group = QGroupBox(_('Select rectangle'))
        lbl_rt_iline_bgn = QLabel(_('Inline start'))
        lbl_rt_iline_end = QLabel(_('Inline end'))
        lbl_rt_xline_bgn = QLabel(_('Crossline start'))
        lbl_rt_xline_end = QLabel(_('Crossline end'))
        self.sp_rt_iline_bgn = QSpinBox()
        self.sp_rt_iline_end = QSpinBox()
        self.sp_rt_xline_bgn = QSpinBox()
        self.sp_rt_xline_end = QSpinBox()
        rect_layout = QFormLayout()
        rect_layout.addRow(lbl_rt_iline_bgn, self.sp_rt_iline_bgn)
        rect_layout.addRow(lbl_rt_iline_end, self.sp_rt_iline_end)
        rect_layout.addRow(lbl_rt_xline_bgn, self.sp_rt_xline_bgn)
        rect_layout.addRow(lbl_rt_xline_end, self.sp_rt_xline_end)
        self.rect_group.setLayout(rect_layout)

        vbox.addWidget(self.iline_group)
        vbox.addWidget(self.xline_group)
        vbox.addWidget(self.rect_group)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.rb_iline.toggled.connect(self.toggle)
        self.rb_xline.toggled.connect(self.toggle)
        self.rb_rect.toggled.connect(self.toggle)
        self.rb_iline.setChecked(True)

    def load(self):
        ilno_min = self.survey.binning['ilno_min']
        ilno_max = self.survey.binning['ilno_max']
        xlno_min = self.survey.binning['xlno_min']
        xlno_max = self.survey.binning['xlno_max']

        self.sp_il_iline.setRange(ilno_min, ilno_max)
        self.sp_il_xline_bgn.setRange(xlno_min, xlno_max)
        self.sp_il_xline_end.setRange(xlno_min, xlno_max)
        self.sp_il_iline.setValue(ilno_min)
        self.sp_il_xline_bgn.setValue(xlno_min)
        self.sp_il_xline_end.setValue(xlno_max)

        self.sp_xl_xline.setRange(xlno_min, xlno_max)
        self.sp_xl_iline_bgn.setRange(ilno_min, ilno_max)
        self.sp_xl_iline_end.setRange(ilno_min, ilno_max)
        self.sp_xl_xline.setValue(xlno_min)
        self.sp_xl_iline_bgn.setValue(ilno_min)
        self.sp_xl_iline_end.setValue(ilno_max)

        self.sp_rt_iline_bgn.setRange(ilno_min, ilno_max)
        self.sp_rt_iline_end.setRange(ilno_min, ilno_max)
        self.sp_rt_xline_bgn.setRange(xlno_min, xlno_max)
        self.sp_rt_xline_end.setRange(xlno_min, xlno_max)
        self.sp_rt_iline_bgn.setValue(ilno_min)
        self.sp_rt_iline_end.setValue(ilno_max)
        self.sp_rt_xline_bgn.setValue(xlno_min)
        self.sp_rt_xline_end.setValue(xlno_max)

        self.sp_il_iline.valueChanged.connect(self.apply)
        self.sp_il_xline_bgn.valueChanged.connect(self.apply)
        self.sp_il_xline_end.valueChanged.connect(self.apply)
        self.sp_xl_xline.valueChanged.connect(self.apply)
        self.sp_xl_iline_bgn.valueChanged.connect(self.apply)
        self.sp_xl_iline_end.valueChanged.connect(self.apply)
        self.sp_rt_iline_bgn.valueChanged.connect(self.apply)
        self.sp_rt_iline_end.valueChanged.connect(self.apply)
        self.sp_rt_xline_bgn.valueChanged.connect(self.apply)
        self.sp_rt_xline_end.valueChanged.connect(self.apply)

    def toggle(self):
        if self.rb_iline.isChecked():
            self.iline_group.setEnabled(True)
            self.xline_group.setEnabled(False)
            self.rect_group.setEnabled(False)
        elif self.rb_xline.isChecked():
            self.iline_group.setEnabled(False)
            self.xline_group.setEnabled(True)
            self.rect_group.setEnabled(False)
        elif self.rb_rect.isChecked():
            self.iline_group.setEnabled(False)
            self.xline_group.setEnabled(False)
            self.rect_group.setEnabled(True)
        else:
            raise ValueError("Unknown value")
        self.apply()

    def apply(self):
        if self.rb_iline.isChecked():
            ilno = self.sp_il_iline.value()
            xlno_bgn = self.sp_il_xline_bgn.value()
            xlno_end = self.sp_il_xline_end.value()
            point1 = [ilno, xlno_bgn]
            point2 = [ilno, xlno_end]
            points = np.array([point1, point2])
        elif self.rb_xline.isChecked():
            xlno = self.sp_xl_xline.value()
            ilno_bgn = self.sp_xl_iline_bgn.value()
            ilno_end = self.sp_xl_iline_end.value()
            point1 = [ilno_bgn, xlno]
            point2 = [ilno_end, xlno]
            points = np.array([point1, point2])
        elif self.rb_rect.isChecked():
            ilno_bgn = self.sp_rt_iline_bgn.value()
            ilno_end = self.sp_rt_iline_end.value()
            xlno_bgn = self.sp_rt_xline_bgn.value()
            xlno_end = self.sp_rt_xline_end.value()
            point1 = [ilno_bgn, xlno_bgn]
            point2 = [ilno_bgn, xlno_end]
            point3 = [ilno_end, xlno_end]
            point4 = [ilno_end, xlno_bgn]
            # explicitly make tail connect to head
            points = np.array([point1, point2, point3, point4, point1])
        else:
            raise ValueError("Unknown value")

        self.sig_start.emit(points)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = Dialog()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
