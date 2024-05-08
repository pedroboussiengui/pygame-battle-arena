import pygame

class Text:
    def __init__(self, x, y):
        # Configurações da fonte
        self.font = pygame.font.Font(None, 36)  # Fonte padrão com tamanho 36

        # Cor do texto
        self.text_color = (0, 0, 0)

        # Posição para exibir o texto na tela
        self.text_position = (x, y)


    def draw(self, screen, text):
        screen.blit(self.font.render(text, True, self.text_color), self.text_position)