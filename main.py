import pygame as pg
from random import randint

pg.init() #Входим в библиотеку pygame

#Константы. Настройка окна
FPS = 60 #Частота обновления экрана
WIDTH = 1500 #Ширина дисплея
HEIGHT = 850 #Высота дисплея
WHITE = (255, 255, 255)
#Настройка игрового окна
window = pg.display.set_mode((WIDTH, HEIGHT)) #Игровое окно
clock = pg.time.Clock() #Таймер

#Игровые переменные
run = True
x = 0
y = 0
speed = 6
jump = False
jump_count = -9

direction = 'stop'
game_mode = "menu"

bg_menu = pg.image.load("images/bg_menu.jpg")
bg_menu = pg.transform.scale(bg_menu, (WIDTH, HEIGHT))

bg_game = pg.image.load("images/bg.jpg")
bg_game = pg.transform.scale(bg_game, (WIDTH, HEIGHT))

bg_skins = pg.image.load("images/bg_skins.png")
bg_skins = pg.transform.scale(bg_skins, (WIDTH, HEIGHT))

start_btn = pg.image.load("images/start.png")
start_box = start_btn.get_rect()
start_box.center = (WIDTH//2, HEIGHT//2-200)

select_level = pg.image.load("images/select_level.png")
select_box = select_level.get_rect()
select_box.center = (WIDTH//2, HEIGHT//2-100)

skins = pg.image.load("images/skins.png")
skins_box = skins.get_rect()
skins_box.center = (WIDTH//2, HEIGHT//2)

exit = pg.image.load("images/exit.png")
exit_box = exit.get_rect()
exit_box.center = (WIDTH//2, HEIGHT//2+100)

player_right = pg.image.load("images/player right.png")
player_box = player_right.get_rect()
player_box.left = 50
player_box.bottom = 620

player_left = pg.image.load("images/player left.png")

player_image = player_right

player_1_right = pg.image.load("images/player_1 right.png")
player_1_left = pg.image.load("images/player_1 left.png")

player_2_right = pg.image.load("images/player_2 right.png")
player_2_left = pg.image.load("images/player_2 left.png")

menu_btn = pg.image.load("images/button_menu.png")
menu_btn_box = menu_btn.get_rect()
menu_btn_box.center = (25, 20)

back_menu_btn = pg.image.load("images/menu.png")
back_menu_box = back_menu_btn.get_rect()
back_menu_box.center = (WIDTH//2, HEIGHT//2-60)

continue_btn = pg.image.load("images/continue.png")
continue_btn_box = continue_btn.get_rect()
continue_btn_box.center = (WIDTH//2, HEIGHT//2+60)

platform = pg.image.load("images/platform.png")
platform_box = platform.get_rect()

stay_on = False

coords = [
    (300, 520),
    (600, 450),
    (900, 375),
    (600, 220),
    (1000, 150)
]
platforms = []
platform_on = None

for i in coords:
    platforms.append(pg.Rect(i[0], i[1], platform_box.width, platform_box.height))

print(platforms)

#Сама игра
while run: 
    if game_mode == "menu":

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_box.collidepoint(event.pos):
                        game_mode = 'game'
                if event.button == 1:
                    if exit_box.collidepoint(event.pos):
                        pg.quit()
                if event.button == 1:
                    if skins_box.collidepoint(event.pos):
                        game_mode = "skins"
                direction = 'stop'

        window.blit(bg_menu, (0, 0))
        window.blit(start_btn, start_box)
        window.blit(select_level, select_box)
        window.blit(skins, skins_box)
        window.blit(exit, exit_box)
  
    if game_mode == "game":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    direction = "right"
                    player_image = player_right
                if event.key == pg.K_LEFT:
                    direction = "left"
                    player_image = player_left
                if event.key == pg.K_SPACE and not jump:
                    jump = True
                    jump_count = -9
            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT and direction == "right":
                    direction = "stop"
                if event.key == pg.K_LEFT and direction == "left":
                    direction = "stop"
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu_btn_box.collidepoint(event.pos):
                        game_mode = "pause"

        if direction == "right":
            if player_box.right < WIDTH:
                player_box.centerx += speed
        if direction == "left":
            if player_box.left > 0:
                player_box.centerx -= speed

        if jump:
            stay_on = False
            player_box.centery += jump_count
            jump_count += 0.272
            if player_box.bottom >= 620:
                jump = False

        #отрисовка платформ
        if not stay_on:
            if player_box.bottom <= 620 and not jump:
                player_box.centery += jump_count
                jump_count += 0.272

            for rect in platforms:
                if player_box.colliderect(rect):
                    if player_box.top <= rect.bottom and jump_count < 0:
                        jump_count *= -1
                    elif player_box.bottom >= rect.top:
                        stay_on = True
                        jump = False
                        platform_on = rect
                        break

        else:
            if player_box.left > platform_on.right or player_box.right < platform_on.left:
                stay_on = False    


        window.blit(bg_game, (0, 0))
        window.blit(player_image, player_box)
        window.blit(menu_btn, menu_btn_box)

        for rect in platforms:
            window.blit(platform, rect)

    if game_mode == "skins":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player_box.collidepoint(event.pos):
                        game_mode = "game"
                        player_image = player
                if event.button == 1:
                    if player_box.collidepoint(event.pos):
                        game_mode = "game"
                        player = player

        window.blit(bg_skins, (0, 0))
        # window.blit(player_1, player_1_box)
        # window.blit(player_2, player_2_box)

    if game_mode == "pause":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if continue_btn_box.collidepoint(event.pos):
                        game_mode = 'game'
                        direction = 'stop'
                    if back_menu_box.collidepoint(event.pos):
                        game_mode = 'menu'

        window.blit(continue_btn, continue_btn_box)
        window.blit(back_menu_btn, back_menu_box)
    pg.display.update()
    clock.tick(FPS)

pg.quit()
