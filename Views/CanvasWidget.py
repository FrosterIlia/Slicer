from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Slot, Signal

from settings import *

from PySide6.QtGui import (
    QPainter,
    QPixmap,
    QImage,
    QColor
)

class CanvasWidget(QWidget):
    
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setFixedSize(CANVAS_WIDTH, CANVAS_HEIGHT)

        self.pixmap = QPixmap(self.size())
        self.painter = QPainter()
        self.image = QImage()
        self.original_image = QImage()
        
        self.mono_threshold = DEFAULT_MONO_THRESHOLD
        
    @Slot(str)
    def load_image(self, path):
        self.original_image.load(path)
        self.update_image()
        
        
    def convert_mono_threshold(self, image):
        image = image.convertToFormat(QImage.Format.Format_Grayscale8)
        
        mono_image = QImage(image.size(), QImage.Format.Format_Mono)
        mono_image.fill(0)

        for x in range(image.width()):
            for y in range(image.height()):
                pixel = QColor(image.pixel(x, y)).red()
                mono_image.setPixel(x, y, 0 if pixel < self.mono_threshold else 1)
        return mono_image
    
    @Slot(int)
    def threshold_changed(self, new_threshold):
        self.mono_threshold = new_threshold
        self.update_image()
        
    def update_image(self):
        self.image = self.convert_mono_threshold(self.original_image)
        self.pixmap = QPixmap.fromImage(self.image.scaled(
                    self.size(), 
                    Qt.AspectRatioMode.KeepAspectRatio,
                ))
        self.update()