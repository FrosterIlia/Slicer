from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Slot, Signal

from settings import *

from PySide6.QtGui import (
    QPainter,
    QPixmap,
    QImage,
    QColor

)

class RawCanvasWidget(QtWidgets.QWidget):
    
    image_changed_signal = Signal(QImage)
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.setFixedSize(CANVAS_WIDTH, CANVAS_HEIGHT)

        self.pixmap = QPixmap(self.size())

        self.painter = QPainter()

        self.image = QImage()


    @Slot(str)
    def load_image(self, path):
        self.image.load(path)
        self.image = self.convert_mono_threshold(self.image, DEFAULT_MONO_THRESHOLD)
        self.pixmap = QPixmap.fromImage(self.image.scaled(
                    self.size(), 
                    Qt.AspectRatioMode.KeepAspectRatio,
                ))
        self.image_changed_signal.emit(self.image)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.pixmap = QPixmap.fromImage(self.image.scaled(
                    self.size(), 
                    Qt.AspectRatioMode.KeepAspectRatio,
                ))
        self.update()
        painter.drawPixmap(0, 0, self.pixmap)

    def convert_mono_threshold(self, image, threshold):
        image = image.convertToFormat(QImage.Format.Format_Grayscale8)
        
        mono_image = QImage(image.size(), QImage.Format.Format_Mono)
        mono_image.fill(0)

        for x in range(image.width()):
            for y in range(image.height()):
                pixel = QColor(image.pixel(x, y)).red()
                mono_image.setPixel(x, y, 0 if pixel < threshold else 1)
        return mono_image
    
    
    
    
