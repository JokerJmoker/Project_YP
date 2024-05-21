import pygame
from random import randint

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Shooting Stars")

icon_app = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon_app)

bg = pygame.image.load('images/background.png').convert_alpha()
bg_sound = pygame.mixer.Sound('sounds/04.Battle.mp3')
bg_sound.play()

label = pygame.font.Font('fonts/Montserrat-Thin.ttf', 40)
loose_label = label.render('Вы проиграли', False, (193, 196, 77))
restart_label = label.render('заново', False, (193, 96, 77))
restart_label_rect = restart_label.get_rect(topleft=(180, 200))

meteor = pygame.image.load('images/meteor.png').convert_alpha()
meteor_timer = pygame.USEREVENT + 1
pygame.time.set_timer(meteor_timer, 3000)

ammo_meteor = pygame.image.load('images/ammo_meteor.png').convert_alpha()
ammo_meteor_timer = pygame.USEREVENT + 2
pygame.time.set_timer(ammo_meteor_timer, 4000)

fuel_meteor = pygame.image.load('images/fuel_meteor.png').convert_alpha()
fuel_meteor_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fuel_meteor_timer, 5000)

meteor_list = []
ammo_meteor_list = []
fuel_meteor_list = []

charge = pygame.image.load('images/Charge_1.png').convert_alpha()
ammo = []

charge_left = 5

move_sheep = [
    pygame.image.load('images/move/1.png').convert_alpha(),
    pygame.image.load('images/move/2.png').convert_alpha(),
    pygame.image.load('images/move/3.png').convert_alpha(),
    pygame.image.load('images/move/4.png').convert_alpha(),
    pygame.image.load('images/move/5.png').convert_alpha(),
    pygame.image.load('images/move/6.png').convert_alpha()
]

sheep_speed = 6
sheep_x = 220
sheep_y = 450

is_boost = False
boost_cnt = 7
is_boost_r = False
boost_cnt_r = 7
is_boost_l = False
boost_cnt_l = 7

move_sheep_cnt = 0
bg_y = 0
gameplay = True
running = True

# Добавляем начальное время и продолжительность таймера
start_time = pygame.time.get_ticks()
fuel_remaining = 15000  # 15 секунд в миллисекундах

while running:

    clock.tick(20)

    screen.blit(bg, (0, bg_y))
    screen.blit(bg, (0, bg_y - 640))

    if gameplay:
        screen.blit(move_sheep[move_sheep_cnt], (sheep_x, sheep_y))

        sheep_rect = move_sheep[0].get_rect(topleft=(sheep_x, sheep_y))

        if meteor_list:
            for (i, el) in enumerate(meteor_list):
                screen.blit(meteor, el)
                el.y += 10

                if el.y > 700:
                    meteor_list.pop(i)

                if sheep_rect.colliderect(el):
                    gameplay = False

        if ammo_meteor_list:
            for (i, el) in enumerate(ammo_meteor_list):
                screen.blit(ammo_meteor, el)
                el.y += 10

                if el.y > 700:
                    ammo_meteor_list.pop(i)

                if sheep_rect.colliderect(el) and boost_cnt != 7:
                    charge_left += randint(1, 5)
                    ammo_meteor_list.pop(i)  # Remove ammo_meteor on collision with the ship
                elif sheep_rect.colliderect(el):
                    gameplay = False

        if fuel_meteor_list:
            for (i, el) in enumerate(fuel_meteor_list):
                screen.blit(fuel_meteor, el)
                el.y += 10

                if el.y > 700:
                    fuel_meteor_list.pop(i)

                if sheep_rect.colliderect(el) and boost_cnt != 7:
                    fuel_remaining += 5000  # Добавляем 5 секунд (5000 миллисекунд)
                    fuel_meteor_list.pop(i) 
                elif sheep_rect.colliderect(el):
                    gameplay = False


        if move_sheep_cnt == 5:
            move_sheep_cnt = 0
        else:
            move_sheep_cnt += 1

        if bg_y == 640:
            bg_y = 0
        else:
            bg_y += 2

        keys = pygame.key.get_pressed()

        

        if keys[pygame.K_LEFT] and sheep_x > -50:
            sheep_x -= sheep_speed
        elif keys[pygame.K_RIGHT] and sheep_x < 550:
            sheep_x += sheep_speed
        elif keys[pygame.K_UP]:
            sheep_y -= sheep_speed
        elif keys[pygame.K_DOWN]:
            sheep_y += sheep_speed

        if ammo:
            for (i, el) in enumerate(ammo):
                screen.blit(charge, (el.x, el.y))
                el.y -= 10

                if el.y < -10:
                    ammo.pop(i)
                    continue  # Пропускаем остальную часть цикла, чтобы избежать обработки удаленного элемента

                if meteor_list:
                    for (index, meteor_el) in enumerate(meteor_list):
                        if el.colliderect(meteor_el):
                            meteor_list.pop(index)
                            try:
                                ammo.pop(i)
                            except IndexError:
                                pass
                if ammo_meteor_list:
                    for (index, ammo_meteor_el) in enumerate(ammo_meteor_list):
                        if el.colliderect(ammo_meteor_el):
                            ammo_meteor_list.pop(index)
                            try:
                                ammo.pop(i)
                            except IndexError:
                                pass
                if fuel_meteor_list:
                    for (index, fuel_meteor_el) in enumerate(fuel_meteor_list):
                        if el.colliderect(fuel_meteor_el):
                            fuel_meteor_list.pop(index)
                            try:
                                ammo.pop(i)
                            except IndexError:
                                pass


        if not is_boost:
            if keys[pygame.K_SPACE]:
                is_boost = True
        else:
            if boost_cnt >= -7:
                if boost_cnt > 0:
                    sheep_y -= (boost_cnt ** 2) / 2
                else:
                    sheep_y += (boost_cnt ** 2) / 2
                boost_cnt -= 1
            else:
                is_boost = False
                boost_cnt = 7
        """
        if not is_boost_r:
            if keys[pygame.K_BACKSPACE &   pygame.K_RIGHT]:
                is_boost_r = True
        else:
            if boost_cnt_r >= -7 :
                if boost_cnt_r > 0:
                    sheep_x += (boost_cnt_r **2)/2
                else:
                    sheep_x -= (boost_cnt_r  **2) /2
                boost_cnt_r -= 1
            else:
                is_boost_r = False
                boost_cnt_r = 7

        if not is_boost_l:
            if keys[pygame.K_BACKSPACE &  pygame.K_LEFT]:
                is_boost_l = True
        else:
            if boost_cnt_l >= -7 :
                if boost_cnt_l > 0:
                    sheep_x -= (boost_cnt_l  **2) /2
                else:
                    sheep_x += (boost_cnt_l  **2) /2
                boost_cnt_l -= 1
            else:
                is_boost_l = False
                boost_cnt_l = 7
        """



        # Отслеживаем и отображаем оставшееся время
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, (fuel_remaining - elapsed_time) // 1000)
        timer_label = label.render(f'топлива осталось на: {remaining_time} км', False, (255, 255, 255))
        screen.blit(timer_label, (80, 580))

        # Завершаем игру, если время истекло
        if elapsed_time >= fuel_remaining:
            gameplay = False

    else:
        screen.fill((87, 89, 89))
        screen.blit(loose_label, (180, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            sheep_x = 220
            sheep_y = 450
            meteor_list.clear()
            ammo_meteor_list.clear()
            ammo.clear()
            charge_left = 0
            charge_left = 5
            fuel_meteor_list.clear()
            start_time = pygame.time.get_ticks()  # Сбрасываем таймер
            fuel_remaining = 15000  # Сбрасываем топливо на 15 секунд

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == meteor_timer:
            for _ in range(randint(1, 8)):
                while True:
                    meteor_x = randint(0, 600)  # Randomize meteor position
                    meteor_y = randint(-500, -70)
                    new_meteor_rect = meteor.get_rect(topleft=(meteor_x, meteor_y))
                    if not any(new_meteor_rect.colliderect(existing) for existing in meteor_list):
                        meteor_list.append(new_meteor_rect)
                        break
        if event.type == ammo_meteor_timer:
            while True:
                ammo_meteor_x = randint(0, 600)  # Randomize ammo meteor position
                new_ammo_meteor = ammo_meteor.get_rect(topleft=(ammo_meteor_x, -30))
                if not any(new_ammo_meteor.colliderect(existing) for existing in ammo_meteor_list):
                    ammo_meteor_list.append(new_ammo_meteor)
                    break
        if event.type == fuel_meteor_timer:
            while True:
                fuel_meteor_x = randint(0, 600)  # Randomize fuel meteor position
                new_fuel_meteor = fuel_meteor.get_rect(topleft=(fuel_meteor_x, -30))
                if not any(new_fuel_meteor.colliderect(existing) for existing in fuel_meteor_list):
                    fuel_meteor_list.append(new_fuel_meteor)
                    break
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT and charge_left > 0:
            ammo.append(charge.get_rect(topleft=(sheep_x + 18 , sheep_y)))
            charge_left -= 1
