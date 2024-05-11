import pygame

class Text:
    def __init__(self, x, y, size, time, color=(0, 0, 0), text=None, animate=False):
        self.font = pygame.font.Font(None, size)
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.time = time  # -1 para tempo infinito por padrão
        self.current_time = 0
        self.deletable = False

    def draw(self, screen, text):
        if self.text == None:
            screen.blit(self.font.render(text, True, self.color), (self.x, self.y))
        else:
            screen.blit(self.font.render(self.text, True, self.color), (self.x, self.y))
    
    def update(self, fps):
        if self.time != -1:
            self.current_time = self.current_time + 1
            if self.current_time >= (self.time * fps) // 1000:
                self.deletable = True




# class Text(pygame.sprite.Sprite):
#     def __init__(self, x, y, size, time, color=(0, 0, 0), text=None, animate=False):
#         super().__init__()
#         self.font = pygame.font.Font(None, size)
#         self.text = text
#         self.color = color
#         self.x = x
#         self.y = y
#         self.image = None
#         self.rect = None
#         self.time = time  # -1 para tempo infinito por padrão
#         self.current_time = 0
#         # self.deletable = False
#         self.animate = animate
#         # self.alpha = 255

#     def draw(self, screen, text):
#         if self.text == None:
#             self.image = self.font.render(text, True, self.color)
#         else:
#             self.image = self.font.render(self.text, True, self.color)
#         self.rect = self.image.get_rect(topleft=(self.x, self.y))
#         screen.blit(self.image, self.rect.topleft)
    
#     def update(self, fps):
#         if self.time != -1:
#             self.current_time = self.current_time + 1
#             if self.current_time >= (self.time * fps) // 1000:
#                 # self.deletable = True
#                 self.kill()
#             # else:
#             #     self.alpha = 255 - int(255 * (elapsed_time / self.duration))
#             #     self.image.set_alpha(self.alpha) 