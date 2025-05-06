import os
import random

import pygame

pygame.font.init()

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

    def collisions(self, obj):
        return collide(self, obj)


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

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collisions(obj):
                obj.health -= 10
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
        self.healthbar(window)

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collisions(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_image.get_height() + 10, self.ship_image.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0),
                         (self.x, self.y + self.ship_image.get_height() + 10,
                          self.ship_image.get_width() * (self.health / self.max_health), 10))


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


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    player_vel = 10
    laser_vel = 10
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 40)
    lost_font = pygame.font.SysFont("comicsans", 60)

    list_lost_labels = ["It's not your day", "You could be better", "Next time you must do it"]
    random_ch = random.choice(list_lost_labels)

    enemies = []
    wave_length = 10
    enemy_vel = 3
    alien_speed_factor = 2
    fleet_direction = 1

    lost = False
    lost_count = 0

    player = Player(570, 500)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))

        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render(f"{random_ch}", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 250))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 4:
                run = False
            else:
                continue

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
            enemy.move_lasers(laser_vel, player)
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()
            if enemy.check_edges():
                fleet_direction *= -1
                break

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 40)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()
