import numpy

class solution:
    def __init__(self, shape):
        distances = numpy.zeros(shape, dtype=numpy.int8)
        directions = numpy.zeros(shape, dtype=numpy.int8)
        is_reachable = False
    def path(self, row, column):
        pass

def analyze(array):
    sol = solution(array.shape)
    return sol







if __name__ == "__main__":
    from generate import maze
    maze = maze(10, 10)
    analyze(maze)
    print(maze)