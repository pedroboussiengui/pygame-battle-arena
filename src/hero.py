import pygame

class RotatingAxe:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 20
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
        self.x = self.x + self.speed
        self.frame_rotating_axe = (self.frame_rotating_axe + 1) % (len(self.frames_rotation_axe))
        
    def draw(self, screen):
        screen.blit(self.frames_rotation_axe[self.frame_rotating_axe], (self.x, self.y))

class WarriorSprite:
    def __init__(self):
        self.max_health = 100
        self.current_health = self.max_health

        self.warrior_atk = pygame.image.load('./src/assets/Warrior_1/Attack_1.png')
        self.warrior_walk = pygame.image.load('./src/assets/Warrior_1/Walk.png')

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
        # self.frame_rotating_axe = 0
        self.animation_walk = 0.01
        self.animation_atk = 0.1
        self.last_update = pygame.time.get_ticks()
        self.moving = False
        self.attacking = False
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
    
    def rect(self):
        return pygame.Rect(self.player_x + 30, self.player_y + self.frame_height // 2, self.frame_width-60, self.frame_height // 2)

    def jump(self):
        if self.dy == 0:
            self.dy = -10

    def update(self):
        current_time = pygame.time.get_ticks()
        self.dy += self.gravity
        self.player_y += self.dy
        if current_time - self.last_update > self.animation_walk * 1000:  # converter para milissegundos
            if self.moving:
                self.frame_index_walk = (self.frame_index_walk + 1) % len(self.frames_walk)
                if self.direction == 'right':
                    self.player_x = self.player_x + self.speed
                else:
                     self.player_x = self.player_x - self.speed
            # self.last_update = current_time
        
        if current_time - self.last_update > self.animation_atk * 1000:  # converter para milissegundos
            if self.throwing_axe:
                for i in self.rotate_axe:
                    i.update()
                    if i.x > 700:
                        self.rotate_axe.remove(i)
            if self.attacking:
                self.frame_index_atk = (self.frame_index_atk + 1) % len(self.frames_atk)
                if self.frame_index_atk == len(self.frames_atk) - 1:
                    self.attacking = False
            self.last_update = current_time

    def draw(self, screen):
        self.draw_hitbox(screen)
        self.draw_attack_hitbox(screen)
        self.draw_health_bar(screen, max_health=self.max_health, current_health=self.current_health)
        if self.throwing_axe:
            self.rotate_axe_sprite(screen)
        if self.moving:
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

    def draw_health_bar(self, screen, max_health, current_health):
        # Define as cores da barra de vida
        bar_color = (0, 255, 0)  # Verde para saúde alta
        if current_health <= max_health / 2:
            bar_color = (255, 255, 0)  # Amarelo para saúde moderada
        if current_health <= max_health / 4:
            bar_color = (255, 0, 0)  # Vermelho para saúde baixa

        # Calcula a largura da barra de vida com base na porcentagem de vida restante
        health_percentage = current_health / max_health
        bar_width = int(health_percentage * self.frame_width)

        # Desenha a barra de vida acima do personagem
        health_bar_rect = pygame.Rect(self.player_x, self.player_y + self.frame_height // 2 - 20, bar_width, 5)
        pygame.draw.rect(screen, bar_color, health_bar_rect)
    
    def take_damage(self, damage):
        self.current_health = self.current_health - damage

    def rotate_axe_sprite(self, screen):
        for i in self.rotate_axe:
            i.draw(screen)


        # screen.blit(self.frames_rotation_axe[self.frame_rotating_axe], (self.axe_x, self.axe_y))