from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QFileDialog, 
    QWidget,
)
from PySide6.QtCore import Slot, Signal, Qt
from constants import *

from .LabelledSlider import LabelledSlider

class UserInterfaceWidget(QWidget):
    
    load_file_signal = Signal(str)
    threshold_signal = Signal(int)
    slice_signal = Signal()
    picture_size_signal = Signal(int, int)

    def __init__(self):
        super().__init__()


        self.layout = QVBoxLayout(self)
        self.load_button = QPushButton("Load")
        self.slice_button = QPushButton("Slice")
        
        self.threshold_slider = LabelledSlider(
            orientation = Qt.Horizontal,
            minimum = MINIMUM_THRESHOLD,
            maximum = MAXIMUM_THRESHOLD,
            label_text = f"Threshold: {DEFAULT_MONO_THRESHOLD}",
            label_position = "top"
        )
        self.threshold_slider.setValue(DEFAULT_MONO_THRESHOLD)
        
        
        self.picture_width_slider = LabelledSlider(
            orientation=Qt.Horizontal,
            minimum = 1,
            maximum = A4_WIDTH,
            label_text = f"Picture width: {DEFAULT_PICTURE_WIDTH}",
            label_position = "top"
        )
        self.picture_width_slider.setValue(DEFAULT_PICTURE_WIDTH)
        
        self.picture_height_slider = LabelledSlider(
            orientation=Qt.Horizontal,
            minimum = 1,
            maximum = A4_HEIGHT,
            label_text = f"Picture height: {DEFAULT_PICTURE_HEIGHT}",
            label_position = "top"
        )
        self.picture_height_slider.setValue(DEFAULT_PICTURE_HEIGHT)
        

        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.threshold_slider.widget())
        self.layout.addWidget(self.picture_width_slider.widget())
        self.layout.addWidget(self.picture_height_slider.widget())
        self.layout.addWidget(self.slice_button)
        

        self.load_button.clicked.connect(self.load_file)
        self.threshold_slider.valueChanged.connect(self.threshold_changed)
        self.picture_width_slider.valueChanged.connect(self.picture_size_changed)
        self.picture_height_slider.valueChanged.connect(self.picture_size_changed)
        self.slice_button.clicked.connect(self.slice_signal.emit)

    @Slot()
    def load_file(self):
        path = QFileDialog.getOpenFileName()

        self.load_file_signal.emit(path[0])
        
    @Slot()
    def threshold_changed(self):
        self.threshold_signal.emit(self.threshold_slider.value())
        self.threshold_slider.label.setText(f"Threshold: {self.threshold_slider.value()}")
        
    @Slot()
    def picture_size_changed(self):
        self.picture_size_signal.emit(self.picture_width_slider.value(), self.picture_height_slider.value())
        self.picture_width_slider.label.setText(f"Picture width: {self.picture_width_slider.value()}")
        self.picture_height_slider.label.setText(f"Picture height: {self.picture_height_slider.value()}")
