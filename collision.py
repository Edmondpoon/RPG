import pygame
def Spawn(mobs, POSx, POSy):
    for mob in mobs:
        #checks if the new spawn will be on top of another mob
        #must check whether mob is a wizard or tank since they are different sizes

        if mob.rect.x == POSx and mob.rect.y == POSy:
            return False
    return True

