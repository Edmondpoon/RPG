import pygame
import images

WIDTH      = 15
HEIGHT     = 15

def generate_store(window, store_font):
    attacks    = []
    PLACEMENTS = [(27, 100), (157, 100), (287, 100), (417, 100), (547, 100)]
    for attack in range(5):    
        attacks.append(images.store_attacks(WIDTH, HEIGHT, PLACEMENTS[attack][0], PLACEMENTS[attack][1], attack))
    return attacks 

def maintain_store(window, sprites_list, FONTS):
    COSTS_FONT, MENU_FONT = FONTS
    PRICES            = [10, 25, 50, 100, 500]
    PLACEMENTS        = [23, 153, 283, 413, 543]
    BUTTON_PLACEMENTS = [21, 151, 281, 411, 541]
    ATTACKS           = ["attack1", "attack2", "attack3", "attack4", "attack5"]   

    MAINMENU_TEXT     = MENU_FONT.render("Main Menu", True, (0, 0, 0))
    PRICES_TEXT       = {}
    for attack in range(len(ATTACKS)):
        PRICES_TEXT[ATTACKS[attack]] = COSTS_FONT.render("Costs " + str(PRICES[attack]) + " coins", True, (0, 0, 0)) 

    window.fill((255, 255, 255))
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect((15, 14), (108, 18)))

    window.blit(MAINMENU_TEXT, (15, 15))
    for price in range(len(ATTACKS)):
        window.blit(PRICES_TEXT[ATTACKS[price]], (PLACEMENTS[price], 175))
    with open("purchases.txt", mode = "r+") as purchases:
        purchasable = purchases.readlines()
        purchasable =         purchasable[0].split(",")
    for attack in range(len(ATTACKS)):
        if "False" in purchasable[attack]:
            pygame.draw.ellipse(window, (200, 200, 200), pygame.Rect((BUTTON_PLACEMENTS[attack], 195), (100, 25))) 
        else:
            #add a different buttton and color that says equip/equipped 
            pass
        
    sprites_list.draw(window)
    pygame.display.flip()
    if pygame.mouse.get_pressed() == (True, False, False):
        position = pygame.mouse.get_pos()
        if position[0] > 15 and position[0] < 123 and position[1] > 14 and position[1] < 32:
            return False, False
    return True, True
