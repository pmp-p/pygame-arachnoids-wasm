import asyncio

import pygame
import math
from pygame.locals import K_w, K_s, K_a, K_d, KEYDOWN, MOUSEBUTTONDOWN
from spider import Spider, SIZE
from projectile import Projectile
from enemy import Enemy
from node import Node


pygame.init()
pygame.mixer.init()

async def main():

    # 800x600 -> 50x50px sprites -> 10x10 board = 500x50a0px board
    game_screen = pygame.display.set_mode([800, 600])
    pygame.display.set_caption("Arachnoids")
    clock = pygame.time.Clock()

    BG = pygame.image.load("gfx/background.png").convert()
    TITLE = pygame.image.load("gfx/title_screen.png").convert()
    HOW_TO = pygame.image.load("gfx/how_to.png").convert()
    END_SCREEN = pygame.image.load("gfx/end_screen.png").convert()


    game_spider = Spider()
    nodes = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    def start_nodes() -> None:
        nodes.empty()
        # initial node grid
        for i in range(10):
            for j in range(10):
                node = Node(i,j)
                nodes.add(node)
                if (i,j) in ((2,4), (2,5), (2,3), (3,4), (1,4),
                (1,3), (1,5), (3,3), (3,5)): # initial grid
                    node.visible = True

    start_nodes()

    for i in range(10):
        for j in range(10):
            node = Node(i,j)
            nodes.add(node)
            if (i,j) in ((2,4), (2,5), (2,3), (3,4), (1,4),
            (1,3), (1,5), (3,3), (3,5)): # initial grid
                node.visible = True

    game_wave = 5
    wave_number = 1

    bullets = pygame.sprite.Group()


    BUTTON_SFX = pygame.mixer.Sound("sfx/button_select.ogg")
    WAVE_SFX = pygame.mixer.Sound("sfx/new_wave.ogg")
    BULLET_SFX = pygame.mixer.Sound("sfx/projectile_shoot.ogg")
    DEATH_SFX = pygame.mixer.Sound("sfx/spider_death.ogg")

    GAME_FONT = pygame.font.Font("gfx/FiraCode-VariableFont_wght.ttf", 20)

    wave_count = 0
    running = True
    title_screen = True
    howto_screen = False
    game_over = False
    while running:

        if title_screen:
            start_button = pygame.Rect(320, 220, 160, 80)
            howto_button = pygame.Rect(320, 327, 160, 80)
            exit_button = pygame.Rect(320, 434, 160, 80)
            if howto_screen:
                game_screen.blit(HOW_TO, (0,0))
            else:
                game_screen.blit(TITLE, (0,0))

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.collidepoint(mouse_pos) and not howto_screen:
                        title_screen = False
                        pygame.mixer.Sound.play(BUTTON_SFX)
                    elif howto_button.collidepoint(mouse_pos) and not howto_screen:
                        howto_screen = True
                        pygame.mixer.Sound.play(BUTTON_SFX)
                    elif exit_button.collidepoint(mouse_pos) and not howto_screen:
                        pygame.quit()
                        pygame.mixer.Sound.play(BUTTON_SFX)
                    elif howto_screen:
                        howto_screen = False
                        pygame.mixer.Sound.play(BUTTON_SFX)
                elif event.type == pygame.QUIT:
                    pygame.quit()

        elif not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # elif event.type == KEYDOWN:
                #     if event.key == K_w:
                #         game_spider.update("up", nodes)
                #     elif event.key == K_s:
                #         game_spider.update("down", nodes)
                #     elif event.key == K_a:
                #         game_spider.update("left", nodes)
                #     elif event.key == K_d:s
                #         game_spider.update("right", nodes)

                elif event.type == MOUSEBUTTONDOWN and game_spider.living:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    vector_x, vector_y = mouse_x - game_spider.x, mouse_y - game_spider.y
                    bullet_angle = math.degrees(math.atan2(-vector_y, +vector_x))

                    # rotating the spider
                    game_spider.rotate(bullet_angle)

                    # creating the Projectile
                    bullets.add(Projectile(game_spider.x + SIZE // 2,
                                            game_spider.y + SIZE // 2,
                                            vector_x, vector_y,
                                            bullet_angle))

                    pygame.mixer.Sound.play(BULLET_SFX)

            keys = pygame.key.get_pressed()
            directions = []
            if keys[K_w] and not keys[K_s]:
                directions.append("up")
            if keys[K_s] and not keys[K_w]:
                directions.append("down")
            if keys[K_a] and not keys[K_d]:
                directions.append("left")
            if keys[K_d] and not keys[K_a]:
                directions.append("right")

            if game_spider.living: game_spider.update(directions, nodes)

            game_screen.blit(BG, (0,0))
            n: Node
            for n in nodes:
                if n.visible == True:
                    n.show(game_screen)

            bullet: Projectile
            for bullet in bullets:
                if bullet.x > 800 or bullet.x < 0 or bullet.y > 600 or bullet.y < 0 or bullet.time > 50:
                    bullets.remove(bullet)
                else:
                    bullet.time += 1
                    n: Node
                    for n in nodes:
                        if bullet.rect.collidepoint(n.rect.x + 25, n.rect.y + 25):
                            n.visible = True

                    e: Enemy
                    for e in enemies:
                        if e.rect.colliderect(bullet.rect):
                            enemies.remove(e)
                            game_spider.score += 10
                    bullet.update()
                    bullet.show(game_screen)

            enemy: Enemy
            if len(enemies) == 0:
                if game_wave == 5:
                    for i in range (game_wave): enemies.add(Enemy())
                    game_wave += 5
                elif wave_count > 100:
                    for i in range (game_wave): enemies.add(Enemy())
                    if game_wave < 30: game_wave += 5
                    wave_number += 1
                    wave_count = 0
                    pygame.mixer.Sound.play(WAVE_SFX)
                else: wave_count += 1
            for enemy in enemies:
                if enemy.rect.colliderect(game_spider.rect) and game_spider.living and game_spider.respawn_count == 0:
                    game_spider.lives -= 1
                    game_spider.living = False
                    pygame.mixer.Sound.play(DEATH_SFX)
                n: Node
                for n in nodes:
                    if enemy.rect.collidepoint(n.rect.x + 25, n.rect.y + 25) and game_spider.living:
                        n.visible = False
                else:
                    enemy.update()
                    enemy.show(game_screen)

            if game_spider.lives < 1:
                game_over = True

            if game_spider.living:
                game_spider.show(game_screen)

                # respawn temporary invicibility
                if game_spider.respawn_count > 0:
                    game_spider.respawn_count -= 1
            else:
                if game_spider.respawn_count < 100:
                    game_spider.respawn_count += 1
                else:
                    game_spider.living = True
            display_score = GAME_FONT.render(str(game_spider.score),
                            True, (255, 255, 255))
            game_screen.blit(display_score, (19,83))
            display_wave = GAME_FONT.render(str(wave_number),
                            True, (255, 255, 255))
            game_screen.blit(display_wave, (19,170))

            display_lives = GAME_FONT.render(str(game_spider.lives),
                            True, (255, 255, 255))
            game_screen.blit(display_lives, (19,269))

            clock.tick(30)


        elif game_over:
            return_button = pygame.Rect(320, 434, 160, 80)
            game_screen.blit(END_SCREEN, (0,0))
            display_score = GAME_FONT.render(str(game_spider.score),
                            True, (255, 255, 255))
            game_screen.blit(display_score, (436, 270))
            display_wave = GAME_FONT.render(str(wave_number),
                            True, (255, 255, 255))
            game_screen.blit(display_wave, (436,330))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if return_button.collidepoint(mouse_pos):
                        pygame.mixer.Sound.play(BUTTON_SFX)
                        game_over, title_screen = False, True
                        game_spider.score = 0
                        game_spider.x = 250
                        game_spider.y = 250
                        game_spider.update([], nodes)
                        game_spider.living = True
                        game_wave = 5
                        wave_number = 1
                        game_spider.lives = 3
                        start_nodes()
                        enemies.empty()
                        bullets.empty()

        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())


