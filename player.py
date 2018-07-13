import numpy as np 

import turtle

from genmaze import Pen 
from genmaze import MazeGenerator

class Player(turtle.Turtle):
    def __init__(self, init_indices, maze_matrix, init_coordinates = None):
        self.draw = False
        if init_coordinates is not None:
            turtle.Turtle.__init__(self, visible=False)
            self.origin = init_coordinates
            self.penup()
            self.speed(10)
            self.shape('tenor.gif')
            self.color('cyan')
            self.goto(self.origin)
            self.showturtle()
            self.draw = True
        self.maze = maze_matrix
        self.position_idx = init_indices

    def move_left(self):
        if self.draw:
            self.setheading(180)
        i = self.position_idx[0]
        tmp_j = self.position_idx[1] - 1
        if tmp_j >= 0 and tmp_j <= len(self.maze[0]):
            if self.maze[i][tmp_j] != 1:
                if self.draw:
                    self.goto(self.xcor() - 24, self.ycor())
                self.position_idx = [i, tmp_j]

    def move_right(self):
        if self.draw:
            self.setheading(0)
        i = self.position_idx[0]
        tmp_j = self.position_idx[1] + 1
        if tmp_j >= 0 and tmp_j <= len(self.maze[0]):
            if self.maze[i][tmp_j] != 1:
                if self.draw:
                    self.goto(self.xcor() + 24, self.ycor())
                self.position_idx = [i, tmp_j]
    def move_up(self):
        if self.draw:
            self.setheading(90)
        j = self.position_idx[1]
        tmp_i = self.position_idx[0] - 1
        if tmp_i >= 0 and tmp_i <= len(self.maze[0]):
            if self.maze[tmp_i][j] != 1:
                if self.draw:
                    self.goto(self.xcor(), self.ycor() + 24)
                self.position_idx = [tmp_i, j]
    def move_down(self):
        if self.draw:
            self.setheading(-90)
        j = self.position_idx[1]
        tmp_i = self.position_idx[0] + 1
        if tmp_i >= 0 and tmp_i <= len(self.maze[0]):
            if self.maze[tmp_i][j] != 1:
                if self.draw:
                    self.goto(self.xcor(), self.ycor() - 24)
                self.position_idx = [tmp_i, j]

if __name__ == "__main__":
    wm = turtle.Screen()
    turtle.register_shape('tenor.gif')
    gen = MazeGenerator(30,30)
    pen = Pen()
    gen.prim_maze()
    gen.set_start()
    gen.set_end()
    wm.tracer(0)
    gen.draw_maze(pen)
    wm.tracer(1)
    player = Player(init_coordinates=gen.start_coordinates, 
                                    init_indices=gen.start_indices, 
                                    maze_matrix=gen.maze)
    turtle.listen()
    turtle.onkey(player.move_left, 'Left')
    turtle.onkey(player.move_right, 'Right')
    turtle.onkey(player.move_up, 'Up')
    turtle.onkey(player.move_down, 'Down')
    turtle.done()

