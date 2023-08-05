# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
Style setting pages for line.
"""

# Standard library imports
import copy

# Third party imports
import numpy as np
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QLabel, QVBoxLayout, QFormLayout, QGroupBox, \
    QPushButton, QScrollBar, QColorDialog, QSpinBox, QComboBox

# Local imports
from ezcad.config.base import _
from ezcad.utils import icon_manager as ima
from ezcad.utils.plotting import atom_symbols
from ezcad.widgets.style_page import StylePage
from ezcad.widgets.property_table import PropertyDistribtionTable


class GraphicsPage(StylePage):
    NAME = _("Line Graphics")
    ICON = ima.icon('genprefs')

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.width = QSpinBox()
        self.opacity = QScrollBar(Qt.Horizontal)
        self.colorLabel = QLabel(_('Color'))
        self.qtColor = None
        self.qtColor_atom = None

    def setup_page(self):
        palette = QPushButton(_('Palette'))
        palette.clicked.connect(self.line_color_picker)

        opacity = QLabel(_('Opacity'))
        self.opacity.setMaximum(255)
        # self.opacity.sliderMoved.connect(self.line_opacity_changed)

        width = QLabel(_('Width'))
        self.width.setRange(0, 10)

        shadow = QLabel(_('Shadow'))
        fillLevel = QLabel(_('Fill level'))
        fillBrush = QLabel(_('Fill brush'))

        form = QFormLayout()
        form.addRow(width, self.width)
        form.addRow(self.colorLabel, palette)
        form.addRow(opacity, self.opacity)
        form.addRow(shadow, QLabel(_('TODO')))
        form.addRow(fillLevel, QLabel(_('TODO')))
        form.addRow(fillBrush, QLabel(_('TODO')))

        group = QGroupBox(_("Line"))
        group.setLayout(form)

        atom_size = QLabel(_('Size'))
        atom_symbol = QLabel(_('Symbol'))
        atom_palette = QPushButton(_('Palette'))
        atom_opacity = QLabel(_('Opacity'))
        self.atom_size = QSpinBox()
        self.atom_symbol = QComboBox()
        self.atom_color_label = QLabel(_('Color'))
        self.atom_opacity = QScrollBar(Qt.Horizontal)
        self.atom_opacity.setMaximum(255)
        atom_palette.clicked.connect(self.atom_color_picker)

        atom_form = QFormLayout()
        atom_form.addRow(atom_size, self.atom_size)
        atom_form.addRow(atom_symbol, self.atom_symbol)
        atom_form.addRow(self.atom_color_label, atom_palette)
        atom_form.addRow(atom_opacity, self.atom_opacity)

        atom_group = QGroupBox(_("Atom"))
        atom_group.setLayout(atom_form)

        box = QVBoxLayout()
        box.addWidget(group)
        box.addWidget(atom_group)
        self.setLayout(box)

    # def line_opacity_changed(self):
    #     # update 2D plot
    #     lineOpacity = self.opacity.value()
    #     self.qtColor.setAlpha(lineOpacity)
    #     self.pg2d.setPen(self.qtColor)
    #     # update 3D plot
    #     color = self.qtColor.getRgbF()
    #     self.dob.set_pg3d_lines(color=color)

    def atom_color_picker(self):
        self.qtColor = QColorDialog.getColor(self.qtColor_atom)
        self.atom_color_label.setStyleSheet("QWidget { background-color: %s}" %
            self.qtColor_atom.name())

    def line_color_picker(self):
        self.qtColor = QColorDialog.getColor(self.qtColor)
        self.colorLabel.setStyleSheet("QWidget { background-color: %s}" %
            self.qtColor.name())

    def load_style(self):
        style = self.dob.line_style
        # self.pg2d = self.dob.pg2d
        alpha = style['opacity']
        self.opacity.setValue(alpha)
        r, g, b, a = style['color']
        self.qtColor = QColor(r, g, b, alpha)  # integers 0-255
        self.width.setValue(style['width'])

        atom_style = self.dob.atom_style
        self.atom_size.setValue(atom_style['size'])
        index = atom_symbols.index(atom_style['symbol'])
        self.atom_symbol.addItems(atom_symbols)
        self.atom_symbol.setCurrentIndex(index)
        alpha = atom_style['opacity']
        self.atom_opacity.setValue(alpha)
        r, g, b, a = atom_style['face_color']
        self.qtColor_atom = QColor(r, g, b, alpha)  # integers 0-255`

    def apply_changes(self):
        opacity = self.opacity.value()
        width = self.width.value()
        r, g, b, a = self.qtColor.getRgb()
        style = copy.deepcopy(self.dob.line_style)
        style['color'] = (r, g, b, opacity)
        style['opacity'] = opacity
        style['width'] = width
        # save style to object in memory
        self.dob.set_line_style(line_style=style, update_plots=True)

        symbol = self.atom_symbol.currentText()
        size = self.atom_size.value()
        alpha = self.atom_opacity.value()
        r, g, b, a = self.qtColor_atom.getRgb()
        style = copy.deepcopy(self.dob.atom_style)
        style['symbol'] = symbol
        style['size'] = size
        style['face_color'] = (r, g, b, alpha)
        style['opacity'] = alpha
        # save style to object in memory
        self.dob.set_atom_style(atom_style=style, update_plots=True)


class DataInfoPage(StylePage):
    NAME = "Information"
    ICON = ima.icon('DataInformation')

    def setup_page(self):
        name_label = QLabel(_("Object name"))
        name_value = QLabel(self.dob.name)
        nv_label = QLabel(_('Number of vertexes'))
        nv_value = QLabel(str(self.dob.n_vertexes))
        if self.dob.vertexes['connect'] is not None:
            connect = self.dob.vertexes['connect']
            nbreak = np.count_nonzero(connect == 0)
        else:
            nbreak = 0
        ns_label = QLabel(_('Number of segments'))
        ns_value = QLabel(str(nbreak+1))
        form = QFormLayout()
        form.addRow(name_label, name_value)
        form.addRow(nv_label, nv_value)
        form.addRow(ns_label, ns_value)

        self.prop_table = PropertyDistribtionTable(self.dob.prop)
        btn_refresh = QPushButton(_('Refresh property table'))
        btn_refresh.clicked.connect(self.refresh_prop_table)
        box = QVBoxLayout()
        box.addLayout(form)
        box.addWidget(btn_refresh)
        box.addWidget(self.prop_table)
        self.setLayout(box)

    def load_style(self):
        pass

    def apply_changes(self):
        pass
