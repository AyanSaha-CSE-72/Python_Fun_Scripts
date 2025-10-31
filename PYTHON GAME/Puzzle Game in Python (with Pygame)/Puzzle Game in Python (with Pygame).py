import pygame
import sys
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("background.mp3")  # your music file here
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 400, 400
TILE_SIZE = WIDTH // 4
FONT_SIZE = 40
BACKGROUND_COLOR = (30, 30, 30)
TILE_COLOR = (70, 130, 180)
EMPTY_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("15 Puzzle Game")
font = pygame.font.SysFont(None, FONT_SIZE)

def create_solved_board():
    board = list(range(1, 16))
    board.append(0)
    return board

def shuffle_board(board, moves=1000):
    empty_pos = board.index(0)
    for _ in range(moves):
        neighbors = get_neighbors(empty_pos)
        swap_pos = random.choice(neighbors)
        board[empty_pos], board[swap_pos] = board[swap_pos], board[empty_pos]
        empty_pos = swap_pos
    return board

def get_neighbors(pos):
    neighbors = []
    row, col = divmod(pos, 4)
    if row > 0:
        neighbors.append(pos - 4)
    if row < 3:
        neighbors.append(pos + 4)
    if col > 0:
        neighbors.append(pos - 1)
    if col < 3:
        neighbors.append(pos + 1)
    return neighbors

def draw_board(board):
    screen.fill(BACKGROUND_COLOR)
    for i, tile in enumerate(board):
        row, col = divmod(i, 4)
        x = col * TILE_SIZE
        y = row * TILE_SIZE
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        if tile == 0:
            pygame.draw.rect(screen, EMPTY_COLOR, rect)
        else:
            pygame.draw.rect(screen, TILE_COLOR, rect)
            text = font.render(str(tile), True, TEXT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        pygame.draw.rect(screen, BACKGROUND_COLOR, rect, 3)

def is_solved(board):
    return board == create_solved_board()

def move_tile(board, tile_pos):
    empty_pos = board.index(0)
    if tile_pos in get_neighbors(empty_pos):
        board[empty_pos], board[tile_pos] = board[tile_pos], board[empty_pos]
        return True
    return False

def main():
    board = create_solved_board()
    board = shuffle_board(board)
    running = True

    while running:
        draw_board(board)
        if is_solved(board):
            pygame.display.set_caption("You solved the puzzle! Press ESC to quit.")
        else:
            pygame.display.set_caption("15 Puzzle Game")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                col = mx // TILE_SIZE
                row = my // TILE_SIZE
                tile_pos = row * 4 + col
                move_tile(board, tile_pos)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
