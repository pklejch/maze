import numpy
from matplotlib import pyplot
import binascii

class solution:
    def __init__(self, shape):
        self.distances = numpy.zeros(shape)
        self.directions = numpy.zeros(shape)
        self.is_reachable = True
    def path(self, row, column):
        path = list()


        #im am in the wall
        if self.distances[row][column] == -1:
            raise Exception


        #load content
        content = self.directions[row][column]


        #im right at finnish, add start and end point
        if content == b'X':
            path.append([row, column])
            path.append([row, column])
            return path


        #follow directions until the end
        while content != b'X':
            path.append([row, column])
            if content == b'>':
                content = self.directions[row][column + 1]
                column+=1
            elif content == b'v':
                content = self.directions[row + 1][column]
                row+=1
            elif content == b'<':
                content = self.directions[row][column - 1]
                column-=1
            elif content == b'^':
                content = self.directions[row - 1][column]
                row-=1

        #add finnish cell
        path.append([row,column])

        return path


class pathSolver:
    def __init__(self,shape):
        self.bestDistance = -2

    def path(self, maze, x, y, distance, first):

        #wall or visited
        if maze[x][y] < 0:
            return

        #finnish
        elif maze[x][y] == 1:
            if distance < self.bestDistance or self.bestDistance == -2:
                self.bestDistance = distance
            return

        #visited
        maze[x][y] = -2


        if first == "R":
            # go right, down, left, up
            if y < maze.shape[1] - 1:
                self.path(maze, x, y + 1, distance + 1, first)
            if x < maze.shape[0] - 1:
                self.path(maze, x + 1, y, distance + 1, first)
            if y > 0:
                self.path(maze, x, y - 1, distance + 1, first)
            if x > 0:
                self.path(maze, x - 1, y, distance + 1, first)
        elif first == "D":
            # go down, left, up, right
            if x < maze.shape[0] - 1:
                self.path(maze, x + 1, y, distance + 1, first)
            if y > 0:
                self.path(maze, x, y - 1, distance + 1, first)
            if x > 0:
                self.path(maze, x - 1, y, distance + 1, first)
            if y < maze.shape[1] - 1:
                    self.path(maze, x, y + 1, distance + 1, first)
        elif first == "L":
            # go  left, up, right, down
            if y > 0:
                self.path(maze, x, y - 1, distance + 1, first)
            if x > 0:
                self.path(maze, x - 1, y, distance + 1, first)
            if y < maze.shape[1] - 1:
                self.path(maze, x, y + 1, distance + 1, first)
            if x < maze.shape[0] - 1:
                self.path(maze, x + 1, y, distance + 1, first)
        elif first == "U":
            if x > 0:
                self.path(maze, x - 1, y, distance + 1, first)
            if y < maze.shape[1] - 1:
                self.path(maze, x, y + 1, distance + 1, first)
            if x < maze.shape[0] - 1:
                self.path(maze, x + 1, y, distance + 1, first)
            if y > 0:
                self.path(maze, x, y - 1, distance + 1, first)


def calculateDistances(array):
    (rows, cols) = array.shape
    matrix = numpy.full((rows, cols), -1)
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            solver = pathSolver(array.shape)
            for mode in ["R","D","L","U"]:
                solver.path(numpy.copy(array),i,j,0,mode)
            #if i have better solution and its open path (or inaccesible part)
            if (matrix[i][j] > solver.bestDistance or matrix[i][j] == -1 ) and (array[i][j] >= 0):
                matrix[i][j] = solver.bestDistance
    return matrix

def calculateDirections(array):
    (rows, cols) = array.shape
    matrix = numpy.full((rows, cols), '#', dtype=('a',1))
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            content = array[i][j]
            contentD = None
            contentU = None
            contentL = None
            contentR = None

            if j < maze.shape[1] - 1:
                contentR=array[i][j+1]
            if i < maze.shape[0] - 1:
                contentD = array[i+1][j]
            if j > 0:
                contentL = array[i][j-1]
            if i > 0:
                contentU = array[i-1][j]

            #wall
            if content == -1:
                matrix[i][j] = '#'
            #finnish
            elif content == 0:
                matrix[i][j] = 'X'
            #innacesible
            elif content == -2:
                matrix[i][j] = ' '
            #<
            elif content-1 == contentL:
                matrix[i][j] = '<'
            #>
            elif content-1 == contentR:
                matrix[i][j] = '>'
            #v
            elif content-1 == contentD:
                matrix[i][j] = 'v'
            #^
            elif content-1 == contentU:
                matrix[i][j] = '^'

    return matrix


def analyze(array):
    sol = solution(array.shape)

    sol.distances = calculateDistances(array)
    sol.directions = calculateDirections(sol.distances)



    #check if reachable
    if -2 in sol.distances:
        sol.is_reachable = False

    #replace inaccesible parts with -1
    sol.distances[sol.distances == -2 ] = -1

    return sol







if __name__ == "__main__":
    from generate import maze
    #maze = maze(15, 10)
    maze=numpy.array([
 [-1 ,-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
 [-1 , 2 , 2 , 2 , 2 , 2 , 2 , 2  ,2 , 2 , 2 , 2 , 2 , 2, -1],
 [-1 , 2 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 , 2 ,-1],
 [-1 , 2 ,-1 , 1 ,-1 , 2 ,-1 , 2 , 2 , 2 , 2 , 2 ,-1 , 2 ,-1],
 [-1 , 2 ,-1 , 2 ,-1 , 2 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 , 2 ,-1],
 [-1 , 2 ,-1 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 ,-1],
 [-1 , 2 ,-1 , 2 ,-1 ,-1 ,-1 , 2 ,-1 ,-1 ,-1 , 2 ,-1  ,2 ,-1],
 [-1 , 2 , 2 , 2 ,-1 , 2 , 2 , 2 ,-1 , 2 ,-1 , 2 ,-1 , 2 ,-1],
 [-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 , 2 ,-1 ,-1 ,-1 , 2 ,-1],
 [-1 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 ,-1],
 [-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1]])
    pyplot.imshow(maze,interpolation='nearest')
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.savefig("maze.png")
    print(maze)
    sol = analyze(maze)

    print(sol.distances)
    (rows, cols) = maze.shape

    for i in range(0, rows):
        print ("".join([item.decode('ascii') for item in sol.directions[i]]))
    print(sol.is_reachable)
    print(sol.path(9,13))