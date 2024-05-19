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
    def __init__(self, colour, pos_x, pos_y, width, height):
        self.colour = colour
        self.rect_pos = pygame.Vector2(pos_x, pos_y)
        self.rect = pygame.Rect(self.rect_pos.x, self.rect_pos.y, width, height)
        self.rect_vel = pygame.Vector2(0, 0)
    
    def update(self, delta_time):
        if pygame.key.get_pressed()[pygame.K_w]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            delta_x = mouse_x - self.rect_pos.x
            delta_y = mouse_y - self.rect_pos.y
            angle = math.atan2(delta_x, delta_y)
            self.rect_vel.x += 0.2 * math.sin(angle) * delta_time
            self.rect_vel.y += 0.2 * math.cos(angle) * delta_time

        self.rect_pos.x += self.rect_vel.x
        self.rect.x = self.rect_pos.x

        self.rect_pos.y += self.rect_vel.y
        self.rect.y = self.rect_pos.y

    def draw(self):
        pygame.draw.rect(window, self.colour, self.rect)


def main():
    previous_time = time.time()

    player = Player((255, 0, 0), window.get_width() / 2 - 24, window.get_height() / 2 - 24, 48, 48)

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
