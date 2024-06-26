import pygame
from .text import Text
from pygame import mixer
from .goblin import Goblin
from .shared.health_bar import HealthBar
from .Square import TextFadeout

pygame.mixer.init(44100, -16, 2, 2048)

class RotatingAxe:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dir = direction
        self.speed = 50
        self.rotating_axe = pygame.image.load('./src/assets/Red Axe sprite.png')

        self.frame_rotating_axe = 0

        self.frames_rotation_axe = []
        for row in range(3):
            for col in range(3):
                if (row == 2 and col == 2):
                    break
                x = col * self.rotating_axe.get_width() // 3
                y = row * self.rotating_axe.get_height() // 3
                sprite = self.rotating_axe.subsurface(pygame.Rect(x, y, self.rotating_axe.get_width() // 3, self.rotating_axe.get_height() // 3))
                scaled_sprite = pygame.transform.scale(sprite, (self.rotating_axe.get_width() // 3 * 0.1, self.rotating_axe.get_height() // 3 * 0.1))
                self.frames_rotation_axe.append(scaled_sprite)

    def update(self):
        if self.dir == 'right':
            self.x = self.x + self.speed
        else:
            self.x = self.x - self.speed
        self.frame_rotating_axe = (self.frame_rotating_axe + 1) % (len(self.frames_rotation_axe))
        
    def draw(self, screen):
        screen.blit(self.frames_rotation_axe[self.frame_rotating_axe], (self.x, self.y))


# class QAbility:
#     def __init__(self, obj: Warrior):
#         self.distance = 150
#         self.direction = obj.direction
#         self.cooldown = 60 * 3 # 3 segundos com 60 fps
#         self.enemies_hitted = []
#         self.damage = 40


class Warrior:
    def __init__(self):
        self.max_health = 100
        self.current_health = self.max_health
        self.name = 'Warrior'
        self.team = None
        self.other_team = None

        self.warrior_atk = pygame.image.load('./src/assets/Warrior_1/Attack_1.png')
        self.warrior_walk = pygame.image.load('./src/assets/Warrior_1/Walk.png')
        self.warrior_jump = pygame.image.load('./src/assets/Warrior_1/Jump.png')
        self.axe_hit = mixer.Sound('./src/assets/axe_hit.wav')
        self.stun_sprites = pygame.image.load('./src/assets/stun_sprites.png')
        # self.damage_sprites = [pygame.image.load('src/assets/pixil-frame-0.png'),pygame.image.load('src/assets/pixil-frame-1.png'),pygame.image.load('src/assets/pixil-frame-2.png') ]

        # self.rotating_axe = pygame.image.load('./src/assets/Red Axe sprite.png')

        self.frame_width = 96
        self.frame_height = 96

        self.frames_atk = []
        for x in range(0, self.warrior_atk.get_width(), self.frame_width):
            frame = self.warrior_atk.subsurface(pygame.Rect(x, 0, self.frame_width, self.frame_height))
            self.frames_atk.append(frame)

        self.frames_walk = []
        for x in range(0, self.warrior_walk.get_width(), self.frame_width):
            frame = self.warrior_walk.subsurface(pygame.Rect(x, 0, self.frame_width, self.frame_height))
            self.frames_walk.append(frame)

        self.frames_jump = []
        for x in range(0, self.warrior_jump.get_width(), self.frame_width):
            frame = self.warrior_jump.subsurface(pygame.Rect(x, 0, self.frame_width, self.frame_height))
            self.frames_jump.append(frame)

        self.stuned_frames = []
        for x in range(0, self.stun_sprites.get_width(), 100):
            frame = self.stun_sprites.subsurface(pygame.Rect(x, 0, 100, 70))
            self.stuned_frames.append(frame)

        # self.frames_rotation_axe = []
        # for row in range(3):
        #     for col in range(3):
        #         if (row == 2 and col == 2):
        #             break
        #         x = col * self.rotating_axe.get_width() // 3
        #         y = row * self.rotating_axe.get_height() // 3
        #         sprite = self.rotating_axe.subsurface(pygame.Rect(x, y, self.rotating_axe.get_width() // 3, self.rotating_axe.get_height() // 3))
        #         scaled_sprite = pygame.transform.scale(sprite, (self.rotating_axe.get_width() // 3 * 0.1, self.rotating_axe.get_height() // 3 * 0.1))
        #         self.frames_rotation_axe.append(scaled_sprite)

        self.frame_index_walk = 0
        self.frame_index_atk = 0
        self.frame_index_jump = 0
        self.frame_index_stunned = 0
        # self.frame_rotating_axe = 0
        self.animation_walk = 0.01
        self.animation_atk = 0.08 # attack speedz
        self.animation_jump = 0.1

        self.damage = 8
        # self.damage_index = 0

        self.health_bar = HealthBar(self.frame_width, self.name)

        self.last_update = pygame.time.get_ticks()
        self.moving = False
        self.attacking = False
        self.jumping = False
        self.stunned = False
        self.direction = 'right'  # Direção inicial do personagem

        self.player_x = 100
        self.player_y = 300
        # self.axe_x = self.player_x
        # self.axe_y = self.player_y
        self.speed = 3
        self.dy = 0
        self.gravity = 0.5  # Valor da gravidade

        self.throwing_axe = False

        self.rotate_axe = []
        
        self.atk_d = 30

        self.damage_frames = pygame.sprite.Group()

        # desh ability by press E
        self.dashing = False
        self.E_distance = 150
        self.e_direction = self.direction
        self.final_x = None
        self.cooldown = 0 # 5 segundos
        self.enemies_hitted = []
        ###################################


        self.can_damage = False
        # self.obj_damaged = None

        self.enemies = []

    def get_data(self):
        return (self.player_x, self.player_y, self.frame_index_walk, self.frame_index_atk, self.frame_index_jump)

    def apply_data(self, data: tuple):
        pass
    
    def attack(self):
        self.attacking = True
    
    def get_stun(self):
        self.stunned = True
    
    def attack_counter(self):
        for i in self.enemies:
            i.add_count_atk()

    def add_enemy(self, enemy):
        if enemy not in self.enemies:
            self.enemies.append(enemy)
    
    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)
    
    def rect(self):
        return pygame.Rect(self.player_x + 30, self.player_y + self.frame_height // 2, self.frame_width-60, self.frame_height // 2)

    def jump(self):
        self.jumping = True
        if self.dy == 0:
            self.dy = -10
    
    def Q_ability(self):
        self.damage = self.damage * 2

    def E_ability(self, obj: Goblin):
        self.dashing = True
        self.e_direction = self.direction
        if self.e_direction == 'right':
            self.final_x = self.player_x + self.E_distance
        else:
            self.final_x = self.player_x - self.E_distance


    def update(self, fps):
        current_time = pygame.time.get_ticks()
        self.dy += self.gravity
        self.player_y += self.dy

        # for d in self.damage_frames:
        #     d.update(fps)
        #     if d.deletable == True:
        #         self.damage_frames.remove(d)

        self.damage_frames.update()

        if current_time - self.last_update > 1.0 * 1000:
            print("heal")
        
        for i in self.other_team:
            print(i)
            if i.get_rect().colliderect(self.get_atk_hitbox()):
                print('add enemy')
                self.add_enemy(i)
            else:
                print('remove enemy')
                self.remove_enemy(i)

        if current_time - self.last_update > self.animation_walk * 1000:  # converter para milissegundos
            if self.dashing:
                for i in self.other_team:
                    # if isinstance(i, Goblin):
                    if self.rect().colliderect(i.get_rect()) and i not in self.enemies_hitted:
                        i.take_damage(30)
                        self.enemies_hitted.append(i)
                        print("hit")

                if self.e_direction == 'right':
                    self.player_x += 10
                    if self.player_x >= self.final_x:
                        self.dashing = False
                        self.final_x = None
                        self.enemies_hitted = []
                else:
                    self.player_x -= 10
                    if self.player_x <= self.final_x:
                        self.dashing = False
                        self.final_x = None
                        self.enemies_hitted = []
                self.cooldown = 180 # segundos
            else:
                if self.cooldown > 0:
                    self.cooldown -= 1

            if self.moving:
                self.frame_index_walk = (self.frame_index_walk + 1) % len(self.frames_walk)
                if self.direction == 'right':
                    self.player_x = self.player_x + self.speed
                else:
                     self.player_x = self.player_x - self.speed
            # self.last_update = current_time
        
        if current_time - self.last_update > self.animation_walk * 1000:
            if self.stunned:
                self.frame_index_stunned = (self.frame_index_stunned + 1) % len(self.stuned_frames)
                # if self.frame_index_stunned == len(self.stuned_frames) - 1:
                #     self.stunned = False
        
        if current_time - self.last_update > self.animation_jump * 1000:
            if self.jumping:
                self.frame_index_jump = (self.frame_index_jump + 1) % len(self.frames_jump)
                if self.frame_index_jump == len(self.frames_jump) - 1:
                    self.jumping = False
        
        if current_time - self.last_update > self.animation_atk * 1000:  # converter para milissegundos
            if self.throwing_axe:
                for i in self.rotate_axe:
                    i.update()
                    if i.x > 700 or i.x < 10:
                        self.rotate_axe.remove(i)
            if self.attacking:
                self.frame_index_atk = (self.frame_index_atk + 1) % len(self.frames_atk)
                if self.frame_index_atk == 2:
                    self.axe_hit.play()
                if self.frame_index_atk == 2:
                    if len(self.enemies) != 0:
                        self.attack_counter()
                    for e in self.enemies:
                        self.to_damage(e)
                if self.frame_index_atk == len(self.frames_atk) - 1:
                    self.attacking = False
                # self.damage_index = (self.damage_index + 1) % len(self.damage_sprites)
            self.last_update = current_time
    
    def to_damage(self, obj: Goblin):
        obj.take_damage(self.damage)

    def draw(self, screen):
        # self.draw_hitbox(screen)
        # self.draw_attack_hitbox(screen)
        self.draw_health_bar(screen)

        # for d in self.damage_frames:
        #     d.draw(screen, d.text)

        self.damage_frames.draw(screen)

        # self.draw_atk_counter(screen)

        if self.throwing_axe:
            self.rotate_axe_sprite(screen)

        if self.stunned:
            screen.blit(self.stuned_frames[self.frame_index_stunned], (self.player_x, self.player_y))

        if self.jumping:
            screen.blit(self.frames_jump[self.frame_index_jump], (self.player_x, self.player_y))
            if self.dy == 0:
                self.jumping = False
        elif self.moving:
            if self.direction == 'right':
                screen.blit(self.frames_walk[self.frame_index_walk], (self.player_x, self.player_y))
            else:  # Flip horizontal se a direção for 'left'
                flipped_frame = pygame.transform.flip(self.frames_walk[self.frame_index_walk], True, False)
                screen.blit(flipped_frame, (self.player_x, self.player_y))
        elif self.attacking:
            if self.direction == 'right':
                screen.blit(self.frames_atk[self.frame_index_atk], (self.player_x, self.player_y))
            else:  # Flip horizontal se a direção for 'left'
                flipped_frame = pygame.transform.flip(self.frames_atk[self.frame_index_atk], True, False)
                screen.blit(flipped_frame, (self.player_x, self.player_y))
        else:
            # Desenhar o personagem parado
            if self.direction == 'right':
                screen.blit(self.frames_walk[0], (self.player_x, self.player_y))
            else:  # Flip horizontal se a direção for 'left'
                flipped_frame = pygame.transform.flip(self.frames_walk[0], True, False)
                screen.blit(flipped_frame, (self.player_x, self.player_y))
    
    def draw_hitbox(self, screen):
        # hitbox_rect = pygame.Rect(self.player_x, self.player_y + self.frame_height // 2, self.frame_width, self.frame_height // 2)
        hitbox_rect = self.rect()
        pygame.draw.rect(screen, (0, 0, 0), hitbox_rect, 2)  # Desenha a hitbox com borda preta

    def draw_attack_hitbox(self, screen):
        if self.direction == 'right':
            atk_hitbox = pygame.Rect(self.player_x + self.atk_d, self.player_y + self.frame_height // 2, self.frame_width - self.atk_d, self.frame_height // 2)
        else:
            atk_hitbox = pygame.Rect(self.player_x, self.player_y + self.frame_height // 2, self.frame_width - self.atk_d,  self.frame_height // 2)
        pygame.draw.rect(screen, (255, 0, 0), atk_hitbox, 2)
    
    def get_atk_hitbox(self):
        if self.direction == 'right':
            return pygame.Rect(self.player_x + self.atk_d, self.player_y + self.frame_height // 2, self.frame_width - self.atk_d, self.frame_height // 2)
        return pygame.Rect(self.player_x, self.player_y + self.frame_height // 2, self.frame_width - self.atk_d,  self.frame_height // 2)

    def draw_health_bar(self, screen):
        self.health_bar.draw(screen, self.current_health, self.max_health, self.player_x, self.player_y)
    
    def take_damage(self, screen, damage, is_critical):
        # t = Text(self.player_x + 100, self.player_y, size=30, time=700, color=(255,0,0), text=str(damage))
        if is_critical:
            t = TextFadeout('☠'+str(damage * 2), self.player_x + 75, self.player_y, 40, (255, 0, 0), duration=500)
            # print('critical')
            self.damage_frames.add(t)
            self.current_health = self.current_health - 2 * damage
        else:
            t = TextFadeout(str(damage), self.player_x + 75, self.player_y, 20, (255, 0, 0), duration=500)
            self.damage_frames.add(t)
            self.current_health = self.current_health - damage

    def rotate_axe_sprite(self, screen):
        for i in self.rotate_axe:
            i.draw(screen)

    def __repr__(self):
        return self.name

        # screen.blit(self.frames_rotation_axe[self.frame_rotating_axe], (self.axe_x, self.axe_y))