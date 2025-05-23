from PySide6.QtCore import Slot, Qt, QSize, QPoint
from PySide6.QtGui import QMouseEvent

from .CanvasWidget import CanvasWidget

from constants import *

from PySide6.QtGui import (
    QPainter,
    QPixmap,
)

class RawCanvasWidget(CanvasWidget):
    
    
    def __init__(self):
        super().__init__()
        
        self.image_pos = QPoint(0, 0)
        self.image_width = self.size().width()
        self.image_height = self.size().height()
        
        self.dragging = False
        self.offset = QPoint(0, 0)
        self.setCursor(Qt.OpenHandCursor)
        
        
    # Drag'n drop
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos() - self.image_pos
            self.setCursor(Qt.ClosedHandCursor)
        # super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            self.image_pos = event.pos() - self.offset
        self.update()
        # super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.OpenHandCursor)
        # super().mouseReleaseEvent(event)


    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.drawPixmap(self.image_pos, self.pixmap)
        
    @Slot(str)
    def load_image(self, path):
        super().load_image(path)
        self.update_image()
        
    @Slot(int)
    def threshold_changed(self, new_threshold):
        super().threshold_changed(new_threshold)
        self.update_image()
        
    def update_image(self):
        self.image = self.convert_mono_threshold(self.original_image)
        self.pixmap = QPixmap.fromImage(self.image.scaled(
                    QSize(self.image_width, self.image_height), 
                    Qt.AspectRatioMode.KeepAspectRatio,
                ))
        self.update()

    @Slot(int, int)
    def change_size(self, width, height):
        self.image_width = width
        self.image_height = height
        self.pixmap = QPixmap.fromImage(self.image.scaled(
                    QSize(self.image_width, self.image_height), 
                    Qt.AspectRatioMode.KeepAspectRatio,
                ))
        self.update()