import pygame

colors = {
    'green': (0, 255, 0),
    'orange': (255, 255, 0),
    'red': (255, 0, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255)

}

class HealthBar:
    def __init__(self, width, name):
        self.width = width
        self.height = 12
        self.name = name
        self.font = pygame.font.SysFont(None, 18)

    def draw(self, screen, current_health, max_health, pos_x, pos_y):
        pos_y = pos_y - 30

        if current_health < 0:
            current_health = 0
        
        if current_health > max_health:
            current_health = max_health

        bar_color = colors['green']
        if current_health <= max_health / 2:
            bar_color = colors['orange']
        if current_health <= max_health / 4:
            bar_color = colors['red']

        health_percentage = current_health / max_health
        bar_width = int(health_percentage * self.width)

        health_bar_frame = pygame.Rect(pos_x-2, pos_y-2, self.width+4, self.height+4)
        pygame.draw.rect(screen, colors['black'], health_bar_frame)

        health_bar_rect = pygame.Rect(pos_x, pos_y, bar_width, self.height)
        pygame.draw.rect(screen, bar_color, health_bar_rect)

        text_surface = self.font.render(f'{current_health}/{max_health}', True, colors['white'])
        text_rect = text_surface.get_rect(center=health_bar_frame.center)
        screen.blit(text_surface, text_rect)

        text_surface = self.font.render(self.name, True, colors['black'])
        text_rect = text_surface.get_rect(center=(health_bar_frame.centerx, pos_y - 10))
        screen.blit(text_surface, text_rect)
