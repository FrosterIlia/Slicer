from PySide6.QtCore import Qt, QTimer, QPoint, Slot

from .CanvasWidget import CanvasWidget

from constants import *
from PathGenerator import PathGenerator
from random import randrange

from PySide6.QtGui import (
    QPainter,
    QPixmap,
    QPen,
    QColor
)

class ResultCanvasWidget(CanvasWidget):
        
    def __init__(self):
        super().__init__()

        # self.load_image("heart.jpg")
        self.path_generator = PathGenerator()
        self.path_generator.add_image(self.image, self.size())
        
        self.path = []
        self.current_index = 0
        self.animation_speed = 1  # milliseconds between steps
        
        self.buffer_pixmap = QPixmap(self.size())
        
        # Timer for animation
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_step)
        

    def start_animation(self):
        """Call this to start the animation"""
        self.current_index = 1
        
        self.buffer_pixmap = QPixmap(self.size())
        self.buffer_pixmap.fill(Qt.transparent)
        
        self.animation_timer.start(self.animation_speed)
        
        
    def animate_step(self):
        """Increment the current drawing index and update"""
        if self.current_index < len(self.path):
            buffer_painter = QPainter(self.buffer_pixmap)
            color = randrange(0, COLOR_RANDOMNESS)
            pen = QPen(QColor(color, color, color, 80))
            buffer_painter.setPen(pen)
            p1 = QPoint(self.path[self.current_index - 1][0], self.path[self.current_index - 1][1])
            p2 = QPoint(self.path[self.current_index][0], self.path[self.current_index][1])
            buffer_painter.drawLine(p1, p2)
            buffer_painter.end()
            
            self.current_index += 1
            if self.current_index > len(self.path):
                self.current_index = len(self.path)
            self.update()  # Trigger paintEvent
        else:
            self.animation_timer.stop()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        color = randrange(0, COLOR_RANDOMNESS)
        pen = QPen(QColor(color, color, color, 80))
        painter.setPen(pen)
        if self.buffer_pixmap:
            painter.drawPixmap(0, 0, self.buffer_pixmap)
        if 0 < self.current_index < len(self.path):
            p1 = QPoint(self.path[self.current_index - 1][0], self.path[self.current_index - 1][1])
            p2 = QPoint(self.path[self.current_index][0], self.path[self.current_index][1])
            painter.drawLine(p1, p2)
        
        super().paintEvent(event)
    
    def update_image(self, image=None):
        super().update_image(image)
        self.path_generator.add_image(self.image, self.size())
        
        self.path = self.path_generator.generate_path()
        
        self.start_animation()
        
    def slice(self, pixmap: QPixmap):
        image = pixmap.toImage()
        self.update_image(image)