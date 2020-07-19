import os
import store
import images
import collision
import pygame
import random
import time
import spawn

pygame.init()
window        = pygame.display.set_mode((650, 500))
sprites_list  = pygame.sprite.Group()
COSTS_FONT    = pygame.font.SysFont("comicsans", 20)
PURCHASE_FONT = pygame.font.SysFont("comicsans", 25)
MENU_FONT     = pygame.font.SysFont("comicsans", 30) 
WORD_FONT     = pygame.font.SysFont('comicsans', 40)
DEATH_FONT    = pygame.font.SysFont("comicsans", 100)
HP_FONT       = pygame.font.SysFont('comicsans', 30)
OPTIONS_FONT  = pygame.font.SysFont("comicsans", 50)
OPTIONS_FONT.set_underline(True)
WIDTH         = 15
HEIGHT        = 15
VEL           = 5
MOB_VEL       = 3

def hp_changer(player, mob_attackers, player_attacks):
    for mob in mob_attackers:
        player.hp -= mob.damage
    for attack in player_attacks:
        player_attacks[attack].hp -= player.damage

def play():
    BORDER      = False
    STORE       = False
    STORE_ADDED = False
    DEAD        = False
    mob_dict    = {}
    WAVES       = 2
    mobs        = []
    attacks     = {}
    run         = True
    p1          = spawn.player()
    sprites_list.add(p1)

    while run:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

        attacks_remove = []
        p1_hp_change   = []
        mob_hp_change  = {}

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


        if keys[pygame.K_SPACE] and not len(attacks.keys()) >= 7:
            attack   = images.player_attack(WIDTH, HEIGHT, p1.rect.x, p1.rect.y)
            closest = [None, 1000000000]
            for mob in mobs:
                if mob.rect.x > p1.rect.x and mob.rect.y > p1.rect.y:
                    if ((mob.rect.x - p1.rect.x) ** 2 + (mob.rect.y - p1.rect.y) ** 2) ** 0.5 < closest[1]:
                        closest = [mob, ((mob.rect.x - p1.rect.x) ** 2 + (mob.rect.y - p1.rect.y) ** 2) ** 0.5]
                elif mob.rect.x < p1.rect.x and mob.rect.y < p1.rect.y:
                    if ((p1.rect.x - mob.rect.x) ** 2 + (p1.rect.y - mob.rect.y) ** 2) ** 0.5 < closest[1]:
                        closest = [mob, ((p1.rect.x - mob.rect.x) ** 2 + (p1.rect.y - mob.rect.y) ** 2) ** 0.5]
                elif mob.rect.x > p1.rect.x and mob.rect.y < p1.rect.y:
                    if ((mob.rect.x - p1.rect.x) ** 2 + (p1.rect.y - mob.rect.y) ** 2) ** 0.5 < closest[1]:
                        closest = [mob, ((mob.rect.x - p1.rect.x) ** 2 + (p1.rect.y - mob.rect.y) ** 2) ** 0.5]
                elif mob.rect.x < p1.rect.x and mob.rect.y > p1.rect.y:
                    if ((p1.rect.x - mob.rect.x) ** 2 + (mob.rect.y - p1.rect.y) ** 2) ** 0.5 < closest[1]:
                        closest = [mob, ((p1.rect.x - mob.rect.x) ** 2 + (mob.rect.y - p1.rect.y) ** 2) ** 0.5]

            if closest[0] != None and closest[0].rect.x > p1.rect.x and closest[0].rect.y > p1.rect.y:
                #fourth quadrant
                RUN   = closest[0].rect.x - p1.rect.x
                RISE  = closest[0].rect.y - p1.rect.y
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant4", SLOPE]
                sprites_list.add(attack)
            elif closest[0] != None and closest[0].rect.x < p1.rect.x and closest[0].rect.y < p1.rect.y:
                #second quadrant
                RUN   = p1.rect.x - closest[0].rect.x
                RISE  = p1.rect.y - closest[0].rect.y
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant2", SLOPE]
                sprites_list.add(attack)
            elif closest[0] != None and closest[0].rect.x < p1.rect.x and closest[0].rect.y > p1.rect.y:
                #third quadrant
                RUN   = p1.rect.x - closest[0].rect.x
                RISE  = closest[0].rect.y - p1.rect.y
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant3", SLOPE]
                sprites_list.add(attack)
            elif closest[0] != None and closest[0].rect.x > p1.rect.x and closest[0].rect.y < p1.rect.y:
                #first quadrant
                RUN   = closest[0].rect.x - p1.rect.x
                RISE  = p1.rect.y - closest[0].rect.y
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant1", SLOPE]
                sprites_list.add(attack)
            elif closest[0] != None and closest[0].rect.x == p1.rect.x and closest[0].rect.y > p1.rect.y:
                #y-axis bottom
                attacks[attack] = ["verticaldown", 1]
                sprites_list.add(attack)
            elif closest[0] != None and closest[0].rect.x == p1.rect.x and closest[0].rect.y < p1.rect.y:
                #y-axis top
                attacks[attack] = ["verticalup", 1]
                sprites_list.add(attack)
            elif closest[0] != None and closest[0].rect.x > p1.rect.x and closest[0].rect.y == p1.rect.y:
                #x-axis right
                attacks[attack] = ["horizontalright", 1]
                sprites_list.add(attack)
            elif closest[0] != None and closest[0].rect.x < p1.rect.x and closest[0].rect.y  == p1.rect.y:
                #x-axis left
                attacks[attack] = ["horizontalleft", 1]
                sprites_list.add(attack)

        for attack in attacks.keys():
            if attacks[attack][0] == "quadrant1":
                p1_attack = attack.quadrant1(attacks[attack][1], mobs, attack, sprites_list, attacks_remove)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "quadrant2":
                p1_attack = attack.quadrant2(attacks[attack][1], mobs, attack, sprites_list, attacks_remove)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "quadrant3":
                p1_attack = attack.quadrant3(attacks[attack][1], mobs, attack, sprites_list, attacks_remove)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "quadrant4":
                p1_attack = attack.quadrant4(attacks[attack][1], mobs, attack, sprites_list, attacks_remove)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "verticaldown":
                p1_attack = attack.verticaldown(attacks[attack][1], mobs, attack, sprites_list, attacks_remove)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "verticalup":
                p1_attack = attack.verticalup(attacks[attack][1], mobs, attack, sprites_list, attacks_remove)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "horizontalright":
                p1_attack = attack.horizontalright(attacks[attack][1], mobs, attack, sprites_list, attacks_remove)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
            elif attacks[attack][0] == "horizontalleft":
                p1_attack = attack.horizontalleft(attacks[attack][1], mobs, attack, sprites_list, attacks_remove)
                if p1_attack != None:
                    mob_hp_change[attack] = p1_attack
        for attack in attacks_remove:
            attacks.pop(attack)

        sprites_list.update()
        hp_changer(p1, p1_hp_change, mob_hp_change)

        for mob in mobs:
            if mob.hp <= 0:
                mobs.remove(mob)
                for sprite in sprites_list:
                    if sprite == mob:
                        sprite.kill()
        
        VARIABLES    = [BORDER, DEAD, STORE]
        FONTS        = [WORD_FONT, HP_FONT, DEATH_FONT, OPTIONS_FONT]
        STORE_FONTS  = [COSTS_FONT, MENU_FONT, PURCHASE_FONT]
        BORDER, DEAD = spawn.map(window, sprites_list, p1.hp, mobs, VARIABLES, FONTS)

        if DEAD:
            if pygame.mouse.get_pressed() == (True, False, False):
                position = pygame.mouse.get_pos()
                if position[0] > 274 and position[0] < 363 and position[1] > 300 and position[1] < 337:
                    STORE = True
                elif position[0] > 234 and position[0] < 408 and position[1] > 370 and position[1] < 387:
                    print("PLAY")

        if STORE:
            if STORE_ADDED == False:
                for attack in store.generate_store(window, COSTS_FONT):
                    sprites_list.add(attack)
                STORE_ADDED == True
            STORE, STORE_ADDED = store.maintain_store(window, sprites_list, STORE_FONTS)


        clock.tick(60)

    pygame.quit()
clock=pygame.time.Clock()
play()
