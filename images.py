import pygame
import collision
import random
import os

class mob(pygame.sprite.Sprite):
    def __init__(self, type_, width, height):
        mobs   = {"W" : "wizard.jpg", "T" : "tank.jpg"}
        hp     = {"W" : 10, "T" : 25}
        damage = {"W" : 3, "T" : 1}
        super().__init__()
        self.maxhp  = hp[type_]
        self.hp     = hp[type_]
        self.damage = damage[type_]
        self.image  = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.image  = pygame.image.load(os.path.join("imgs", mobs[type_]))
        self.rect   = self.image.get_rect()
    

    def move(self, VEL, entities, mob, player):
        DIRECTION = random.choice(["right", "left", "up", "down"])
        collide = collision.movement(entities, mob)
        if DIRECTION == "right":
            if collide[0]:
                if collide[1] != player:
                    if self.rect.x - VEL >= 38:
                        self.rect.x -= 2 * VEL
                    else:
                        self.rect.x = 38
                else:
                    if self.rect.x - VEL >= 38:
                        self.rect.x -= 2 * VEL
                        return mob
                    else:
                        self.rect.x = 38
                        return mob
            else:
                if self.rect.x + VEL <= 433:
                    self.rect.x += VEL
                else:
                    self.rect.x = 433

        elif DIRECTION == "left":
            if collide[0]:
                if collide[1] != player:
                    if self.rect.x + VEL <= 433:
                        self.rect.x += 2 * VEL
                    else:
                        self.rect.x = 433
                else:
                    if self.rect.x + VEL <= 433:
                        self.rect.x += 2 * VEL
                        return mob
                    else:
                        self.rect.x = 433
                        return mob
            else:
                if self.rect.x -  VEL >= 38:
                    self.rect.x -= VEL
                else:
                    self.rect.x = 38

        if DIRECTION == "up":
            if collide[0]:
                if collide[1] != player:
                    if self.rect.y + VEL <= 417:
                        self.rect.y += 2 * VEL
                    else:
                        self.rect.y = 417
                else:
                    if self.rect.y + VEL <= 417:
                        self.rect.y += 2 * VEL
                        return mob
                    else:
                        self.rect.y = 417
                        return mob
            else:
                if self.rect.y - VEL >= 38:
                    self.rect.y -= VEL
                else:
                    self.rect.y = 38

        elif DIRECTION == "down":
            if collide[0]:
                if collide[1] != player:
                    if self.rect.y - VEL >= 38:
                        self.rect.y -= 2 * VEL
                    else:
                        self.rect.y = 38
                else:
                    if self.rect.y - VEL >= 38:
                        self.rect.y -= 2 * VEL
                        return mob
                    else:
                        self.rect.y = 38
                        return mob
            else:
                if self.rect.y +  VEL <= 417:
                    self.rect.y += VEL
                else:
                    self.rect.y = 417



class tree(pygame.sprite.Sprite):
    def __init__(self, width, height, POSx, POSy):
        super().__init__()
        self.hp     = 20
        self.damage = 2
        self.image  = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.image  = pygame.image.load(os.path.join("imgs", "player.jpg"))
        self.rect   = self.image.get_rect()
        self.rect.x = POSx
        self.rect.y = POSy

    def move_right(self, VEL, player, mobs):
        if collision.movement(mobs, player)[0]:
            if self.rect.x - VEL >= 38:
                self.rect.x -= 2 * VEL
            else:
                self.rect.x = 38
        elif self.rect.x + VEL <= 433:
            self.rect.x += VEL
        elif self.rect.x + VEL > 433:
            self.rect.x = 433

    def move_left(self, VEL, player, mobs):
        if collision.movement(mobs, player)[0]:
            if self.rect.x + VEL <= 433:
                self.rect.x += 2 * VEL
            else:
                self.rect.x = 433
        elif self.rect.x - VEL >= 38:
            self.rect.x -= VEL
        elif self.rect.x - VEL < 38:
            self.rect.x = 38

    def move_up(self, VEL, player, mobs):
        if collision.movement(mobs, player)[0]:
            if self.rect.y + VEL <= 417:
                self.rect.y += 2 * VEL
            else:
                self.rect.y = 417
        elif self.rect.y - VEL >= 38:
            self.rect.y -= VEL
        elif self.rect.y - VEL < 38:
            self.rect.y = 38

    def move_down(self, VEL, player, mobs):
        if collision.movement(mobs, player)[0]:
            if self.rect.y - VEL >= 38:
                self.rect.y -= 2 * VEL
            else:
                self.rect.y = 38
        elif self.rect.y + VEL <= 417:
            self.rect.y += VEL
        elif self.rect.y + VEL > 417:
            self.rect.y = 417



class side_wall(pygame.sprite.Sprite):
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
    def __init__(self, width, height, POSx, POSy):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.image  = pygame.image.load(os.path.join("imgs", "attack.png"))
        self.rect   = self.image.get_rect()
        self.rect.x = POSx
        self.rect.y = POSy
        
    def quadrant1(self, SLOPE, mobs, attack, sprites_list, attacks_list):
        DELTAx     = 1 / SLOPE
        multiplier = 1
        if DELTAx < 1:
            while not (SLOPE * multiplier > round(SLOPE * multiplier) - 0.1) and not (SLOPE * multiplier < round(SLOPE * multiplier) + 0.1):
                multiplier +=1
            DELTAx = multiplier
            DELTAy = SLOPE * multiplier
        else:
            DELTAy = 1
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.x + DELTAx > 450 or self.rect.y - DELTAy < 38:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.x += round(DELTAx)
            self.rect.y -= DELTAy

    def quadrant2(self, SLOPE, mobs, attack, sprites_list, attacks_list):
        DELTAx = 1 / SLOPE
        multiplier = 1
        if DELTAx < 1:
            while not (SLOPE * multiplier > round(SLOPE * multiplier) - 0.1) and not (SLOPE * multiplier < round(SLOPE * multiplier) + 0.1):
                multiplier +=1
            DELTAx = multiplier
            DELTAy = SLOPE * multiplier
        else:
            DELTAy = 1
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
    
    def quadrant3(self, SLOPE, mobs, attack, sprites_list, attacks_list):
        DELTAx = 1 / SLOPE
        multiplier = 1
        if DELTAx < 1:
            while not (SLOPE * multiplier > round(SLOPE * multiplier) - 0.1) and not (SLOPE * multiplier < round(SLOPE * multiplier) + 0.1):
                multiplier +=1
            DELTAx = multiplier
            DELTAy = SLOPE * multiplier
        else:
            DELTAy = 1
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.x - DELTAx < 38 or self.rect.y + DELTAy > 452:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.x -= round(DELTAx)
            self.rect.y += DELTAy

    def quadrant4(self, SLOPE, mobs, attack, sprites_list, attacks_list):
        DELTAx = 1 / SLOPE
        multiplier = 1
        if DELTAx < 1:
            while not (SLOPE * multiplier > round(SLOPE * multiplier) - 0.1) and not (SLOPE * multiplier < round(SLOPE * multiplier) + 0.1):
                multiplier +=1
            DELTAx = multiplier
            DELTAy = SLOPE * multiplier
        else:
            DELTAy = 1
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.x + DELTAx > 450 or self.rect.y + DELTAy > 452:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.x += round(DELTAx)
            self.rect.y += DELTAy

    def horizontalright(self, SPEED, mobs, attack, sprites_list, attacks_list):
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.x + SPEED> 450:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.x += SPEED

    def horizontalleft(self, SPEED, mobs, attack, sprites_list, attacks_list):
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.x - SPEED< 38:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.x -= SPEED

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

    def verticaldown(self, SPEED, mobs, attack, sprites_list, attacks_list):
        if collision.attack_movement(mobs, attack)[0]:
           sprites_list.remove(attack)
           attacks_list.append(attack)
           return collision.attack_movement(mobs, attack)[1]
        elif self.rect.y + SPEED > 452:
            sprites_list.remove(attack)
            attacks_list.append(attack)
        else:
            self.rect.y += SPEED
