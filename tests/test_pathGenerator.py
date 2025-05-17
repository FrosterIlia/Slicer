import pytest
from ..settings import *
from ..PathGenerator import *
from PySide6.QtGui import QImage



def test_build_graph():
    path_generator = PathGenerator()
    
    array = [ # 0 - black
        [0, 1, 0],
        [1, 0, 1],
        [0, 0, 1]
    ]
    
    expected_graph = {
        (0, 0) : [(1, 1)],
        (2, 0) : [(1, 1)],
        (1, 1) : [(0, 0), (2, 0), (0, 2), (1, 2)],
        (0, 2) : [(1, 1), (1, 2)],
        (1, 2) : [(0, 2), (1, 1)]
    }
    
    result_graph = path_generator.build_graph(QImage(3, 3, QImage.Format.Format_Mono), array)
    
    assert sorted(result_graph) == sorted(expected_graph) # testing keys in any order
    assert [sorted(i) for i in result_graph.values()] == [sorted(i) for i in expected_graph.values()] # testing values in any order
    
def test_build_path():
    path_generator = PathGenerator()
    
    initial_graph = {
        (0, 0) : [(1, 1)],
        (2, 0) : [(1, 1)],
        (1, 1) : [(0, 0), (2, 0), (0, 2), (1, 2)],
        (0, 2) : [(1, 1), (1, 2)],
        (1, 2) : [(0, 2), (1, 1)]
    }
    
    expected_path = [(0, 0), (1, 1), (2, 0), (0, 2), (1, 2)]
    
    result_path = path_generator.build_path(initial_graph)
    
    assert result_path == expected_path
    
def test_simplify_path():
    path_generator = PathGenerator()
    
    test1 = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]  # Straight diagonal
    test2 = [(0, 0), (1, 0), (2, 0), (3, 1), (4, 2)]  # Horizontal then diagonal
    test3 = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]  # Vertical then horizontal
    test4 = [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)]  # Zig-zag
    
    expected_result_1 = [(0, 0), (4, 4)]
    expected_result_2 = [(0, 0), (2, 0), (4, 2)]
    expected_result_3 = [(0, 0), (0, 2), (2, 2)]
    expected_result_4 = [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)]
    
    result_1 = path_generator.simplify_path(test1)
    result_2 = path_generator.simplify_path(test2)
    result_3 = path_generator.simplify_path(test3)
    result_4 = path_generator.simplify_path(test4)
    
    assert result_1 == expected_result_1
    assert result_2 == expected_result_2
    assert result_3 == expected_result_3
    assert result_4 == expected_result_4
    