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
    export_signal = Signal()

    def __init__(self):
        super().__init__()


        self.layout = QVBoxLayout(self)
        self.load_button = QPushButton("Load")
        self.slice_button = QPushButton("Slice")
        self.export_button = QPushButton("Export")
        
        self.threshold_slider = LabelledSlider(
            orientation = Qt.Horizontal,
            minimum = MINIMUM_THRESHOLD,
            maximum = MAXIMUM_THRESHOLD,
            label_text = f"Threshold: {DEFAULT_MONO_THRESHOLD}",
            label_position = "top"
        )
        self.threshold_slider.setValue(DEFAULT_MONO_THRESHOLD)
        
        

        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.threshold_slider.widget())
        self.layout.addWidget(self.slice_button)
        self.layout.addWidget(self.export_button)
        

        self.load_button.clicked.connect(self.load_file)
        self.threshold_slider.valueChanged.connect(self.threshold_changed)
        self.slice_button.clicked.connect(self.slice_signal.emit)
        self.export_button.clicked.connect(self.export_signal.emit)

    @Slot()
    def load_file(self):
        path = QFileDialog.getOpenFileName()

        self.load_file_signal.emit(path[0])
        
    @Slot()
    def threshold_changed(self):
        self.threshold_signal.emit(self.threshold_slider.value())
        self.threshold_slider.label.setText(f"Threshold: {self.threshold_slider.value()}")

