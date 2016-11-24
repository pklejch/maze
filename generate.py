import numpy
from numpy.random import random_integers as rand
import matplotlib.pyplot as pyplot
import random
def maze(width=3, height=3, complexity=.75, density=.75):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density    = int(density * ((shape[0] // 2) * (shape[1] // 2)))
    # Build actual maze
    Z = numpy.zeros(shape, dtype=numpy.int8)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make aisles
    for i in range(density):
        x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_

    pyplot.figure(figsize=(10, 5))

    X = numpy.copy(Z)


    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            if Z[i][j] == 1:
                Z[i][j] = -1
                X[i][j] = 255
            elif Z[i][j] == 0:
                Z[i][j] = 2
                X[i][j] = 50


    i=0
    j=0
    cell = Z[i][j]
    while cell != 2:
        i = random.randrange(0, shape[0])
        j = random.randrange(0, shape[1])
        cell = Z[i][j]
    #finnish
    print("Finnish is at "+str(i)+" "+str(j))
    Z[i][j]=1
    X[i][j]=200
    pyplot.imshow(X,interpolation='nearest')
    pyplot.xticks([]), pyplot.yticks([])
    #pyplot.savefig("maze.png")
    return Z

