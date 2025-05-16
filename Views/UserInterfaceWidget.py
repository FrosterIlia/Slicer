from PySide6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QWidget
from PySide6.QtCore import Slot, Signal

class UserInterfaceWidget(QWidget):
    
    load_file_signal = Signal(str)

    def __init__(self):
        super().__init__()


        self.layout = QVBoxLayout(self)
        self.load_button = QPushButton("Load")

        self.layout.addWidget(self.load_button)

        self.load_button.clicked.connect(self.load_file)

    @Slot()
    def load_file(self):
        path = QFileDialog.getOpenFileName()

        print(path[0])

        self.load_file_signal.emit(path[0])