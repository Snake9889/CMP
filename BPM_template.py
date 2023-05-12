#
#
from PyQt5.QtCore import pyqtSignal, QObject
import numpy as np
from PyQt5.QtWidgets import QLabel


class BPMTemplate(QObject):
    """   """
    data_ready = pyqtSignal(object)

    def __init__(self, bpm_name='', parent=None):
        super().__init__(parent)

        self.bpm_name = bpm_name
        self.num_pts = 1024
        self.data_len = self.num_pts

        self.dataT = None
        self.dataX = None
        self.dataZ = None
        self.dataI = None

        self.lboard = 0.01
        self.rboard = 0.5

    def force_data_ready(self, signature):
        """   """
        if signature == True:
            if self.dataT is not None:
                self.data_ready.emit(self)
            else:
                pass

    def save_settings(self):
        """   """
        pass

    def read_settings(self):
        """   """
        pass
