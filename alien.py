import pygame
import random

class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        path = f"Graphics/alien_{type}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft = (x, y))
        
    def update(self, direction):
        if self.rect is not None:
            self.rect.x += direction
        else:
            print('Error: self.rect is None')
        
class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = offset
        self.image = pygame.image.load('Graphics/mystery.png')

        x = random.choice([self.offset/2, self.screen_width + self.offset - self.image.get_width()])
        self.speed = 3 if x == self.offset/2 else -3
        self.rect = self.image.get_rect(topleft = (x, 90))
        
    def update(self):
        if self.rect is not None:
            self.rect.x += self.speed
        else: 
            print('Error: self.rect is None')
        if self.rect is not None:
            if self.rect.right > self.screen_width + self.offset / 2:
                self.kill()
            elif self.rect.left < self.offset / 2:
                self.kill()