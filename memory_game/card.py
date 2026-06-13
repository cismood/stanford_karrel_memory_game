import pygame

RED = (220, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_croatia_tile(screen, rect):
    pygame.draw.rect(screen, BLACK, rect, 2)

    rows = 4
    cols = 4

    square_w = rect.width // cols
    square_h = rect.height // rows

    for row in range(rows):
        for col in range(cols):
            color = RED if (row + col) % 2 == 0 else WHITE

            pygame.draw.rect(
                screen,
                color,
                (
                    rect.x + col * square_w,
                    rect.y + row * square_h,
                    square_w,
                    square_h
                )
            )