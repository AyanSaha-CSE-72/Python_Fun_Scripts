import pygame
import random

pygame.init()

WIDTH, HEIGHT = 480, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Real Car Style Racing")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# লেনের এক্স কোঅর্ডিনেট (৩ লেন)
lanes_x = [80, 200, 320]

# প্লেয়ার গাড়ি settings
car_width, car_height = 60, 120
player_lane = 1  # মাঝের লেন
player_y = HEIGHT - car_height - 20
player_speed = 10

# বাধা গাড়ি settings
obs_width, obs_height = 60, 120
obs_speed = 5
obstacles = []

# স্টার (স্কোর আইটেম)
star_radius = 10
stars = []

score = 0
level = 1

def draw_player():
    x = lanes_x[player_lane]
    pygame.draw.rect(screen, GREEN, (x, player_y, car_width, car_height))

def draw_obstacle(obs):
    pygame.draw.rect(screen, RED, (obs['x'], obs['y'], obs_width, obs_height))

def draw_star(star):
    pygame.draw.circle(screen, YELLOW, (star['x'], star['y']), star_radius)

def create_obstacle():
    lane = random.choice([0,1,2])
    x = lanes_x[lane]
    y = -obs_height
    obstacles.append({'x': x, 'y': y})

def create_star():
    lane = random.choice([0,1,2])
    x = lanes_x[lane] + car_width//2
    y = -star_radius * 2
    stars.append({'x': x, 'y': y})

# শুরুতে কিছু বাধা ও স্টার তৈরি
for _ in range(3):
    create_obstacle()
for _ in range(2):
    create_star()

running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_lane > 0:
        player_lane -= 1
        pygame.time.wait(100)  # লেন পরিবর্তনের মাঝে একটু দেরি
    if keys[pygame.K_RIGHT] and player_lane < 2:
        player_lane += 1
        pygame.time.wait(100)

    # বাধাগুলোর আপডেট
    for obs in obstacles:
        obs['y'] += obs_speed
    obstacles = [o for o in obstacles if o['y'] < HEIGHT + obs_height]

    # স্টার আপডেট
    for star in stars:
        star['y'] += obs_speed
    stars = [s for s in stars if s['y'] < HEIGHT + star_radius]

    # নতুন বাধা ও স্টার যোগ করা
    if len(obstacles) < 5:
        create_obstacle()
    if len(stars) < 3:
        create_star()

    # গাড়ি ও বাধা আঁকা
    draw_player()
    for obs in obstacles:
        draw_obstacle(obs)
    for star in stars:
        draw_star(star)

    # সংঘর্ষ চেক (বাধার সাথে)
    player_rect = pygame.Rect(lanes_x[player_lane], player_y, car_width, car_height)
    for obs in obstacles:
        obs_rect = pygame.Rect(obs['x'], obs['y'], obs_width, obs_height)
        if player_rect.colliderect(obs_rect):
            print("Game Over! Your Score:", score)
            running = False

    # স্টার কালেক্ট করা চেক
    for star in stars[:]:
        star_rect = pygame.Rect(star['x'] - star_radius, star['y'] - star_radius, star_radius*2, star_radius*2)
        if player_rect.colliderect(star_rect):
            score += 1
            stars.remove(star)
            # লেভেল বাড়ানো
            if score % 5 == 0:
                level += 1
                obs_speed += 1

    # স্কোর এবং লেভেল দেখানো
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
