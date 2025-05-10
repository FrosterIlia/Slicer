from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, Slot, QStandardPaths

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
    def __init__(self):
        super().__init__()


        self.layout = QtWidgets.QVBoxLayout(self)
        self.loadButton = QtWidgets.QPushButton("Load")


        self.layout.addWidget(self.loadButton)

        self.loadButton.clicked.connect(self.loadFile)

    @Slot()
    def loadFile(self, canvas):
        path = QtWidgets.QFileDialog.getOpenFileName()

        canvas.load_image(path[0])

        print(path)