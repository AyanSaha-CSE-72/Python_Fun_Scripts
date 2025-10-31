import pygame
import sys
import os
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()

# 🎵 Load background music & sounds
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)
coin_sound = pygame.mixer.Sound("coin.wav")
death_sound = pygame.mixer.Sound("death.wav")

# 📦 High score file
SCORE_FILE = "highscore.txt"
if not os.path.exists(SCORE_FILE):
    with open(SCORE_FILE, "w") as f:
        f.write("0")

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Player
player = pygame.Rect(100, 450, 50, 50)
velocity_y = 0
gravity = 1
jump_power = -15
on_ground = True

# Platforms
platforms = [
    pygame.Rect(0, 550, 800, 50),
    pygame.Rect(300, 450, 200, 20),
    pygame.Rect(550, 350, 150, 20),
    pygame.Rect(100, 250, 150, 20),
]

# Coins
coins = [pygame.Rect(random.randint(100, 700), random.randint(100, 500), 20, 20) for _ in range(5)]

# Enemies
enemies = [pygame.Rect(600, 510, 40, 40)]

# Score
score = 0
level = 1

def draw_text(text, size, x, y, color=(0,0,0)):
    font = pygame.font.SysFont("arial", size)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Main loop
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_SPACE] and on_ground:
        velocity_y = jump_power
        on_ground = False

    # Gravity
    velocity_y += gravity
    player.y += velocity_y

    # Platform Collision
    on_ground = False
    for plat in platforms:
        if player.colliderect(plat) and velocity_y > 0:
            player.bottom = plat.top
            velocity_y = 0
            on_ground = True

    # Coin Collection
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 10
            coin_sound.play()

    # Enemy Collision
    for enemy in enemies:
        if player.colliderect(enemy):
            death_sound.play()
            draw_text("Game Over!", 50, WIDTH//2 - 100, HEIGHT//2, RED)
            pygame.display.flip()
            pygame.time.wait(2000)

            # Save high score
            with open(SCORE_FILE, "r") as f:
                high = int(f.read())
            if score > high:
                with open(SCORE_FILE, "w") as f:
                    f.write(str(score))

            pygame.quit()
            sys.exit()

    # Draw
    pygame.draw.rect(screen, BLUE, player)
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)
    for coin in coins:
        pygame.draw.circle(screen, (255, 223, 0), coin.center, 10)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    draw_text(f"Score: {score}", 30, 10, 10)
    draw_text(f"Level: {level}", 30, 10, 40)

    # Level Up
    if not coins:
        level += 1
        coins = [pygame.Rect(random.randint(100, 700), random.randint(100, 500), 20, 20) for _ in range(5)]
        enemies.append(pygame.Rect(random.randint(100, 700), 510, 40, 40))

    pygame.display.flip()
    clock.tick(60)
