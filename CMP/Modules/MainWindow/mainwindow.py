# This Python file uses the following encoding: utf-8

import os.path
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel
from PyQt5.QtCore import pyqtSignal, QRectF, Qt, QSettings, QSize, QPoint
from PyQt5 import uic
import pyqtgraph as pg
from CMP.Modules.MainWindow.helpwidget import HelpWidget


class MainWindow(QMainWindow):
    """   """
    region_changed = pyqtSignal(object)

    def __init__(self, data_source, data_proc_X, data_proc_Z, settings_control, bpm_name, parent=None):
        super().__init__(parent)

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'MainWindow.ui'), self)

        self.window_str = "None"
        self.bpm = bpm_name

        self.images_list = []
        self.x_rect = None
        self.fx_rect = None
        self.z_rect = None
        self.fz_rect = None

        self.data_source = data_source
        self.data_proc_X = data_proc_X
        self.data_proc_Z = data_proc_Z
        self.settingsControl = settings_control

        self.data_proc_X.data_processed.connect(self.on_data_FX_ready)
        self.data_proc_Z.data_processed.connect(self.on_data_FZ_ready)

        self.controlWidgetX.window_changed_str.connect(self.data_proc_X.on_wind_changed)
        self.controlWidgetX.groupBox.setTitle("X Controller")
        self.controlWidgetX.set_str_id("Data_X")
        self.controlWidgetX.scale_changed_obj.connect(self.on_scale_changing)

        self.controlWidgetZ.window_changed_str.connect(self.data_proc_Z.on_wind_changed)
        self.controlWidgetZ.groupBox.setTitle("Z Controller")
        self.controlWidgetZ.set_str_id("Data_Z")
        self.controlWidgetZ.scale_changed_obj.connect(self.on_scale_changing)

        self.controlWidgetX.method_changed_str.connect(self.data_proc_X.on_method_changed)
        self.controlWidgetX.boards_changed.connect(self.data_proc_X.on_boards_changed)

        self.controlWidgetZ.method_changed_str.connect(self.data_proc_Z.on_method_changed)
        self.controlWidgetZ.boards_changed.connect(self.data_proc_Z.on_boards_changed)

        self.actionSave.triggered.connect(self.on_save_button)
        self.actionRead.triggered.connect(self.on_read_button)

        self.actionExit.triggered.connect(self.on_exit_button)
        self.actionExit.triggered.connect(QApplication.instance().quit)

        self.help_widget = HelpWidget(os.path.join(ui_path, 'etc/icons/Help_1.png'))
        self.actionHelp.triggered.connect(self.help_widget.show)

        self.controlWidgetX.boards_changed.connect(self.boards_X_changed)
        self.controlWidgetZ.boards_changed.connect(self.boards_Z_changed)

        self.ui.nu_x_label.setText('\u03BD<sub>x</sub> = ')
        self.ui.nu_z_label.setText('\u03BD<sub>z</sub> = ')
        self.ui.delta_I_label.setText('\u0394I = ')

        self.plots_customization()

        self.data_curve11 = self.ui.tabWidget.widget(0).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotSignal_X').plot(pen='r', title='X_plot')
        self.data_curve12 = self.ui.tabWidget.widget(1).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotSignal_Z').plot(pen='b', title='Z_plot')
        self.data_curve2 = self.ui.tabWidget.widget(0).findChild(pg.widgets.PlotWidget.PlotWidget, 'plot_FX').plot(pen='r', title='Fourier Transform X_plot')
        self.data_curve3 = self.ui.tabWidget.widget(1).findChild(pg.widgets.PlotWidget.PlotWidget, 'plot_FZ').plot(pen='b', title='Fourier Transform Z_plot')
        self.data_curve4 = self.ui.plotI.plot(pen='k', title='Current_plot')
        self.data_curve51 = self.ui.tabWidget.widget(0).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotPhase_X').scatterPlot(pen='k', title='X_phase', symbol='o', size=3, brush='r')
        self.data_curve52 = self.ui.tabWidget.widget(1).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotPhase_Z').scatterPlot(pen='k', title='Z_phase', symbol='o', size=3, brush='b')


    @staticmethod
    def customise_label(plot, text_item, html_str):
        """   """
        plot_vb = plot.getViewBox()
        text_item.setHtml(html_str)
        text_item.setParentItem(plot_vb)

    def plots_customization(self):
        """   """
        label_str_x = "<span style=\"color:red; font-size:16px\">{}</span>"
        label_str_z = "<span style=\"color:blue;font-size:16px\">{}</span>"
        label_str_i = "<span style=\"color:black;font-size:16px\">{}</span>"

        print(self.ui.tabWidget.widget(0).children())
        plot = self.ui.tabWidget.widget(0).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotSignal_X')
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_x.format("X"))

        plot = self.ui.tabWidget.widget(1).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotSignal_Z')
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_z.format("Z"))

        plot = self.ui.plotI
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_i.format("I"))

        plot = self.ui.tabWidget.widget(0).findChild(pg.widgets.PlotWidget.PlotWidget, 'plot_FX')
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_x.format("Ax"))

        self.FX = pg.LinearRegionItem([self.controlWidgetX.lboard, self.controlWidgetX.rboard])
        self.FX.setBounds([0,0.5])
        plot.addItem(self.FX)
        self.FX.sigRegionChangeFinished.connect(self.region_X_changed)

        plot = self.ui.tabWidget.widget(1).findChild(pg.widgets.PlotWidget.PlotWidget, 'plot_FZ')
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_z.format("Az"))

        self.FZ = pg.LinearRegionItem([self.controlWidgetX.lboard, self.controlWidgetZ.rboard])
        self.FZ.setBounds([0,0.5])
        plot.addItem(self.FZ)
        self.FZ.sigRegionChangeFinished.connect(self.region_Z_changed)

        plot = self.ui.tabWidget.widget(0).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotPhase_X')
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_x.format("Phase_X"))
        self.plotPhase_X.setAspectLocked(True)

        plot = self.ui.tabWidget.widget(1).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotPhase_Z')
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_z.format("Phase_Z"))
        self.plotPhase_Z.setAspectLocked(True)

    @staticmethod
    def customize_plot(plot):
        """   """
        plot.setBackground('w')
        plot.showAxis('top')
        plot.showAxis('right')
        plot.getAxis('top').setStyle(showValues=False)
        plot.getAxis('right').setStyle(showValues=False)
        plot.showGrid(x=True, y=True)

    def on_scale_changing(self, control_widget):
        """   """
        scale = control_widget.scale
        if control_widget.str_id == "Data_X":
            self.plot_mode(self.ui.tabWidget.widget(0).findChild(pg.widgets.PlotWidget.PlotWidget, 'plot_FX'), scale)
        elif control_widget.str_id == "Data_Z":
            self.plot_mode(self.ui.tabWidget.widget(1).findChild(pg.widgets.PlotWidget.PlotWidget, 'plot_FZ'), scale)
        else:
            print("Error in control_widget!")

    @staticmethod
    def plot_mode(plot, scale):
        """   """
        if scale == "Normal":
            plot.setLogMode(False, False)
        if scale == 'Log_Y':
            plot.setLogMode(False, True)

    def boards_X_changed(self, dict):
        """   """
        self.FX.setRegion([dict.get("lboard", 0.1), dict.get("rboard", 0.5)])

    def boards_Z_changed(self, dict):
        """   """
        self.FZ.setRegion([dict.get("lboard", 0.1), dict.get("rboard", 0.5)])

    def region_X_changed(self):
        """   """
        self.controlWidgetX.on_boards_changed_ext(self.FX.getRegion())

    def region_Z_changed(self):
        """   """
        self.controlWidgetZ.on_boards_changed_ext(self.FZ.getRegion())

    def on_exit_button(self):
        """   """
        print(self, ' Exiting... Bye...')

    def on_read_button(self):
        """   """
        self.settingsControl.read_settings()

    def on_save_button(self):
        """   """
        self.settingsControl.save_settings()

    def on_data_ready(self, data_source):
        """   """
        self.data_curve11.setData(data_source.dataT, data_source.dataX)
        self.data_curve12.setData(data_source.dataT, data_source.dataZ)
        self.signal_x_rect = self.ui.tabWidget.widget(0).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotSignal_X').viewRange()
        self.signal_z_rect = self.ui.tabWidget.widget(1).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotSignal_Z').viewRange()

    def on_current_ready(self, data_source):
        """   """
        self.data_curve4.setData(data_source.dataT, data_source.dataI)
        self.current_rect = self.ui.plotI.viewRange()

    def on_data_FX_ready(self, data_processor):
        """   """
        self.data_curve2.setData(data_processor.fftwT, data_processor.fftw_to_process)
        self.fx_rect = self.ui.tabWidget.widget(0).findChild(pg.widgets.PlotWidget.PlotWidget, 'plot_FX').viewRange()

    def on_data_FZ_ready(self, data_processor):
        """   """
        self.data_curve3.setData(data_processor.fftwT, data_processor.fftw_to_process)
        self.fz_rect = self.ui.tabWidget.widget(1).findChild(pg.widgets.PlotWidget.PlotWidget, 'plot_FZ').viewRange()

    def on_freq_status_X(self, data_processor):
        """   """
        if data_processor.warning == 0:
            self.ui.tabWidget.widget(0).findChild(QLabel, 'frq_x').setText('{:.5f}'.format(data_processor.frq_founded))
        elif data_processor.warning == 1:
            self.ui.tabWidget.widget(0).findChild(QLabel, 'frq_x').setText(data_processor.warningText)
        else:
            self.ui.tabWidget.widget(0).findChild(QLabel, 'frq_x').setText('Unexpected value!')

    def on_freq_status_Z(self, data_processor):
        """   """
        if data_processor.warning == 0:
            self.ui.tabWidget.widget(1).findChild(QLabel, 'frq_z').setText('{:.5f}'.format(data_processor.frq_founded))
        elif data_processor.warning == 1:
            self.ui.tabWidget.widget(1).findChild(QLabel, 'frq_z').setText(data_processor.warningText)
        else:
            self.ui.tabWidget.widget(1).findChild(QLabel, 'frq_z').setText('Unexpected value!')

    def on_phase_status(self, data_processor):
        """   """
        self.data_curve51.setData(data_processor.dataX[0:len(data_processor.momentum)], data_processor.momentum)
        self.data_curve52.setData(data_processor.dataZ[0:len(data_processor.momentum)], data_processor.momentum)
        self.phase_x_rect = self.ui.tabWidget.widget(0).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotPhase_X').viewRange()
        self.phase_z_rect = self.ui.tabWidget.widget(1).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotPhase_Z').viewRange()


    def on_current_status(self, data_processor):
        """   """
        if data_processor.warning == 0:
            self.ui.delta_I.setText('{:.5f}'.format(data_processor.delta_I))
            self.ui.time_I.setText('{:.5f}'.format(data_processor.t_zero))
        elif data_processor.warning == 1:
            self.ui.delta_I.setText(data_processor.warningText)
            self.ui.time_I.setText(data_processor.warningText)
        else:
            self.ui.delta_I.setText('Unexpected value!')
            self.ui.time_I.setText('Unexpected value!')


    def save_settings(self):
        """   """
        settings = QSettings()
        settings.beginGroup(self.bpm)
        settings.beginGroup("Plots")
        settings.setValue("signal_x_zoom", self.signal_x_rect)
        settings.setValue("signal_z_zoom", self.signal_z_rect)
        settings.setValue("current_zoom", self.current_rect)
        settings.setValue("fx_zoom", self.fx_rect)
        settings.setValue("fz_zoom", self.fz_rect)
        settings.setValue("phase_x_zoom", self.phase_x_rect)
        settings.setValue("phase_z_zoom", self.phase_z_rect)
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())
        settings.endGroup()
        settings.endGroup()
        settings.sync()

    def read_settings(self):
        """   """
        rect_def = [[0, 1], [0, 1]]
        rect_def_phase = [[-1, 1], [-1, 1]]
        settings = QSettings()
        settings.beginGroup(self.bpm)
        settings.beginGroup("Plots")
        self.signal_x_rect = settings.value("signal_x_zoom", rect_def)
        self.signal_z_rect = settings.value("signal_z_zoom", rect_def)
        self.current_rect = settings.value("current_zoom", rect_def)
        self.fx_rect = settings.value("fx_zoom", rect_def)
        self.fz_rect = settings.value("fz_zoom", rect_def)
        self.phase_x_rect = settings.value("phase_x_zoom", rect_def_phase)
        self.phase_z_rect = settings.value("phase_z_zoom", rect_def_phase)
        self.resize(settings.value('size', QSize(500, 500)))
        self.move(settings.value('pos', QPoint(60, 60)))
        settings.endGroup()
        settings.endGroup()

        self.ui.tabWidget.widget(0).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotSignal_X').setRange(xRange=self.signal_x_rect[0], yRange=self.signal_x_rect[1])
        self.ui.tabWidget.widget(1).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotSignal_Z').setRange(xRange=self.signal_z_rect[0], yRange=self.signal_z_rect[1])
        self.ui.tabWidget.widget(0).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotPhase_X').setRange(xRange=self.phase_x_rect[0], yRange=self.phase_x_rect[1])
        self.ui.tabWidget.widget(1).findChild(pg.widgets.PlotWidget.PlotWidget, 'plotPhase_Z').setRange(xRange=self.phase_z_rect[0], yRange=self.phase_z_rect[1])
        self.ui.tabWidget.widget(0).findChild(pg.widgets.PlotWidget.PlotWidget, 'plot_FX').setRange(xRange=self.fx_rect[0], yRange=self.fx_rect[1])
        self.ui.tabWidget.widget(1).findChild(pg.widgets.PlotWidget.PlotWidget, 'plot_FZ').setRange(xRange=self.fz_rect[0], yRange=self.fz_rect[1])

