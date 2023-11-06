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

    def __init__(self, rows, cols, obstacle_length):
        self.rows = rows
        self.cols = cols
        self.maze = np.zeros((rows, cols), dtype=int)
        self.obstacle_length = obstacle_length
        self.setup_obstacle((7, 9))
        self.add_to_obstacle_length()

    def setup_obstacle(self, center_pos):
        self.obstacle_center = center_pos
        self.maze[center_pos[0]][center_pos[1]] = 1

    # original length is always 3
    # length to be added
    def add_to_obstacle_length(self):
        right = self.obstacle_center[1] + 1
        left = self.obstacle_center[1] - 1
        self.obstacle_right = (self.obstacle_center[0], right)
        self.obstacle_left = (self.obstacle_center[0], left)

        # loop to set everything up
        i = 0
        temp_length = self.obstacle_length
        while i <= temp_length:
            self.maze[self.obstacle_center[0]][right] = 1
            right += 1
            i += 1
            self.maze[self.obstacle_center[0]][left] = 1
            left -= 1
            i += 1
            self.obstacle_length += 2

    def get_maze(self):
        return self.maze

    def get_obstacle_length(self):
        return self.obstacle_length
