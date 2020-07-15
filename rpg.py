import os
import images
import collision
import pygame
import random
import time
import spawn

pygame.init()
window = pygame.display.set_mode((650, 500))
sprites_list = pygame.sprite.Group()

WORD_FONT    = pygame.font.SysFont('comicsans', 40)
HP_FONT      = pygame.font.SysFont('comicsans', 30)
WIDTH        = 15
HEIGHT       = 15
VEL          = 5
MOB_VEL      = 3

#generates wall
def generate_wall(sprites_list, BORDER):
    left_wall   = images.side_wall(40, 10000, 0, 0)
    right_wall  = images.side_wall(40, 500, 460, 0)
    top_wall    = images.top_wall(500, 40, 0, 0)
    bottom_wall = images.top_wall(40, 500, 0, 460)
    for wall in [left_wall, right_wall, top_wall, bottom_wall]:
        sprites_list.add(wall)

def hp_changer(player, mob_attackers, player_attacks):
    for mob in mob_attackers:
        player.hp -= mob.damage
    for attack in player_attacks:
        player_attacks[attack].hp -= player.damage

#creates the map
def map(window, sprites_list, BORDER, player_hp):
    window.fill((255, 255, 255))

    #draws black sidebar
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect((500, 0), (150, 500)))
    #draws the hp bar background
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect((520, 81), (110, 30)))

    #changes the length of the player hp bar depedning on the player's hp
    if int(player_hp) < 20 and int(player_hp) > 0:
        percentage = int(player_hp) / 20
        hp_size    = int( 100 * percentage)
        pygame.draw.rect(window, (255, 0, 0), pygame.Rect((525, 86), (hp_size, 20)))
    elif int(player_hp) <= 0:
        for sprite in sprites_list:
            sprite.kill()
        window.fill((0, 0, 0))
        ending_text = WORD_FONT.render("You died", True, (255, 255, 255))
        window.blit(ending_text, (100, 200))

    else:
        pygame.draw.rect(window, (255, 0, 0), pygame.Rect((525, 86), (100, 20)))


    enemy_hp_bar = WORD_FONT.render("Enemy hp", True, (255, 255, 255))

    if int(player_hp) > 0:
        hp_bar = WORD_FONT.render("Player hp", True, (255, 255, 255))
        window.blit(hp_bar, (510, 50))
        hp = HP_FONT.render(str(player_hp) + " / 20", True, (200, 200, 200))
        window.blit(hp, (545, 88))

    if BORDER == 0:
        generate_wall(sprites_list, BORDER)
    sprites_list.draw(window)
    pygame.display.flip()
    return 1

def play():
    BORDER = 0
    mob_dict      = {}
    WAVES         = 0
    mobs          = []
    attacks       = {}
    run           = True
    p1            = spawn.player()
    sprites_list.add(p1)

    while run:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

        p1_hp_change  = []
        mob_hp_change = {}

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            p1.move_left(VEL, p1, mobs)
        if keys[pygame.K_RIGHT]:
            p1.move_right(VEL, p1, mobs)
        if keys[pygame.K_UP]:
            p1.move_up(VEL, p1, mobs)
        if keys[pygame.K_DOWN]:
            p1.move_down(VEL, p1, mobs)

        if WAVES != 0 and mobs == []:
            WAVES -= 1
            spawn.spawn_mobs(mobs, p1, sprites_list, mob_dict)
        else:
            for mob in mobs:
                entities = mobs[:]
                entities.append(p1)
                entities.remove(mob)
                attack = mob.move(MOB_VEL, entities, mob, p1)
                if attack != None:
                   p1_hp_change.append(attack)


        if pygame.mouse.get_pressed() == (True, False, False):
            position = pygame.mouse.get_pos()
            attack   = images.player_attack(WIDTH, HEIGHT, p1.rect.x, p1.rect.y)
            if position[0] > p1.rect.x and position[1] > p1.rect.y:
                #fourth quadrant
                RUN   = position[0] - p1.rect.x
                RISE  = position[1] - p1.rect.y
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant4", SLOPE]
                sprites_list.add(attack)
            elif position[0] < p1.rect.x and position[1] < p1.rect.y:
                #second quadrant
                RUN   = p1.rect.x - position[0]
                RISE  = p1.rect.y - position[1]
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant2", SLOPE]
                sprites_list.add(attack)
            elif position[0] < p1.rect.x and position[1] > p1.rect.y:
                #third quadrant
                RUN   = p1.rect.x - position[0]
                RISE  = position[1] - p1.rect.y
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant3", SLOPE]
                sprites_list.add(attack)
            elif position[0] > p1.rect.x and position[1] < p1.rect.y:
                #first quadrant
                RUN   = position[0] - p1.rect.x
                RISE  = p1.rect.y - position[1]
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant1", SLOPE]
                sprites_list.add(attack)
            elif position[0] == p1.rect.x and position[1] > p1.rect.y:
                #y-axis bottom
                attacks[attack] = ["verticaldown", 2]
                sprites_list.add(attack)
            elif position[0] == p1.rect.x and position[1] < p1.rect.y:
                #y-axis top
                attacks[attack] = ["verticalup", 2]
                sprites_list.add(attack)
            elif position[0] > p1.rect.x and position[1] == p1.rect.y:
                #x-axis right
                attacks[attack] = ["horizontalright", 2]
                sprites_list.add(attack)
            elif position[0] < p1.rect.x and position[1] == p1.rect.y:
                #x-axis left
                attacks[attack] = ["horizontalleft", 2]
                sprites_list.add(attack)

        for attack in attacks.keys():
            if attacks[attack][0] == "quadrant1":
                p1_attack = attack.quadrant1(attacks[attack][1], mobs, attack, sprites_list)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "quadrant2":
                p1_attack = attack.quadrant2(attacks[attack][1], mobs, attack, sprites_list)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "quadrant3":
                p1_attack = attack.quadrant3(attacks[attack][1], mobs, attack, sprites_list)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "quadrant4":
                p1_attack = attack.quadrant4(attacks[attack][1], mobs, attack, sprites_list)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "verticaldown":
                p1_attack = attack.verticaldown(attacks[attack][1], mobs, attack, sprites_list)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "verticalup":
                p1_attack = attack.verticalup(attacks[attack][1], mobs, attack, sprites_list)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "horizontalright":
                p1_attack = attack.horizontalright(attacks[attack][1], mobs, attack, sprites_list)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "horizontalleft":
                p1_attack = attack.horizontalleft(attacks[attack][1], mobs, attack, sprites_list)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack

        sprites_list.update()
        hp_changer(p1, p1_hp_change, mob_hp_change)

        BORDER = map(window, sprites_list, BORDER, p1.hp)
        clock.tick(60)

    pygame.quit()
clock=pygame.time.Clock()
play()
