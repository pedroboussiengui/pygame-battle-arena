import pygame

class Block:
    def __init__(self, x, y, width, height, color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)  # Cria um retângulo de colisão
        self.color = color  # Cor do retângulo de colisão

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    

block1 = Block(500, 350, 50, 50)

ground = Block(0, 500, 800, 100)


blocks = [block1, ground]