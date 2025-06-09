from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Slot

from constants import *

from PySide6.QtGui import (
    QPainter,
    QPixmap,
    QImage,
    QColor,
)


class CanvasWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setFixedSize(int(A4_WIDTH * CANVAS_SIZE_SCALER),
                          int(A4_HEIGHT * CANVAS_SIZE_SCALER))

        self.pixmap = QPixmap(self.size())
        self.painter = QPainter()
        self.image = QImage()
        self.original_image = QImage()

        self.mono_threshold = DEFAULT_MONO_THRESHOLD

    def paintEvent(self, event):
        pass

    @Slot(str)
    def load_image(self, path):
        self.original_image.load(path)

    @Slot(QPixmap)
    def load_pixmap(self, pixmap):
        self.pixmap = pixmap

    def convert_mono_threshold(self, image):
        image = image.convertToFormat(QImage.Format.Format_Grayscale8)

        mono_image = QImage(image.size(), QImage.Format.Format_Mono)
        mono_image.fill(0)

        for x in range(image.width()):
            for y in range(image.height()):
                pixel = QColor(image.pixel(x, y)).red()
                mono_image.setPixel(x, y, 0 if pixel <
                                    self.mono_threshold else 1)
        return mono_image

    @Slot(int)
    def threshold_changed(self, new_threshold):
        self.mono_threshold = new_threshold

    def update_image(self, image=None):
        if image is None:
            image = self.original_image
        self.image = self.convert_mono_threshold(image)
        self.pixmap = QPixmap.fromImage(self.image.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
        ))
        self.update()
