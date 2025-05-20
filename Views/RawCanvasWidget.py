from PySide6.QtCore import Slot

from .CanvasWidget import CanvasWidget

from settings import *

from PySide6.QtGui import (
    QPainter,
    QPixmap,
)

class RawCanvasWidget(CanvasWidget):
    
    
    def __init__(self):
        super().__init__()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)
        
    @Slot(str)
    def load_image(self, path):
        super().load_image(path)
        self.update_image()
        
    @Slot(int)
    def threshold_changed(self, new_threshold):
        super().threshold_changed(new_threshold)
        self.update_image()
