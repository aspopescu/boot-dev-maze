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

        self.left_wall = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        self.right_wall = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
        self.top_wall = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        self.bottom_wall = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))

    def draw(self):
        if self._win is None:
            return
        if self.has_left_wall:
            self._win.draw_line(self.left_wall)
        else:
            self._win.draw_line(self.left_wall, "#d9d9d9")
        if self.has_right_wall:
            self._win.draw_line(self.right_wall)
        else:
            self._win.draw_line(self.right_wall, "#d9d9d9")
        if self.has_top_wall:
            self._win.draw_line(self.top_wall)
        else:
            self._win.draw_line(self.top_wall, "#d9d9d9")
        if self.has_bottom_wall:
            self._win.draw_line(self.bottom_wall)
        else:
            self._win.draw_line(self.bottom_wall, "#d9d9d9")

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
        self._break_walls_r(num_cols - 1, num_rows - 1)
        self._reset_cells_visited()

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
        time.sleep(0.0035)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
        self._draw_cell(self._num_cols-1, self._num_rows-1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        print(f"cell i: {i}, cell j: {j}")
        while True:
            cells_to_visit = []
            to_right_x = i + 1
            to_bottom_y = j + 1
            to_left_x = i - 1
            to_top_y = j - 1

            if to_right_x != self._num_cols:
                if self._cells[to_right_x][j].visited == False:
                    cells_to_visit.append((self._cells[to_right_x][j], "right"))
                    print("ok to go right")
            if to_bottom_y != self._num_rows:
                if self._cells[i][to_bottom_y].visited == False:
                    cells_to_visit.append((self._cells[i][to_bottom_y], "bottom"))
                    print("ok to go bottom")
            if to_left_x >= 0:
                if self._cells[to_left_x][j].visited == False:
                    cells_to_visit.append((self._cells[to_left_x][j], "left"))
                    print("ok to go left")
            if to_top_y >= 0:
                if self._cells[i][to_top_y].visited == False:
                    cells_to_visit.append((self._cells[i][to_top_y], "top"))
                    print("ok to go top")

            if len(cells_to_visit) == 0:
                self._draw_cell(i, j)
                return

            next_move = random.choice(range(0, len(cells_to_visit)))
            print(f"next move: {next_move}")
            next_cell = cells_to_visit[next_move][0]
            direction = cells_to_visit[next_move][1]
            if direction == "right":
                print("moving right")
                self._cells[i][j].has_right_wall = False
                next_cell.has_left_wall = False
                self._break_walls_r(i + 1, j)
            if direction == "bottom":
                print("moving bottom")
                self._cells[i][j].has_bottom_wall = False
                next_cell.has_top_wall = False
                self._break_walls_r(i, j + 1)
            if direction == "left":
                print("moving left")
                self._cells[i][j].has_left_wall = False
                next_cell.has_right_wall = False
                self._break_walls_r(i - 1, j)
            if direction == "top":
                print("moving top")
                self._cells[i][j].has_top_wall = False
                next_cell.has_bottom_wall = False
                self._break_walls_r(i, j - 1)
            
    def _reset_cells_visited(self):
        for cells_list in self._cells:
            for cell in cells_list:
                cell.visited = False



window_width = 800
window_height = 600
win = Window(window_width, window_height)
maze_num_cols = 16
maze_num_rows = 12 
maze_window_border = 20
cell_width = (window_width - 2 * maze_window_border) / maze_num_cols
cell_height = (window_height - 2 * maze_window_border) / maze_num_rows
seed = 0
the_maze = Maze(maze_window_border, maze_window_border, maze_num_rows, maze_num_cols, cell_width, cell_height, win, seed)

#the_maze._cells[5][2].visited = True
#the_maze._cells[4][3].visited = True
#the_maze._cells[3][2].visited = True
#the_maze._cells[4][1].visited = True
#the_maze._break_walls_r(4, 2)


win.wait_for_close()

