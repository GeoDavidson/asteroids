import math
import os
import sys
import time

import pygame

pygame.init()

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroids")
pygame.display.set_icon(pygame.image.load(os.path.join("icon", "icon.png")).convert_alpha())


class Player():
    def __init__(self, colour, pos_x, pos_y):
        self.colour = colour
        self.angle = 0
        self.velocity = pygame.Vector2(0, 0)
        self.center = pygame.Vector2(pos_x, pos_y)
        self.actual_pos = [
            pygame.Vector2(self.center.x, self.center.y + 32),
            pygame.Vector2(self.center.x + 16, self.center.y - 24),
            pygame.Vector2(self.center.x - 16, self.center.y - 24)
            ]

    def update(self, delta_time):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.angle += 225 * delta_time
        elif key[pygame.K_d]:
            self.angle -= 225 * delta_time

        cx, cy = self.center.xy
        x, y = self.actual_pos[0].xy
        x1 = (x - cx) * math.cos(math.radians(self.angle)) - (y - cy) * math.sin(math.radians(self.angle)) + cx
        y1 = (x - cx) * math.sin(math.radians(self.angle)) + (y - cy) * math.cos(math.radians(self.angle)) + cy
        x, y = self.actual_pos[1].xy
        x2 = (x - cx) * math.cos(math.radians(self.angle)) - (y - cy) * math.sin(math.radians(self.angle)) + cx
        y2 = (x - cx) * math.sin(math.radians(self.angle)) + (y - cy) * math.cos(math.radians(self.angle)) + cy
        x, y = self.actual_pos[2].xy
        x3 = (x - cx) * math.cos(math.radians(self.angle)) - (y - cy) * math.sin(math.radians(self.angle)) + cx
        y3 = (x - cx) * math.sin(math.radians(self.angle)) + (y - cy) * math.cos(math.radians(self.angle)) + cy

        self.triangle = [(x1, y1), (x2, y2), (x3, y3)]

        if pygame.key.get_pressed()[pygame.K_w]:
                self.velocity.x += 0.2 * math.sin(math.radians(-self.angle)) * delta_time
                self.velocity.y += 0.2 * math.cos(math.radians(self.angle)) * delta_time

        self.center.x += self.velocity.x
        self.center.y += self.velocity.y

        self.actual_pos = [
            pygame.Vector2(self.center.x, self.center.y + 32),
            pygame.Vector2(self.center.x + 16, self.center.y - 24),
            pygame.Vector2(self.center.x - 16, self.center.y - 24)
            ]

    def draw(self):
        pygame.draw.polygon(window, (255, 0, 0), self.triangle)


def main():
    previous_time = time.time()

    player = Player((255, 0, 0), window.get_width() / 2 - 24, window.get_height() / 2 - 24)

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

        player.update(delta_time)

        player.draw()

        pygame.display.update()


if __name__ == "__main__":
    main()
