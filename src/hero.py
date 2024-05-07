import pygame

class WarriorSprite:
    def __init__(self):
        self.max_health = 100
        self.current_health = self.max_health

        self.warrior_atk = pygame.image.load('./src/assets/Warrior_1/Attack_1.png')
        self.warrior_walk = pygame.image.load('./src/assets/Warrior_1/Walk.png')

        self.rotating_axe = pygame.image.load('./src/assets/Red Axe sprite.png')

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

        self.frames_rotation_axe = []
        for row in range(3):
            for col in range(3):
                if (row == 2 and col == 2):
                    break
                x = col * self.rotating_axe.get_width() // 3
                y = row * self.rotating_axe.get_height() // 3
                print(x, y)
                sprite = self.rotating_axe.subsurface(pygame.Rect(x, y, self.rotating_axe.get_width() // 3, self.rotating_axe.get_height() // 3))
                scaled_sprite = pygame.transform.scale(sprite, (self.rotating_axe.get_width() // 3 * 0.1, self.rotating_axe.get_height() // 3 * 0.1))
                self.frames_rotation_axe.append(scaled_sprite)

        self.frame_index_walk = 0
        self.frame_index_atk = 0
        self.frame_rotating_axe = 0
        self.animation_walk = 0.1
        self.animation_atk = 0.1
        self.last_update = pygame.time.get_ticks()
        self.moving = False
        self.attacking = False
        self.direction = 'right'  # Direção inicial do personagem

        self.player_x = 100
        self.player_y = 300
        self.speed = 25

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_walk * 1000:  # converter para milissegundos
            if self.moving:
                self.frame_index_walk = (self.frame_index_walk + 1) % len(self.frames_walk)
                if self.direction == 'right':
                    self.player_x = self.player_x + self.speed
                else:
                     self.player_x = self.player_x - self.speed
            # self.last_update = current_time
        
        if current_time - self.last_update > self.animation_atk * 1000:  # converter para milissegundos
            self.frame_rotating_axe = (self.frame_rotating_axe + 1) % (len(self.frames_rotation_axe))
            if self.attacking:
                self.frame_index_atk = (self.frame_index_atk + 1) % len(self.frames_atk)
                if self.frame_index_atk == len(self.frames_atk) - 1:
                    self.attacking = False
            self.last_update = current_time

    def draw(self, screen):
        self.draw_hitbox(screen)
        self.draw_health_bar(screen, max_health=self.max_health, current_health=self.current_health)
        self.rotation_axe(screen)
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
        hitbox_rect = pygame.Rect(self.player_x, self.player_y + self.frame_height // 2, self.frame_width, self.frame_height // 2)
        pygame.draw.rect(screen, (0, 0, 0), hitbox_rect, 2)  # Desenha a hitbox com borda preta

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

    
    def rotation_axe(self, screen):
        screen.blit(self.frames_rotation_axe[self.frame_rotating_axe], (self.player_x, self.player_y - 250))
