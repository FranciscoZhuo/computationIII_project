from utils import * #acho que não é preciso
import pygame
from config import resolution, width, height
from weapons import MachineGun, ShotGun, SniperRifle, Flamethrower
from abilities import ExtraSpeed, Shield, NewLife, DoubleDamage
from inventory import Inventory
from monetarysystem import MonetarySystem

white=(255, 255, 255)
dark = (50, 50, 50)
class Shop:
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
            {"name": "Machine Gun", "type": "weapon", "price": 50, "object": MachineGun()},
            {"name": "Shot Gun", "type": "weapon", "price": 150, "object": ShotGun()},
            {"name": "Sniper Rifle", "type": "weapon", "price": 100, "object": SniperRifle()},
            {"name": "Flamethrower", "type": "weapon", "price": 200, "object": Flamethrower()},
            {"name": "Extra Speed", "type": "ability", "price": 30, "object": ExtraSpeed()},
            {"name": "Shield", "type": "ability", "price": 50, "object": Shield()},
            {"name": "New Life", "type": "ability", "price": 75, "object": NewLife()},
            {"name": "Double Damage", "type": "ability", "price": 50, "object": DoubleDamage()},
        ]

        #self.selected_item= None #For now

    def shop(self):
        square_positions = [
            (254, 318, 360, 428),
            (390, 318, 496, 428),
            (528, 318, 634, 428),
            (666, 318, 772, 428),
            (254, 477, 360, 589),
            (390, 477, 496, 589),
            (528, 477, 634, 589),
            (666, 477, 772, 589),
        ]

        message = ""
        message_time = 0
        small_font = pygame.font.Font("assets/Creepster-Regular.ttf", 20)

        #Confirmation button of the
        while self.running:
            self.screen.blit(self.shop_background, (0, 0))  # Drawing the background of the shop

            #Show the current balance
            balance_text = self.font.render(f"Coins: {self.monetary_system.balance}", True, white)
            self.screen.blit(balance_text, (50, 50))

            #Instructions
            instruction_text = self.font.render("Click on the item you want to purchase.", True, white)
            self.screen.blit(instruction_text, (50, 700))

            #Temporary Message
            if message and pygame.time.get_ticks() - message_time < 2000: #2 seconds
                message_color = (0, 204, 0) if "added to inventory" in message else (255, 102, 102)
                message_text = self.font.render(message, True, message_color)
                message_rect = message_text.get_rect(center=(self.screen.get_width() // 2, 50)) #center the text
                self.screen.blit(message_text, message_rect) #where the message is going to appear
            elif message:
                message="" #Clean the message

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "shop"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    #Verifies if the player clicked on the item
                    for index, item in enumerate(self.items):
                        x1, y1, x2, y2 = square_positions[index]
                        if x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2:
                            #Prevent rebuying weapons
                            if item["type"] == "weapon" and item["object"] in self.inventory.items: #checks if the exact same object exists in the inventory
                                message = f"{item['name']} is already in your inventory!"
                                message_time = pygame.time.get_ticks()
                            #Tries to buy
                            elif self.monetary_system.spend_money(item["price"]):
                                if item["type"] == "weapon":
                                    self.inventory.add_item(item["object"])
                                elif item["type"] == "ability":
                                    self.inventory.add_ability(item["object"])
                                message = f"{item['name']} added to inventory!"
                                message_time = pygame.time.get_ticks()
                            else:
                                message = "Not enough money!"
                                message_time=pygame.time.get_ticks()



            for index, item in enumerate(self.items):
                x1, y1, x2, y2 = square_positions[index]
                x_center = (x1 + x2) // 2
                y_center = (y1 +y2)  // 2

                if item["type"] == "weapon" and item["object"] in self.inventory.items: #Checks if the item is already on the inventory
                    square_color = (192, 192, 192) # Grey to the items bought
                elif self.monetary_system.balance < item["price"]:
                    square_color = (255, 153, 153)  # Red if you don´t have enough money.
                else:
                    square_color = (204, 255, 204)  # Green if you have enough money and not bought yet.

                    #Draw the squares (we need to have 8 aquares)
                pygame.draw.rect(self.screen, square_color, (x1, y1, x2 - x1, y2 - y1), border_radius=10) #going to be the dark square
                pygame.draw.rect(self.screen, (41, 0, 48), (x1, y1, x2 - x1, y2 - y1), 2, border_radius=10) #going to be the white square borda(?)

                #imagem
                image_item = pygame.transform.scale(item["object"].image, (80,80))
                self.screen.blit(image_item, (x_center-40, y_center-40))

                # name item and price item
                name_text = small_font.render(item["name"], True, white)
                price_text = small_font.render(f"{item['price']} coins", True, (255,255,102))

                if index < 4: #superior line
                    self.screen.blit(name_text, (x_center - name_text.get_width() // 2, y1 - 55))
                    self.screen.blit(price_text, (x_center -price_text.get_width() // 2, y1-35))
                else: #inferior line
                    self.screen.blit(name_text, (x_center - name_text.get_width() // 2, y2 + 5))
                    self.screen.blit(price_text, (x_center - price_text.get_width() // 2, y2 + 25))

            # Render the "Press Enter to continue" message in the bottom-right corner
            enter_text = small_font.render('Press "Enter" to continue game', True, white)
            enter_text_rect = enter_text.get_rect(bottomright=(resolution[0] - 20, resolution[1] - 20))
            self.screen.blit(enter_text, enter_text_rect)

            pygame.display.flip()
            self.clock.tick(fps)
