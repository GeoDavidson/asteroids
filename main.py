import math
import os
import sys
import random
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


class Player():
    def __init__(self, colour, speed, rotation_speed, pos_x, pos_y):
        self.colour = colour
        self.speed = speed
        self.rotation_speed = rotation_speed
        self.angle = 0
        self.velocity = pygame.Vector2(0, 0)
        self.center = pygame.Vector2(pos_x, pos_y)
        self.actual_pos = [
            pygame.Vector2(self.center.x, self.center.y + 32),
            pygame.Vector2(self.center.x + 16, self.center.y - 24),
            pygame.Vector2(self.center.x - 16, self.center.y - 24)
            ]
        self.triangle_pos = [self.actual_pos[0], self.actual_pos[1], self.actual_pos[2]]

    def update(self, delta_time):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.angle += self.rotation_speed * delta_time
        elif key[pygame.K_d]:
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

        self.triangle_pos = [(rotated_x1, rotated_y1), (rotated_x2, rotated_y2), (rotated_x3, rotated_y3)]

        if pygame.key.get_pressed()[pygame.K_w]:
                self.velocity.x += self.speed * math.sin(math.radians(-self.angle)) * delta_time
                self.velocity.y += self.speed * math.cos(math.radians(self.angle)) * delta_time

        self.center.x += self.velocity.x
        self.center.y += self.velocity.y

        if self.center.x < -32:
            self.center.x = window.get_width() + 32
        elif self.center.x > window.get_width() + 32:
            self.center.x = -32

        if self.center.y < -32:
            self.center.y = window.get_height() + 32
        elif self.center.y > window.get_height() + 32:
            self.center.y = -32

        self.actual_pos = [
            pygame.Vector2(self.center.x, self.center.y + 32),
            pygame.Vector2(self.center.x + 16, self.center.y - 24),
            pygame.Vector2(self.center.x - 16, self.center.y - 24)
            ]

    def draw(self):
        pygame.draw.polygon(window, self.colour, self.triangle_pos, 4)


class Asteroid():
    def __init__(self, colour, radius, vel_x, vel_y, pos_x, pos_y):
        self.colour = colour
        self.radius = radius
        self.center = pygame.Vector2(pos_x, pos_y)
        self.velocity = pygame.Vector2(vel_x, vel_y)
    
    def update(self, delta_time):
        self.center.x += self.velocity.x * delta_time
        self.center.y += self.velocity.y * delta_time

        if self.center.x < -self.radius:
            self.center.x = window.get_width() + self.radius
        elif self.center.x > window.get_width() + self.radius:
            self.center.x = -self.radius
        
        if self.center.y < -self.radius:
            self.center.y = window.get_height() + self.radius
        elif self.center.y > window.get_height() + self.radius:
            self.center.y = -self.radius

        for player in player_group:
            for i in range(3):
                distance = math.sqrt((player.triangle_pos[i][0] - self.center.x) ** 2 + (player.triangle_pos[i][1] - self.center.y) ** 2)
                if distance <= self.radius:
                    player_group.pop()

    def draw(self):
        pygame.draw.circle(window, self.colour, self.center, self.radius, 4)

def main():
    previous_time = time.time()

    player = Player((0, 200, 255), 0.2, 225, window.get_width() / 2 - 24, window.get_height() / 2 - 24)
    player_group.append(player)

    for i in range(3):
        asteroid = Asteroid((255, 0, 0), random.randint(25, 50), random.randint(-100, 100), random.randint(-100, 100), window.get_width() / 4, window.get_height() / 2)
        asteroid_group.append(asteroid)

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

        # draw
        for player in player_group:
            player.draw()

        for asteroid in asteroid_group:
            asteroid.draw()

        pygame.display.update()


if __name__ == "__main__":
    main()
