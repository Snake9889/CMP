# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, Qt, QSettings
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from command_parser import TerminalParser
import os.path


class ControlWidget(QWidget):
    """   """
    window_changed_str = pyqtSignal(str)
    method_changed_str = pyqtSignal(str)
    boards_changed = pyqtSignal(object)
    scale_changed_obj = pyqtSignal(object)
    signature = pyqtSignal(bool)

    default_str_id = "Warning"

    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'ControlWidget.ui'), self)

        argument_parser = TerminalParser()

        self.window = "None"
        self.method = argument_parser.method_name_parsed
        self.bpm = argument_parser.bpm_name_parsed
        self.boards = None
        self.lboard = 0.01
        self.rboard = 0.5
        self.scale = "None"

        self.str_id = self.default_str_id

        buttons = [
            self.usePeakBtn,
            self.useGassiorBtn,
            self.useNaffBtn,
        ]

        id = 1
        for btn in buttons:
            btn.setStyleSheet("QPushButton {background-color: none}"
                              "QPushButton:checked {background-color: green}")
            self.buttonGroup.setId(btn, id)
            id = id + 1

        self.lboardSBox.setValue(0.05)
        self.rboardSBox.setValue(0.3)

        self.checkWindowBox.currentIndexChanged.connect(self.on_window_checked)
        self.buttonGroup.buttonClicked['int'].connect(self.on_method_checked)
        self.lboardSBox.valueChanged.connect(self.on_lboardsbox_changed)
        self.rboardSBox.valueChanged.connect(self.on_rboardsbox_changed)
        self.log_mod.stateChanged.connect(self.on_plot_checked)

    def on_window_checked(self, state):
        """   """
        if state == 0:
            self.window = "None"
        elif state == 1:
            self.window = "Hann"
        elif state == 2:
            self.window = "Hamming"
        else:
            self.window = "None"

        self.window_changed_str.emit(self.window)

    def on_method_checked(self, state):
        """   """
        if state == 0:
            self.method = "None"
        elif state == 1:
            self.method = "Peak"
        elif state == 2:
            self.method = "Gassior"
        elif state == 3:
            self.method = "Naff"
        else:
            self.method = "None"

        self.method_changed_str.emit(self.method)

    def on_lboardsbox_changed(self, value):
        """   """
        self.lboard = value
        self.on_boards_changed()

    def on_rboardsbox_changed(self, value):
        """   """
        self.rboard = value
        self.on_boards_changed()

    def on_plot_checked(self, state):
        """   """
        if state == Qt.Checked:
            self.scale = "Log_Y"
        else:
            self.scale = "Normal"
        self.scale_changed_obj.emit(self)

    def on_boards_changed(self):
        """   """
        self.boards = {
            "lboard": self.lboard,
            "rboard": self.rboard
        }
        self.boards_changed.emit(self.boards)
        self.signature.emit(True)

    def on_boards_changed_ext(self, boards_dict):
        """   """
        self.lboard = boards_dict[0]
        self.rboard = boards_dict[1]

        self.lboardSBox.valueChanged.disconnect()
        self.lboardSBox.setValue(self.lboard)
        self.lboardSBox.valueChanged.connect(self.on_lboardsbox_changed)

        self.rboardSBox.valueChanged.disconnect()
        self.rboardSBox.setValue(self.rboard)
        self.rboardSBox.valueChanged.connect(self.on_rboardsbox_changed)

        self.on_boards_changed()

    def set_str_id(self, str):
        """   """
        self.str_id = str

    def save_settings(self):
        """   """
        settings = QSettings()
        settings.beginGroup(self.bpm)
        settings.beginGroup(self.str_id)
        settings.setValue("window", self.window)
        settings.setValue("method", self.method)
        settings.setValue("lboard", self.lboard)
        settings.setValue("rboard", self.rboard)
        settings.setValue("scale", self.scale)
        settings.endGroup()
        print("Saved!!!!!")
        settings.sync()

    def read_settings(self):
        """   """
        settings = QSettings()

        if self.str_id == "Data_X":
            settings.beginGroup(self.bpm)
            settings.beginGroup(self.str_id)
            self.window = settings.value("window", "None")
            self.method = settings.value("method", "None")
            self.lboard = settings.value("lboard", 0.10, type=float)
            self.rboard = settings.value("rboard", 0.25, type=float)
            self.scale = settings.value("scale", "Normal")
            settings.endGroup()

        elif self.str_id == "Data_Z":
            settings.beginGroup(self.bpm)
            settings.beginGroup(self.str_id)
            self.window = settings.value("window", "Hann")
            self.method = settings.value("method", "Peak")
            self.lboard = settings.value("lboard", 0.10, type=float)
            self.rboard = settings.value("rboard", 0.30, type=float)
            self.scale = settings.value("scale", "Normal")
            settings.endGroup()

        else:
            print("Have no SETTINGS!!!!!")

        self.checkWindowBox.setCurrentText(self.window)
        self.window_changed_str.emit(self.window)

        if self.scale == "Normal":
            self.log_mod.setCheckState(Qt.Unchecked)
        elif self.scale == "Log_Y":
            self.log_mod.setCheckState(Qt.Checked)
        self.scale_changed_obj.emit(self)

        self.lboardSBox.setValue(self.lboard)
        self.rboardSBox.setValue(self.rboard)

        if self.method == "Peak":
            self.usePeakBtn.setChecked(True)
        elif self.method == "Gassior":
            self.useGassiorBtn.setChecked(True)
        elif self.method == "Naff":
            self.useNaffBtn.setChecked(True)
        self.method_changed_str.emit(self.method)
