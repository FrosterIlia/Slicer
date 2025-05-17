from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Slot, QTimer, QPoint

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
        self.current_index = 0
        self.animation_speed = 1  # milliseconds between steps
        
        self.buffer_pixmap = QPixmap(self.size())
        
        # Timer for animation
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_step)
        


    @Slot(str)
    def load_image(self, path):
        self.image.load(path)
        self.image = self.convert_mono_threshold(self.image, 10)
        self.pixmap = QPixmap.fromImage(self.image.scaled(
                    self.size(), 
                    Qt.AspectRatioMode.KeepAspectRatio,
                ))
        self.update()

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
            p1 = QPoint(self.path[self.current_index-1][0], self.path[self.current_index-1][1])
            p2 = QPoint(self.path[self.current_index][0], self.path[self.current_index][1])
            buffer_painter.drawLine(p1, p2)
            buffer_painter.end()
            
            self.current_index += ANIMATION_STEP
            if self.current_index > len(self.path):
                self.current_index = len(self.path)
            self.update()  # Trigger paintEvent
        else:
            self.animation_timer.stop()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        if self.buffer_pixmap:
            painter.drawPixmap(0, 0, self.buffer_pixmap)
        if 0 < self.current_index < len(self.path):
            p1 = QPoint(self.path[self.current_index-1][0], self.path[self.current_index-1][1])
            p2 = QPoint(self.path[self.current_index][0], self.path[self.current_index][1])
            painter.drawLine(p1, p2)
    
    @Slot(QImage)
    def image_changed(self, image: QImage):
        self.path_generator.add_image(image)
        print("IMage changed")
        
        self.path = self.path_generator.generate_path()
        
        self.start_animation()