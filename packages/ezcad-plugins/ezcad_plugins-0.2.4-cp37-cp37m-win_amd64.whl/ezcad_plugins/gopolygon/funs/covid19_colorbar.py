# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

from qtpy.QtGui import QColor
from qtpy.QtWidgets import QDialog, QLabel, QFormLayout


def new_ticks():
    # Note add 1 because it starts from -1 of no data available.
    base = 1000001.  # 1000K or 1 million
    vals = [0, 1, 1001, 5001, 10001, 50001, 100001, 500001, 1000001]
    colors = [
        (170, 255, 255, 255),  # -1        cyan
        (255, 255, 255, 255),  # 0         white
        (255, 200, 255, 255),  # 1000      pink gray
        (255, 50, 255, 255),   # 5000      pink
        (255, 170, 170, 255),  # 10000     salmon
        (255, 0, 0, 255),      # 50000     red
        (160, 0, 0, 255),      # 100000    dark red
        (100, 0, 0, 255),      # 500000
        (0, 0, 0, 255),        # 1000000    black
    ]
    ticks = []
    for i in range(len(vals)):
        tick = (vals[i]/base, colors[i])
        ticks.append(tick)
    return ticks, vals, colors


class DiscreteColor(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        form = QFormLayout()
        self.setLayout(form)
        ticks, vals, colors = new_ticks()
        # for i in range(len(vals)):
        # Common display low at bottom and high at top.
        for i, e in reversed(list(enumerate(vals))):
            val = vals[i] - 1
            c = colors[i]
            qcolor = QColor(c[0], c[1], c[2], c[3])
            lbc = QLabel()
            lbc.setFixedWidth(20)
            lbv = QLabel(str(val))
            lbc.setStyleSheet("QWidget { background-color: %s}" %
                qcolor.name())
            form.addRow(lbc, lbv)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    test = DiscreteColor()
    test.show()
    app.exec_()


if __name__ == '__main__':
    main()
