import os

import pygame

WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

SPACE_SHIP_1 = pygame.image.load(os.path.join("images", "1_monstr.png"))
SPACE_SHIP_2 = pygame.image.load(os.path.join("images", "2_monstr.png"))
SPACE_SHIP_3 = pygame.image.load(os.path.join("images", "3_monstr.png"))

MAIN_SPACE_SHIP = pygame.image.load(os.path.join("images", "airplane.jpg"))

LASER = pygame.image.load(os.path.join("images", "pixel_laser_green.png"))

BG = pygame.image.load(os.path.join("images", "backgr.jpg"))


def main():
    run = True
    FPS = 60

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

main()