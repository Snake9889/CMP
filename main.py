# This Python file uses the following encoding: utf-8

from PyQt5.QtCore import QCoreApplication, QSettings, QSize
from PyQt5.QtGui import QIcon
import signal
from mainwindow import *
from dataprocessor import DataProcessor
from settingscontrol import SettingsControl
from command_parser import TerminalParser

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

# Allow CTRL+C and/or SIGTERM to kill us (PyQt blocks it otherwise)
signal.signal(signal.SIGINT, signal.SIG_DFL)
signal.signal(signal.SIGTERM, signal.SIG_DFL)

if __name__ == "__main__":
    """   """
    import sys

    QCoreApplication.setOrganizationName("Denisov")
    QCoreApplication.setApplicationName("CMP")
    QSettings.setDefaultFormat(QSettings.IniFormat)

    app = QApplication(sys.argv)
    app.setStyle('Cleanlooks')

    argument_parser = TerminalParser()
    bpm_name_parsed = argument_parser.bpm_name_parsed
    
    data_source = None

    if bpm_name_parsed == "model":
        from datasources import BPMData
        data_source = BPMData()

    elif bpm_name_parsed == "all":
        from datasources_all import BPMDataAll
        data_source = BPMDataAll()

    else:
        from datasources_bpm import BPMData
        data_source = BPMData(bpm_name=bpm_name_parsed)

    if data_source is None:
        print("Data source doesn't exists!!! You can't use this program!!!")
        exit()

    data_proc_X = DataProcessor("X")
    data_proc_Z = DataProcessor("Z")
    settingsControl = SettingsControl()

    mw = MainWindow(data_source, data_proc_X, data_proc_Z, settingsControl, bpm_name_parsed)
    mw.setWindowTitle('CMP ({})'.format('all'))

    icon_path = os.path.dirname(os.path.abspath(__file__))
    mw_icon = QIcon()
    mw_icon.addFile(os.path.join(icon_path, 'etc/icons/app_icon.png'), QSize(32, 32))
    mw.setWindowIcon(mw_icon)

    data_source.data_ready.connect(mw.on_data_ready)
    data_source.data_ready.connect(mw.on_current_ready)
    data_source.data_ready.connect(data_proc_X.on_data_recv)
    data_source.data_ready.connect(data_proc_Z.on_data_recv)

    data_proc_X.data_processed.connect(mw.on_freq_status_X)
    data_proc_Z.data_processed.connect(mw.on_freq_status_Z)

    settingsControl.add_object(mw)
    settingsControl.add_object(mw.controlWidgetX)
    settingsControl.add_object(mw.controlWidgetZ)
    settingsControl.add_object(data_source)
    settingsControl.read_settings()

    data_proc_X.data_processed.connect(mw.on_freq_status_X)
    data_proc_Z.data_processed.connect(mw.on_freq_status_Z)
    data_proc_X.data_processed.connect(mw.on_phase_status)
    data_proc_Z.data_processed.connect(mw.on_phase_status)
    data_proc_X.data_processed.connect(mw.on_current_status)

    mw.controlWidgetX.signature.connect(data_source.force_data_ready)
    mw.controlWidgetZ.signature.connect(data_source.force_data_ready)

    mw.show()
    sys.exit(app.exec_())
