import pygame
import images

WIDTH      = 15
HEIGHT     = 15

def COINS(mob, TOTAL_COINS):
    VALUES = {"10": 2, "25" : 1, "100": 10}
    TOTAL_COINS += VALUES[str(mob.maxhp)]
    return TOTAL_COINS

def generate_store(window, store_font):
    attacks    = []
    PLACEMENTS = [(27, 100), (157, 100), (287, 100), (417, 100), (547, 100)]
    for attack in range(5):
        attacks.append(images.store_attacks(WIDTH, HEIGHT, PLACEMENTS[attack][0], PLACEMENTS[attack][1], attack))
    return attacks

def maintain_store(window, sprites_list, FONTS):
    COSTS_FONT, MENU_FONT, PURCHASE_FONT = FONTS
    PRICES            = [10, 25, 50, 100, 500]
    PLACEMENTS        = [23, 153, 283, 413, 543]
    BUTTON_PLACEMENTS = [21, 151, 281, 411, 541]
    ATTACKS           = ["attack1", "attack2", "attack3", "attack4", "attack5"]

    with open("coins.txt", mode = "r") as coin:
        TOTAL_COINS = coin.readlines()
        TOTAL_COINS = TOTAL_COINS[0].split(" ")

    MAINMENU_TEXT     = MENU_FONT.render("Main Menu", True, (0, 0, 0))
    COINS_TEXT        = MENU_FONT.render("Total coins: " + str(TOTAL_COINS[1]), True, (0, 0, 0))
    PRICES_TEXT       = {}
    for attack in range(len(ATTACKS)):
        PRICES_TEXT[ATTACKS[attack]] = COSTS_FONT.render("Costs " + str(PRICES[attack]) + " coins", True, (0, 0, 0))

    window.fill((255, 255, 255))
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect((15, 14), (108, 18)))

    window.blit(MAINMENU_TEXT, (15, 15))
    window.blit(COINS_TEXT, (450, 15))
    for price in range(len(ATTACKS)):
        window.blit(PRICES_TEXT[ATTACKS[price]], (PLACEMENTS[price], 175))

    with open("purchases.txt", mode = "r+") as purchases:
        purchasable = purchases.readlines()
        purchasable = purchasable[0].split(" ")
    for attack in range(len(ATTACKS)):
        if "False" in purchasable[attack + 1]:
            pygame.draw.ellipse(window, (200, 200, 200), pygame.Rect((BUTTON_PLACEMENTS[attack], 195), (100, 25)))
            PURCHASE_TEXT = PURCHASE_FONT.render("Purchase", True, (0, 0, 0))
            window.blit(PURCHASE_TEXT, (BUTTON_PLACEMENTS[attack] + 13, 199))
        else:
            pygame.draw.ellipse(window, (0, 0, 0), pygame.Rect((BUTTON_PLACEMENTS[attack], 195), (100, 25)))

    with open("equipped.txt", mode = "r+") as equip:
        equipped = equip.readlines()
        equipped = equipped[0].split(" ")
    for attack in range(len(ATTACKS)):
        if "True" in equipped[attack + 1]:
            EQUIPPED_TEXT = PURCHASE_FONT.render("Equipped", True, (255, 255, 255))
            window.blit(EQUIPPED_TEXT, (BUTTON_PLACEMENTS[attack] + 13, 199))
        elif "False" in equipped[attack + 1]:
            EQUIP_TEXT = PURCHASE_FONT.render("Equip", True, (255, 255, 255))
            window.blit(EQUIP_TEXT, (BUTTON_PLACEMENTS[attack] + 28, 199))


    sprites_list.draw(window)
    pygame.display.flip()
    if pygame.mouse.get_pressed() == (True, False, False):
        position = pygame.mouse.get_pos()
        if position[0] > 15 and position[0] < 123 and position[1] > 14 and position[1] < 32:
            return False, False
        else:
            for attack in range(len(ATTACKS)):
                if position[0] > BUTTON_PLACEMENTS[attack] + 1 and position[0] < BUTTON_PLACEMENTS[attack] + 99 and position[1] > 196 and position[1] < 219:
                    with open("purchases.txt", mode = "r") as purchase:
                        purchasable = purchase.readlines()
                        purchasable = purchasable[0].split(" ")
                        if PRICES[attack] <= int(TOTAL_COINS[1]) and "False" in purchasable[attack + 1]:
                            with open("coins.txt", mode = "r+") as coins:
                                COIN = coins.readlines()
                                COIN = COIN[0].split(" ")
                                temp = []
                                temp2 = ""
                                for item in range(len(COIN)):
                                    if item == 0:
                                        temp.append("PLACEHOLDER")
                                    elif item <= 2:
                                        temp.append(COIN[item])
                                temp[1] = int(temp[1]) - PRICES[attack]
                                coins.truncate(0)
                                for item in temp:
                                    temp2 += str(item) + " "
                                coins.write(temp2)
                            with open("equipped.txt", mode = "r+") as equip:
                                equipped = equip.readlines()
                                equipped = equipped[0].split(" ")
                                temp  = []
                                temp2 = ""
                                for item in equipped:
                                    temp.append(item)
                                temp[attack + 1] = "False"
                                equip.truncate(0)
                                for item in temp:
                                    temp2 += item + " "
                                equip.write(temp2)
                            with open("purchases.txt", mode = "r+") as purchases:
                                purchasable = purchases.readlines()
                                purchasable = purchasable[0].split(" ")
                                temp  = []
                                temp2 = ""
                                for item in purchasable:
                                    temp.append(item)
                                temp[attack + 1] = "True"
                                purchases.truncate(0)
                                for item in temp:
                                    temp2 += item + " "
                                purchases.write(temp2)




    return True, True
