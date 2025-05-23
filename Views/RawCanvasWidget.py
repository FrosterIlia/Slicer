from PySide6.QtCore import Slot, Qt, QSize, QPoint
from PySide6.QtGui import QMouseEvent, QWheelEvent

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
        self.image_size = self.size()
        
        self.dragging = False
        self.offset = QPoint(0, 0)
        self.setCursor(Qt.OpenHandCursor)
        
        self.scale_factor = 1
        
        
    # Drag'n drop
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos() - self.image_pos
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            self.image_pos = event.pos() - self.offset
        self.update()
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)
        
    def wheelEvent(self, event):
        print(self.scale_factor)
        self.scale_factor += event.pixelDelta().y() / 1000
        self.pixmap = QPixmap.fromImage(self.image.scaled(
                    self.image_size * self.scale_factor, 
                    Qt.AspectRatioMode.KeepAspectRatio,
                ))
        self.update()
        super().wheelEvent(event)


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
                    self.size() * self.scale_factor, 
                    Qt.AspectRatioMode.KeepAspectRatio,
                ))
        self.update()

        
    def get_current_pixmap(self):
        pixmap = self.grab()
        return pixmap