import pygame
import random
import sys
from pygame.locals import *
pygame.init()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

font = pygame.font.Font(None, 36)
text = font.render('The player has encountered an enemy! Game over', True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.center = (width // 2, height // 2)



class Square(pygame.sprite.Sprite):
    def __init__(self, size, color):
        super(Square, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.rect = self.surf.get_rect()

class Player(Square):
    def __init__(self):
        super(Player, self).__init__((25, 25), (0, 255, 0))
        
class Enemy(Square):
    def __init__(self):
        super(Enemy, self).__init__((25, 25), (255, 0, 0))

def handle_player_enemy_collision():
    screen.fill((255, 255, 255))  # clear
    text_rect.center = (width // 2, height // 2)  # Set the center point of the text rectangle
    screen.blit(text, text_rect) 
    pygame.display.flip()  
    start_time = pygame.time.get_ticks()
    delay = 3000  # 3 seconds delay
        
    while True:
        current_time = pygame.time.get_ticks()
        if current_time - start_time > delay:
            break
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                    
pygame.init()

screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)

tile_size = (80, 60)
rows, cols = 10, 10

num_obstacles = 20
obstacles = pygame.sprite.Group()

for _ in range(num_obstacles):
    row_idx = random.randint(0, rows - 1)
    col_idx = random.randint(0, cols - 1)
    obstacle = Square(tile_size, (0, 0, 0))
    obstacle.rect.x = col_idx * tile_size[0]
    obstacle.rect.y = row_idx * tile_size[1]
    obstacles.add(obstacle)

corner_square_size = (25, 25)
corner_square_color = (0, 200, 255)
square1 = Square(corner_square_size, corner_square_color)
square2 = Square(corner_square_size, corner_square_color)
square3 = Square(corner_square_size, corner_square_color)
square4 = Square(corner_square_size, corner_square_color)

player = Player()
enemy = Enemy()
# Choose an initial position for the player that is free of obstacles
while True:
    player.rect.x = random.randint(0, cols - 1) * tile_size[0]
    player.rect.y = random.randint(0, rows - 1) * tile_size[1]
    if not pygame.sprite.spritecollideany(player, obstacles):
        break
    
# Choose an initial position for the enemy that is free of obstacles
while True:
    enemy.rect.x = random.randint(0, cols - 1) * tile_size[0]
    enemy.rect.y = random.randint(0, rows - 1) * tile_size[1]
    if not pygame.sprite.spritecollideany(enemy, obstacles) and (enemy.rect.x, enemy.rect.y) != (player.rect.x, player.rect.y):
        break
        

gameOn = True
clock = pygame.time.Clock()

# Main loop
while gameOn:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                gameOn = False
        elif event.type == QUIT:
            gameOn = False
        if pygame.sprite.collide_rect(player, enemy):
            handle_player_enemy_collision()

    # Player Move
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
            player.rect.move_ip(-1, 0)
    if pygame.sprite.spritecollideany(player, obstacles):
                player.rect.move_ip(1, 0)
    if keys[K_RIGHT]:
            player.rect.move_ip(1, 0)
    if pygame.sprite.spritecollideany(player, obstacles):
                player.rect.move_ip(-1, 0)
    if keys[K_UP]:
            player.rect.move_ip(0, -1)
    if pygame.sprite.spritecollideany(player, obstacles):
                player.rect.move_ip(0, 1)
    if keys[K_DOWN]:
            player.rect.move_ip(0, 1)
    if pygame.sprite.spritecollideany(player, obstacles):
                player.rect.move_ip(0, -1)

            
    # Make sure the player cannot move off screen
    if player.rect.top < 0:
        player.rect.top = 0
    if player.rect.bottom > screen_size[1]:
        player.rect.bottom = screen_size[1]
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > screen_size[0]:
        player.rect.right = screen_size[0]
        
    # clear
    screen.fill((255, 255, 255))
    
    for obstacle in obstacles:
        screen.blit(obstacle.surf, obstacle.rect)

    screen.blit(square1.surf, (40, 40))
    screen.blit(square2.surf, (40, 530))
    screen.blit(square3.surf, (730, 40))
    screen.blit(square4.surf, (730, 530))
    
    screen.blit(enemy.surf, enemy.rect)
    screen.blit(player.surf, player.rect)


    pygame.display.flip()
    clock.tick(120)

pygame.quit()
        