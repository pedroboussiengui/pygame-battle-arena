import pygame
from .text import Text
from .shared.health_bar import HealthBar
from pygame import mixer
import random
from .Square import TextFadeout

pygame.mixer.init(44100, -16, 2, 2048)

class Arrow:
    def __init__(self, x, y, direction, is_critical = False):
        self.arrow = pygame.image.load('./src/assets/GoblinPack/Arrow.png')
        self.arrow_shot_sound = mixer.Sound('./src/assets/throw_arrow.mp3')
        self.arrow_hitting_sound = mixer.Sound('./src/assets/arrow_impact.mp3')
        self.scale = 0.2
        self.arrow = pygame.transform.scale(self.arrow, (self.arrow.get_width() * self.scale, self.arrow.get_height() * self.scale))
        self.direction = direction
        self.pos_x = x
        self.pos_y = y
        self.speed = 70
        self.is_critical = is_critical
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
        self.base_heal = 1 # cura 1 de vida a cada segundo

        self.throw_arrow_sprites = pygame.image.load('./src/assets/GoblinPack/GoblinArcher-Sheet.png')
        self.damage_sprites = [pygame.image.load('src/assets/pixil-frame-0.png'),pygame.image.load('src/assets/pixil-frame-1.png'),pygame.image.load('src/assets/pixil-frame-2.png') ]

        self.pos_x = 400
        self.pos_y = 450
        self.speed = 30

        self.name = 'Goblin'
        self.team = None
        self.other_team = None

        self.scale = 0.1

        self.damage = 5
        self.critical_chance = 40
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

        self.health_bar = HealthBar(self.sprint_width, self.name)
        
        self.last_update = pygame.time.get_ticks()

        self.attacking = False
        self.can_attack = True
        self.atk_cooldown= 250
        self.last_attack_time = 0

        self.moving = False
        self.stunned = False
        self.index_atk = 0
        self.index_move = 0
        self.direction = 'right'

        self.damaged = False

        self.arrows: list[Arrow] = []
        self.current_arrow = None

        self.frames = pygame.sprite.Group() # frames de dano e cura 

        # jump status
        self.dy = 0
        self.gravity = 0.5

        # contador do warrior
        self.c = 0

        self.timers = [
            (10, self.update_attacking),
            (50, self.update_arrows), 
            (100, self.update_move),
            (1000, self.heal),
            (100, self.frames.update),
            (100, self.update_damage_frames)
        ]
    
        self.last_print_times = [pygame.time.get_ticks() for _ in range(len(self.timers))]
    
    def attack(self):
        self.attacking = True

    # def attack_idle(self):


    def add_count_atk(self):
        self.c = self.c + 1

    def draw_atk_counter(self, screen):
        text = Text(self.pos_x, self.pos_y, size=30, time=-1)
        text.draw(screen, str(self.c))
    
    def get_rect(self):
        return pygame.Rect(self.pos_x, self.pos_y, self.sprint_width, self.sprint_heigth)

    def draw_rect(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.get_rect(), 2)
    
    def take_damage(self, damage):
        self.current_health = self.current_health - damage
        self.damaged = True

    def draw_health_bar(self, screen):
        self.health_bar.draw(screen, self.current_health, self.max_health, self.pos_x, self.pos_y)
    
    def jump(self):
        if self.dy == 0:
            self.dy = -10

    def heal(self):
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        if self.current_health < self.max_health:
            frame_text = '+' + str(self.base_heal)
            frame = TextFadeout(frame_text, self.pos_x + 50, self.pos_y - 10, 20, (0, 255, 0), duration=500)
            self.frames.add(frame)
            self.current_health = self.current_health + self.base_heal
        
    def update(self, FPS):
        current_time = pygame.time.get_ticks()
        self.dy += self.gravity
        self.pos_y += self.dy

        for i, (interval, func) in enumerate(self.timers):
            if current_time - self.last_print_times[i] >= interval:
                func()
                self.last_print_times[i] = current_time
        

        # if current_time - self.last_update > 0.1 * 1000:
        #     for i in self.arrows:
        #         i.update()
        #         if i.pos_x > 700 or i.pos_x < 10:
        #             self.arrows.remove(i)
            
        #     if self.damaged:
        #         self.damage_index = (self.damage_index + 1) % len(self.damage_sprites)
        #         if self.damage_index == len(self.damage_sprites) - 1:
        #             self.damaged = False

        #     if self.attacking:
        #         self.index_atk = (self.index_atk + 1) % len(self.frames_atk)
        #         if self.index_atk == 5:
        #             self.current_arrow = Arrow(self.pos_x + 5, self.pos_y + 25, self.direction)
        #             self.arrows.append(self.current_arrow)
        #             self.current_arrow.arrow_shot_sound.play()
        #         if self.index_atk == len(self.frames_atk) - 1:
        #             self.attacking = False

        #     if self.moving:
        #         self.index_move = (self.index_move + 1) % len(self.frames_walk)
        #         if self.direction == 'right':
        #             self.pos_x = self.pos_x + self.speed
        #         else:
        #              self.pos_x = self.pos_x - self.speed

        #     self.last_update = current_time

    def update_arrows(self):
        for i in self.arrows:
            i.update()
            if i.pos_x > 700 or i.pos_x < 10:
                self.arrows.remove(i)
    
    def update_damage_frames(self):
        if self.damaged:
            self.damage_index = (self.damage_index + 1) % len(self.damage_sprites)
            if self.damage_index == len(self.damage_sprites) - 1:
                self.damaged = False

    def update_attacking(self):
        if self.attacking and self.can_attack:
            self.index_atk = (self.index_atk + 1) % len(self.frames_atk)
            if self.index_atk == 5:
                is_critcal = self.calculate_critical()
                self.current_arrow = Arrow(self.pos_x + 5, self.pos_y + 25, self.direction, is_critical=is_critcal)
                self.arrows.append(self.current_arrow)
                self.current_arrow.arrow_shot_sound.play()
            if self.index_atk == len(self.frames_atk) - 1:
                self.attacking = False
                self.last_attack_time = pygame.time.get_ticks()
                self.can_attack = False
        self.attack_idle()

    def attack_idle(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.atk_cooldown:
            self.can_attack = True

    
    def calculate_critical(self):
        return random.randint(0, 101) < self.critical_chance

    def update_move(self):
        if self.moving:
            self.index_move = (self.index_move + 1) % len(self.frames_walk)
            if self.direction == 'right':
                self.pos_x = self.pos_x + self.speed
            else:
                self.pos_x = self.pos_x - self.speed

    def draw(self, screen):
        # self.draw_rect(screen)
        self.draw_health_bar(screen)
        self.draw_atk_counter(screen)

        self.frames.draw(screen)

        for i in self.arrows:
            i.draw(screen)

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
        
        # as animações que aparecem por cima devem ir por último
        if self.damaged:
            screen.blit(self.damage_sprites[self.damage_index], (self.pos_x, self.pos_y))

    def __repr__(self):
        return self.name
