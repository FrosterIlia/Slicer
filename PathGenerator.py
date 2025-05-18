from PySide6.QtGui import (
    QImage,
    QColor
)
from PySide6.QtCore import Qt, Slot

import math

from settings import *

class PathGenerator:
    def __init__(self):
        self.image = QImage()
        self.mono_threshold = DEFAULT_MONO_THRESHOLD
    
    def add_image(self, image: QImage, size):
        self.image = self.convert_mono_threshold(image)
        self.image = self.image.scaled(size, Qt.AspectRatioMode.KeepAspectRatio)
        
        
    def convert_mono_threshold(self, image): # Convert colorful image into monochrome
        image = image.convertToFormat(QImage.Format.Format_Grayscale8)
        
        mono_image = QImage(image.size(), QImage.Format.Format_Mono)
        mono_image.fill(0)

        for x in range(image.width()):
            for y in range(image.height()):
                pixel = QColor(image.pixel(x, y)).red()
                mono_image.setPixel(x, y, 0 if pixel < self.mono_threshold else 1)
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
        height, width = image.height(), image.width()
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
                        if 0 <= ny and ny < height and 0 <= nx and nx < width:
                            if binary_array[ny][nx] == 0:
                                neighbor = (nx, ny)
                                graph[node].append(neighbor)
        return graph
    
    def build_path(self, graph_image): # Generate path from the graph
        if not graph_image:
            return []
        
        visited = set()
        path = []
        stack = []
        
        for node in graph_image: # Accounting for disconnected regions
            if node not in visited:
                stack = [node]
                while stack:
                    x, y = stack.pop()
                    
                    if (x,y) not in visited:
                        visited.add((x, y))
                        path.append((x, y))
                        
                        for neighbour in reversed(graph_image.get((x, y), [])):
                            if neighbour not in visited:
                                stack.append(neighbour)
        return path
    
    def simplify_path(self, path): # Combine points that are in one line
        if len(path) <= 2:
            return path
        
        simplified_path = [path[0]]
        current_direction = self.get_direction(path[0], path[1])
        for i in range(1, len(path) - 1):
            if self.get_direction(path[i], path[i+1]) != current_direction:
                current_direction = self.get_direction(path[i], path[i+1])
                simplified_path.append(path[i])
                
        simplified_path.append(path[-1])
        return simplified_path
        
        
    def get_direction(self, point1, point2):
        distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
        return [(point2[0] - point1[0]) / distance, (point2[1] - point1[1]) / distance]
                
    def generate_path(self):
        binary_image = self.convert_to_binary_array(self.image)
        image_graph = self.build_graph(self.image, binary_image)
        raw_path = self.build_path(image_graph)
        simplified_path = self.simplify_path(raw_path)
    
        return simplified_path
