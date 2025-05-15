from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Slot

from settings import *

from PySide6.QtGui import (
    QPainter,
    QPixmap,
    QImage,
    QColor
    
)

class RawCanvasWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.setFixedSize(CANVAS_WIDTH, CANVAS_HEIGHT)

        self.pixmap = QPixmap(self.size())

        self.painter = QPainter()

        self.image = QImage()
        self.load_image("iron_sword.jpg")


    @Slot(str)
    def load_image(self, path):
        self.image.load(path)
        self.image = self.convert_mono_threshold(self.image, DEFAULT_MONO_THRESHOLD)
        self.pixmap = QPixmap.fromImage(self.image.scaled(
                    self.size(), 
                    Qt.AspectRatioMode.KeepAspectRatio,
                ))
