import os
import random

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


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)


class Ship:
    COOLDOWN = 20

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.laser_image = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        if self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_image)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_image = MAIN_SPACE_SHIP
        self.laser_image = LASER
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health

    def draw(self, window):
        super().draw(window)


class EnemyShip(Ship):
    NUM_MONSTERS = {
        "1": (SPACE_SHIP_1, LASER),
        "2": (SPACE_SHIP_2, LASER),
        "3": (SPACE_SHIP_3, LASER)
    }

    def __init__(self, x, y, num_monstr, health=100):
        super().__init__(x, y, health)
        self.ship_image, self.laser_image = self.NUM_MONSTERS[num_monstr]
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.rect = self.ship_image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def check_edges(self):
        screen_rect = WIN.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def move(self, vel, alien_speed_factor, fleet_direction):
        self.y += vel
        self.x += (alien_speed_factor * fleet_direction)
        self.rect.x = self.x

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_image)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def main():
    run = True
    FPS = 60
    player_vel = 10
    laser_vel = 10
    level = 0

    enemies = []
    wave_length = 10
    enemy_vel = 3
    alien_speed_factor = 4
    fleet_direction = 1

    player = Player(570, 500)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = EnemyShip(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                                  random.choice(["1", "2", "3"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 10 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies:
            enemy.move(enemy_vel, alien_speed_factor, fleet_direction)
            enemy.move_lasers(laser_vel)
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()
            if enemy.check_edges():
                fleet_direction *= -1
                break

        player.move_lasers(-laser_vel)


main()
