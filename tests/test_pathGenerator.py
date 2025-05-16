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
    