# Eddie Castro
# Maze class
import numpy as np


class Maze:
    # Maze Attributes
    rows = None
    cols = None

    # Obstacle Attributes
    obstacle_center = None
    obstacle_left = None
    obstacle_right = None
    obstacle_length = None

    # Maze Array
    maze = None

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = np.zeros((rows, cols), dtype=int)
        self.obstacle_length = 1
        self.setup_obstacle((9, 16))

    def setup_obstacle(self, center_pos):
        self.obstacle_center = center_pos
        self.obstacle_left = center_pos[1]
        self.obstacle_right = center_pos[1]
        self.maze[center_pos[0]][center_pos[1]] = 1

    # length added to the obstacle
    def add_to_obstacle_length(self):
        self.obstacle_left = self.obstacle_left - 1
        self.obstacle_right = self.obstacle_right + 1
        self.maze[self.obstacle_center[0]][self.obstacle_left] = 1
        self.maze[self.obstacle_center[0]][self.obstacle_right] = 1
        self.obstacle_length += 2


    def get_maze(self):
        return self.maze

    def get_maze_row(self):
        return self.rows

    def get_maze_cols(self):
        return self.cols

    def get_obstacle_length(self):
        return self.obstacle_length
