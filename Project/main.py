import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((640,640)) 
pygame.display.set_caption(" Shooting Stars")

icon_app = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon_app)

# заготовка области для заднего фона , шрифтов и тд 

"""
myfont = pygame.font.Font('fonts/Montserrat-Thin.ttf', 40)
test_surface = myfont.render(' test font', False , 'purple')
"""


bg = pygame.image.load('images/background.png').convert_alpha()

bg_sound = pygame.mixer.Sound('sounds/04.Battle.mp3')

bg_sound.play()

label = pygame.font.Font('fonts/Montserrat-Thin.ttf', 40)
loose_label = label.render(' Вы проиграли ', False , (193,196,77))
restart_label = label.render(' заново ', False , (193,96,77))
restart_label_rect= restart_label.get_rect(topleft = (180, 200))


# варги 
meteor = pygame.image.load('images/meteor.png').convert_alpha()

meteor_y = -30
meteor_x = 220

meteor_timer = pygame.USEREVENT + 1
pygame.time.set_timer(meteor_timer , 3000 )

meteor_list = []

# корабль выстрел

charge = pygame.image.load('images/Charge_1.png').convert_alpha()
ammo = []

charge_left = 5 
# облсть для анимаций корабля 1 

move_sheep = [
    pygame.image.load('images/move/1.png').convert_alpha(),
    pygame.image.load('images/move/2.png').convert_alpha(),
    pygame.image.load('images/move/3.png').convert_alpha(),
    pygame.image.load('images/move/4.png').convert_alpha(),
    pygame.image.load('images/move/5.png').convert_alpha(),
    pygame.image.load('images/move/6.png').convert_alpha()
]

# перемещения 

sheep_speed = 5

sheep_x = 220
sheep_y = 450

is_boost = False
boost_cnt = 7 

# область для разных счетчиков
move_sheep_cnt = 0

bg_y = 0


gameplay = True

running = True

while running:

    clock.tick(20)

    
    # отрисовка элементов

    screen.blit(bg, (0,bg_y))
    screen.blit(bg, (0, bg_y - 640))

    if gameplay:

        screen.blit(move_sheep[move_sheep_cnt], (sheep_x,sheep_y)) # sheep 


        sheep_rect = move_sheep[0].get_rect(topleft =(sheep_x, sheep_y)) # квадрат / здесь надо исправиьт png 
        meteor_rect = meteor.get_rect(topleft =(meteor_x, meteor_y))

        #---------------- условия на контакт с врагом

        if meteor_list:
            for (i, el) in enumerate(meteor_list):
                screen.blit(meteor, el)
                el.y += 10 
        
                if el.y > 700 :
                    meteor_list.pop(i)

                if sheep_rect.colliderect(el):
                    gameplay = False

        #---------------- условия на анимации

        if move_sheep_cnt == 5:
            move_sheep_cnt =0
        else:
            move_sheep_cnt += 1


        if bg_y == 640:
            bg_y = 0 
        else:
            bg_y += 2

    
        # отслеживания 
        


        # доделать условия 
        keys = pygame.key.get_pressed()


        if keys[pygame.K_LEFT] and sheep_x > 0:
            sheep_x -= sheep_speed 
        elif keys[pygame.K_RIGHT] and sheep_x < 500:
            sheep_x += sheep_speed 
        elif keys[pygame.K_UP]  :
            sheep_y -= sheep_speed 
        elif keys[pygame.K_DOWN]   :
            sheep_y += sheep_speed
        ### реализовать ускорение + анимации + логику + выстерлы...
        """
        if keys[pygame.K_LEFT]  :
            screen.blit( "массив с анимациями + индекс", (sheep_x,sheep_y))
        elif keys[pygame.K_RIGHT]  :
            screen.blit( "массив с анимациями + индекс", (sheep_x,sheep_y))
        """
        #### уже сверху будут анимации поворота, причем проигрываться один раз 


        # выстрел 

        if ammo:
            for ( i, el)  in enumerate(ammo):
                screen.blit(charge, (el.x , el.y))
                el.y -= 5

                if el.y < -10:
                    ammo.pop(i)

                if meteor_list:
                    for (index , meteor_el) in enumerate(meteor_list):
                        if el.colliderect(meteor_el):
                            meteor_list.pop(index)
                            ammo.pop(i)
                    




        # логика буста бессмыслена пока( в общем это таран, которым можно быстро сбивать предметы с топливом и патронами ), но на ее примере надо реализовать резкие уклонения в стороны 

        # неверно работает , но как пример норм 
        if not is_boost:
            if keys[pygame.K_SPACE]:
                is_boost = True
        else:
            if boost_cnt >= -7 :
                if boost_cnt > 0:
                    sheep_y -= (boost_cnt ** 2) / 2 
                else:
                    sheep_y += (boost_cnt ** 2) / 2 
                boost_cnt -= 1
            else: 
                is_boost = False
                boost_cnt = 0 
    else:
        screen.fill((87,89,89))
        screen.blit(loose_label,(180,100))
        screen.blit(restart_label,restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]: # исправить 
            gameplay = True 
            sheep_x = 220
            sheep_y = 450
            meteor_list.clear()
            ammo.clear()
    



    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == meteor_timer:      
            meteor_list.append(meteor.get_rect(topleft=(meteor_x , meteor_y)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT and charge_left > 0:
            ammo.append(charge.get_rect(topleft=(sheep_x + 80 ,sheep_y )))  # из-за плохой пнг корабля +80, потом убрать 
            charge_left -= 1