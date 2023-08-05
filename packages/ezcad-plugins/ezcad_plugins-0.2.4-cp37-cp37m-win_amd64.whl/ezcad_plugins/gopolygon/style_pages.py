# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
Style setting pages for polygon.
"""

# Standard library imports
import copy

# Third party imports
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QLabel, QComboBox, QVBoxLayout, QFormLayout, \
    QRadioButton, QHBoxLayout, QGroupBox, QPushButton, QColorDialog, \
    QScrollBar, QSpinBox, QButtonGroup

# Local imports
from ezcad.config.base import _
from ezcad.utils import icon_manager as ima
from ezcad.widgets.style_page import StylePage
# from ezcad.widgets.property_table import PropertyDistribtionTable


class GraphicsPage(StylePage):
    NAME = _("Polygon Graphics")
    ICON = ima.icon('genprefs')

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.fc_label = QLabel(_('Fill color'))
        self.color_vary = QRadioButton(_('vary'))
        self.color_mono = QRadioButton(_('single'))
        self.bc_label = QLabel(_('Border color'))
        self.border_width = QSpinBox()
        self.fill_qcolor = None
        self.border_qcolor = None

    def setup_page(self):
        border_width = QLabel(_('Border width'))
        coloring = QLabel(_('Fill coloring'))
        bg_method = QButtonGroup()
        bg_method.addButton(self.color_mono)
        bg_method.addButton(self.color_vary)
        box_method = QHBoxLayout()
        box_method.addWidget(self.color_mono)
        box_method.addWidget(self.color_vary)

        fill_palette = QPushButton(_('Palette'))
        fill_palette.clicked.connect(self.fill_color_picker)
        border_palette = QPushButton(_('Palette'))
        border_palette.clicked.connect(self.border_color_picker)

        form = QFormLayout()
        form.addRow(coloring, box_method)
        form.addRow(self.fc_label, fill_palette)
        form.addRow(self.bc_label, border_palette)
        form.addRow(border_width, self.border_width)

        group = QGroupBox(_("Polygon"))
        group.setLayout(form)

        box = QVBoxLayout()
        box.addWidget(group)
        self.setLayout(box)

    def fill_color_picker(self):
        self.fill_qcolor = QColorDialog.getColor(self.fill_qcolor)
        self.fc_label.setStyleSheet("QWidget { background-color: %s}" %
            self.fill_qcolor.name())

    def border_color_picker(self):
        self.border_qcolor = QColorDialog.getColor(self.border_qcolor)
        self.bc_label.setStyleSheet("QWidget { background-color: %s}" %
            self.border_qcolor.name())

    def load_style(self):
        if self.dob.style is None:
            self.dob.set_style()
        style = self.dob.style
        self.border_width.setValue(style['border_width'])
        coloring = style['coloring']
        if coloring == 1:
            self.color_mono.setChecked(True)
        else:
            self.color_vary.setChecked(True)
        r, g, b, a = style['fill_color']
        self.fill_qcolor = QColor(r, g, b, a)
        r, g, b, a = style['border_color']
        self.border_qcolor = QColor(r, g, b, a)

    def apply_changes(self):
        if self.color_mono.isChecked():
            coloring = 1
        else:
            coloring = 2
        style = copy.deepcopy(self.dob.style)
        style['border_width'] = self.border_width.value()
        style['coloring'] = coloring
        r, g, b, a = self.fill_qcolor.getRgb()
        style['fill_color'] = (r, g, b, a)
        r, g, b, a = self.border_qcolor.getRgb()
        style['border_color'] = (r, g, b, a)
        # save style to object in memory
        self.dob.set_style(style=style, update_plots=True)


class DataInfoPage(StylePage):
    NAME = "Information"
    ICON = ima.icon('DataInformation')

    def setup_page(self):
        name_label = QLabel(_("Object name"))
        name_value = QLabel(self.dob.name)
        nv_label = QLabel(_('Number of records'))
        nv_value = QLabel(str(self.dob.n_records))
        np_label = QLabel(_('Number of properties'))
        np_value = QLabel(str(self.dob.n_properties))
        nt_label = QLabel(_('Number of times'))
        nt_value = QLabel(str(self.dob.n_times))

        form = QFormLayout()
        form.addRow(name_label, name_value)
        form.addRow(nv_label, nv_value)
        form.addRow(np_label, np_value)
        form.addRow(nt_label, nt_value)

        # self.prop_table = PropertyDistribtionTable(self.dob.prop)
        # refresh = QPushButton(_('Refresh property table'))
        # refresh.clicked.connect(self.refresh_prop_table)

        box = QVBoxLayout()
        box.addLayout(form)
        # box.addWidget(refresh)
        # box.addWidget(self.prop_table)
        self.setLayout(box)

    def load_style(self):
        pass

    def apply_changes(self):
        pass


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = GraphicsPage()
    test.setup_page()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
