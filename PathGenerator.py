from PySide6.QtGui import QImage, QColor
from PySide6.QtCore import Qt, QSize

import math
from collections import deque

from constants import *


class PathGenerator:
    def __init__(self):
        self.image = QImage()
        self.mono_threshold = DEFAULT_MONO_THRESHOLD

    def add_image(self, image: QImage, size: QSize):
        self.image = self.convert_mono_threshold(image)
        self.image = self.image.scaled(
            size, Qt.AspectRatioMode.KeepAspectRatio)

    # Convert colorful image into monochrome
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

    def convert_to_binary_array(
        self, image: QImage
    ):  # Convert monochrome image to binary array
        binary_array = []
        for y in range(image.height()):
            binary_array.append([])
            for x in range(image.width()):
                pixel = bool(image.pixel(x, y) & 0xFF)
                binary_array[y].append(pixel)

        return binary_array

    # Convert monochrome image to a graph (black - nodes)
    def build_graph(self, image: QImage, binary_array):
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

    def build_path(self, graph_image):  # Generate path from the graph
        if not graph_image:
            return []

        visited = set()
        path = []
        stack = deque()

        for node in graph_image:  # Accounting for disconnected regions
            if node not in visited:
                temp_path = []
                stack = [node]
                while stack:
                    x, y = stack.pop()

                    if (x, y) not in visited:
                        visited.add((x, y))
                        temp_path.append((x, y))

                        for neighbour in reversed(graph_image.get((x, y), [])):
                            if neighbour not in visited:
                                stack.append(neighbour)
                path.append(temp_path)
        return path

    def simplify_path(self, path):  # Combine points that are in one line
        simplified_path = []
        for region in path:
            # Move to the first node in the region
            simplified_path.append(region[0])
            simplified_path.append("down")  # Then start drawing
            if len(region) < 2:
                simplified_path.append("up")
                return simplified_path
            current_direction = self.get_direction(region[0], region[1])

            for j in range(1, len(region) - 1):
                if self.get_direction(region[j], region[j + 1]) != current_direction:
                    current_direction = self.get_direction(
                        region[j], region[j + 1])
                    simplified_path.append(region[j])

            simplified_path.append(region[-1])
            # Pen up after the last node in the region
            simplified_path.append("up")
        return simplified_path

    def get_direction(self, point1, point2):
        distance = math.sqrt(
            (point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2
        )
        return [(point2[0] - point1[0]) / distance, (point2[1] - point1[1]) / distance]

    def scale_path(self, path, size0: QSize, size1: QSize):
        new_path = []
        for i in path:
            if i == "up":
                new_path.append(i)
            elif i == "down":
                new_path.append(i)
            else:
                x = int(self.map(i[0], 0, size0.width(), 0, size1.width()))
                y = int(self.map(i[1], 0, size0.height(), 0, size1.height()))
                new_path.append([x, y])

        return new_path

    def map(self, value, min0, max0, min1, max1):  # Linear interpolation
        if max0 - min0 == 0:
            return min1  # Avoid division by zero
        return (value - min0) / (max0 - min0) * (max1 - min1) + min1

    def generate_path(self):
        binary_image = self.convert_to_binary_array(self.image)
        image_graph = self.build_graph(self.image, binary_image)
        raw_path = self.build_path(image_graph)
        simplified_path = self.simplify_path(raw_path)
        return simplified_path

    def generate_file(self, path, file_path: str):
        if not file_path.endswith(".txt"):
            file_path += ".txt"
        file_text = ""
        for i in path:
            if i == "up":
                file_text += f"p 1;\n"
            elif i == "down":
                file_text += f"p 0;\n"
            else:
                file_text += f"m {i[0]}, {i[1]};\n"

        with open(file_path, "w") as file:
            file.write(file_text)
