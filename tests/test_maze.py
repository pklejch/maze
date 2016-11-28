import pytest
import numpy
from maze import analyze


@pytest.fixture
def maze():
    maze = numpy.array([
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1],
    [-1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1],
    [-1, 2, -1, 1, -1, 2, -1, 2, 2, 2, 2, 2, -1, 2, -1],
    [-1, 2, -1, 2, -1, 2, -1, -1, -1, -1, -1, -1, -1, 2, -1],
    [-1, 2, -1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1],
    [-1, 2, -1, 2, -1, -1, -1, 2, -1, -1, -1, 2, -1, 2, -1],
    [-1, 2, 2, 2, -1, 2, 2, 2, -1, 2, -1, 2, -1, 2, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, 2, -1],
    [-1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]])
    return maze


@pytest.fixture
def maze2():
    maze = numpy.array([
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1],
    [-1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1],
    [-1, 2, -1, 1, -1, 2, -1, -1, -1, -1, -1, -1, -1, 2, -1],
    [-1, 2, -1, 2, -1, 2, -1, -1, -1, -1, -1, -1, -1, 2, -1],
    [-1, 2, -1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1],
    [-1, 2, -1, 2, -1, -1, -1, 2, -1, -1, -1, 2, -1, 2, -1],
    [-1, 2, 2, 2, -1, 2, 2, 2, -1, 2, -1, 2, -1, 2, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, 2, -1],
    [-1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]])
    return maze


def test_attributes(maze):
    sol = analyze(maze)
    assert hasattr(sol,'directions')
    assert hasattr(sol,'distances')
    assert hasattr(sol,'is_reachable')
    assert hasattr(sol,'path')
    assert not hasattr(sol,'nonexistent_attribute')


def test_isreachable(maze):
    sol = analyze(maze)
    assert not sol.is_reachable
    assert b" " in sol.directions


def test_isreachable2(maze2):
    sol = analyze(maze2)
    assert sol.is_reachable
    assert not b" " in sol.directions


def test_walls(maze):
    sol = analyze(maze)
    (rows, cols) = maze.shape
    assert numpy.all(char == b"#" for char in sol.directions[0])
    assert numpy.all(char == b"#" for char in sol.directions[rows-1])
    assert numpy.all(char == b"#" for char in sol.directions[:0])
    assert numpy.all(char == b"#" for char in sol.directions[:cols-1])


def test_pathInWall(maze):
    sol = analyze(maze)
    with pytest.raises(Exception):
        sol.path(0,0)


def test_path(maze):
    sol = analyze(maze)
    path = sol.path(1, 1)
    assert isinstance(path, list)
    assert isinstance(path[0][0], int)
    assert isinstance(path[0][1], int)

def test_distances(maze):
    sol = analyze(maze)
    assert 12 == sol.distances[1][1]

def test_finnish(maze):
    sol = analyze(maze)
    x,y = numpy.where(sol.distances == 0)
    assert sol.directions[x,y] == b"X"