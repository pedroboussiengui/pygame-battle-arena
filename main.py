import pygame
import sys
from src.hero import WarriorSprite  # Importar a classe WarriorSprite do arquivo separado
from src.scanario import Block, blocks
from src.text import Text

pygame.init()

text = Text(100, 100)

# Função principal (main)
def main():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Warrior Game")
    clock = pygame.time.Clock()

    warrior_sprite = WarriorSprite()

    # Loop principal do jogo
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    warrior_sprite.moving = True
                    warrior_sprite.direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    warrior_sprite.moving = True
                    warrior_sprite.direction = 'right'
                elif event.key == pygame.K_SPACE:
                    warrior_sprite.attacking = True
                elif event.key == pygame.K_UP:
                    warrior_sprite.jump()
                elif event.key == pygame.K_q:
                    warrior_sprite.throwing_axe = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    warrior_sprite.moving = False
                # elif event.key == pygame.K_SPACE:
                #     warrior_sprite.attacking = False

        screen.fill((255, 255, 255))

        warrior_sprite.update()
        warrior_sprite.draw(screen)

        text.draw(screen, f'x:{warrior_sprite.player_x} - y:{warrior_sprite.player_y}')

        for block in blocks:
            block.draw(screen)
            # check if collision is by top, bot, left or right
            if warrior_sprite.rect().colliderect(block.rect):
                # warrior_sprite.player_x = block.rect.left - warrior_sprite.frame_width
                warrior_sprite.player_y = block.rect.top - warrior_sprite.frame_height + 1
                warrior_sprite.dy = 0


        pygame.display.flip()
        clock.tick(30)  # 30 FPS

    pygame.quit()
    sys.exit()

# Chamar a função principal
if __name__ == "__main__":
    main()