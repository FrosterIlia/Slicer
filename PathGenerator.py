from PySide6.QtGui import (
    QImage,
    QColor
)

from settings import *

class PathGenerator:
    def __init__(self):
        self.image = QImage()
    
    def add_image(self, image: QImage):
        self.image = self.convert_mono_threshold(image, DEFAULT_MONO_THRESHOLD)
        binary_array = self.convert_to_binary_array(self.image)
        
        test_graph = self.build_graph(self.image, binary_array)        
        
    def convert_mono_threshold(self, image, threshold):
        image = image.convertToFormat(QImage.Format.Format_Grayscale8)
        
        mono_image = QImage(image.size(), QImage.Format.Format_Mono)
        mono_image.fill(0)

        for x in range(image.width()):
            for y in range(image.height()):
                pixel = QColor(image.pixel(x, y)).red()
                mono_image.setPixel(x, y, 0 if pixel < threshold else 1)
        return mono_image
    
    def convert_to_binary_array(self, image: QImage):
        binary_array = []
        for y in range(image.height()):
            binary_array.append([])
            for x in range(image.width()):
                pixel = bool(image.pixel(x, y) & 0xff)
                binary_array[y].append(pixel)
                
        return binary_array
                
    
    def build_graph(self, image : QImage, binary_array):
        height, width = image.width(), image.height()
        graph = {} 
        
        directions = DIRECTIONS
        
        for y in range(height):
            for x in range(width):
                if binary_array[y][x] == 0:  # Black pixel
                    node = (y, x)
                    if node not in graph:  # Initialize key if missing
                        graph[node] = []
                    for dy, dx in directions:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            if binary_array[ny][nx] == 0:
                                neighbor = (ny, nx)
                                graph[node].append(neighbor)
        return graph