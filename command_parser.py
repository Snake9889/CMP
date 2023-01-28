# This Python file uses the following encoding: utf-8

from PyQt5.QtCore import Qt, QObject
import argparse

class TerminalParser(QObject):
    """   """
    def __init__(self, parent=None):
        super(TerminalParser, self).__init__(parent)

        self.parser = argparse.ArgumentParser(description='Startup settings for software')

        self.parser.add_argument('-bn', action='store', default='bpm04', dest='bpm_name',
                                  help='name of bpm, like bpm01 / bpm02 / bpm03 / bpm04 / model, '
                                         'where model - simulated signal, and bpm01 - data from first bpm.')
        self.parser.add_argument('-mt', action='store', default='peak', dest='method_name',
                                  help='naff / peak / gass - NAFF / Peak / Gassior detection method.')

        self.results = self.parser.parse_args()
        self.bpm_name_parsed = self.results.bpm_name
        self.method_name_parsed = self.results.method_name
