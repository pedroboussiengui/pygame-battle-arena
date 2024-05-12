import pygame
from pygame import mixer

pygame.mixer.init(44100, -16, 2, 2048)

class Arrow:
    def __init__(self, x, y, direction):
        self.arrow = pygame.image.load('./src/assets/GoblinPack/Arrow.png')
        self.arrow_shot_sound = mixer.Sound('./src/assets/throw_arrow.mp3')
        self.arrow_hitting_sound = mixer.Sound('./src/assets/arrow_impact.mp3')
        self.scale = 0.2
        self.arrow = pygame.transform.scale(self.arrow, (self.arrow.get_width() * self.scale, self.arrow.get_height() * self.scale))
        self.direction = direction
        self.pos_x = x
        self.pos_y = y
        self.speed = 70
        self.w = self.arrow.get_width()
        self.h = self.arrow.get_height()
    
    def get_rect(self):
        return pygame.Rect(self.pos_x, self.pos_y, self.w, self.h)
    
    def update(self):
        if self.direction == 'right':
            self.pos_x = self.pos_x + self.speed
        else:
            self.pos_x = self.pos_x - self.speed

    def draw(self, screen):
        if self.direction == 'right':
            screen.blit(self.arrow, (self.pos_x, self.pos_y))
        else:
            flipped_arrow = pygame.transform.flip(self.arrow, True, False)
            screen.blit(flipped_arrow, (self.pos_x, self.pos_y))

class Goblin:
    def __init__(self):
        self.max_health = 80
        self.current_health = self.max_health

        self.throw_arrow_sprites = pygame.image.load('./src/assets/GoblinPack/GoblinArcher-Sheet.png')
        self.damage_sprites = [pygame.image.load('src/assets/pixil-frame-0.png'),pygame.image.load('src/assets/pixil-frame-1.png'),pygame.image.load('src/assets/pixil-frame-2.png') ]

        self.pos_x = 400
        self.pos_y = 450
        self.speed = 30

        self.scale = 0.1

        self.damage = 25
        self.damage_index = 0
        
        self.sprint_width = self.throw_arrow_sprites.get_width() // 9
        self.sprint_heigth = self.throw_arrow_sprites.get_height() // 5

        self.frames_atk  = []
        self.frames_walk = []
        for row in range(0, 2):
            for col in range(9):
                if row == 0:
                    x = col * self.throw_arrow_sprites.get_width() // 9
                    y = row * self.throw_arrow_sprites.get_height() // 5
                    sprite = self.throw_arrow_sprites.subsurface(pygame.Rect(x, y, self.sprint_width, self.sprint_heigth))
                    scaled_sprite = pygame.transform.scale(sprite, (self.sprint_width * self.scale, self.sprint_heigth * self.scale))
                    self.frames_walk.append(scaled_sprite)
                elif row == 1:
                    x = col * self.throw_arrow_sprites.get_width() // 9
                    y = row * self.throw_arrow_sprites.get_height() // 5
                    sprite = self.throw_arrow_sprites.subsurface(pygame.Rect(x, y, self.sprint_width, self.sprint_heigth))
                    scaled_sprite = pygame.transform.scale(sprite, (self.sprint_width * self.scale, self.sprint_heigth * self.scale))
                    self.frames_atk.append(scaled_sprite)
        self.frames_walk = self.frames_walk[:-1]

        self.sprint_width = self.sprint_width * self.scale
        self.sprint_heigth = self.sprint_heigth * self.scale
        
        self.last_update = pygame.time.get_ticks()
        self.attacking = False
        self.moving = False
        self.index_atk = 0
        self.index_move = 0
        self.direction = 'right'

        self.damaged = False

        self.arrows = []
        self.current_arrow = None
    
    def new_arrow(self):
        self.current_arrow = Arrow(self.pos_x + 5, self.pos_y + 25, self.direction)
    
    def get_rect(self):
        return pygame.Rect(self.pos_x, self.pos_y, self.sprint_width, self.sprint_heigth)

    def draw_rect(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.get_rect(), 2)
    
    def take_damage(self, damage):
        self.current_health = self.current_health - damage
        self.damaged = True

    def draw_health_bar(self, screen):
        if self.current_health < 0:
            self.current_health = 0

        # Calcula a largura da barra de vida com base na porcentagem de vida restante
        health_percentage = self.current_health / self.max_health
        bar_width = int(health_percentage * self.sprint_width)

        # Desenha a barra de vida acima do personagem
        health_bar_rect = pygame.Rect(self.pos_x, self.pos_y, bar_width, 5)
        pygame.draw.rect(screen, (0, 255, 0), health_bar_rect)
        
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > 0.1 * 1000:
            for i in self.arrows:
                i.update()
                if i.pos_x > 700 or i.pos_x < 10:
                    self.arrows.remove(i)
            
            if self.damaged:
                self.damage_index = (self.damage_index + 1) % len(self.damage_sprites)
                if self.damage_index == len(self.damage_sprites) - 1:
                    self.damaged = False

            if self.attacking:
                self.index_atk = (self.index_atk + 1) % len(self.frames_atk)
                if self.index_atk == 3:
                    self.current_arrow.arrow_shot_sound.play()
                if self.index_atk == 5:
                    self.arrows.append(self.current_arrow)
                if self.index_atk == len(self.frames_atk) - 1:
                    self.attacking = False

            if self.moving:
                self.index_move = (self.index_move + 1) % len(self.frames_walk)
                if self.direction == 'right':
                    self.pos_x = self.pos_x + self.speed
                else:
                     self.pos_x = self.pos_x - self.speed

            self.last_update = current_time

    def draw(self, screen):
        # self.draw_rect(screen)
        self.draw_health_bar(screen)
        for i in self.arrows:
            i.draw(screen)
        
        if self.damaged:
            screen.blit(self.damage_sprites[self.damage_index], (self.pos_x, self.pos_y))

        if self.moving:
            if self.direction == 'right':
                screen.blit(self.frames_walk[self.index_move], (self.pos_x, self.pos_y))
            else:
                flipped_frame = pygame.transform.flip(self.frames_walk[self.index_move], True, False)
                screen.blit(flipped_frame, (self.pos_x, self.pos_y))
        elif self.attacking:
            if self.direction == 'right':
                screen.blit(self.frames_atk[self.index_atk], (self.pos_x, self.pos_y))
            else:
                flipped_frame = pygame.transform.flip(self.frames_atk[self.index_atk], True, False)
                screen.blit(flipped_frame, (self.pos_x, self.pos_y))
        else:
            if self.direction == 'right':
                screen.blit(self.frames_walk[0], (self.pos_x, self.pos_y))
            else:
                flipped_frame = pygame.transform.flip(self.frames_walk[self.index_move], True, False)
                screen.blit(flipped_frame, (self.pos_x, self.pos_y))

