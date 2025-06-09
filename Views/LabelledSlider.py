from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout,
    QSizePolicy,
    QWidget,
    QSlider,
    QLabel
)

from PySide6.QtCore import Qt
from constants import *

from constants import *


class LabelledSlider(QSlider):
    def __init__(self, label_text="", orientation=Qt.Horizontal, label_position="top", minimum=0, maximum=255, parent=None):
        super().__init__(orientation, parent)

        self.setRange(minimum, maximum)

        # Create container widget
        self.container = QWidget(parent)
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(2, 2, 2, 2)  # Tight margins
        self.layout.setSpacing(3)  # Minimal spacing between label and slider

        # Create label
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # Position elements based on label_position
        if label_position.lower() == "top":
            self.layout.addWidget(self.label)
            self.layout.addWidget(self)
        elif label_position.lower() == "bottom":
            self.layout.addWidget(self)
            self.layout.addWidget(self.label)
        else:
            raise ValueError("label_position must be 'top' or 'bottom'")

        self.container.setFixedSize(
            DEFAULT_LABELLED_SLIDER_WIDTH, DEFAULT_LABELLED_SLIDER_HEIGHT)

        # Maintain direct access to QSlider methods
        self.setOrientation = super().setOrientation
        self.setMinimum = super().setMinimum
        self.setMaximum = super().setMaximum
        self.setRange = super().setRange
        self.setValue = super().setValue
        self.value = super().value

    def widget(self):
        """Returns the container widget for easy layout integration."""
        return self.container

    # Override setOrientation to handle layout changes
    def setOrientation(self, orientation):
        super().setOrientation(orientation)
        if orientation == Qt.Vertical:
            # Switch to horizontal layout for vertical sliders
            self.layout.setDirection(QVBoxLayout.TopToBottom)
        else:
            self.layout.setDirection(QVBoxLayout.TopToBottom)
