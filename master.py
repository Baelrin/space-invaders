import random
import sys

import pygame

from game import Game

# Initialize the pygame library
pygame.init()

# Define screen dimensions and offset
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

# Define color constants
GREY = (29, 29, 27)
YELLOW = (243, 216, 63)

# Load and set up fonts for rendering text
font = pygame.font.Font('Font/monogram.ttf', 40)
level_surface = font.render('BATTLE 01', False, YELLOW)
game_over_surface = font.render('EARTH LOST', False, YELLOW)
score_text_surface = font.render('SCORE', False, YELLOW)
highscore_text_surface = font.render('HIGH-SCORE', False, YELLOW)

# Initialize the game screen
screen = pygame.display.set_mode(
    (SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2*OFFSET))
pygame.display.set_caption("Baelrin's Space Invaders")

# Set up the clock for controlling frame rate
clock = pygame.time.Clock()

# Create a new game instance
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

# Define custom events for shooting lasers and spawning mystery ships
SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

# Main game loop
while True:
    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()

        if event.type == MYSTERYSHIP and game.run:
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

        # Process key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game.run is False:
            game.reset()

    # Update game state
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()

    # Clear screen and draw UI elements
    screen.fill(GREY)

    # Draw the UI elements on the screen
    pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60)
    pygame.draw.line(screen, YELLOW, (25, 730), (775, 730), 3)

    # Display the current level or game over text
    if game.run:
        screen.blit(level_surface, (570, 740, 50, 50))
    else:
        screen.blit(game_over_surface, (570, 740, 50, 50))

    # Display player lives
    x = 50
    for _ in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 745))
        x += 50

    # Render and display the score and highscore
    formatted_score = str(game.score).zfill(5)
    formatted_highscore = str(game.highscore).zfill(5)
    score_surface = font.render(formatted_score, False, YELLOW)
    highscore_surface = font.render(formatted_highscore, False, YELLOW)
    screen.blit(score_text_surface, (50, 15, 50, 50))
    screen.blit(score_surface, (50, 40, 50, 50))
    screen.blit(highscore_text_surface, (550, 15, 50, 50))
    screen.blit(highscore_surface, (625, 40, 50, 50))

    # Draw game entities on the screen
    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen)

    # Update the display and maintain frame rate
    pygame.display.update()
    clock.tick(60)
