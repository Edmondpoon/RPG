import pygame
import random
import os

class mob(pygame.sprite.Sprite):
    def __init__(self, type_, width, height):
        mobs = {"W" : "wizard.jpg", "T" : "tank.jpg"}
        hp   = {"W" : 10, "T" : 25}
        super().__init__()
        self.hp    = hp[type_]
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.image  = pygame.image.load(os.path.join("imgs", mobs[type_]))
        self.rect   = self.image.get_rect()
    

    def move(self, VEL):
        DIRECTION = random.choice(["right", "left", "up", "down"])
        if DIRECTION == "right":
            if self.rect.x + VEL <= 433:
                self.rect.x += VEL
            elif self.rect.x + VEL > 433:
                pass
        elif DIRECTION == "left":
            if self.rect.x - VEL >= 38:
                self.rect.x -= VEL
            elif self.rect.x - VEL < 38:
                pass
        elif DIRECTION == "up":
            if self.rect.y - VEL >= 38:
                self.rect.y -= VEL
            elif self.rect.y - VEL < 38:
                pass
        elif DIRECTION == "down":
            if self.rect.y + VEL <= 417:
                self.rect.y += VEL
            elif self.rect.y + VEL > 417:
                pass




class tree(pygame.sprite.Sprite):
    def __init__(self, width, height, POSx, POSy):
        super().__init__()
        self.hp    = 20
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.image  = pygame.image.load(os.path.join("imgs", "player.jpg"))
        self.rect   = self.image.get_rect()
        self.rect.x = POSx
        self.rect.y = POSy

    def move_right(self, VEL):
        if self.rect.x + VEL <= 433:
            self.rect.x += VEL
        elif self.rect.x + VEL > 433:
            self.rect.x = 433

    def move_left(self, VEL):
        if self.rect.x - VEL >= 38:
            self.rect.x -= VEL
        elif self.rect.x - VEL < 38:
            self.rect.x = 38

    def move_up(self, VEL):
        if self.rect.y - VEL >= 38:
            self.rect.y -= VEL
        elif self.rect.y - VEL < 38:
            self.rect.y = 38

    def move_down(self, VEL):
        if self.rect.y + VEL <= 417:
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
        
    def quadrant1(self, playerpos, cursorpos):
        RUN   = cursorpos[0] - playerpos.rect.x
        RISE  = cursorpos[1] - playerpos.rect.y
        SLOPE = RISE / RUN
        self.rect.x += 1
        self.rect.y -= SLOPE

    def quadrant2(self, playerpos, cursorpos): 
        RUN   = playerpos.rect.x - cursorpos[0]
        RISE  = cursorpos[1] - playerpos.rect.y
        SLOPE = RISE / RUN
        self.rect.x -= 1
        self.rect.y -= SLOPE
    
    def quadrant3(self, playerpos, cursorpos): 
        RUN   = playerpos.rect.x - cursorpos[0]
        RISE  = playerpos.rect.y - cursorpos[1]
        SLOPE = RISE / RUN
        self.rect.x -=1
        self.rect.y += SLOPE

    def quadrant4(self, playerpos, cursorpos): 
        RUN   = cursorpos[0] - playerpos.rect.x
        RISE  = playerpos.rect.y - cursorpos[1]
        SLOPE = RISE / RUN
        self.rect.x +=1
        self.rect.y += SLOPE
