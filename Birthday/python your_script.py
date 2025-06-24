import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Test Image")

try:
    img = pygame.image.load("cake.png")
except pygame.error as e:
    print(f"Cannot load image: {e}")
    pygame.quit()
    exit()

img = pygame.transform.scale(img, (400, 300))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    screen.blit(img, (0, 0))
    pygame.display.flip()

pygame.quit()
