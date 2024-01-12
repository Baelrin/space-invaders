import pygame
import sys
from spaceship import Spaceship

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700

GREY = (29, 29, 27)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Baelrin's Space Invaders")

clock = pygame.time.Clock()

spaceship = Spaceship(SCREEN_WIDTH, SCREEN_HEIGHT)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

while True:
    # Checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Updating
    spaceship_group.update()

    # Drawing
    screen.fill(GREY)
    spaceship_group.draw(screen)

    pygame.display.update()
    clock.tick(60)
