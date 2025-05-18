from PySide6.QtCore import Qt

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
