import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
pygame.display.set_caption("My Pygame Window")

TIMEREVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENT, 1000)  # 1 second = 1000 milliseconds

warrior_atk = pygame.image.load('./src/assets/Warrior_1/Attack_1.png')

warrior_walk = pygame.image.load('./src/assets/Warrior_1/Walk.png')

frame_width = 96
frame_height = 96

frames_atk = []
for x in range(0, warrior_atk.get_width(), frame_width):
    frame = warrior_atk.subsurface(pygame.Rect(x, 0, frame_width, frame_height))
    frames_atk.append(frame)

frames_walk = []
for x in range(0, warrior_atk.get_width(), frame_width):
    frame = warrior_walk.subsurface(pygame.Rect(x, 0, frame_width, frame_height))
    frames_walk.append(frame)

# sprite1 = MySprite('./src/assets/Warrior_1/Attack_1.png', 96, 0*96)

frame_index_walk = 0
frame_index_atk = 0
animation_speed = 0.2  # 0.1 segundos por quadro
last_update = pygame.time.get_ticks()
moving = False
attacking = False
# attack_done = False  # Flag para indicar se o ataque foi concluído

# Posição inicial do personagem
player_x = 100
player_y = 300

speed = 0

# Main game loop
running = True
while running:
    screen.fill((255, 255, 255))
    current_time = pygame.time.get_ticks()
    if current_time - last_update > animation_speed * 1000:  # converter para milissegundos
        if moving:
            frame_index_walk = (frame_index_walk + 1) % len(frames_walk)
            player_x = player_x + speed
        if attacking:
            frame_index_atk = (frame_index_atk + 1) % len(frames_atk)
            if frame_index_atk == 3:
                attacking = False
        last_update = current_time

    # Verificar eventos do Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving = True
                speed = -10
            elif event.key == pygame.K_RIGHT:
                moving = True
                speed = 10
            elif event.key == pygame.K_SPACE and not attacking:
                attacking = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                moving = False

    # Limpar a tela
    screen.fill((255, 255, 255))

    # Desenhar o quadro atual da animação
    if moving:
        screen.blit(frames_walk[frame_index_walk], (player_x, player_y))
    elif attacking:
        screen.blit(frames_atk[frame_index_atk], (player_x, player_y))
    else:
        # Desenhar o personagem parado
        screen.blit(frames_walk[0], (player_x, player_y))

    # Atualizar tela
    pygame.display.flip()

    # Controlar a velocidade de atualização
    clock.tick(60)  # 60 FPS

# Quit Pygame properly
pygame.quit()
sys.exit()
