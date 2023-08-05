# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.

import numpy as np
from ezcad.utils.worker_thread import WorkerThread
from .new.from_coordinate import Dialog as PolygonCoordDialog
from .new.covid19_spread import Dialog as Covid19Dialog
from .tool.time_player import TimePlayer
from .funs.covid19_colorbar import DiscreteColor

from .new.new import from_coordinate, dummy_dob, covid19_pandemic


class Bartender:
    """Bartender handles orders from the menubar."""
    def __init__(self, treebase):
        self.treebase = treebase
        self.workerThreads = []

    def new_from_coord(self):
        dialog = PolygonCoordDialog(self.treebase)
        dialog.sig_start.connect(self.new_from_coord_worker)
        dialog.show()
        return dialog

    def new_from_coord_worker(self, *args):
        # dob = from_coordinate(*args, survey=self.treebase.survey)
        dob = dummy_dob()
        self.treebase.sigDataObjectLoaded.emit(dob)

    def covid19_global_spread(self):
        dialog = Covid19Dialog(self.treebase)
        dialog.sig_start.connect(self.covid19_global_spread_worker)
        dialog.show()
        return dialog

    def covid19_global_spread_worker(self, *args):
        dob = covid19_pandemic(*args, survey=self.treebase.survey)
        self.treebase.sigDataObjectLoaded.emit(dob)

    def open_time_player(self):
        dialog = TimePlayer(self.treebase)
        dialog.show()
        return dialog

    def covid19_global_cmap(self):
        dialog = DiscreteColor(self.treebase)
        dialog.show()
        return dialog
