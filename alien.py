import pygame
import random

class Alien(pygame.sprite.Sprite):
    """
    Represents an alien in a space-invaders style game.

    Attributes:
        type (str): The type of alien.
        image (Surface): The image surface for the alien.
        rect (Rect): The rectangle defining the position of the alien.
    """

    def __init__(self, type, x, y):
        """
        Initialize the alien sprite.

        Args:
            type (str): The type of alien.
            x (int): The x-coordinate for the alien's starting position.
            y (int): The y-coordinate for the alien's starting position.
        """
        super().__init__()
        self.type = type
        path = f"Graphics/alien_{type}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, direction):
        """
        Updates the alien's position based on the given direction.

        Args:
            direction (int): The direction to move the alien (positive for right, negative for left).
        """
        # Checks if the rect attribute has been set before moving the alien
        if self.rect is not None:
            self.rect.x += direction
        else:
            print('Error: self.rect is None')

class MysteryShip(pygame.sprite.Sprite):
    """
    Represents a mysterious ship that appears randomly on the screen.

    Attributes:
        screen_width (int): Width of the game screen.
        offset (int): Offset used in positioning and determining speed.
        image (Surface): The image surface for the mystery ship.
        rect (Rect): The rectangle defining the position of the mystery ship.
        speed (int): The speed at which the ship moves.
    """

    def __init__(self, screen_width, offset):
        """
        Initialize the mystery ship sprite.

        Args:
            screen_width (int): Width of the game screen.
            offset (int): Offset for positioning at start and determining speed and movement limits.
        """
        super().__init__()
        self.screen_width = screen_width
        self.offset = offset
        self.image = pygame.image.load('Graphics/mystery.png')

        # Randomly decide the starting side of the mystery ship (left or right)
        x = random.choice([self.offset/2, self.screen_width + self.offset - self.image.get_width()])
        # Set speed direction based on starting side (positive for right start, negative for left start)
        self.speed = 3 if x == self.offset/2 else -3
        self.rect = self.image.get_rect(topleft = (x, 90))

    def update(self):
        """
        Updates the mystery ship's position and checks if it needs to be removed.
        """
        # Checks if the rect attribute has been set before moving the ship
        if self.rect is not None:
            self.rect.x += self.speed

            # Remove the sprite if it moves beyond the screen plus the offset
            if self.rect.right > self.screen_width + self.offset / 2:
                self.kill()
            elif self.rect.left < self.offset / 2:
                self.kill()
        else:
            print('Error: self.rect is None')