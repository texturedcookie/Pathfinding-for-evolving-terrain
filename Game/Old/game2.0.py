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
player_pos = [1, 1]
enemy_pos = [rows - 2, cols - 2]

# colordef
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# A* algorithm
def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def astar(maze, start, goal):
    closed_set = set()
    open_set = [(0, start)]
    came_from = {}
    g_score = {tuple(position): float('inf') for position in np.ndindex(maze.shape)}
    g_score[start] = 0
    f_score = {tuple(position): float('inf') for position in np.ndindex(maze.shape)}
    f_score[start] = heuristic(start, goal)
    
    while open_set:
        current_f_score, current = heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, current)
        
        closed_set.add(current)
        
        for neighbor in [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
                         (current[0], current[1] - 1), (current[0], current[1] + 1)]:
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]):
                if maze[neighbor[0]][neighbor[1]] == 1 or neighbor in closed_set:
                    continue
                
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    if neighbor not in open_set:
                        heappush(open_set, (f_score[neighbor], neighbor))
                        
    return []

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]

# Maze generation function
def generate_maze(rows, cols):
    maze = np.ones((rows, cols), dtype=int)
    def is_valid_cell(row, col, visited):
        return 0 <= row < rows and 0 <= col < cols and not visited[row, col]
    
    def dfs(row, col, visited):
        visited[row, col] = True
        maze[row, col] = 0
        movements = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(movements)
        for dr, dc in movements:
            new_row, new_col = row + dr * 2, col + dc * 2
            if is_valid_cell(new_row, new_col, visited):
                maze[row + dr, col + dc] = 0
                dfs(new_row, new_col, visited)
                
    visited = np.zeros((rows, cols), dtype=bool)
    dfs(1, 1, visited)
    maze[0, 1] = 0
    maze[-1, cols - 2] = 0
    return maze

# Game main loop
def game_loop():
    maze = generate_maze(rows, cols)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[1] > 0 and maze[player_pos[0]][player_pos[1] - 1] == 0:
            player_pos[1] -= 1
        if keys[pygame.K_RIGHT] and player_pos[1] < cols - 1 and maze[player_pos[0]][player_pos[1] + 1] == 0:
            player_pos[1] += 1
        if keys[pygame.K_UP] and player_pos[0] > 0 and maze[player_pos[0] - 1][player_pos[1]] == 0:
            player_pos[0] -= 1
        if keys[pygame.K_DOWN] and player_pos[0] < rows - 1 and maze[player_pos[0] + 1][player_pos[1]] == 0:
            player_pos[0] += 1
        
        # Enemy A* movement logic
        path = astar(maze, tuple(enemy_pos), tuple(player_pos))
        if len(path) > 1:
            enemy_pos[0], enemy_pos[1] = path[1]
        
        screen.fill(WHITE)
        for row in range(rows):
            for col in range(cols):
                if maze[row][col] == 1:
                    pygame.draw.rect(screen, BLUE, (col * tile_size[0], row * tile_size[1], tile_size[0], tile_size[1]))
        pygame.draw.rect(screen, RED, (player_pos[1] * tile_size[0], player_pos[0] * tile_size[1], tile_size[0], tile_size[1]))
        pygame.draw.rect(screen, GREEN, (enemy_pos[1] * tile_size[0], enemy_pos[0] * tile_size[1], tile_size[0], tile_size[1]))
        pygame.display.flip()
        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
