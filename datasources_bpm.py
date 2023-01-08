#
#
from PyQt5.QtCore import pyqtSignal, QObject
import numpy as np
import pycx4.qcda as cda
from BPM_template import BPMTemplate


class BPMData(BPMTemplate):
    """   """

    bpm_channel_template = "v2cx::hemera:2."
    #bpm_channel_template = "v2cx::hemera:4."

    def __init__(self, bpm_name='', parent=None):
        super(BPMData, self).__init__(bpm_name, parent)

        if bpm_name == "bpm01":
            bpm_channel = 4
        elif bpm_name == "bpm02":
            bpm_channel = 5
        elif bpm_name == "bpm03":
            bpm_channel = 6
        elif bpm_name == "bpm04":
            bpm_channel = 7
        else:
            bpm_channel = -1

        #self.bpm_name = bpm_name

        bpm_data_name = '{0}{1}{2}'.format(self.bpm_channel_template, bpm_channel, "@s")
        bpm_numpts_name = '{0}{1}{2}'.format(self.bpm_channel_template, bpm_channel, "@p10")
        bpm_istart_name = '{0}{1}{2}'.format(self.bpm_channel_template, bpm_channel, "@p2") #1 - run mode, 0 - kick mode

        print(bpm_data_name)
        print(bpm_numpts_name)

        self.bpmChan = cda.VChan(bpm_data_name, max_nelems=8 * 1024 * 4, dtype=cda.DTYPE_INT32)
        self.bpmChan_numpts = cda.IChan(bpm_numpts_name)
        self.bpmChan_istart = cda.IChan(bpm_istart_name)

        self.bpmChan_numpts.valueMeasured.connect(self._on_numpts_update)
        self.bpmChan_istart.valueMeasured.connect(self._on_istart_update)
        self.bpmChan.valueMeasured.connect(self._on_signal_update)

    def _on_signal_update(self, chan):
        """   """
        self.data = np.frombuffer(chan.val.data, dtype=np.dtype('f4'), count=chan.val.size)

    def _on_numpts_update(self, chan):
        """   """
        self.num_pts = chan.val
        self.data_len = self.num_pts

        tmp = np.reshape(self.data, (4, self.num_pts))

        self.dataT = tmp[0]
        self.dataX = tmp[1]
        self.dataZ = tmp[2]
        self.dataI = tmp[3]

        self.data_ready.emit(self)

    def _on_istart_update(self, chan):
        """   """
        self.istart = chan.val
        #print(self.bpm_name, ":", self.istart)


