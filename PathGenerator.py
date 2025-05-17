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
        
        test_path = self.build_path(test_graph)
        print(test_path) 
         
        
    def convert_mono_threshold(self, image, threshold): # Convert colorful image into monochrome
        image = image.convertToFormat(QImage.Format.Format_Grayscale8)
        
        mono_image = QImage(image.size(), QImage.Format.Format_Mono)
        mono_image.fill(0)

        for x in range(image.width()):
            for y in range(image.height()):
                pixel = QColor(image.pixel(x, y)).red()
                mono_image.setPixel(x, y, 0 if pixel < threshold else 1)
        return mono_image
    
    def convert_to_binary_array(self, image: QImage): # Convert monochrome image to binary array
        binary_array = []
        for y in range(image.height()):
            binary_array.append([])
            for x in range(image.width()):
                pixel = bool(image.pixel(x, y) & 0xff)
                binary_array[y].append(pixel)
                
        return binary_array
                
    
    def build_graph(self, image : QImage, binary_array): # Convert monochrome image to a graph (black - nodes)
        height, width = image.width(), image.height()
        graph = {} 
        
        directions = DIRECTIONS
        
        for y in range(height):
            for x in range(width):
                if binary_array[y][x] == 0: 
                    node = (x, y)
                    if node not in graph:
                        graph[node] = []
                    for dx, dy in directions:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            if binary_array[ny][nx] == 0:
                                neighbor = (nx, ny)
                                graph[node].append(neighbor)
        return graph
    
    def build_path(self, graph_image): # Generate path from the graph
        if not graph_image:
            return []
        
        visited = set()
        path = []
        stack = [next(iter(graph_image))]
        
        while stack:
            x, y = stack.pop()
            
            if (x,y) not in visited:
                visited.add((x, y))
                path.append((x, y))
                
                for neighbour in reversed(graph_image.get((x, y), [])):
                    if neighbour not in visited:
                        stack.append(neighbour)
        return path
                