import pygame
import collision
import random
import os

class mob(pygame.sprite.Sprite):
    #creates either a boss, tank, or wizard
    def __init__(self, type_, width, height):
        BOSS_image  = {"R" : "boss1.png", "K" : "boss3.png", "M" : "boss2.png"}
        BOSS_hp     = {"R" : 150, "K" : 100, "M" : 75}
        BOSS_damage = {"R" : 10, "K" : 20, "M" : 5}
        mobs        = {"W" : "wizard.jpg", "T" : "tank.jpg"}
        hp          = {"W" : 10, "T" : 25}
        damage      = {"W" : 3, "T" : 1}
        super().__init__()
        self.image  = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        if "boss" not in type_: 
            #spawns either a tank or wizard
            self.maxhp  = hp[type_]
            self.hp     = hp[type_]
            self.damage = damage[type_]
            self.image  = pygame.image.load(os.path.join("imgs", mobs[type_]))
        else:
            #spawns a boss
            BOSS_TYPE   = random.choice(["R", "K", "M"])
            self.maxhp  = BOSS_hp[BOSS_TYPE]
            self.hp     = BOSS_hp[BOSS_TYPE]
            self.damage = BOSS_damage[BOSS_TYPE]
            self.image  = pygame.image.load(os.path.join("imgs", BOSS_image[BOSS_TYPE]))
        self.rect   = self.image.get_rect()

    #controls the mob's movement
    def move(self, VEL, entities, mob, player):
        BORDER_SIZE = {10 : [38, 433, 38, 412], 25 : [38, 423, 38, 420], 150 : [38, 358, 38, 49], 100 : [38, 377, 38, 347], 75 : [45, 348, 45,343]}
        DIRECTION = random.choice(["right", "left", "up", "down"])
        collide = collision.movement(entities, mob)
        #30% chance to move toward player and 70% chance to move randomly
        if random.random() <= 0.30:
            RISE = mob.rect.y - player.rect.y
            RUN  = mob.rect.x - player.rect.x
            if RUN > 1 and RISE / RUN < 0:
                if RISE > 0:
                    RUN = player.rect.x - mob.rect.x
                    SLOPE = RISE / RUN
                    if collide[0]:
                        if collide[1] != player:
                            if self.rect.x - 3 >= BORDER_SIZE[mob.maxhp][0] and self.rect.y + (SLOPE * 3) <= BORDER_SIZE[mob.maxhp][3] and SLOPE <= 3:
                                self.rect.x -= 3
                                self.rect.y += SLOPE * 3
                            elif self.rect.x - 3 >= BORDER_SIZE[mob.maxhp][0] and self.rect.y + 9 <= BORDER_SIZE[mob.maxhp][3]:
                                self.rect.x -= 3
                                self.rect.y += 9
                            elif self.rect.y + 9 <= BORDER_SIZE[mob.maxhp][3]:
                                self.rect.y = BORDER_SIZE[mob.maxhp][3]
                            elif self.rect.x - 3 >= BORDER_SIZE[mob.maxhp][0]:
                                self.rect.x = BORDER_SIZE[mob.maxhp][0]
                            else:
                                self.rect.x = BORDER_SIZE[mob.maxhp][0]
                                self.rect.y = BORDER_SIZE[mob.maxhp][3]
                        else:
                            if self.rect.x - 3 >= BORDER_SIZE[mob.maxhp][0] and self.rect.y + (SLOPE * 3) <= BORDER_SIZE[mob.maxhp][3] and SLOPE <= 3:
                                self.rect.x -= 3
                                self.rect.y += SLOPE * 3
                                return mob
                            elif self.rect.x - 3 >= BORDER_SIZE[mob.maxhp][0] and self.rect.y + 9 <= BORDER_SIZE[mob.maxhp][3]:
                                self.rect.x -= 3
                                self.rect.y += 9
                                return mob
                            elif self.rect.y + 9 <= BORDER_SIZE[mob.maxhp][3]:
                                self.rect.y = BORDER_SIZE[mob.maxhp][3]
                                return mob
                            elif self.rect.x - 3 >= BORDER_SIZE[mob.maxhp][0]:
                                self.rect.x = BORDER_SIZE[mob.maxhp][0]
                                return mob
                            else:
                                self.rect.x = BORDER_SIZE[mob.maxhp][0]
                                self.rect.y = BORDER_SIZE[mob.maxhp][3]
                                return mob
                    else:
                        if self.rect.x + 3 <= BORDER_SIZE[mob.maxhp][1] and self.rect.y - (SLOPE * 3) >= BORDER_SIZE[mob.maxhp][2] and SLOPE <= 3:
                            self.rect.x += 3
                            self.rect.y -= SLOPE * 3
                        elif self.rect.x + 3 >= BORDER_SIZE[mob.maxhp][0] and self.rect.y - 9 <= BORDER_SIZE[mob.maxhp][3]:
                            self.rect.x += 3
                            self.rect.y -= 9
                        elif self.rect.x + 3 <= BORDER_SIZE[mob.maxhp][1]:
                            self.rect.x = BORDER_SIZE[mob.maxhp][1] 
                        elif self.rect.y - 9 <= BORDER_SIZE[mob.maxhp][2]:
                            self.rect.y = BORDER_SIZE[mob.maxhp][2]
                        else:
                            self.rect.x = BORDER_SIZE[mob.maxhp][1]
                            self.rect.y = BORDER_SIZE[mob.maxhp][2]
                else: 
                    RISE = player.rect.y - mob.rect.y
                    SLOPE = RISE / RUN
                    if collide[0]:
                        if collide[1] != player:
                            if self.rect.x + 3 <= BORDER_SIZE[mob.maxhp][1] and self.rect.y - (SLOPE * 3) >= BORDER_SIZE[mob.maxhp][2] and SLOPE <= 3:
                                self.rect.x += 3
                                self.rect.y -= SLOPE * 3
                            elif self.rect.x + 3 >= BORDER_SIZE[mob.maxhp][0] and self.rect.y - 9 <= BORDER_SIZE[mob.maxhp][3]:
                                self.rect.x += 3
                                self.rect.y -= 9
                            elif self.rect.y - 9 >= BORDER_SIZE[mob.maxhp][2]:
                                self.rect.y = BORDER_SIZE[mob.maxhp][2]
                            elif self.rect.x + 3 <= BORDER_SIZE[mob.maxhp][1]:
                                self.rect.x = BORDER_SIZE[mob.maxhp][1]
                            else:
                                self.rect.x = BORDER_SIZE[mob.maxhp][1]
                                self.rect.y = BORDER_SIZE[mob.maxhp][2]
                        else:
                            if self.rect.x + 3 <= BORDER_SIZE[mob.maxhp][1] and self.rect.y - (SLOPE * 3) >= BORDER_SIZE[mob.maxhp][2] and SLOPE <= 3:
                                self.rect.x += 3
                                self.rect.y -= SLOPE * 3
                                return mob
                            elif self.rect.x + 3 >= BORDER_SIZE[mob.maxhp][0] and self.rect.y - 9 <= BORDER_SIZE[mob.maxhp][3]:
                                self.rect.x += 3
                                self.rect.y -= 9
                                return mob
                            elif self.rect.y - 9 >= BORDER_SIZE[mob.maxhp][2]:
                                self.rect.y = BORDER_SIZE[mob.maxhp][2]
                                return mob
                            elif self.rect.x + 3 <= BORDER_SIZE[mob.maxhp][1]:
                                self.rect.x = BORDER_SIZE[mob.maxhp][1]
                                return mob
                            else:
                                self.rect.x = BORDER_SIZE[mob.maxhp][1]
                                self.rect.y = BORDER_SIZE[mob.maxhp][2]
                                return mob
                    else:
                        if self.rect.x - 3 >= BORDER_SIZE[mob.maxhp][0] and self.rect.y + (SLOPE * 3) <= BORDER_SIZE[mob.maxhp][3] and SLOPE <= 3:
                            self.rect.x -= 3
                            self.rect.y += SLOPE * 3
                        elif self.rect.x - 3 >= BORDER_SIZE[mob.maxhp][0] and self.rect.y + 9 <= BORDER_SIZE[mob.maxhp][3]:
                            self.rect.x -= 3
                            self.rect.y += 9
                        elif self.rect.x - 3 <= BORDER_SIZE[mob.maxhp][0]:
                            self.rect.x = BORDER_SIZE[mob.maxhp][0] 
                        elif self.rect.y + 9 <= BORDER_SIZE[mob.maxhp][3]:
                            self.rect.y = BORDER_SIZE[mob.maxhp][3]
                        else:
                            self.rect.x = BORDER_SIZE[mob.maxhp][0]
                            self.rect.y = BORDER_SIZE[mob.maxhp][3]
            elif  RUN > 1 and RISE / RUN > 0 and RISE / RUN <= 3:
                if RISE > 0:
                    SLOPE = RISE / RUN
                    if collide[0]:
                        if collide[1] != player:
                            if self.rect.x + 3 <= BORDER_SIZE[mob.maxhp][1] and self.rect.y + (SLOPE * 3) <= BORDER_SIZE[mob.maxhp][3]:
                                self.rect.x += 3
                                self.rect.y += SLOPE * 3
                            elif self.rect.y + 9 <= BORDER_SIZE[mob.maxhp][3]:
                                self.rect.y = BORDER_SIZE[mob.maxhp][3]
                            elif self.rect.x + 3 >= BORDER_SIZE[mob.maxhp][1]:
                                self.rect.x = BORDER_SIZE[mob.maxhp][1]
                            else:
                                self.rect.x = BORDER_SIZE[mob.maxhp][1]
                                self.rect.y = BORDER_SIZE[mob.maxhp][3]
                        else:
                            if self.rect.x + 3 <= BORDER_SIZE[mob.maxhp][1] and self.rect.y + (SLOPE * 3) <= BORDER_SIZE[mob.maxhp][3]:
                                self.rect.x += 3
                                self.rect.y += SLOPE * 3
                                return mob
                            elif self.rect.y + 9 <= BORDER_SIZE[mob.maxhp][3]:
                                self.rect.y = BORDER_SIZE[mob.maxhp][3]
                                return mob
                            elif self.rect.x + 3 >= BORDER_SIZE[mob.maxhp][1]:
                                self.rect.x = BORDER_SIZE[mob.maxhp][1]
                                return mob
                            else:
                                self.rect.x = BORDER_SIZE[mob.maxhp][1]
                                self.rect.y = BORDER_SIZE[mob.maxhp][3]
                                return mob
                    else:
                        if self.rect.x - 3 >= BORDER_SIZE[mob.maxhp][0] and self.rect.y - (SLOPE * 3) >= BORDER_SIZE[mob.maxhp][2]:
                            self.rect.x -= 3
                            self.rect.y -= SLOPE * 3
                        elif self.rect.x - 3 >= BORDER_SIZE[mob.maxhp][0]:
                            self.rect.x = BORDER_SIZE[mob.maxhp][0] 
                        elif self.rect.y - 9 <= BORDER_SIZE[mob.maxhp][2]:
                            self.rect.y = BORDER_SIZE[mob.maxhp][2]
                        else:
                            self.rect.x = BORDER_SIZE[mob.maxhp][0]
                            self.rect.y = BORDER_SIZE[mob.maxhp][2]
                else: 
                    SLOPE = RISE / RUN
                    if collide[0]:
                        if collide[1] != player:
                            if self.rect.x - 3 >= BORDER_SIZE[mob.maxhp][0] and self.rect.y - (SLOPE * 3) >= BORDER_SIZE[mob.maxhp][2]:
                                self.rect.x -= 3
                                self.rect.y -= SLOPE * 3
                            elif self.rect.y - 9 >= BORDER_SIZE[mob.maxhp][2]:
                                self.rect.y = BORDER_SIZE[mob.maxhp][2]
                            elif self.rect.x - 3 <= BORDER_SIZE[mob.maxhp][0]:
                                self.rect.x = BORDER_SIZE[mob.maxhp][0]
                            else:
                                self.rect.x = BORDER_SIZE[mob.maxhp][0]
                                self.rect.y = BORDER_SIZE[mob.maxhp][2]
                        else:
                            if self.rect.x - 3 >= BORDER_SIZE[mob.maxhp][0] and self.rect.y - (SLOPE * 3) >= BORDER_SIZE[mob.maxhp][2]:
                                self.rect.x -= 3
                                self.rect.y -= SLOPE * 3
                                return mob
                            elif self.rect.y - 9 >= BORDER_SIZE[mob.maxhp][2]:
                                self.rect.y = BORDER_SIZE[mob.maxhp][2]
                                return mob
                            elif self.rect.x - 3 >= BORDER_SIZE[mob.maxhp][0]:
                                self.rect.x = BORDER_SIZE[mob.maxhp][0]
                                return mob
                            else:
                                self.rect.x = BORDER_SIZE[mob.maxhp][0]
                                self.rect.y = BORDER_SIZE[mob.maxhp][2]
                                return mob
                    else:
                        if self.rect.x + 3 <= BORDER_SIZE[mob.maxhp][1] and self.rect.y + (SLOPE * 3) <= BORDER_SIZE[mob.maxhp][3]:
                            self.rect.x += 3
                            self.rect.y += 3 * SLOPE
                        elif self.rect.x + 3 >= BORDER_SIZE[mob.maxhp][1]:
                            self.rect.x = BORDER_SIZE[mob.maxhp][1] 
                        elif self.rect.y + 9 <= BORDER_SIZE[mob.maxhp][3]:
                            self.rect.y = BORDER_SIZE[mob.maxhp][3]
                        else:
                            self.rect.x = BORDER_SIZE[mob.maxhp][1]
                            self.rect.y = BORDER_SIZE[mob.maxhp][3]
            elif RUN != 0 and RISE / RUN > 3:
                pass
            else:
                random_movement = random.random()
                if random_movement < 0.25:
                    if self.rect.y - VEL >= BORDER_SIZE[mob.maxhp][2]:
                        self.rect.y -= VEL
                    else:
                        self.rect.y = BORDER_SIZE[mob.maxhp][2]
                elif random_movement < 0.50:
                    if self.rect.x + VEL <= BORDER_SIZE[mob.maxhp][1]:
                        self.rect.x += VEL
                    else:
                        self.rect.x = BORDER_SIZE[mob.maxhp][1]
                elif random_movement < 0.75:
                    if self.rect.x - VEL >= BORDER_SIZE[mob.maxhp][0]:
                        self.rect.x -= VEL
                    else:
                        self.rect.x = BORDER_SIZE[mob.maxhp][0]
                else:
                    if self.rect.y +  VEL <= BORDER_SIZE[mob.maxhp][3]:
                        self.rect.y += VEL
                    else:
                        self.rect.y = BORDER_SIZE[mob.maxhp][3]

        else:
            if DIRECTION == "right":
                if collide[0]:
                    if collide[1] != player:
                        if self.rect.x - VEL >= BORDER_SIZE[mob.maxhp][0]:
                            self.rect.x -= 2 * VEL
                        else:
                            self.rect.x = BORDER_SIZE[mob.maxhp][0]
                    else:
                        if self.rect.x - VEL >= BORDER_SIZE[mob.maxhp][0]:
                            self.rect.x -= 2 * VEL
                            return mob
                        else:
                            self.rect.x = BORDER_SIZE[mob.maxhp][0]
                            return mob
                else:
                    if self.rect.x + VEL <= BORDER_SIZE[mob.maxhp][1]:
                        self.rect.x += VEL
                    else:
                        self.rect.x = BORDER_SIZE[mob.maxhp][1]

            elif DIRECTION == "left":
                if collide[0]:
                    if collide[1] != player:
                        if self.rect.x + VEL <= BORDER_SIZE[mob.maxhp][1]:
                            self.rect.x += 2 * VEL
                        else:
                            self.rect.x = BORDER_SIZE[mob.maxhp][1]
                    else:
                        if self.rect.x + VEL <= BORDER_SIZE[mob.maxhp][1]:
                            self.rect.x += 2 * VEL
                            return mob
                        else:
                            self.rect.x = BORDER_SIZE[mob.maxhp][1]
                            return mob
                else:
                    if self.rect.x - VEL >= BORDER_SIZE[mob.maxhp][0]:
                        self.rect.x -= VEL
                    else:
                        self.rect.x = BORDER_SIZE[mob.maxhp][0]

            if DIRECTION == "up":
                if collide[0]:
                    if collide[1] != player:
                        if self.rect.y + VEL <= BORDER_SIZE[mob.maxhp][3]:
                            self.rect.y += 2 * VEL
                        else:
                            self.rect.y = BORDER_SIZE[mob.maxhp][3]
                    else:
                        if self.rect.y + VEL <= BORDER_SIZE[mob.maxhp][3]:
                            self.rect.y += 2 * VEL
                            return mob
                        else:
                            self.rect.y = BORDER_SIZE[mob.maxhp][3]
                            return mob
                else:
                    if self.rect.y - VEL >= BORDER_SIZE[mob.maxhp][2]:
                        self.rect.y -= VEL
                    else:
                        self.rect.y = BORDER_SIZE[mob.maxhp][2]

            elif DIRECTION == "down":
                if collide[0]:
                    if collide[1] != player:
                        if self.rect.y - VEL >= BORDER_SIZE[mob.maxhp][2]:
                            self.rect.y -= 2 * VEL
                        else:
                            self.rect.y = BORDER_SIZE[mob.maxhp][2]
                    else:
                        if self.rect.y - VEL >= BORDER_SIZE[mob.maxhp][2]:
                            self.rect.y -= 2 * VEL
                            return mob
                        else:
                            self.rect.y = BORDER_SIZE[mob.maxhp][2]
                            return mob
                else:
                    if self.rect.y +  VEL <= BORDER_SIZE[mob.maxhp][3]:
                        self.rect.y += VEL
                    else:
                        self.rect.y = BORDER_SIZE[mob.maxhp][3]



class tree(pygame.sprite.Sprite):
    #creates the player sprite
    def __init__(self, width, height, POSx, POSy):
        super().__init__()
        DAMAGE = [2, 5, 7, 10, 15]
        damage = 0
        with open("equipped.txt", mode = "r") as equip:
            EQUIP = equip.readlines()
            EQUIP = EQUIP[0].split(" ")
            for item in range(len(EQUIP)):
                if "True" in EQUIP[item] and item < 6:
                    damage = item - 1
        self.special = 0
        self.damage  = DAMAGE[damage]
        self.hp      = 1
        self.image   = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.image   = pygame.image.load(os.path.join("imgs", "player.jpg"))
        self.rect    = self.image.get_rect()
        self.rect.x  = POSx
        self.rect.y  = POSy

    #controls the player's ability to move right
    def move_right(self, VEL, player, mobs):
        if collision.movement(mobs, player)[0]:
            if self.rect.x - VEL >= 38:
                self.rect.x -= 2 * VEL
            else:
                self.rect.x = 38
        elif self.rect.x + VEL <= 428:
            self.rect.x += VEL
        elif self.rect.x + VEL > 428:
            self.rect.x = 428

    #controls the player's ability to move left
    def move_left(self, VEL, player, mobs):
        if collision.movement(mobs, player)[0]:
            if self.rect.x + VEL <= 428:
                self.rect.x += 2 * VEL
            else:
                self.rect.x = 428
        elif self.rect.x - VEL >= 38:
            self.rect.x -= VEL
        elif self.rect.x - VEL < 38:
            self.rect.x = 38

    #controls the player's ability to move up
    def move_up(self, VEL, player, mobs):
        if collision.movement(mobs, player)[0]:
            if self.rect.y + VEL <= 413:
                self.rect.y += 2 * VEL
            else:
                self.rect.y = 413
        elif self.rect.y - VEL >= 38:
            self.rect.y -= VEL
        elif self.rect.y - VEL < 38:
            self.rect.y = 38

    #controls the player's ability to move down
    def move_down(self, VEL, player, mobs):
        if collision.movement(mobs, player)[0]:
            if self.rect.y - VEL >= 38:
                self.rect.y -= 2 * VEL
            else:
                self.rect.y = 38
        elif self.rect.y + VEL <= 413:
            self.rect.y += VEL
        elif self.rect.y + VEL > 413:
            self.rect.y = 413



class side_wall(pygame.sprite.Sprite):
    #creates the side walls for the map
    def __init__(self, width, height, POSx, POSy):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.image  = pygame.image.load(os.path.join("imgs", "side_wall.png"))
        self.rect   = self.image.get_rect()
        self.rect.x = POSx
        self.rect.y = POSy



class top_wall(pygame.sprite.Sprite):
    #creates the top and bottom walls for the map
    def __init__(self, width, height, POSx, POSy):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.image  = pygame.image.load(os.path.join("imgs", "top_wall.png"))
        self.rect   = self.image.get_rect()
        self.rect.x = POSx
        self.rect.y = POSy



class player_attack(pygame.sprite.Sprite):
    #creates the player attack's sprite
    def __init__(self, width, height, POSx, POSy, player):
        super().__init__()
        ATTACK_IMAGES = {2 : "attack_1.png", 5 : "attack_2.png", 7 : "attack_3.png", 10 : "attack_4.png", 15 : "attack_5.png"}
        self.image    = pygame.Surface([width,height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.image  = pygame.image.load(os.path.join("imgs", ATTACK_IMAGES[player.damage]))
        self.rect   = self.image.get_rect()
        self.rect.x = POSx
        self.rect.y = POSy

    #controls the player attack's ability to move in the first quadrant
    def quadrant1(self, SLOPE, mobs, attack, sprites_list, attacks_list):
        DELTAx     = 1 / SLOPE
        multiplier = 1
        if DELTAx < 1:
            while not (SLOPE * multiplier > round(SLOPE * multiplier) - 0.1) and not (SLOPE * multiplier < round(SLOPE * multiplier) + 0.1):
                multiplier +=1
            DELTAx = multiplier
            DELTAy = SLOPE * multiplier
        else:
            DELTAy = SLOPE * DELTAx
            if DELTAy < 1:
                DELTAy = 3
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.x + DELTAx > 434 or self.rect.y - DELTAy < 38:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.x += round(DELTAx)
            self.rect.y -= DELTAy

    #controls the player attack's ability to move in the second quadrant
    def quadrant2(self, SLOPE, mobs, attack, sprites_list, attacks_list):
        DELTAx = 1 / SLOPE
        multiplier = 1
        if DELTAx < 1:
            while not (SLOPE * multiplier > round(SLOPE * multiplier) - 0.1) and not (SLOPE * multiplier < round(SLOPE * multiplier) + 0.1):
                multiplier +=1
            DELTAx = multiplier
            DELTAy = SLOPE * multiplier
        else:
            DELTAy = SLOPE * DELTAx
            if DELTAy < 1:
                DELTAy = 3
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.x - DELTAx < 38 or self.rect.y - DELTAy < 38:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.x -= round(DELTAx)
            self.rect.y -= DELTAy

    #controls the player attack's ability to move in the third quadrant
    def quadrant3(self, SLOPE, mobs, attack, sprites_list, attacks_list):
        DELTAx = 1 / SLOPE
        multiplier = 1
        if DELTAx < 1:
            while not (SLOPE * multiplier > round(SLOPE * multiplier) - 0.1) and not (SLOPE * multiplier < round(SLOPE * multiplier) + 0.1):
                multiplier +=1
            DELTAx = multiplier
            DELTAy = SLOPE * multiplier
        else:
            DELTAy = SLOPE * DELTAx
            if DELTAy < 1:
                DELTAy = 3
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.x - DELTAx < 38 or self.rect.y + DELTAy > 437:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.x -= round(DELTAx)
            self.rect.y += DELTAy

    #controls the player attack's ability to move in the fourth quadrant
    def quadrant4(self, SLOPE, mobs, attack, sprites_list, attacks_list):
        DELTAx = 1 / SLOPE
        multiplier = 1
        if DELTAx < 1:
            while not (SLOPE * multiplier > round(SLOPE * multiplier) - 0.1) and not (SLOPE * multiplier < round(SLOPE * multiplier) + 0.1):
                multiplier +=1
            DELTAx = multiplier
            DELTAy = SLOPE * multiplier
        else:
            DELTAy = SLOPE * DELTAx
            if DELTAy < 1:
                DELTAy = 3
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.x + DELTAx > 434 or self.rect.y + DELTAy > 437:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.x += round(DELTAx)
            self.rect.y += DELTAy

    #controls the player attack's ability to move to the right (horizontally)
    def horizontalright(self, SPEED, mobs, attack, sprites_list, attacks_list):
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.x + SPEED > 434:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.x += SPEED

    #controls the player attack's ability to move to the left (horizontally)
    def horizontalleft(self, SPEED, mobs, attack, sprites_list, attacks_list):
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.x - SPEED < 38:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.x -= SPEED

    #controls the player attack's ability to move up (vertically)
    def verticalup(self, SPEED,  mobs, attack, sprites_list, attacks_list):
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.y - SPEED < 38:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.y -= SPEED

    #controls the player attack's ability to move down (vertically)
    def verticaldown(self, SPEED, mobs, attack, sprites_list, attacks_list):
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.y + SPEED > 437:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.y += SPEED



class store_attacks(pygame.sprite.Sprite):
    #creates the images of the different attacks that can be purchased in the store
    def __init__(self, width, height, POSx, POSy, attack):
        super().__init__()
        ITEMS       = ["attack1.png", "attack2.png", "attack3.png", "attack4.png", "attack5.png", "special1.jpg", "special2.jpg", "special3.jpg", "special4.jpg"]
        self.image  = pygame.Surface([width,height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.image  = pygame.image.load(os.path.join("store_imgs", ITEMS[attack]))
        self.rect   = self.image.get_rect()
        self.rect.x = POSx
        self.rect.y = POSy
