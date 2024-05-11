import pygame
import random
import numpy as np

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, time):
        super().__init__()
        self.time = time
        self.current_time = 0
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y)) 

    def update(self, fps):
        self.current_time = self.current_time + 1
        if self.current_time >= self.time * fps:
            self.kill()
