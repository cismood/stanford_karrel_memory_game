import pygame

def load_image(path, size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

def load_player_images(): # relative path
    return [
        load_image("assets/images/Modric.png", (80, 80)),
        load_image("assets/images/KovacicMateo.png", (80, 80)),
        load_image("assets/images/Perisic.png", (80, 80)),
        load_image("assets/images/PetarSucic.png", (80, 80)),
        load_image("assets/images/GvardiolJosko.png", (80, 80)),
        load_image("assets/images/MartinBaturina.png", (80, 80)),
        load_image("assets/images/Kramaric.png", (80, 80)),
        load_image("assets/images/JosipStanisic.png", (80, 80)),
        load_image("assets/images/MarinErlic.png", (80, 80)),
        load_image("assets/images/Kotarski.png", (80, 80)),
        load_image("assets/images/MarinPongracic.png", (80, 80)),
        load_image("assets/images/SucicLuka.png", (80, 80)),
        load_image("assets/images/JosipSutalo.png", (80, 80)),
        load_image("assets/images/ToniFruk.png", (80, 80)),
        load_image("assets/images/KristianJakic.png", (80, 80)),
        load_image("assets/images/PasalicMario.png", (80, 80)),
        load_image("assets/images/VlasicNikola.png", (80, 80)),
        load_image("assets/images/AnteBudimir.png", (80, 80)),
    ]