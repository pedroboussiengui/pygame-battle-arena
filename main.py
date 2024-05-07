import pygame
import sys
from src.hero import WarriorSprite  # Importar a classe WarriorSprite do arquivo separado

pygame.init()

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
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    warrior_sprite.moving = False
                # elif event.key == pygame.K_SPACE:
                #     warrior_sprite.attacking = False

        screen.fill((255, 255, 255))

        warrior_sprite.update()
        warrior_sprite.draw(screen)

        pygame.display.flip()
        clock.tick(30)  # 30 FPS

    pygame.quit()
    sys.exit()

# Chamar a função principal
if __name__ == "__main__":
    main()