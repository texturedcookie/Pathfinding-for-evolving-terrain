import pygame
import numpy as np
import random
from heapq import heappush, heappop

# Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Game")
font = pygame.font.Font(None, 36)

# mazesize
tile_size = (40, 40)
rows, cols = height // tile_size[1], width // tile_size[0]
player_pos = [1, 1] # Starting position of the player
enemy_pos = [rows - 2, cols - 2] # Starting position of the enemy

# colordef
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# A* algorithm
def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) # Calculate the Euclidean distance between two points

def astar(maze, start, goal):
    closed_set = set() # Initialize an empty set to store the nodes that have been evaluated
    open_set = [(0, start)] # Initialize the open set with the starting node
    came_from = {} # Initialize an empty dictionary to store the most efficient previous step
    g_score = {tuple(position): float('inf') for position in np.ndindex(maze.shape)}
         # Initialize g_score with infinity for each position in the maze
    g_score[start] = 0  # Set the g_score for the start position to 0
    f_score = {tuple(position): float('inf') for position in np.ndindex(maze.shape)} 
         # Initialize f_score with infinity for each position in the maze
    f_score[start] = heuristic(start, goal) 
         # Set the f_score for the start position using the heuristic function
    
    while open_set: # Start the main loop of the A* algorithm
        current_f_score, current = heappop(open_set) # Remove and return the node with the lowest f_score from the priority queue
        if current == goal: # If the current node is the goal, we've found the path
            return reconstruct_path(came_from, current) # Return the path from start to goal
        
        closed_set.add(current) # Add the current node to the set of nodes already evaluated
        
        
        # Iterate over the direct neighbors of the current node (up, down, left, right)
        for neighbor in [(current[0] - 1, current[1]), (current[0] + 1, current[1]), 
                         (current[0], current[1] - 1), (current[0], current[1] + 1)]:
                    #The neighbor above/below/left/right to the current node
                    
            # Check if the neighbor is within the maze boundaries and not a wall (maze value 1)        
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]):
                # If the neighbor is a wall or in the closed set, skip it
                if maze[neighbor[0]][neighbor[1]] == 1 or neighbor in closed_set:
                    continue
                
                tentative_g_score = g_score[current] + 1
                # If this g_score is better (lower) than any previously recorded g_score, update the path and scores
                if tentative_g_score < g_score[neighbor]: # Record the current node as the best step to reach the neighbor
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)  
                      # Update the f_score for the neighbor (g_score plus heuristic)
            
                    if neighbor not in open_set:          # If the neighbor is not in the open set, add it
                        heappush(open_set, (f_score[neighbor], neighbor))
                        
    return [] # If the goal cannot be reached, return an empty list

def reconstruct_path(came_from, current):
    total_path = [current]   # Initialize the path with the goal node
    while current in came_from:    # As long as the current node is in the came_from map, which records where we came from for each node...
        current = came_from[current] #update the current node to the one we came from
        total_path.append(current)  # and add it to the path
        
        # Once we've reached the start node, it won't be in the came_from map, and the loop will end. 
            # We then return the reversed path, starting from the start node and ending at the goal node.
    return total_path[::-1] # Reverse the path to get the correct order from start to goal



# Maze generation function

def generate_maze(rows, cols):
    maze = np.ones((rows, cols), dtype=int)  # Initialize the maze as a grid of '1's (walls)
    def is_valid_cell(row, col, visited): 
        return 0 <= row < rows and 0 <= col < cols and not visited[row, col]
    
    def dfs(row, col, visited):  # The recursive DFS function to carve out the maze
        visited[row, col] = True # Mark the current cell as visited
        maze[row, col] = 0 # Carve out the current cell by setting it to '0' (open path)
        movements = [(0, 1), (1, 0), (0, -1), (-1, 0)] # Possible movements (right, down, left, up)
        random.shuffle(movements) # Shuffle movements to ensure a random maze
        for dr, dc in movements:
            new_row, new_col = row + dr * 2, col + dc * 2  # Calculate the new cell position
            if is_valid_cell(new_row, new_col, visited):  # If the new cell is valid...
                maze[row + dr, col + dc] = 0 # Carve a path to the new cell
                dfs(new_row, new_col, visited)  # Recursively call dfs for the new cell
                
    visited = np.zeros((rows, cols), dtype=bool)  # Initialize the visited cells grid
    dfs(1, 1, visited)    # Start the DFS from the upper-left corner
    
    # Create the entrance and exit for the maze
    maze[0, 1] = 0   # Entrance
    maze[-1, cols - 2] = 0   # Exit
    return maze

def game_loop():
    valid_maze = False  # Start with the assumption that the maze is not valid
    while not valid_maze:  # Keep generating mazes until a valid one is found
        maze = generate_maze(rows, cols)  # Generate a new maze
        path = astar(maze, (1, 1), (rows - 2, cols - 2))  # Use A* algorithm to find a path from start to goal
        if path: # If a path exists, the maze is valid
            valid_maze = True  # Set valid_maze to True to exit the loop
            
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate
    running = True  # Set the running flag to True to start the game loop
    step_size = 2   # Define the step size for player movement
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False   # Set running to False to exit the game loop
                
        # Random player movement logic
        directions = [
            ('left', lambda: player_pos[1] > 0 and maze[player_pos[0]][player_pos[1] - 1] == 0),# 'left' move is valid if player is not on the leftmost column and the left cell is not a wall
            ('right', lambda: player_pos[1] < cols - 1 and maze[player_pos[0]][player_pos[1] + 1] == 0),# 'right' move is valid if player is not on the rightmost column and the right cell is not a wall
            ('up', lambda: player_pos[0] > 0 and maze[player_pos[0] - 1][player_pos[1]] == 0),
            ('down', lambda: player_pos[0] < rows - 1 and maze[player_pos[0] + 1][player_pos[1]] == 0),
        ]
        random_direction, condition_fn = random.choice(directions)
        if condition_fn():
            
            if random_direction == 'left': # Move the player left if the random direction is 'left' and the move is valid
                player_pos[1] -= 1
            elif random_direction == 'right':
                player_pos[1] += 1
            elif random_direction == 'up':# Move the player up if the random direction is 'up' and the move is valid
                player_pos[0] -= 1
            elif random_direction == 'down':
                player_pos[0] += 1
                
        # Enemy A* movement logic
        path = astar(maze, tuple(enemy_pos), tuple(player_pos)) # Calculate the path from the enemy to the player using A*
        if len(path) > 1:
            enemy_pos[0], enemy_pos[1] = path[1] # Move the enemy to the next step in the path
                
        screen.fill(WHITE)  # Clear the screen with a white background? There have some bugs here...
        for row in range(rows):  # Loop through each row
            for col in range(cols): # Loop through each cols
                if maze[row][col] == 1: # If there's a wall at this position
                    pygame.draw.rect(screen, BLUE, (col * tile_size[0], row * tile_size[1], tile_size[0], tile_size[1]))
                    # Draw a blue rectangle (wall) on the screen at the corresponding position
                    
                    
        pygame.draw.rect(screen, GREEN, (player_pos[1] * tile_size[0], player_pos[0] * tile_size[1], tile_size[0], tile_size[1]))  # green means player
        pygame.draw.rect(screen, RED, (enemy_pos[1] * tile_size[0], enemy_pos[0] * tile_size[1], tile_size[0], tile_size[1]))  # red means enemy
        pygame.display.flip() # Update the full display surface to the screen
        clock.tick(5) # Limit the game to 5 frames per second (fps)
        
    pygame.quit()

if __name__ == "__main__":
    game_loop()
    