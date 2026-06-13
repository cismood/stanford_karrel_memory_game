import pygame
import random
from card import draw_croatia_tile
from settings import *
from assets import load_player_images

# INIT
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

font = pygame.font.SysFont(None, FONT_SIZE)

# UĆITAJ SLIKE
PLAYER_IMAGES = load_player_images()

CARD_VALUES = list(range(len(PLAYER_IMAGES))) * 2
random.shuffle(CARD_VALUES)

# ZAPAMTI STANJA KARTICA AKO JE KARTICA POGOĐENA
revealed = [False] * NUM_CARDS
matched = [False] * NUM_CARDS

first_pick = None
second_pick = None
waiting = False
wait_start = 0

# HUD / STANJE IGRE
moves = 0
score = 0
start_time = None
game_won = False
last_clicked = None

# ANIMACIJA
animating = False
anim_index = None
anim_progress = 0
anim_reveal = False


#  IDEXI 
def get_xy(index):
    row = index // COLS
    col = index % COLS

    x = col * (CARD_SIZE + GAP) + GAP
    y = row * (CARD_SIZE + GAP) + GAP + HEADER_HEIGHT
    return x, y


def get_index_from_mouse(pos):
    x, y = pos

    if y < HEADER_HEIGHT:
        return None

    row = (y - HEADER_HEIGHT) // (CARD_SIZE + GAP)
    col = x // (CARD_SIZE + GAP)

    if col >= COLS or row >= ROWS:
        return None

    return row * COLS + col


def get_time():
    if start_time is None:
        return 0
    return (pygame.time.get_ticks() - start_time) // 1000


def reset_game():
    global revealed, matched, first_pick, second_pick
    global waiting, moves, score, start_time, game_won, last_clicked
    global CARD_VALUES

    revealed = [False] * NUM_CARDS
    matched = [False] * NUM_CARDS

    first_pick = None
    second_pick = None
    waiting = False

    moves = 0
    score = 0
    start_time = None
    game_won = False
    last_clicked = None

    random.shuffle(CARD_VALUES)


#  HEADER - za vrijeme i scoring, da bude iznad kockica
def draw_header():
    pygame.draw.rect(screen, (20, 20, 20), (0, 0, WIDTH, HEADER_HEIGHT))

    hud_text = f"Time: {get_time()}s | Moves: {moves} | Score: {score}/{len(PLAYER_IMAGES)}"
    text = font.render(hud_text, True, (255, 255, 255))
    screen.blit(text, (20, HEADER_HEIGHT // 2 - 10))


# CRTANJE PLOČE  
def draw_board(scale_override=None):
    screen.fill(BG_COLOR)
    draw_header()

    for index in range(NUM_CARDS):
        draw_card(index, scale_override)

    pygame.display.flip()


def draw_card(index, scale_override=None):
    x, y = get_xy(index)

    scale = 1
    if scale_override and index == scale_override[0]:
        scale = scale_override[1]

    scaled_w = max(2, int(CARD_SIZE * scale))
    offset_x = (CARD_SIZE - scaled_w) // 2

    rect = pygame.Rect(x + offset_x, y, scaled_w, CARD_SIZE)

    if index == last_clicked:
        pygame.draw.rect(screen, (255, 215, 0), rect, 3)

    if revealed[index] or matched[index]:
        pygame.draw.rect(screen, (255, 255, 255), rect)

        if scale > 0.5:
            value = CARD_VALUES[index]
            img = PLAYER_IMAGES[value]
            img_rect = img.get_rect(center=(x + CARD_SIZE // 2, y + CARD_SIZE // 2))
            screen.blit(img, img_rect)

    else:
        draw_croatia_tile(screen, rect)


#  ANIMACIJA 
def update_animation():
    global animating, anim_progress, anim_index, anim_reveal, revealed

    if not animating:
        return

    anim_progress += FLIP_SPEED

    if anim_progress <= 0.5:
        scale = 1 - (anim_progress * 2)
    else:
        scale = (anim_progress - 0.5) * 2

    if anim_progress >= 0.5 and not anim_reveal:
        revealed[anim_index] = True
        anim_reveal = True

    draw_board(scale_override=(anim_index, scale))

    if anim_progress >= 1:
        animating = False
        anim_progress = 0


def start_animation(index):
    global animating, anim_index, anim_progress, anim_reveal

    animating = True
    anim_index = index
    anim_progress = 0
    anim_reveal = False


#  MAIN 
def main():
    global first_pick, second_pick, waiting, wait_start
    global moves, score, start_time, game_won, last_clicked

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        update_animation()

        # EVENTI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if waiting or animating or game_won:
                    continue

                index = get_index_from_mouse(event.pos)

                if index is None:
                    continue

                if revealed[index] or matched[index]:
                    continue

                last_clicked = index

                # STARTAJ (SAMO JEDNOM)
                if start_time is None:
                    start_time = pygame.time.get_ticks()

                start_animation(index)

                if first_pick is None:
                    first_pick = index
                else:
                    second_pick = index
                    waiting = True
                    wait_start = pygame.time.get_ticks()
                    moves += 1

        # PROVJERA KARTICE - Ako je ista zadrži ju otvorenom!
        if waiting:
            if pygame.time.get_ticks() - wait_start > 700:

                if CARD_VALUES[first_pick] == CARD_VALUES[second_pick]:
                    matched[first_pick] = True
                    matched[second_pick] = True
                    score += 1
                else:
                    revealed[first_pick] = False
                    revealed[second_pick] = False

                first_pick = None
                second_pick = None
                waiting = False

        # Ako je igra završena, završi igru
        if score == len(PLAYER_IMAGES):
            game_won = True

        draw_board()

        # ANIMACIJA - POBJEDNIČKI EKRAN 
        if game_won:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            text = pygame.font.SysFont(None, 60).render(
                "🇭🇷 Vatreni Memory Champion 🇭🇷",
                True,
                (255, 255, 255)
            )

            screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()