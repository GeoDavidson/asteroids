import math
import os
import random
import sys
import time

import pygame

pygame.init()

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroids")
pygame.display.set_icon(pygame.image.load(os.path.join("icon", "icon.png")).convert_alpha())

player_group = []
asteroid_group = []
bullet_group = []


class Player():
    def __init__(self, colour, speed, rotation_speed, pos_x, pos_y):
        self.colour = colour
        self.speed = speed
        self.rotation_speed = rotation_speed
        self.center = pygame.Vector2(pos_x, pos_y)
        self.velocity = pygame.Vector2(0, 0)
        self.actual_pos = [
            pygame.Vector2(self.center.x, self.center.y + 32),
            pygame.Vector2(self.center.x + 16, self.center.y - 24),
            pygame.Vector2(self.center.x - 16, self.center.y - 24)
        ]
        self.rotated_pos = [self.actual_pos[0], self.actual_pos[1], self.actual_pos[2]]
        self.angle = 0
        self.shot = False

    def __rotation(self, delta_time):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.angle += self.rotation_speed * delta_time
        elif key[pygame.K_LEFT]:
            self.angle -= self.rotation_speed * delta_time

        center_x, center_y = self.center.xy
        current_x, current_y = self.actual_pos[0].xy
        rotated_x1 = (current_x - center_x) * math.cos(math.radians(self.angle)) - (current_y - center_y) * math.sin(math.radians(self.angle)) + center_x
        rotated_y1 = (current_x - center_x) * math.sin(math.radians(self.angle)) + (current_y - center_y) * math.cos(math.radians(self.angle)) + center_y
        current_x, current_y = self.actual_pos[1].xy
        rotated_x2 = (current_x - center_x) * math.cos(math.radians(self.angle)) - (current_y - center_y) * math.sin(math.radians(self.angle)) + center_x
        rotated_y2 = (current_x - center_x) * math.sin(math.radians(self.angle)) + (current_y - center_y) * math.cos(math.radians(self.angle)) + center_y
        current_x, current_y = self.actual_pos[2].xy
        rotated_x3 = (current_x - center_x) * math.cos(math.radians(self.angle)) - (current_y - center_y) * math.sin(math.radians(self.angle)) + center_x
        rotated_y3 = (current_x - center_x) * math.sin(math.radians(self.angle)) + (current_y - center_y) * math.cos(math.radians(self.angle)) + center_y

        self.rotated_pos = [(rotated_x1, rotated_y1), (rotated_x2, rotated_y2), (rotated_x3, rotated_y3)]

    def __movement(self, delta_time):
        if pygame.key.get_pressed()[pygame.K_UP]:
            if abs(self.velocity.x) < 0.25:
                self.velocity.x += self.speed * math.sin(math.radians(-self.angle)) * delta_time
            else:
                self.velocity.x -= math.sin(math.radians(-self.angle)) * delta_time
            if abs(self.velocity.y) < 0.25:
                self.velocity.y += self.speed * math.cos(math.radians(self.angle)) * delta_time
            else:
                self.velocity.y -= math.cos(math.radians(self.angle)) * delta_time

        self.center.x += self.velocity.x
        self.center.y += self.velocity.y

        self.actual_pos = [
            pygame.Vector2(self.center.x, self.center.y + 32),
            pygame.Vector2(self.center.x + 16, self.center.y - 24),
            pygame.Vector2(self.center.x - 16, self.center.y - 24)
        ]

    def __collision(self):
        if self.center.x < -32:
            self.center.x = window.get_width() + 32
        elif self.center.x > window.get_width() + 32:
            self.center.x = -32

        if self.center.y < -32:
            self.center.y = window.get_height() + 32
        elif self.center.y > window.get_height() + 32:
            self.center.y = -32

    def __shoot(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if not self.shot:
                bullet_group.append(Bullet((0, 140, 0), 4, 0.8, 490, self.rotated_pos[0][0], self.rotated_pos[0][1], math.radians(self.angle)))
                self.shot = True
        else:
            self.shot = False

    def update(self, delta_time):
        self.__rotation(delta_time)
        self.__movement(delta_time)
        self.__collision()
        self.__shoot()

    def draw(self):
        pygame.draw.polygon(window, self.colour, self.rotated_pos, 4)


class Asteroid():
    def __init__(self, colour, stage, vel_x, vel_y, pos_x, pos_y):
        self.colour = colour
        self.stage = stage
        self.radius = self.stage * 20
        self.center = pygame.Vector2(pos_x, pos_y)
        self.velocity = pygame.Vector2(vel_x, vel_y)

    def __movement(self, delta_time):
        self.center.x += self.velocity.x * delta_time
        self.center.y += self.velocity.y * delta_time

    def __collision(self):
        if self.center.x < -self.radius:
            self.center.x = window.get_width() + self.radius
        elif self.center.x > window.get_width() + self.radius:
            self.center.x = -self.radius

        if self.center.y < -self.radius:
            self.center.y = window.get_height() + self.radius
        elif self.center.y > window.get_height() + self.radius:
            self.center.y = -self.radius

    def update(self, delta_time):
        self.__movement(delta_time)
        self.__collision()

    def draw(self):
        pygame.draw.circle(window, self.colour, self.center, self.radius, 4)


class Bullet():
    def __init__(self, colour, radius, alive_time, speed, start_x, start_y, angle):
        self.colour = colour
        self.radius = radius
        self.alive_time = alive_time
        self.center = pygame.Vector2(start_x, start_y)
        self.delta_y = math.cos(-angle) * speed
        self.delta_x = math.sin(-angle) * speed

    def __movement(self, delta_time):
        self.center.x += self.delta_x * delta_time
        self.center.y += self.delta_y * delta_time

    def __collision(self):
        if self.center.x < -self.radius:
            self.center.x = window.get_width() + self.radius
        elif self.center.x > window.get_width() + self.radius:
            self.center.x = -self.radius

        if self.center.y < -self.radius:
            self.center.y = window.get_height() + self.radius
        elif self.center.y > window.get_height() + self.radius:
            self.center.y = -self.radius

    def __suicide(self, delta_time):
        self.alive_time -= delta_time
        if self.alive_time <= 0:
            bullet_group.remove(self)

    def update(self, delta_time):
        self.__movement(delta_time)
        self.__collision()
        self.__suicide(delta_time)

    def draw(self):
        pygame.draw.circle(window, self.colour, self.center, self.radius)


def player_asteroid_collision():
    for player in player_group:
        for asteroid in asteroid_group:
            for i in range(3):
                distance = math.sqrt((player.rotated_pos[i][0] - asteroid.center.x) ** 2 + (player.rotated_pos[i][1] - asteroid.center.y) ** 2)
                if distance <= asteroid.radius:
                    player_group.pop()


def bullet_asteroid_collision():
    for bullet in bullet_group:
        for asteroid in asteroid_group:
            distance = math.sqrt((bullet.center.x - asteroid.center.x) ** 2 + (bullet.center.y - asteroid.center.y) ** 2)
            if distance <= asteroid.radius:
                bullet_group.remove(bullet)
                if asteroid.stage == 3:
                    asteroid_group.append(Asteroid((234, 0, 0), 2, asteroid.velocity.x + random.randint(-100, 100), asteroid.velocity.y + random.randint(-100, 100), asteroid.center.x, asteroid.center.y))
                    asteroid_group.append(Asteroid((234, 0, 0), 2, asteroid.velocity.x + random.randint(-100, 100), asteroid.velocity.y + random.randint(-100, 100), asteroid.center.x, asteroid.center.y))
                elif asteroid.stage == 2:
                    asteroid_group.append(Asteroid((234, 0, 0), 1, asteroid.velocity.x + random.randint(-100, 100), asteroid.velocity.y + random.randint(-100, 100), asteroid.center.x, asteroid.center.y))
                    asteroid_group.append(Asteroid((234, 0, 0), 1, asteroid.velocity.x + random.randint(-100, 100), asteroid.velocity.y + random.randint(-100, 100), asteroid.center.x, asteroid.center.y))
                asteroid_group.remove(asteroid)


def main():
    player_group.append(Player((0, 200, 255), 0.2, 225, window.get_width() / 2 - 24, window.get_height() / 2 - 24))

    asteroid_group.append(Asteroid((234, 0, 0), 3, random.randint(-100, 100), random.randint(-100, 100), 0, 0))
    asteroid_group.append(Asteroid((234, 0, 0), 2, random.randint(-100, 100), random.randint(-100, 100), window.get_width(), 0))
    asteroid_group.append(Asteroid((234, 0, 0), 2, random.randint(-100, 100), random.randint(-100, 100), window.get_width(), window.get_height()))
    asteroid_group.append(Asteroid((234, 0, 0), 1, random.randint(-100, 100), random.randint(-100, 100), 0, window.get_height()))

    previous_time = time.time()

    while True:
        delta_time = time.time() - previous_time
        previous_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        window.fill((217, 244, 200))

        # update
        for player in player_group:
            player.update(delta_time)

        for asteroid in asteroid_group:
            asteroid.update(delta_time)

        player_asteroid_collision()

        for bullet in bullet_group:
            bullet.update(delta_time)

        bullet_asteroid_collision()

        # draw
        for player in player_group:
            player.draw()

        for asteroid in asteroid_group:
            asteroid.draw()

        for bullet in bullet_group:
            bullet.draw()

        pygame.display.update()


if __name__ == "__main__":
    main()
