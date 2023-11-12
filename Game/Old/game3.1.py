import pygame
import numpy as np
import random
import time
# import numbers
import matplotlib.pyplot as plt
from heapq import heappush, heappop

from Maze import Maze

# Pygame
pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pathfinding for Evolving Terrain")
font = pygame.font.Font(None, 36)

# Maze instance & attributes
tile_size = (40, 40)
rows, cols = height // tile_size[1], width // tile_size[0]
maze_object = Maze(rows, cols)
maze = maze_object.get_maze()

# Player & Enemy attributes
player_pos = [8, 16]  # Starting position of the player
enemy_pos = [10, 16]  # Starting position of the enemy

# colordef
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

global_run_time = {}
input_size = 0
start_timer = None

# A* algorithm
def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)  # Calculate the Euclidean distance between two points


def astar(maze, start, goal):
    closed_set = set()  # Initialize an empty set to store the nodes that have been evaluated
    open_set = [(0, start)]  # Initialize the open set with the starting node
    came_from = {}  # Initialize an empty dictionary to store the most efficient previous step
    g_score = {tuple(position): float('inf') for position in np.ndindex(maze.shape)}
    # Initialize g_score with infinity for each position in the maze
    g_score[start] = 0  # Set the g_score for the start position to 0
    f_score = {tuple(position): float('inf') for position in np.ndindex(maze.shape)}
    # Initialize f_score with infinity for each position in the maze
    f_score[start] = heuristic(start, goal)
    # Set the f_score for the start position using the heuristic function

    while open_set:  # Start the main loop of the A* algorithm
        current_f_score, current = heappop(
            open_set)  # Remove and return the node with the lowest f_score from the priority queue
        if current == goal:  # If the current node is the goal, we've found the path
            return reconstruct_path(came_from, current)  # Return the path from start to goal

        closed_set.add(current)  # Add the current node to the set of nodes already evaluated

        # Iterate over the direct neighbors of the current node (up, down, left, right)
        for neighbor in [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
                         (current[0], current[1] - 1), (current[0], current[1] + 1)]:
            # The neighbor above/below/left/right to the current node

            # Check if the neighbor is within the maze boundaries and not a wall (maze value 1)        
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]):
                # If the neighbor is a wall or in the closed set, skip it
                if maze[neighbor[0]][neighbor[1]] == 1 or neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current] + 1
                # If this g_score is better (lower) than any previously recorded g_score, update the path and scores
                if tentative_g_score < g_score[
                    neighbor]:  # Record the current node as the best step to reach the neighbor
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    # Update the f_score for the neighbor (g_score plus heuristic)

                    if neighbor not in open_set:  # If the neighbor is not in the open set, add it
                        heappush(open_set, (f_score[neighbor], neighbor))

    return []  # If the goal cannot be reached, return an empty list


def reconstruct_path(came_from, current):
    total_path = [current]  # Initialize the path with the goal node
    while current in came_from:  # As long as the current node is in the came_from map, which records where we came from for each node...
        current = came_from[current]  # update the current node to the one we came from
        total_path.append(current)  # and add it to the path

        # Once we've reached the start node, it won't be in the came_from map, and the loop will end. 
        # We then return the reversed path, starting from the start node and ending at the goal node.
    return total_path[::-1]  # Reverse the path to get the correct order from start to goal


def player_movement():
    directions = [
        ('left', lambda: player_pos[1] > 0 and maze[player_pos[0]][player_pos[1] - 1] == 0),
        # 'left' move is valid if player is not on the leftmost column and the left cell is not a wall
        ('right', lambda: player_pos[1] < cols - 1 and maze[player_pos[0]][player_pos[1] + 1] == 0),
        # 'right' move is valid if player is not on the rightmost column and the right cell is not a wall
        ('up', lambda: player_pos[0] > 0 and maze[player_pos[0] - 1][player_pos[1]] == 0),
        ('down', lambda: player_pos[0] < rows - 1 and maze[player_pos[0] + 1][player_pos[1]] == 0),
    ]
    random_direction, condition_fn = random.choice(directions)
    if condition_fn():

        if random_direction == 'left':  # Move the player left if the random direction is 'left' and the move is valid
            player_pos[1] -= 1
        elif random_direction == 'right':
            player_pos[1] += 1
        elif random_direction == 'up':  # Move the player up if the random direction is 'up' and the move is valid
            player_pos[0] -= 1
        elif random_direction == 'down':
            player_pos[0] += 1


def enemy_movement_logic():
    # Enemy A* movement logic
    path = astar(maze, tuple(enemy_pos),
                 tuple(player_pos))  # Calculate the path from the enemy to the player using A*
    if len(path) > 1:
        enemy_pos[0], enemy_pos[1] = path[1]  # Move the enemy to the next step in the path


def render():
    screen.fill(WHITE)  # Clear the screen with a white background? There have some bugs here...
    for row in range(rows):  # Loop through each row
        for col in range(cols):  # Loop through each cols
            if maze[row][col] == 1:  # If there's a wall at this position
                pygame.draw.rect(screen, BLUE,
                                 (col * tile_size[0], row * tile_size[1], tile_size[0], tile_size[1]))
                # Draw a blue rectangle (wall) on the screen at the corresponding position

    draw_grid()

    pygame.draw.rect(screen, GREEN, (player_pos[1] * tile_size[0], player_pos[0] * tile_size[1], tile_size[0],
                                     tile_size[1]))  # green means player
    pygame.draw.rect(screen, RED, (
        enemy_pos[1] * tile_size[0], enemy_pos[0] * tile_size[1], tile_size[0],
        tile_size[1]))  # red means enemy
    pygame.display.flip()  # Update the full display surface to the screen


def draw_grid():
    block_size = 40  # Set the size of the grid block
    for x in range(0, width, block_size):
        for y in range(0, height, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, BLACK, rect, 1)


def game_loop():
    global player_pos, enemy_pos, start_timer, input_size
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate
    running = True  # Set the running flag to True to start the game loop
    step_size = 2  # Define the step size for player movement

    try:
        while running:
            render()
            clock.tick(10)  # Limit the game to 5 frames per second (fps)

            for event in pygame.event.get():
                if player_pos == enemy_pos:
                    end_timer = time.perf_counter()

                    global_run_time[input_size] = end_timer - start_timer
                    print(global_run_time)

                    player_pos = [8, 16]
                    enemy_pos = [10, 16]
                    maze_object.add_to_obstacle_length()
                    input_size = maze_object.get_obstacle_length()
                if maze_object.get_obstacle_length() == 1:
                    input_size = maze_object.get_obstacle_length()
                    start_timer = time.perf_counter()
                if maze_object.get_obstacle_length() == 32:
                    running = False
                if event.type == pygame.QUIT:
                    running = False  # Set running too false to exit the game loop

            player_movement()
            enemy_movement_logic()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    game_loop()

    # Extract the input sizes and runtimes from the run time dictionary
    input_x = list(global_run_time.keys())
    print(input_x)
    runtimesy = list(global_run_time.values())
    print(runtimesy)
    # Create a line graph
    plt.figure(figsize=(10, 6))
    plt.plot(input_x, runtimesy, marker='o', linestyle='-', color='b')
    plt.title('Runtime vs Input Size')
    plt.xlabel('Input Size')
    plt.ylabel('Runtime (Seconds)')
    plt.grid(True)

    # Display the graph
    plt.grid()
    plt.show()
