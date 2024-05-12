import pygame
import sys
from src.hero import WarriorSprite, RotatingAxe
from src.GoblinArcher import Goblin
from src.scanario import Block, blocks
from src.text import Text
from src.Square import Square

pygame.init()

# Função principal (main)
def main():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Warrior Game")
    clock = pygame.time.Clock()
    FPS = 60

    text = Text(100, 100, size=30, time=-1)

    warrior_sprite = WarriorSprite()

    goblin = Goblin()

    all_sprites = pygame.sprite.Group()

    current_selected = goblin

    # Loop principal do jogo
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         current_selected.moving = True
            #         current_selected.direction = 'left'
            #     elif event.key == pygame.K_RIGHT:
            #         current_selected.moving = True
            #         current_selected.direction = 'right'
            #     elif event.key == pygame.K_SPACE:
            #         current_selected.attacking = True
            #         current_selected.new_arrow()
            #     elif event.key == pygame.K_w:
            #         sq = Square(200, 300, 1)
            #         all_sprites.add(sq)
            # elif event.type == pygame.KEYUP:
            #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #         current_selected.moving = False

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
                elif event.key == pygame.K_w:
                    sq = Square(200, 300, 1)
                    all_sprites.add(sq)
                elif event.key == pygame.K_q:
                    # warrior_sprite.rotate_axe.x, warrior_sprite.rotate_axe.y = warrior_sprite.player_x, warrior_sprite.player_y
                    warrior_sprite.rotate_axe.append(RotatingAxe(warrior_sprite.player_x, warrior_sprite.player_y + 30, warrior_sprite.direction))
                    warrior_sprite.throwing_axe = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    warrior_sprite.moving = False
        
        # print(goblin.arrows)

        screen.fill((255, 255, 255))

        warrior_sprite.update(FPS)
        warrior_sprite.draw(screen)

        goblin.update()
        goblin.draw(screen)

        all_sprites.update(FPS)

        all_sprites.draw(screen)

        text.draw(screen, f'x:{warrior_sprite.player_x} - y:{warrior_sprite.player_y}')

        for block in blocks:
            block.draw(screen)
            # check if collision is by top, bot, left or right
            if warrior_sprite.rect().colliderect(block.rect):
                # warrior_sprite.player_x = block.rect.left - warrior_sprite.frame_width
                warrior_sprite.player_y = block.rect.top - warrior_sprite.frame_height + 1
                warrior_sprite.dy = 0

        if warrior_sprite.get_atk_hitbox().colliderect(goblin.get_rect()) and warrior_sprite.attacking == True:
            warrior_sprite.can_damage = True
            warrior_sprite.obj_damaged = goblin
        else:
            warrior_sprite.can_damage = False
            warrior_sprite.obj_damaged = None

        # for a in goblin.arrows:
        #     if a.get_rect().colliderect(warrior_sprite.rect()):
        #         goblin.arrows.remove(a)
        #         warrior_sprite.take_damage(screen, goblin.damage)
        #         a.arrow_hitting_sound.play()

        # print([(d.deletable, d.current_time) for d in warrior_sprite.damage_frames])

        pygame.display.flip()
        clock.tick(FPS)  # 60 FPS

    pygame.quit()
    sys.exit()

# Chamar a função principal
if __name__ == "__main__":
    main()