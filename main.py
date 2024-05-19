import pygame
import sys
from src.hero import Warrior, RotatingAxe
from src.goblin import Goblin
from src.scanario import Block, blocks
from src.text import Text
from src.Square import Square, TextFadeout
from src.teams import Team

pygame.init()

# Função principal (main)
def main():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Warrior Game")
    clock = pygame.time.Clock()
    FPS = 60

    bg_image = pygame.image.load('./src/assets/background-misterious-jungle.png')
    bg_image = pygame.transform.scale(bg_image, (bg_image.get_width() * 4, bg_image.get_height() * 4))

    all_sprites = pygame.sprite.Group()

    text = Text(100, 100, size=30, time=-1)

    text2 = TextFadeout("Fadeout Text", 300, 200, 36, (255, 0, 0), duration=500)

    all_sprites.add(text2)

    warrior = Warrior()
    goblin = Goblin()
    current_selected = warrior

    team = Team()
    team.add_to_team1(warrior)
    team.add_to_team2(goblin)

    # Loop principal do jogo
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not (current_selected.stunned):
                        current_selected.moving = True
                        current_selected.direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    if not (current_selected.stunned):
                        current_selected.moving = True
                        current_selected.direction = 'right'
                elif event.key == pygame.K_SPACE:
                    current_selected.attack()
                elif event.key == pygame.K_UP:
                    current_selected.jump()
                # elif event.key == pygame.K_q:
                #     current_selected.Q_ability()
                elif event.key == pygame.K_e:
                    if current_selected.cooldown == 0:
                        current_selected.E_ability(goblin)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    current_selected.moving = False


        #     elif event.key == pygame.K_q:
        #         # warrior_sprite.rotate_axe.x, warrior_sprite.rotate_axe.y = warrior_sprite.player_x, warrior_sprite.player_y
        #         warrior_sprite.rotate_axe.append(RotatingAxe(warrior_sprite.player_x, warrior_sprite.player_y + 30, warrior_sprite.direction))
        #         warrior_sprite.throwing_axe = True

        # elif event.key == pygame.K_w:
        #             sq = Square(200, 300, 1)
        #             all_sprites.add(sq)
        
        # print(warrior.damage)

        # print(warrior.get_data())

        # send to server

        # print(f'{warrior.team}')
        # print(warrior.other_team)

        warrior.apply_data(warrior.get_data())

        screen.blit(bg_image, bg_image.get_rect())

        warrior.update(FPS)
        warrior.draw(screen)

        goblin.update(FPS)
        goblin.draw(screen)

        all_sprites.update()

        all_sprites.draw(screen)

        text.draw(screen, f'x:{warrior.player_x} - y:{warrior.player_y}')

        for block in blocks:
            block.draw(screen)
            # check if collision is by top, bot, left or right
            if warrior.rect().colliderect(block.rect):
                # warrior.player_x = block.rect.left - warrior.frame_width
                warrior.player_y = block.rect.top - warrior.frame_height + 1
                warrior.dy = 0
            if goblin.get_rect().colliderect(block.rect):
                # warrior.player_x = block.rect.left - warrior.frame_width
                goblin.pos_y = block.rect.top - goblin.sprint_heigth + 1
                goblin.dy = 0

        # print(warrior.enemies)

        # if warrior.get_atk_hitbox().colliderect(goblin.get_rect()):
        #     warrior.add_enemy(goblin)
        # else:
        #     warrior.remove_enemy(goblin)

        # if warrior.get_atk_hitbox().colliderect(goblin.get_rect()) and warrior.attacking:
        #     warrior.can_damage = True
        #     warrior.obj_damaged = goblin
        # else:
        #     warrior.can_damage = False
        #     warrior.obj_damaged = None


        for a in goblin.arrows:
            if a.get_rect().colliderect(warrior.rect()):
                goblin.arrows.remove(a)
                warrior.take_damage(screen, goblin.damage, a.is_critical)
                a.arrow_hitting_sound.play()

        # print([(d.deletable, d.current_time) for d in warrior_sprite.damage_frames])

        pygame.display.flip()
        clock.tick(FPS)  # 60 FPS

    pygame.quit()
    sys.exit()

# Chamar a função principal
if __name__ == "__main__":
    main()