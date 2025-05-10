from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, Slot, Signal

from PySide6.QtGui import (
    QMouseEvent,
    QPaintEvent,
    QPen,
    QAction,
    QPainter,
    QColor, 
    QPixmap,
    QIcon,
    QKeySequence,
)

class UserInterfaceWidget(QtWidgets.QWidget):
    
    load_file_signal = Signal(str)

    def __init__(self):
        super().__init__()


        self.layout = QtWidgets.QVBoxLayout(self)
        self.load_button = QtWidgets.QPushButton("Load")

        self.layout.addWidget(self.load_button)

        self.load_button.clicked.connect(self.load_file)

    @Slot()
    def load_file(self):
        path = QtWidgets.QFileDialog.getOpenFileName()

        print(path[0])

        self.load_file_signal.emit(path[0])