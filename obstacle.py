import itertools
import pygame

class Block(pygame.sprite.Sprite):
    """A Block is a sprite for representing objects in a game.

    It inherits from pygame's Sprite class. It is displayed as a small square
    with a specified color filled in it.

    Attributes:
        image (pygame.Surface): The surface drawn as the sprite's image.
        rect (pygame.Rect): The rectangle defining the position and size of the image.
    """

    def __init__(self, x, y):
        """Initializes a Block instance with specified top-left corner position.

        Args:
            x (int): The x-coordinate of the top-left corner of the block.
            y (int): The y-coordinate of the top-left corner of the block.
        """
        super().__init__()
        self.image = pygame.Surface((3, 3))  # Size of the block
        self.image.fill((243, 216, 63))  # Yellow color
        self.rect = self.image.get_rect(topleft=(x, y))  # Positioned at (x, y)


# Define a 2D array to represent the presence (1) or absence (0) of blocks.
grid = [
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]]

class Obstacle:
    """An Obstacle represents a collection of blocks arranged in a specific pattern.

    It creates a group of Block instances forming the shape defined in a grid.

    Attributes:
        blocks_group (pygame.sprite.Group): A group containing all Block sprites of the obstacle.
    """

    def __init__(self, x, y):
        """Initializes an Obstacle instance at a specified location.

        Reads a grid pattern, and creates Block instances for each occupied cell
        (where grid value is 1). It uses the given (x, y) top-left corner coordinate
        as the starting point for placing the blocks.

        Args:
            x (int): The x-coordinate of the top-left corner of the obstacle.
            y (int): The y-coordinate of the top-left corner of the obstacle.
        """
        self.blocks_group = pygame.sprite.Group()
        for row, column in itertools.product(range(len(grid)), range(len(grid[0]))):
            if grid[row][column] == 1:
                pos_x = x + column * 3  # X position of the block
                pos_y = y + row * 3    # Y position of the block
                block = Block(pos_x, pos_y)
                self.blocks_group.add(block)  # Add the block to the group