import itertools
import random

import pygame

from alien import Alien, MysteryShip
from laser import Laser
from obstacle import Obstacle, grid
from spaceship import Spaceship


class Game:
    """
    Main Game class that controls game events, objects, and state.

    Attributes:
        screen_width (int): The width of the game screen.
        screen_height (int): The height of the game screen.
        offset (int): An offset value meant to position elements on the screen.
        spaceship_group (pygame.sprite.GroupSingle): A group containing the player's spaceship sprite.
        obstacles (list): A list of Obstacle instances representing barriers.
        aliens_group (pygame.sprite.Group): A group containing all alien sprites.
        aliens_direction (int): The current direction of alien movement, 1 means right, -1 means left.
        alien_lasers_group (pygame.sprite.Group): A group containing all lasers shot by aliens.
        mystery_ship_group (pygame.sprite.GroupSingle): A group containing the mystery ship sprite, if present.
        lives (int): The number of lives the player has.
        score (int): The current player score.
        highscore (int): The highest score achieved.
        run (bool): Boolean to determine if the game is running.
        explosion_sound (pygame.mixer.Sound): Sound played when an explosion occurs.

    Methods:
        create_obstacles: Creates and positions the obstacle objects.
        create_aliens: Creates alien sprites and adds them to the aliens_group.
        move_aliens: Moves the aliens horizontally and vertically if they hit screen edges.
        alien_move_down: Moves all aliens downwards by a specified distance.
        alien_shoot_laser: Randomly selects an alien to shoot a laser.
        create_mystery_ship: Creates the mystery ship at the top of the screen.
        check_for_highscore: Updates the highscore if the current score is greater.
        load_highscore: Loads the highscore from 'highscore.txt'.
        check_for_collisions: Checks for collisions between lasers, aliens, obstacles, and the spaceship.
        game_over: Ends the game and prints a game over message.
        reset: Resets the game to its starting state.

    """
    def __init__(self, screen_width, screen_height, offset):
        """
        Initializes the Game object with screen dimensions, offset, and loads resources.

        Args:
            screen_width (int): Width of the game window.
            screen_height (int): Height of the game window.
            offset (int): Offset used for positioning elements.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.lives = 3
        self.score = 0
        self.highscore = 0
        self.run = True
        self.load_highscore()
        self.explosion_sound = pygame.mixer.Sound('Sounds/explosion.ogg')
        pygame.mixer.music.load('Sounds/music.ogg')
        pygame.mixer.music.play(-1)

    def create_obstacles(self):
        """Create and position the obstacles on the screen."""
        obstacle_width = len(grid[0]) * 3
        gap = (self.screen_width + self.offset - (4 * obstacle_width))/5
        obstacles = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100)
            obstacles.append(obstacle)
        return obstacles

    def create_aliens(self):
        """Creates aliens and adds them to the alien group."""
        for row, column in itertools.product(range(5), range(11)):
            x = 75 + column * 55
            y = 110 + row * 55

            if row == 0:
                alien_type = 3
            elif row in (1, 2):
                alien_type = 2
            else:
                alien_type = 1

            alien = Alien(alien_type, x + self.offset/2, y)
            self.aliens_group.add(alien)

    def move_aliens(self):
        """Moves the aliens horizontally and switch direction if they hit the edges."""
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + self.offset:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= self.offset/2:
                self.aliens_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        """Move all aliens down by a specified distance."""
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        """Randomly selects an alien to shoot a laser."""
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height)
            self.alien_lasers_group.add(laser_sprite)

    def create_mystery_ship(self):
        """Creates the mystery ship and adds it to the game."""
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))

    def check_for_highscore(self):
        """
        Updates the highscore if the current score is greater
        and saves it to 'highscore.txt'.
        """
        if self.score > self.highscore:
            self.highscore = self.score

            with open('highscore.txt', 'w') as file:
                file.write(str(self.highscore))

    def load_highscore(self):
        """Loads the highscore from 'highscore.txt', if it exists."""
        try:
            with open('highscore.txt', 'r') as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0

    def check_for_collisions(self):
        """
        Checks and handles collisions between lasers, aliens, obstacles, and the spaceship.
        Updates the score and plays explosion sounds upon hits.
        """
        # Spaceship
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:

                if aliens_hit := pygame.sprite.spritecollide(
                    laser_sprite, self.aliens_group, True
                ):
                    self.explosion_sound.play()
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        laser_sprite.kill()

                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    self.explosion_sound.play()
                    self.score += 500
                    self.check_for_highscore()
                    laser_sprite.kill()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        # Aliens
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                    laser_sprite.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

                if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    self.game_over()

    def game_over(self):
        """End the game and display the game over message."""
        self.run = False
        print("We're under their control now!")

    def reset(self):
        """Reset the game to the initial state, except for the high score."""
        self.run = True
        self.lives = 3
        self.score = 0
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.mystery_ship_group.empty()
        self.create_aliens()
        self.obstacles = self.create_obstacles()

