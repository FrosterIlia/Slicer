from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Slot

from settings import *
from PathGenerator import PathGenerator

from PySide6.QtGui import (
    QPainter,
    QPixmap,
    QImage,
    QColor
    
)

class ResultCanvasWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.setFixedSize(CANVAS_WIDTH, CANVAS_HEIGHT)

        self.pixmap = QPixmap(self.size())

        self.painter = QPainter()

        self.image = QImage()
        self.load_image("iron_sword.jpg")
        
        self.path_generator = PathGenerator()
        
        self.path_generator.add_image(self.image)
        


    @Slot(str)
    def load_image(self, path):
        self.image.load(path)
        self.image = self.convert_mono_threshold(self.image, 10)
        self.pixmap = QPixmap.fromImage(self.image.scaled(
                    self.size(), 
                    Qt.AspectRatioMode.KeepAspectRatio,
                ))
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
        
        mono_image = QImage(self.image.size(), QImage.Format.Format_Mono)
        mono_image.fill(0)

        for x in range(image.width()):
            for y in range(image.height()):
                pixel = QColor(image.pixel(x, y)).red()
                mono_image.setPixel(x, y, 0 if pixel < threshold else 1)
        return mono_image
    
    def generate_path(self):
        pass
    
    
