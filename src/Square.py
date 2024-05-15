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


class TextFadeout(pygame.sprite.Sprite):
    def __init__(self, text, x, y, size, color=(0, 0, 0), duration=2000):
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(None, size)
        self.text_color = color
        self.image = self.font.render(text, True, self.text_color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.alpha = 255  # Transparência inicial (opacidade total)

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        if elapsed_time >= self.duration:
            self.kill()  # Remove o texto da tela quando a duração terminar
        else:
            # Calcula a transparência com base no tempo decorrido
            self.alpha = 255 - int(255 * (elapsed_time / self.duration))
            self.image = self.font.render(self.text, True, self.text_color)
            self.image.set_alpha(self.alpha)  # Define a transparência da imagem
            self.rect.y = self.rect.y - 2 # particula subindo

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)