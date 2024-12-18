import pygame
from config import *
from utils import *
from utils import under_construction
from weapons import Pistol, ShotGun, MachineGun
from abilities import ExtraSpeed, Shield
from inventory import Inventory
from monetarysystem import MonetarySystem

pygame.init()

resolution = (1024, 768)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Loja")
creepster_font = pygame.font.Font("assets/Creepster-Regular.ttf", 30)

#Shop background
shop_background = pygame.image.load("assets/Fundo_shop.png")
shop_background = pygame.transform.scale(shop_background, resolution)

items = [
    {"name": "Shield", "price": 50, "ability": Shield(), "pos": (280, 200)},
    {"name": "Extra Speed", "price": 50, "ability": ExtraSpeed(), "pos": (480, 200)},
]
def shop(player, monetary_system, inventory):
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.blit(shop_background, (0,0))
        monetary_system.show_balance(screen, creepster_font, 20, 20) #shows the amount of money
        for item in items:
            image = pygame.transform.scale(item["ability"].image, (80,80))
            screen.blit(image, item["pos"])
            text = creepster_font.render(f"{item['price']} coins", True, (255, 255, 255))
            screen.blit(text, (item["pos"][0], item["pos"][1] + 90))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clique esquerdo
                mouse_pos = pygame.mouse.get_pos()
                for item in items:
                    item_rect = pygame.Rect(item["pos"][0], item["pos"][1], 80, 80)
                    if item_rect.collidepoint(mouse_pos):
                        if monetary_system.spend_money(item["price"]):
                            inventory.add_ability(item["ability"])
                            print("Done!")
                        else:
                            print("Not enough money!")

            if event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        clock.tick(30)



#Cada uso da habilidade consome uma unidade que o jogador comprou.
#Se o jogador tiver 3 escudos, ele pode usar o escudo 3 vezes antes de precisar comprar mais.
# o uso é limitado ao número de unidades no inventário.