# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtCore import QSize, QCoreApplication


class SettingsControl(QObject):
    """   """
    save_data = pyqtSignal(object)
    read_data = pyqtSignal(QObject)

    def __init__(self, parent=None):
        super(SettingsControl, self).__init__(parent)

        self.obj_list = []

    def add_object(self, object):
        """   """
        self.obj_list.append(object)

    def save_settings(self):
        """   """
        QCoreApplication.setApplicationName("BTMS")
        for obj in self.obj_list:
            obj.save_settings()

    def read_settings(self):
        """   """
        QCoreApplication.setApplicationName("BTMS")
        for obj in self.obj_list:
            obj.read_settings()
