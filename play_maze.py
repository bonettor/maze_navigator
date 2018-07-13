import numpy as np 
import time
import turtle

from numpy.random import randint

from genmaze import Pen 
from genmaze import MazeGenerator

from player import Player 

def init_q_matrix(h, w):
    Q = 0 * np.ones(shape = [h, w, 4])
    return Q

def learn(Q, player, maze, alpha, discount, max_episodes, fancy_player=False, 
            render_interval=None):
    episode = 0
    maze_matrix = maze.maze 
    reward = -0.1/(maze_matrix.shape[0]*maze_matrix.shape[1])
    inital_state = player.position_idx
    final_state = maze.end_indices
    actions = {
        0: player.move_left,
        1: player.move_right,
        2: player.move_up,
        3: player.move_down,
    }

    if fancy_player:
        fancy_player = Player(init_coordinates=maze.start_coordinates, init_indices=maze.start_indices, 
                        maze_matrix=maze.maze)
        fancy_actions = {
            0: fancy_player.move_left,
            1: fancy_player.move_right,
            2: fancy_player.move_up,
            3: fancy_player.move_down,
        }

    while episode < max_episodes:
        if episode % 2 == 0:
                print("training episode: {}".format(episode))
        player.position_idx = inital_state
        state = player.position_idx
        while True:
            action = randint(0,4)
            prev_state = state
            actions[action]()
            state = player.position_idx
            if state == final_state:
                Q[state[0], state[1], action] = 100
                break
            Q[prev_state[0], prev_state[1], action] = (1 - alpha) * Q[state[0], state[1], action] + alpha \
                                                    * (reward + discount * np.max(Q[state[0], state[1], :]))

        if fancy_player:
            if episode > 0 and episode % render_interval == 0:
                fancy_state = inital_state

                stuck = 0
                iterations = 0
                while fancy_state != final_state:
                    if iterations > 300:
                        break
                    iterations += 1
                    fancy_actions[np.argmax(Q[fancy_state[0], fancy_state[1], :])]()
                    if fancy_state == fancy_player.position_idx:
                        stuck += 1
                    if stuck > 10:
                        #print("player stuck, random action")
                        for _ in range(10):
                            fancy_actions[randint(0,4)]()    
                        stuck = 0
                    fancy_state = fancy_player.position_idx
                fancy_player.__init__(init_coordinates=maze.start_coordinates, 
                                    init_indices=maze.start_indices, 
                                    maze_matrix=maze.maze)
                fancy_actions = {
                            0: fancy_player.move_left,
                            1: fancy_player.move_right,
                            2: fancy_player.move_up,
                            3: fancy_player.move_down,
                        }

        episode += 1


if __name__ == "__main__":

    wm = turtle.Screen()
    turtle.register_shape('tenor.gif')
    wm.bgcolor('black')
    wm.title("MAZINGA")
    gen = MazeGenerator(50,50)
    gen.prim_maze()


    gen.set_start()
    gen.set_end()

    pen = Pen()
    wm.tracer(0)
    gen.draw_maze(pen)
    wm.tracer(1)

    player_1 = Player(init_indices=gen.start_indices, maze_matrix=gen.maze)

    maze_matrix = np.array(gen.maze)
    gen.maze = maze_matrix
    Q = init_q_matrix(gen.maze.shape[0], gen.maze.shape[1])
    learn(Q=Q, player=player_1, maze=gen, alpha=0.7, discount=0.8, max_episodes=1000, 
        fancy_player=True, render_interval=2)

