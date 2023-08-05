# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog, QLabel, QLineEdit, QSpinBox, QSlider, \
    QMessageBox, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox

from ezcad.config.base import _
from ezcad.utils.qthelpers import create_toolbutton_help
from ezcad.utils.logger import logger


class TimePlayer(QDialog):
    NAME = "Time player"

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        if parent is not None:
            self.treebase = parent  # connection wire to outside world
            self.database = self.treebase.object_data

        self.setup_page()
        self.load_polygon()

    def setup_page(self):
        self.setWindowTitle(_(self.NAME))
        vbox = QVBoxLayout()

        lbl_polygon = QLabel(_('Polygon object'))
        self.le_polygon = QLineEdit()
        btn_grab_polygon = QPushButton(_('Grab'))
        btn_grab_polygon.clicked.connect(self.grab_polygon)
        btn_load_polygon = QPushButton(_('Load'))
        btn_load_polygon.clicked.connect(self.load_polygon)

        hbox = QHBoxLayout()
        hbox.addWidget(lbl_polygon)
        hbox.addWidget(self.le_polygon)
        hbox.addWidget(btn_grab_polygon)
        hbox.addWidget(btn_load_polygon)
        vbox.addLayout(hbox)

        time_group = self.setup_page_time()
        vbox.addWidget(time_group)

        # help_btn = create_toolbutton_help(self, triggered=self.show_help)
        # hbox = QHBoxLayout()
        # hbox.addStretch()
        # hbox.addWidget(help_btn)
        # vbox.addLayout(hbox)
        
        self.setLayout(vbox)

    def setup_page_time(self):
        tm_group = QGroupBox(_('Select time'))
        lbl_tm0 = QLabel('First')
        lbl_tm1 = QLabel('Last')
        self.le_tm0 = QLineEdit()
        self.le_tm1 = QLineEdit()
        self.sld_tm = QSlider(Qt.Horizontal)
        self.sp_tm = QSpinBox()
        hbox = QHBoxLayout()
        hbox.addWidget(lbl_tm0)
        hbox.addWidget(self.le_tm0)
        hbox.addWidget(lbl_tm1)
        hbox.addWidget(self.le_tm1)
        tm_layout = QVBoxLayout()
        tm_layout.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.sld_tm)
        hbox.addWidget(self.sp_tm)
        tm_layout.addLayout(hbox)

        self.ctime_index = QLabel('Current index: ')
        self.ctime_value = QLabel('Current value: ')
        hbox = QHBoxLayout()
        hbox.addWidget(self.ctime_index)
        hbox.addWidget(self.ctime_value)
        tm_layout.addLayout(hbox)

        tm_group.setLayout(tm_layout)

        self.le_tm0.setReadOnly(True)
        self.le_tm1.setReadOnly(True)
        self.sld_tm.setTracking(False)
        self.sld_tm.setTickPosition(QSlider.TicksBelow)
        self.sld_tm.setSingleStep(1)
        self.sld_tm.valueChanged.connect(self.slider_value_changed_tm)
        # self.sp_tm.valueChanged.connect(self.spinbox_value_changed_tm)
        self.sp_tm.editingFinished.connect(self.spinbox_editing_finished_tm)

        return tm_group

    def slider_value_changed_tm(self, sliderValue):
        self.index = sliderValue
        self.sp_tm.setValue(self.index)  # sync spinbox
        self.check_index()

    def spinbox_value_changed_tm(self, spinboxValue):
        self.index = spinboxValue
        self.sld_tm.setValue(self.index)  # sync slider
        self.check_index()

    def spinbox_editing_finished_tm(self):
        self.index = self.sp_tm.value()
        self.sld_tm.setValue(self.index)  # sync slider
        self.check_index()

    def grab_polygon(self):
        geom = ['Polygon']
        self.polygon = self.treebase.grab_object(geom)
        self.le_polygon.setText(self.polygon.name)
        self.load_polygon()

    def load_polygon(self):
        """
        """
        self.index_old = 0
        if len(self.le_polygon.text().strip()) == 0:
            # This is for testing GUI without data polygon.
            self.dob = None
            self.tm0, self.tm1 = 1, 10
            self.index = self.tm0
        else:
            polygon_name = self.le_polygon.text()
            self.dob = self.database[polygon_name]
            self.tm0 = 1
            self.tm1 = self.dob.n_times
            self.index = self.dob.current_time_index + 1
            self.update_time_value()

        self.le_tm0.setText(str(self.tm0))
        self.le_tm1.setText(str(self.tm1))
        self.sld_tm.setRange(self.tm0, self.tm1)
        self.sld_tm.setTickInterval(int(self.tm1/5))
        self.sld_tm.setValue(self.index)
        self.sp_tm.setRange(self.tm0, self.tm1)
        # self.sp_tm.setSingleStep(self.tms)
        self.sp_tm.setValue(self.index)

    def check_index(self):
        """
        Avoid act twice by slider and spinbox
        """
        if self.index != self.index_old:
            self.time_changed(self.index)
            self.index_old = self.index

    def time_changed(self, index):
        logger.info("{} changes time to {}".format(self.NAME, index))
        if self.dob is not None:
            self.dob.change_time(index - 1)
            self.update_time_value()

    def update_time_value(self):
        self.ctime_index.setText("Current index: {}".format(self.index))
        self.ctime_value.setText("Current value: {}".format(
            self.dob.times[self.index-1]))

    def show_help(self):
        pass


def main():
    from qtpy.QtWidgets import QApplication, QDesktopWidget
    app = QApplication([])
    test = TimePlayer()
    test.show()

    screen = QDesktopWidget().screenGeometry()
    widget = test.geometry()
    print('screen', screen)
    print('widget', widget)

    app.exec_()


if __name__ == '__main__':
    main()
