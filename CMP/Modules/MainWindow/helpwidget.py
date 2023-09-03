import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QSize, QCoreApplication
from PyQt5.QtGui import QPixmap, QIcon
import os.path


class HelpWidget(QWidget):
    """   """
    def __init__(self, file_name, parent=None):
        super().__init__(parent)
        self.label = QLabel(self)

        icon_path = os.path.dirname(os.path.abspath(__file__))
        help_icon = QIcon()
        help_icon.addFile(os.path.join(icon_path, 'etc/icons/app_icon_color.png'), QSize(32, 32))
        self.setWindowIcon(help_icon)
        self.setWindowTitle('Help')

        pixmap = QPixmap(file_name)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        #self.show()
