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
            {"name": "New Life", "type": "ability", "price": 200, "object": NewLife()},
        ]

        #self.selected_item= None #For now

    def shop(self):
        square_positions = [
            (170, 210, 270, 310),  # Quadrado 1
            (320, 210, 420, 310),  # Quadrado 2
            (470, 210, 570, 310),  # Quadrado 3
            (620, 210, 720, 310),  # Quadrado 4
            (170, 360, 270, 460),  # Quadrado 5
            (320, 360, 420, 460),  # Quadrado 6
            (470, 360, 570, 460),  # Quadrado 7
            (620, 360, 720, 460),  # Quadrado 8
        ]

        while self.running:
            self.screen.blit(self.shop_background, (0, 0))  # Drawing the background of the shop

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "level1"
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for index, item in enumerate(self.items):
                            x1, y1, x2, y2 = square_positions[index]

                            if x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2:
                                #Tries to buy
                                if self.monetary_system.spend_money(item["price"]):
                                    self.inventory.add_item(item["object"])
                                    print(f"{item['name']} bought")
                                else:
                                    print(f"Not enough money!")



            for index, item in enumerate(self.items):
                x1, y1, x2, y2 = square_positions[index]
                x_center = (x1 + x2) // 2
                y_center = (y1 +y2)  // 2

                #Draw the squares (we need to have 8 aquares)
                pygame.draw.rect(self.screen, dark, (x1, y1, x2 - x1, y2 - y1), 0) #going to be the dark square
                pygame.draw.rect(self.screen, white, (x1, y1, x2 - x1, y2 - y1), 2) #going to be the white square borda(?)

                #imagem
                image_item = pygame.transform.scale(item["object"].image, (80,80))
                self.screen.blit(image_item, (x_center-40, y_center-40))

                #Item name
                text_item = self.font.render(item["name"], True, white)
                text_rect = text_item.get_rect(center=(x_center, y2 + 10))
                self.screen.blit(text_item, text_rect) #just ajustments to text appears above the sqaure (em cima do quadrado)

                #price
                price_item = self.font.render(f"{item['price']} coins", True, (0,255,0))
                price_rect=price_item.get_rect(center=(x_center, y2+30))
                self.screen.blit(price_item, price_rect)

            pygame.display.flip()
            self.clock.tick(60)
