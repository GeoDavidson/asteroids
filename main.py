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
pygame.display.set_icon(pygame.image.load(
    os.path.join("icon", "icon.png")).convert_alpha())


class Player():
    def __init__(self, colour, pos_x, pos_y, width, height):
        self.colour = colour
        # self.actual_pos = pygame.Vector2(pos_x, pos_y)
        # self.screen_pos = pygame.Vector2(self.actual_pos.x, self.actual_pos.y)
        self.velocity = pygame.Vector2(0, 0)
        self.center = pygame.Vector2(pos_x, pos_y)
        self.actual_pos = [
            pygame.Vector2(pos_x, pos_y + 32),
            pygame.Vector2(pos_x + 16, pos_y - 24),
            pygame.Vector2(pos_x - 16, pos_y - 24)
            ]
        self.screen_pos = [
            self.actual_pos[0].xy,
            self.actual_pos[1].xy,
            self.actual_pos[2].xy
            ]
        self.rotation = 0
        self.rotated_triangle = [(0, 0), (0, 0), (0, 0)]

    def update(self, delta_time):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rotation += 150 * delta_time
        elif key[pygame.K_d]:
            self.rotation -= 150 * delta_time

        cx, cy = self.center.xy
        x, y = self.actual_pos[0].xy
        new_x1 = (x - cx) * math.cos(math.radians(self.rotation)) - (y - cy) * math.sin(math.radians(self.rotation)) + cx
        new_y1 = (x - cx) * math.sin(math.radians(self.rotation)) + (y - cy) * math.cos(math.radians(self.rotation)) + cy
        x, y = self.actual_pos[1].xy
        new_x2 = (x - cx) * math.cos(math.radians(self.rotation)) - (y - cy) * math.sin(math.radians(self.rotation)) + cx
        new_y2 = (x - cx) * math.sin(math.radians(self.rotation)) + (y - cy) * math.cos(math.radians(self.rotation)) + cy
        x, y = self.actual_pos[2].xy
        new_x3 = (x - cx) * math.cos(math.radians(self.rotation)) - (y - cy) * math.sin(math.radians(self.rotation)) + cx
        new_y3 = (x - cx) * math.sin(math.radians(self.rotation)) + (y - cy) * math.cos(math.radians(self.rotation)) + cy

        self.rotated_triangle = [(new_x1, new_y1), (new_x2, new_y2), (new_x3, new_y3)]

        if pygame.key.get_pressed()[pygame.K_w]:
                self.velocity.x += 0.2 * math.sin(math.radians(-self.rotation)) * delta_time
                self.velocity.y += 0.2 * math.cos(math.radians(self.rotation)) * delta_time

        self.center.x += self.velocity.x
        self.center.x = self.center.x
        self.center.y += self.velocity.y
        self.center.y = self.center.y
        self.actual_pos[0].x += self.velocity.x
        self.screen_pos[0].x = self.actual_pos[0].x
        self.actual_pos[0].y += self.velocity.y
        self.screen_pos[0].y = self.actual_pos[0].y
        self.actual_pos[1].x += self.velocity.x
        self.screen_pos[1].x = self.actual_pos[1].x
        self.actual_pos[1].y += self.velocity.y
        self.screen_pos[1].y = self.actual_pos[1].y
        self.actual_pos[2].x += self.velocity.x
        self.screen_pos[2].x = self.actual_pos[2].x
        self.actual_pos[2].y += self.velocity.y
        self.screen_pos[2].y = self.actual_pos[2].y

    def draw(self):
        pygame.draw.polygon(window, (255, 0, 0), self.rotated_triangle)


def main():
    previous_time = time.time()

    player = Player((255, 0, 0), window.get_width() / 2 -
                    24, window.get_height() / 2 - 24, 48, 48)

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
