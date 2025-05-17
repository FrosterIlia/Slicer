from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Slot, QLine, QPoint

from settings import *
from PathGenerator import PathGenerator

from PySide6.QtGui import (
    QPainter,
    QPixmap,
    QImage,
    
)

class ResultCanvasWidget(QWidget):
        
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.setFixedSize(CANVAS_WIDTH, CANVAS_HEIGHT)

        self.pixmap = QPixmap(self.size())

        self.painter = QPainter()

        self.image = QImage()
        # self.load_image("iron_sword.jpg")
        
        self.path_generator = PathGenerator()
        
        self.path_generator.add_image(self.image)
        
        self.path = []
        


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
        if (self.image != QImage()):
            self.pixmap = QPixmap.fromImage(self.image.scaled(
                        self.size(), 
                        Qt.AspectRatioMode.KeepAspectRatio,
                    ))
        self.update()
        painter.drawPixmap(0, 0, self.pixmap)
        if self.path != []:
            painter.drawLines([QPoint(i[0], i[1]) for i in self.path])
    
    @Slot(QImage)
    def image_changed(self, image: QImage):
        self.path_generator.add_image(image)
        print("IMage changed")
        
        self.path = self.path_generator.generate_path()