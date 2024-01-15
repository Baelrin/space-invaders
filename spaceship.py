import pygame

from laser import Laser

class Spaceship(pygame.sprite.Sprite):
    """
    Represents the spaceship which is controlled by the player in the game.

    Attributes:
        offset (int): The initial offset for the spaceship from the screen's edge.
        screen_width (int): The width of the screen.
        screen_height (int): The height of the screen.
        image (Surface): The surface object representing the spaceship image.
        rect (Rect): The rectangular area of the spaceship image.
        speed (int): The speed at which the spaceship moves left or right.
        lasers_group (Group): Group containing all the lasers fired by the spaceship.
        laser_ready (bool): Boolean indicating if the spaceship is ready to fire a laser.
        laser_time (int): Timestamp of the last fired laser.
        laser_delay (int): Delay before the spaceship can fire another laser.
        laser_sound (Sound): Sound object that plays when a laser is fired.
    """
    def __init__(self, screen_width, screen_height, offset):
        super().__init__()
        self.offset = offset
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load('Graphics/spaceship.png')
        self.rect = self.image.get_rect(
            midbottom=((self.screen_width + self.offset)/2, self.screen_height))
        self.speed = 6
        self.lasers_group = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 300
        self.laser_sound = pygame.mixer.Sound('Sounds/laser.ogg')

    def get_user_input(self):
        """
        Processes the user input to control the spaceship and fire lasers.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and self.rect is not None:
            self.rect.x += self.speed

        if keys[pygame.K_LEFT] and self.rect is not None:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            if self.rect is not None:
                laser = Laser(self.rect.center, 5, self.screen_height)
                self.lasers_group.add(laser)
                self.laser_time = pygame.time.get_ticks()
            else:
                print("Warning: self.rect is None")
            self.laser_sound.play()

    def update(self):
        """
        Updates the spaceship's movement and actions every frame.
        """
        self.get_user_input()
        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()

    def constrain_movement(self):
        """
        Ensures the spaceship cannot move beyond the screen boundaries.
        """
        if self.rect is not None:
            self.rect.right = min(self.rect.right, self.screen_width)
            self.rect.left = max(self.rect.left, self.offset)
        else:
            print("Error: Laser can't be recharged")

    def recharge_laser(self):
        """
        Recharges the laser, allowing the spaceship to fire again after a delay.
        """
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True

    def reset(self):
        """
        Resets the spaceship to its initial state.
        """
        if self.image is not None:
            self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2, self.screen_height))
            self.lasers_group.empty()
        else:
            print('Error: Image not loaded')