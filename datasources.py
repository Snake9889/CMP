
from PyQt5.QtCore import pyqtSignal, QObject, QTimer, QSettings
import numpy as np
import random
from BPM_template import BPMTemplate


class BPMData(BPMTemplate):
    """   """

    def __init__(self, bpm_name='', parent=None):
        super().__init__('model', parent)

        self.data_len = 8000

        self.mu, self.sigma = 0, 1
        self.a0 = 1
        self.a1 = 0.8
        self.a2 = 0.5
        self.w0 = 0.181
        self.w1 = 0.176
        self.w2 = 0.02
        self.k = 0.0000005

        self.phase = 0.00101
        self.n_amp = 0.1
        self.bn_amp = 0.25

        self.dataX = None
        self.dataZ = None
        self.dataI = None

        self.dataT = np.arange(0, self.data_len, dtype=float)

        self.def_time = 5*10**3
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_update)
        self.timer.start(self.def_time)
        self.particles = "e+"
        self.bpm = bpm_name


    def on_timer_update(self):
        """   """

        self.dataX, self.dataZ, self.dataI = self.generate_bpm_data(self.phase, self.dataT, self.n_amp, self.bn_amp)
        self.data_ready.emit(self)

    def generate_bpm_data(self, phase, dataT, namp, bnamp):
        """   """

        dataX = np.exp(-1*self.k*dataT**2)*\
                (self.harmonic_oscillations(phase, dataT, self.a0, self.w0, namp) + \
                self.harmonic_oscillations(phase, dataT, self.a1, self.w1, namp) + \
                self.harmonic_oscillations(phase, dataT, self.a2, self.w2, namp)) + \
                [x for x in bnamp*(np.random.normal(self.mu, self.sigma, self.data_len))]

        dataZ = np.exp(-0.5*self.k*dataT**2)*\
                (self.harmonic_oscillations(phase, dataT, self.a0, self.w0, namp) + \
                1.5*self.harmonic_oscillations(phase, dataT, self.a1, self.w1, namp) + \
                3* self.harmonic_oscillations(phase, dataT, self.a2, self.w2, namp)) + \
                [x for x in bnamp*(np.random.normal(self.mu, self.sigma, self.data_len))]

        dataI = self.current_generator(self.data_len)

        return(dataX, dataZ, dataI)

    def harmonic_oscillations(self, phase, dataT, amp1, freq, amp2):
        """   """
        osc = (amp1 + amp2*(np.random.normal(self.mu, self.sigma, self.data_len)))*np.sin(2 * np.pi * freq * dataT + 2 * np.pi * phase)

        return(osc)

    def current_generator(self, num):
        """   """
        I = np.zeros(num)
        point = random.randint(0, num)
        for i in range(num):
            if i < point:
                I[i] = 0.5 - 0.1*random.random()
            else:
                I[i] = 5 + 0.5 - 0.1*random.random()
        return(I)

    def force_data_ready(self, signature):
        """   """
        super().force_data_ready(signature)

    def read_settings(self):
        """   """
        settings = QSettings()
        settings.beginGroup(self.bpm)
        self.particles = settings.value("particles", "e-")
        settings.endGroup()

    def save_settings(self):
        """   """
        settings = QSettings()
        settings.beginGroup(self.bpm)
        settings.setValue("particles", self.particles)
        settings.endGroup()
        print("Saved!!!!!")
        settings.sync()
