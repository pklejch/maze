# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, uic, QtGui, QtCore, QtSvg
import numpy
import os
from .solver import analyze
dir = os.path.dirname(__file__)

CELL_SIZE = 32

SVG_GRASS = QtSvg.QSvgRenderer(os.path.join(dir, 'images/grass.svg'))
SVG_WALL = QtSvg.QSvgRenderer(os.path.join(dir, 'images/wall.svg'))
SVG_CASTLE = QtSvg.QSvgRenderer(os.path.join(dir, 'images/castle.svg'))
SVG_DUDE1 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/dude1.svg'))
SVG_DUDE2 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/dude2.svg'))
SVG_DUDE3 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/dude3.svg'))
SVG_DUDE4 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/dude4.svg'))
SVG_DUDE5 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/dude5.svg'))

SVG_UP = QtSvg.QSvgRenderer(os.path.join(dir, 'images/arrows/up.svg'))
SVG_DOWN = QtSvg.QSvgRenderer(os.path.join(dir, 'images/arrows/down.svg'))
SVG_LEFT = QtSvg.QSvgRenderer(os.path.join(dir, 'images/arrows/left.svg'))
SVG_RIGHT = QtSvg.QSvgRenderer(os.path.join(dir, 'images/arrows/right.svg'))


SVG_1 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/1.svg'))
SVG_2 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/2.svg'))
SVG_3 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/3.svg'))
SVG_4 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/4.svg'))
SVG_5 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/5.svg'))
SVG_6 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/6.svg'))
SVG_7 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/7.svg'))
SVG_8 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/8.svg'))
SVG_9 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/9.svg'))
SVG_10 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/10.svg'))
SVG_11 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/11.svg'))
SVG_12 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/12.svg'))
SVG_13 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/13.svg'))
SVG_14 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/14.svg'))
SVG_15 = QtSvg.QSvgRenderer(os.path.join(dir, 'images/lines/15.svg'))


VALUE_ROLE = QtCore.Qt.UserRole


def pixels_to_logical(x, y):
    """return row, column"""
    return y // CELL_SIZE, x // CELL_SIZE


def logical_to_pixels(row, column):
    return column * CELL_SIZE, row * CELL_SIZE


class GridWidget(QtWidgets.QWidget):
    def __init__(self, array):
        super().__init__()
        self.array = array
        self.paths = numpy.zeros(array.shape, dtype=numpy.int8)
        self.lines = numpy.zeros(array.shape, dtype=numpy.int8)
        self.before_last_target = 0
        # * =  rozbaleni dvojice do dvou argumentu
        size = logical_to_pixels(*array.shape)
        self.setMinimumSize(*size)
        self.setMaximumSize(*size)
        self.resize(*size)

    def paintEvent(self, event):
        # ziskame informace o prekreslované oblasti
        rect = event.rect()
 
        # zjistime, jakou oblast nasi matice to predstavuje
        # nesmime se pritom dostat z matice ven
        row_min, col_min = pixels_to_logical(rect.left(), rect.top())
        row_min = max(row_min, 0)
        col_min = max(col_min, 0)
        row_max, col_max = pixels_to_logical(rect.right(), rect.bottom())
        row_max = min(row_max + 1, self.array.shape[0])
        col_max = min(col_max + 1, self.array.shape[1])

        # budeme kreslit
        painter = QtGui.QPainter(self)

        solution = analyze(self.array)
        directions = solution.directions
        dudes_x, dudes_y = numpy.where(self.array >= 2)

        tar_x, tar_y = numpy.where(self.array == 1)
        has_target = True
        if not len(tar_x) or not len(tar_y):
            has_target = False

        # mark paths
        if has_target:
            # reset paths
            self.paths = numpy.zeros(self.array.shape, dtype=numpy.int8)
            self.lines = numpy.zeros(self.array.shape, dtype=numpy.int8)

            # for each dude
            for i in range(0, len(dudes_x)):
                dude_x = dudes_x[i]
                dude_y = dudes_y[i]
                # find path from dude to castle
                try:
                    path = solution.path(dude_x, dude_y)
                except ValueError:
                    path = []
                # mark path to auxiliar array
                for step in path:
                    step_x = step[0]
                    step_y = step[1]
                    self.paths[step_x, step_y] = 1

            for i in range(0, self.lines.shape[0]):
                for j in range(0, self.lines.shape[1]):
                    self.lines[i][j] = self.searchLine(i, j, self.lines.shape)
        else:
            self.paths = numpy.zeros(self.array.shape, dtype=numpy.int8)
            self.lines = numpy.zeros(self.array.shape, dtype=numpy.int8)

        for row in range(row_min, row_max):
            for column in range(col_min, col_max):
                # ziskame ctverecek, ktery budeme vybarvovat
                x, y = logical_to_pixels(row, column)
                rect = QtCore.QRectF(x, y, CELL_SIZE, CELL_SIZE)
 
                # bila barva
                color = QtGui.QColor(255, 255, 255)

                # vyplnime ctverecek barvou
                painter.fillRect(rect, QtGui.QBrush(color))
                SVG_GRASS.render(painter, rect)

                # draw correct line
                if self.lines[row][column] == 1:
                    SVG_1.render(painter, rect)
                elif self.lines[row][column] == 2:
                    SVG_2.render(painter, rect)
                elif self.lines[row][column] == 3:
                    SVG_3.render(painter, rect)
                elif self.lines[row][column] == 4:
                    SVG_4.render(painter, rect)
                elif self.lines[row][column] == 5:
                    SVG_5.render(painter, rect)
                elif self.lines[row][column] == 6:
                    SVG_6.render(painter, rect)
                elif self.lines[row][column] == 7:
                    SVG_7.render(painter, rect)
                elif self.lines[row][column] == 8:
                    SVG_8.render(painter, rect)
                elif self.lines[row][column] == 9:
                    SVG_9.render(painter, rect)
                elif self.lines[row][column] == 10:
                    SVG_10.render(painter, rect)
                elif self.lines[row][column] == 11:
                    SVG_11.render(painter, rect)
                elif self.lines[row][column] == 12:
                    SVG_12.render(painter, rect)
                elif self.lines[row][column] == 13:
                    SVG_13.render(painter, rect)
                elif self.lines[row][column] == 14:
                    SVG_14.render(painter, rect)
                elif self.lines[row][column] == 15:
                    SVG_15.render(painter, rect)

                # draw wall, castle, dude
                if self.array[row, column] < 0:
                    SVG_WALL.render(painter, rect)
                elif self.array[row, column] == 1:
                    SVG_CASTLE.render(painter, rect)
                elif self.array[row, column] == 2:
                    SVG_DUDE1.render(painter, rect)
                elif self.array[row, column] == 3:
                    SVG_DUDE2.render(painter, rect)
                elif self.array[row, column] == 4:
                    SVG_DUDE3.render(painter, rect)
                elif self.array[row, column] == 5:
                    SVG_DUDE4.render(painter, rect)
                elif self.array[row, column] == 6:
                    SVG_DUDE5.render(painter, rect)

                # i am on the road and grass, draw direction
                if self.paths[row][column] == 1 and self.array[row][column] == 0:
                    if directions[row][column] == b'^':
                        SVG_UP.render(painter, rect)
                    elif directions[row][column] == b'v':
                        SVG_DOWN.render(painter, rect)
                    elif directions[row][column] == b'<':
                        SVG_LEFT.render(painter, rect)
                    elif directions[row][column] == b'>':
                        SVG_RIGHT.render(painter, rect)

    def mousePressEvent(self, event):
        row, column = pixels_to_logical(event.x(), event.y())
        shape = self.array.shape
        if 0 <= row < shape[0] and 0 <= column < shape[1]:
            if event.button() == QtCore.Qt.LeftButton:
                # click on castle
                if self.selected == 1:
                    # seach for existing castle
                    tar = numpy.where(self.array == 1)
                    print(tar)
                    self.array[tar[0], tar[1]] = 0
                self.array[row, column] = self.selected
            elif event.button() == QtCore.Qt.RightButton:
                self.array[row, column] = 0
            else:
                return
            # self.update(*logical_to_pixels(row,column),CELL_SIZE, CELL_SIZE) # prekresli novy widget, bez argumentu prekresli vse
            self.update()

    def searchLine(self, row, column, shape):

        if self.paths[row][column] == 0:
            return 0

        if row > 0:
            path_up = self.paths[row-1][column]
        else:
            path_up = None

        if row < shape[0] - 1:
            path_down = self.paths[row+1][column]
        else:
            path_down = None

        if column < shape[1] - 1:
            path_right = self.paths[row][column+1]
        else:
            path_right = None

        if column > 0:
            path_left = self.paths[row][column-1]
        else:
            path_left = None

        if path_up == 1 and (path_right == 0 or path_right is None) and (path_down == 0 or path_down is None) and (path_left == 0 or path_left is None):
            return 1
        elif (path_up == 0 or path_up is None) and (path_right == 0 or path_right is None) and (path_down == 0 or path_down is None) and (path_left == 1):
            return 2
        elif (path_up == 1) and (path_right == 0 or path_right is None) and (path_down == 0 or path_down is None) and (path_left == 1):
            return 3
        elif (path_up == 0 or path_up is None) and (path_right == 0 or path_right is None) and (path_down == 1) and (path_left == 0 or path_left is None):
            return 4
        elif (path_up == 1) and (path_right == 0 or path_right is None) and (path_down ==1 ) and (path_left == 0 or path_left is None):
            return 5
        elif (path_up == 0 or path_up is None) and (path_right == 0 or path_right is None) and (path_down == 1) and (path_left == 1):
            return 6
        elif (path_up == 1) and (path_right == 0 or path_right is None) and (path_down == 1) and (path_left == 1):
            return 7
        elif (path_up == 0 or path_up is None) and (path_right == 1) and (path_down == 0 or path_down is None) and (path_left == 0 or path_left is None):
            return 8
        elif (path_up == 1) and (path_right == 1) and (path_down == 0 or path_down is None) and (path_left ==  0 or path_left is None):
            return 9
        elif (path_up == 0 or path_up is None) and (path_right == 1) and (path_down == 0 or path_down is None) and (path_left == 1):
            return 10
        elif (path_up == 1) and (path_right == 1) and (path_down == 0 or path_down is None) and (path_left == 1):
            return 11
        elif (path_up == 0 or path_up is None) and (path_right == 1) and (path_down == 1) and (path_left == 0 or path_left is None):
            return 12
        elif (path_up == 1) and (path_right == 1) and (path_down == 1) and (path_left == 0 or path_left is None):
            return 13
        elif (path_up == 0 or path_up is None) and (path_right == 1) and (path_down == 1) and (path_left == 1):
            return 14
        elif (path_up == 1) and (path_right == 1) and (path_down == 1) and (path_left == 1):
            return 15


def new_dialog(grid, window):
    dialog = QtWidgets.QDialog(window)
    with open(os.path.join(dir, 'newmaze.ui')) as f:
        uic.loadUi(f, dialog)
        
    result = dialog.exec()
    if result == QtWidgets.QDialog.Rejected:
        return
        
    cols = dialog.findChild(QtWidgets.QSpinBox, 'widthBox').value()
    rows = dialog.findChild(QtWidgets.QSpinBox, 'heightBox').value()

    # grid.array = generate.maze(cols,rows)
    grid.array = numpy.zeros((rows, cols), dtype=numpy.int8)
    grid.lines = numpy.zeros((rows, cols), dtype=numpy.int8)
    grid.paths = numpy.zeros((rows, cols), dtype=numpy.int8)

    size = logical_to_pixels(rows, cols)
    grid.setMinimumSize(*size)
    grid.setMaximumSize(*size)
    grid.resize(*size)
    grid.update()


def save_maze(grid, window):
    result = QtWidgets.QFileDialog.getSaveFileName(window)
    filepath = result[0]

    if filepath == '':
        return

    print("Saving to " + filepath)
    try:
        numpy.savetxt(filepath, grid.array)
    except:
        QtWidgets.QMessageBox.critical(window, "Error", "Error while saving maze. Check file permissions.", QtWidgets.QMessageBox.Close)
        return


def load_maze(grid, window):
    result = QtWidgets.QFileDialog.getOpenFileName(window)
    filepath = result[0]

    if filepath == '':
        return

    print("Loading from " + filepath)
    try:
        grid.array = numpy.loadtxt(filepath, dtype=numpy.int8)
    except:
        QtWidgets.QMessageBox.critical(window, "Error", "Error while loading maze. Check file permissions.", QtWidgets.QMessageBox.Close)
        return
    rows, cols = grid.array.shape
    size = logical_to_pixels(rows, cols)
    grid.setMinimumSize(*size)
    grid.setMaximumSize(*size)
    grid.resize(*size)
    grid.update()


def show_about(window):
    text = """
    This is Maze v0.3

    This program is used for editing and vizualizing mazes.

    Authors: Ing. Miro Hroncok, MSc. Petr Viktorin, Bc. Petr Klejch

    Git repository: https://github.com/pklejch/maze

    License: GPL-3.0

    Graphics by http://kenney.nl/
    """
    QtWidgets.QMessageBox.about(window, "About this application", text)


def addItem(image, label, value, palette):
    item = QtWidgets.QListWidgetItem(label)
    icon = QtGui.QIcon(image)
    item.setIcon(icon)
    item.setData(VALUE_ROLE, value)
    palette.addItem(item)


def main():
    app = QtWidgets.QApplication([])
 
    window = QtWidgets.QMainWindow()
 
    with open(os.path.join(dir, 'maze.ui')) as f:
        uic.loadUi(f, window)

    array = numpy.zeros((5, 5), dtype=numpy.int8)
    array[0, 4] = -1
    array[1, 4] = -1
    array[2, 4] = -1
    array[3, 4] = -1
    array[3, 3] = -1
    array[3, 2] = -1
    array[3, 0] = -1
    array[1, 0] = -1
    array[1, 1] = -1
    array[1, 2] = -1
    array[2, 0] = -1

    # dostanu prvek z okynka
    scroll_area = window.findChild(QtWidgets.QScrollArea, 'scrollArea')

    grid = GridWidget(array)
    scroll_area.setWidget(grid)
    palette = window.findChild(QtWidgets.QListWidget, 'palette')

    addItem(os.path.join(dir, 'images/grass.svg'), 'Grass', 0, palette)
    addItem(os.path.join(dir, 'images/wall.svg'), 'Wall', -1, palette)
    addItem(os.path.join(dir, 'images/castle.svg'), 'Castle', 1, palette)
    addItem(os.path.join(dir, 'images/dude1.svg'), 'Dude', 2, palette)
    addItem(os.path.join(dir, 'images/dude2.svg'), 'Dude 2', 3, palette)
    addItem(os.path.join(dir, 'images/dude3.svg'), 'Dude 3', 4, palette)
    addItem(os.path.join(dir, 'images/dude4.svg'), 'Dude 4', 5, palette)
    addItem(os.path.join(dir, 'images/dude5.svg'), 'Dude 5', 6, palette)

    def item_activated():
        for item in palette.selectedItems():
            grid.selected = item.data(VALUE_ROLE)
            
    palette.itemSelectionChanged.connect(item_activated)
    palette.setCurrentRow(1)
    
    action = window.findChild(QtWidgets.QAction, 'actionNew')
    action.triggered.connect(lambda: new_dialog(grid, window))

    action = window.findChild(QtWidgets.QAction, 'actionSave')
    action.triggered.connect(lambda: save_maze(grid, window))

    action = window.findChild(QtWidgets.QAction, 'actionLoad')
    action.triggered.connect(lambda: load_maze(grid, window))

    action = window.findChild(QtWidgets.QAction, 'actionAbout')
    action.triggered.connect(lambda: show_about(window))
    
    window.show()
 
    return app.exec()
