# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, Qt, QSettings
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import uic
import os.path


class StatusWidget(QWidget):
    """   """

    def __init__(self, parent=None):
        super(StatusWidget, self).__init__(parent)

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'StatusWidget.ui'), self)

