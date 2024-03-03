from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("boot.dev maze course")
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__window_running = True
        while self.__window_running:
            self.redraw()

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def close(self):
        self.__window_running = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)
        canvas.pack(fill=BOTH, expand=True)

class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

    def draw(self):
        if self._win is None:
            return
        left_wall = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        right_wall = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
        top_wall = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        bottom_wall = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
        if self.has_left_wall:
            self._win.draw_line(left_wall)
        else:
            self._win.draw_line(left_wall, "#d9d9d9")
        if self.has_right_wall:
            self._win.draw_line(right_wall)
        else:
            self._win.draw_line(right_wall, "#d9d9d9")
        if self.has_top_wall:
            self._win.draw_line(top_wall)
        else:
            self._win.draw_line(top_wall, "#d9d9d9")
        if self.has_bottom_wall:
            self._win.draw_line(bottom_wall)
        else:
            self._win.draw_line(bottom_wall, "#d9d9d9")

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        self.from_cell_middle_x = (self._x2 + self._x1) / 2
        self.from_cell_middle_y = (self._y2 + self._y1) / 2
        self.to_cell_middle_x = (to_cell._x2 + to_cell._x1) / 2
        self.to_cell_middle_y = (to_cell._y2 + to_cell._y1) / 2
        self.from_cell_point = Point(self.from_cell_middle_x, self.from_cell_middle_y)
        self.to_cell_point = Point(self.to_cell_middle_x, self.to_cell_middle_y)
        fill_color = "red"
        if undo:
            fill_color = "grey"
        self._win.draw_line(Line(self.from_cell_point, self.to_cell_point), fill_color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        if seed != None:
            random.seed(seed)


    def _create_cells(self):
        for a in range(self._num_cols):
            self._cells.append([])
            cell_to_append_x1 = self._x1 + self._cell_size_x * a
            cell_to_append_x2 = self._x1 + self._cell_size_x * (a + 1)
            for b in range (self._num_rows):
                cell_to_append_y1 = self._y1 + self._cell_size_y * b
                cell_to_append_y2 = self._y1 + self._cell_size_y * (b + 1)
                cell_to_append = Cell(cell_to_append_x1, cell_to_append_y1, cell_to_append_x2, cell_to_append_y2, self._win)
                self._cells[a].append(cell_to_append)
                self._draw_cell(a, b)

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.035)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
        self._draw_cell(self._num_cols-1, self._num_rows-1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True


window_width = 800
window_height = 600
win = Window(window_width, window_height)
#cell1 = Cell(100, 100, 200, 200, win)
#cell2 = Cell(200, 100, 300, 200, win)
#cell3 = Cell(300, 100, 400, 200, win)
#cell1.has_right_wall = False
#cell2.has_left_wall = False
#cell1.draw()
#cell2.draw()
#cell3.draw()
#cell1.draw_move(cell2)
#cell2.draw_move(cell3, True)
maze_num_rows = 4
maze_num_cols = 6
maze_window_border = 20
cell_width = (window_width - 2 * maze_window_border) / maze_num_cols
cell_height = (window_height - 2 * maze_window_border) / maze_num_rows
seed = 0
the_maze = Maze(maze_window_border, maze_window_border, maze_num_rows, maze_num_cols, cell_width, cell_height, win, seed)

#cellm1 = maze1._cells[5][3]
#cellm1.draw()

win.wait_for_close()

