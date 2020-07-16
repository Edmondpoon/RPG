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


#creates a wizard mob
def wizard(mobs, player, mob_dict):
    mob      = images.mob("W", WIDTH, HEIGHT)
    entities = mobs[:]
    entities.append(player)
    mob.rect.x          = random.randint(38, 433)
    mob.rect.y          = random.randint(38, 417)
    FLAG          = collision.Spawn(entities, mob)
    while FLAG == True:
        mob.rect.x = random.randint(38, 433)
        mob.rect.y = random.randint(38, 417)
        FLAG = collision.Spawn(entities, mob)
    mobs.append(mob)
    return mob

#creates a tank mob
def tank(mobs, player): 
    mob      = images.mob("T", WIDTH, HEIGHT)
    entities = mobs[:]
    entities.append(player)
    mob.rect.x          = random.randint(38, 433)
    mob.rect.y          = random.randint(38, 417)
    FLAG          = collision.Spawn(entities, mob)
    while FLAG == True: 
        mob.rect.x = random.randint(38, 433)
        mob.rect.y = random.randint(38, 417)
        FLAG = collision.Spawn(entities, mob)

    mobs.append(mob)
    return mob

#spawns a random amount of wizards and tanks
def spawn_mobs(mobs, player, sprites_list, mob_dict):
    num_mobs = random.randint(1, 5)
    for mob in range(num_mobs):
        spawn = random.random()
        if spawn  <= 0.4:
            sprites_list.add(wizard(mobs, player, mob_dict))
        elif spawn < 1.0:
            sprites_list.add(tank(mobs, player))

#creates a player sprite
def player():
    POSx = random.randint(38, 433)
    POSy = random.randint(38, 417)
    return images.tree(WIDTH, HEIGHT, POSx, POSy)
=======
MOB_VEL      = 3
>>>>>>> test

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
def map(window, sprites_list, BORDER, player_hp, mobs):
    window.fill((255, 255, 255))

    #draws black sidebar
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect((500, 0), (150, 500)))
    #draws the hp bar background
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect((520, 81), (110, 30)))

    #changes the length of the player hp bar depedning on the player's hp
    if int(player_hp) <= 20 and int(player_hp) > 0:
        percentage = int(player_hp) / 20
        hp_size    = int( 100 * percentage)
        pygame.draw.rect(window, (255, 0, 0), pygame.Rect((525, 86), (hp_size, 20)))
    elif int(player_hp) <= 0:
        for sprite in sprites_list:
            sprite.kill()
        window.fill((0, 0, 0))
        ending_text = WORD_FONT.render("You died", True, (255, 255, 255))
        window.blit(ending_text, (100, 200))


    enemy_hp_bar = WORD_FONT.render("Enemy hp", True, (255, 255, 255))
    window.blit(enemy_hp_bar, (510, 200))
    placements    = [233, 273, 313, 353, 393, 433]
    hp_placements = [238, 278, 318, 358, 398, 438]
    for value in placements[:len(mobs)]:
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect((520, value), (110, 30)))
    for mob in range(len(mobs)):
        if int(mobs[mob].hp) <= mobs[mob].maxhp and int(mobs[mob].hp) > 0:
            percentage = int(mobs[mob].hp) / mobs[mob].maxhp
            hp_size    = int( 100 * percentage)
            pygame.draw.rect(window, (255, 0, 0), pygame.Rect((525, hp_placements[mob]), (hp_size, 20)))

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
    BORDER   = 0
    mob_dict = {}
    WAVES    = 1
    mobs     = []
    attacks  = {}
    run      = True
    p1       = spawn.player()
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

            if closest[0].rect.x > p1.rect.x and closest[0].rect.y > p1.rect.y:
                #fourth quadrant
                RUN   = closest[0].rect.x - p1.rect.x
                RISE  = closest[0].rect.y - p1.rect.y
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant4", SLOPE]
                sprites_list.add(attack)
            elif closest[0].rect.x < p1.rect.x and closest[0].rect.y < p1.rect.y:
                #second quadrant
                RUN   = p1.rect.x - closest[0].rect.x 
                RISE  = p1.rect.y - closest[0].rect.y
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant2", SLOPE]
                sprites_list.add(attack)
            elif closest[0].rect.x < p1.rect.x and closest[0].rect.y > p1.rect.y:
                #third quadrant
                RUN   = p1.rect.x - closest[0].rect.x
                RISE  = closest[0].rect.y - p1.rect.y
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant3", SLOPE]
                sprites_list.add(attack)
            elif closest[0].rect.x > p1.rect.x and closest[0].rect.y < p1.rect.y:
                #first quadrant
                RUN   = closest[0].rect.x - p1.rect.x
                RISE  = p1.rect.y - closest[0].rect.y
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant1", SLOPE]
                sprites_list.add(attack)
            elif closest[0].rect.x == p1.rect.x and closest[0].rect.y > p1.rect.y:
                #y-axis bottom
                attacks[attack] = ["verticaldown", 2]
                sprites_list.add(attack)
            elif closest[0].rect.x == p1.rect.x and closest[0].rect.y < p1.rect.y:
                #y-axis top
                attacks[attack] = ["verticalup", 2]
                sprites_list.add(attack)
            elif closest[0].rect.x > p1.rect.x and closest[0].rect.y == p1.rect.y:
                #x-axis right
                attacks[attack] = ["horizontalright", 2]
                sprites_list.add(attack)
            elif closest[0].rect.x < p1.rect.x and closest[0].rect.y  == p1.rect.y:
                #x-axis left
                attacks[attack] = ["horizontalleft", 2]
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

        BORDER = map(window, sprites_list, BORDER, p1.hp, mobs)
        clock.tick(60)

    pygame.quit()
clock=pygame.time.Clock()
play()
