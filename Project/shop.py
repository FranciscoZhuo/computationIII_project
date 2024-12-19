from utils import * #acho que não é preciso
from utils import under_construction #acho que não é preciso
import pygame
from config import resolution, width, height
from weapons import MachineGun, ShotGun, SniperRifle, Flamethrower
from abilities import ExtraSpeed, Shield, NewLife
from inventory import Inventory
from monetarysystem import MonetarySystem

white=(255, 255, 255)
dark = (50, 50, 50)
class Shop():
    def __init__(self, player):
        pygame.init()
        self.player=player
        self.inventory = player.inventory
        self.monetary_system = player.monetary_system
        self.screen = pygame.display.set_mode(resolution)
        self.shop_background = pygame.image.load("assets/Fundo_shop.png").convert()
        #self.shop_background = pygame.transform.scale(self.shop_background, resolution)
        self.font = pygame.font.Font("assets/Creepster-Regular.ttf", 30)
        self.clock=pygame.time.Clock()
        self.running = True

        self.items = [
            {"name": "Machine Gun", "type": "weapon", "price": 100, "object": MachineGun()},
            {"name": "Shot Gun", "type": "weapon", "price": 150, "object": ShotGun()},
            {"name": "Sniper Rifle", "type": "weapon", "price": 200, "object": SniperRifle()},
            {"name": "Flamethrower", "type": "weapon", "price": 250, "object": Flamethrower()},
            {"name": "Extra Speed", "type": "ability", "price": 100, "object": ExtraSpeed()},
            {"name": "Shield", "type": "ability", "price": 150, "object": Shield()},
            {"name": "New Life", "type": "ability", "price": 200, "object": NewLife()},
            {"name": "New Life", "type": "ability", "price": 200, "object": NewLife()}, #repetida porqie falta 1

        ]

        self.selected_item= None #For now

    def shop(self):
        while self.running:
            self.screen.blit(self.shop_background, (0, 0))  # Drawing the background of the shop

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "level1"


            x_start = 120 #Where x starts, initial position
            y_start = 200 #Where y starts, initial position
            x_gap = 200 #Gap between squares horizontal
            y_gap = 150 #Gap between squares vertically

            for index, item in enumerate(self.items):
                 #Square position
                row = index // 4 #Divide by 4
                col = index % 4  #Divide by 4

                x = x_start + (col*x_gap)
                y = y_start +(row * y_gap)

                #Draw the squares (we need to have 8 aquares)
                pygame.draw.rect(self.screen, dark, (x, y, 100, 100), 0) #going to be the dark square
                pygame.draw.rect(self.screen, white, (x, y, 100, 100), 2) #going to be the white square borda(?)

                #Item name
                text_item = self.font.render(item["name"], True, white)
                self.screen.blit(text_item, (x+5, y+110)) #just ajustments to text appears above the sqaure (em cima do quadrado)

                #price
                price_item = self.font.render(f"{item['price']} coins", True, (0,255,0))
                self.screen.blit(price_item, (x+20, y+130))

            if self.player.monetary_system.spend_money(item["price"]):
                #if we have enough balance:
                self.player.inventory[item["name"]] = item["object"]

            pygame.display.flip()
            self.clock.tick(60)
