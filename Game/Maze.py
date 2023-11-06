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

    # Maze Array
    maze = None


    def __init__(self, rows, cols, obstacle_length):
        self.rows = rows
        self.cols = cols
        self.maze = np.zeros((15,20), dtype=int)
        self.setup_obstacle((7, 9))
        self.set_obstacle_length(obstacle_length)


    def setup_obstacle(self, center_pos):
        self.obstacle_center = center_pos
        self.maze[center_pos[0]][center_pos[1]] = 1

    def set_obstacle_length(self, length):
        right = self.obstacle_center[1] + 1
        left = self.obstacle_center[1] - 1
        self.obstacle_right = (self.obstacle_center[0], right)
        self.obstacle_left = (self.obstacle_center[0], left)

        # loop to set everything up
        i = 0
        while i <= length:
            self.maze[self.obstacle_center[0]][right] = 1
            right += 1
            i += 1
            self.maze[self.obstacle_center[0]][left] = 1
            left -= 1
            i += 1

    def get_maze(self):
        return self.maze



