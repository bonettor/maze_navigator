import numpy as np 
import turtle

from numpy.random import randint

class Pen(turtle.Turtle):
    def __init__(self, screen_h=600, screen_w=600):
        turtle.Turtle.__init__(self, visible=False)
        self.ts = 20
        self.h = screen_h
        self.w = screen_w
        self.origin = [-700, 600]
        #self.origin = [24 / 2 - self.w // 2, self.h // 2 - 24 / 2]
        self.penup()
        self.speed(10)
        self.shape('square')
        self.color('red')
        self.goto(self.origin)

class MazeGenerator(object):
    def __init__(self, h, w):
        # Initialize the grid
        self.w = w
        self.h = h
        if w % 2 == 1:
            self.w += 1
        if h % 2 == 1:
            self.h += 1
        self.maze = [[1] * (self.w+1)] 
        self.cells = []
        self.walls = []
        for i in range(self.h - 1):
            if i % 2 == 0:
                self.maze.append([1,0] * (self.w // 2) + [1])
            else:
                self.maze.append([1] * (self.w + 1))
        self.maze.append([1] * (self.w+1))
        self.w = len(self.maze[0])
        self.h = len(self.maze)
        for i in range(self.h):
            for j in range(self.w):
                if i % 2 == 1:
                    if j % 2 == 1:
                        self.cells.append([i, j])
                else:
                    self.walls.append([i, j])

    def add_walls(self, cell_coordinates, walls_list):
        c_i = cell_coordinates[0]
        c_j = cell_coordinates[1]

        up_wall = [c_i - 1, c_j]
        down_wall = [c_i + 1, c_j]
        left_wall = [c_i, c_j - 1]
        right_wall = [c_i, c_j + 1]

        if up_wall[0] > 0 and up_wall[0] < self.h - 1:
            if up_wall[1] > 0 and up_wall[1] < self.w - 1:
                walls_list.append(up_wall)

        if down_wall[0] > 0 and down_wall[0] < self.h - 1:
            if down_wall[1] > 0 and down_wall[1] < self.w - 1:
                walls_list.append(down_wall)

        if left_wall[0] > 0 and left_wall[0] < self.h - 1:
            if left_wall[1] > 0 and left_wall[1] < self.w - 1:
                walls_list.append(left_wall)

        if right_wall[0] > 0 and right_wall[0] < self.h - 1:
            if right_wall[1] > 0 and right_wall[1] < self.w - 1:
                walls_list.append(right_wall)



    def prim_maze(self):

        visited_cells = []
        walls_list = []

        # self.maze is a grid full of walls
        # pick a starting cell (only internal cells):
        current_cell = self.cells[randint(0, len(self.cells))]
        visited_cells.append(current_cell)
        self.add_walls(current_cell, walls_list)

        while walls_list != []:
            wall = walls_list.pop(randint(0, len(walls_list)))
            w_i = wall[0]
            w_j = wall[1]

            if w_i % 2 == 0:
                neighboring_cell_1 = [w_i - 1, w_j]
                neighboring_cell_2 = [w_i + 1, w_j]
            else:
                neighboring_cell_1 = [w_i, w_j - 1]
                neighboring_cell_2 = [w_i, w_j + 1]

            if neighboring_cell_1 not in visited_cells:
                self.maze[w_i][w_j] = 0
                visited_cells.append(neighboring_cell_1)
                self.add_walls(neighboring_cell_1, walls_list)
            elif neighboring_cell_2 not in visited_cells:
                self.maze[w_i][w_j] = 0
                visited_cells.append(neighboring_cell_2)
                self.add_walls(neighboring_cell_2, walls_list)

    def draw_maze(self, pen):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                pen.goto(pen.xcor() + 24, pen.ycor())
                if self.maze[i][j] == 1:
                    pen.stamp()
                if self.maze[i][j] == -1:
                    pen.shape('circle')
                    pen.color('blue')
                    pen.stamp()
                    self.start_coordinates = [pen.xcor(), pen.ycor()]
                if self.maze[i][j] == +2:
                    pen.shape('circle')
                    pen.color('green')
                    pen.stamp()
                    self.end_coordinates = [pen.xcor(), pen.ycor()]
                pen.shape('square')
                pen.color('red')
            pen.goto(pen.origin[0], pen.ycor()-24)

    def set_start(self):
        i = randint(0, self.h)
        j = randint(0, self.w)
        while self.maze[i][j] == 1:
            i = randint(0, self.h)
            j = randint(0, self.w)
        self.maze[i][j] = -1
        self.start_indices = [i, j]

    def set_end(self):
        possible_i = [i for i in range(self.h) if i % 2 != 0]
        i = possible_i[randint(0, len(possible_i))]
        if i == 0 or i == self.h - 1:
            possible_j = [j for j in range(self.w) if j % 2 != 0]
        else:
            possible_j = [0, self.w - 1]

        j = possible_j[randint(0, len(possible_j))]
        self.maze[i][j] = +2
        self.end_indices = [i, j]



if __name__ == '__main__':
    wm = turtle.Screen()
    wm.bgcolor('black')
    wm.title("MAZINGA")
    wm.setup(600, 600)   
    pen = Pen()
    gen = MazeGenerator(30,30)
    gen.prim_maze()
    gen.set_start()
    gen.set_end()
    #print(gen.maze)
    gen.draw_maze(pen)
    turtle.done()
