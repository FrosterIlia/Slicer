import sys
from constants import *

from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QApplication,
    QGridLayout
)

from PySide6.QtGui import (
    QPainter,
    QPen
)

from PySide6.QtCore import Slot, Qt

from Views.RawCanvasWidget import RawCanvasWidget
from Views.ResultCanvasWidget import ResultCanvasWidget
from Views.UserInterfaceWidget import UserInterfaceWidget


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create layout for the central widget
        self.layout = QGridLayout(central_widget)

        self.raw_canvas_widget = RawCanvasWidget()
        self.result_canvas_widget = ResultCanvasWidget()
        self.ui = UserInterfaceWidget()

        self.layout.addWidget(self.ui, 0, 0, 1, 1)
        self.layout.addWidget(self.raw_canvas_widget, 0, 1, 1, 1)
        self.layout.addWidget(self.result_canvas_widget, 0, 2, 1, 1)

        self.connect_signals()

        self.raw_canvas_widget.load_image("Slicer/heart.jpg")

        self.update()

    def connect_signals(self):
        self.ui.load_file_signal.connect(self.raw_canvas_widget.load_image)
        self.ui.load_file_signal.connect(self.result_canvas_widget.load_image)
        self.ui.threshold_signal.connect(
            self.raw_canvas_widget.threshold_changed)
        self.ui.threshold_signal.connect(
            self.result_canvas_widget.threshold_changed)
        self.ui.slice_signal.connect(self.slice)
        self.ui.export_signal.connect(self.result_canvas_widget.export)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)

        pen = QPen(Qt.black, 1, Qt.SolidLine)
        painter.setPen(pen)

        raw_rect = self.raw_canvas_widget.geometry()
        result_rect = self.result_canvas_widget.geometry()

        painter.drawRect(raw_rect)
        painter.drawRect(result_rect)

    @Slot()
    def slice(self):
        raw_pixmap = self.raw_canvas_widget.get_current_pixmap()
        self.result_canvas_widget.slice(raw_pixmap)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()
    sys.exit(app.exec())
