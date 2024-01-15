import pygame

class Laser(pygame.sprite.Sprite):
    """
    Represents a laser beam in a game, which is a subclass of pygame's Sprite.
    """

    def __init__(self, position, speed, screen_height):
        """
        Initialize a new Laser instance.

        :param position: A tuple (x, y) representing the starting position of the laser.
        :param speed: An integer representing the speed of the laser.
        :param screen_height: An integer representing the height of the game screen, used to check if the laser is off-screen.
        """
        super().__init__()  # Call to the parent class (Sprite) constructor.
        self.image = pygame.Surface((4, 15))  # Create a surface for the laser image.
        self.image.fill((243, 216, 63))  # Fill the surface with a color to represent the laser.
        self.rect = self.image.get_rect(center=position)  # Get the rectangular area of the surface.
        self.speed = speed  # Set the speed of the laser.
        self.screen_height = screen_height  # Set the screen height to determine bounds.

    def update(self):
        """
        Update the position of the laser every frame.
        """
        # If the laser's rect is not set, exit the function.
        if self.rect is None:
            return

        # Move the laser up the screen by decreasing its y-coordinate by its speed.
        self.rect.y -= self.speed

        # If the laser moves off the screen, remove it from all sprite groups.
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            self.kill()  # Remove the sprite from all sprite groups to which it belongs.