import random
import pygame

class TreasureChest(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/chest.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.last_spawn_time = 0  # Time when chest was last spawned
        self.spawn_interval = 20000  # 20 seconds interval between chest spawns
        self.disappear_time = 10000  # Chest disappears after 10 seconds
        self.spawned = False  # Whether the chest is currently active on the screen


    def spawn(self):
            """
            Spawns the chest at a random location on the screen.
            """
            self.rect.x = random.randint(50, 974)
            self.rect.y = random.randint(50, 718)
            self.last_spawn_time = pygame.time.get_ticks()
            self.spawned = True
            print(f"Chest spawned at ({self.rect.x}, {self.rect.y})")

    def update(self):
        """
        Handles spawning logic based on the spawn interval.
        """
        current_time = pygame.time.get_ticks()
        if not self.spawned and current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn()

        # Check if the chest should disappear
        if self.spawned and current_time - self.last_spawn_time > self.disappear_time:
            self.spawned = False
            print("Chest disappeared after 10 seconds.")

    def display_reward_screen(self,screen):
        """
        Displays the reward screen and waits for the player to press OK.
        """
        font = pygame.font.Font("assets/bloodcrow.ttf", 36)
        screen.fill((0, 0, 0))  # Clear the screen

        # Display reward text
        reward_text = font.render("You found a treasure chest!", True, (255, 255, 255))
        screen.blit(reward_text, (100, 100))

        # Display OK button
        ok_button = pygame.Rect(200, 200, 100, 50)
        pygame.draw.rect(screen, (0, 128, 0), ok_button)  # Green button
        ok_text = font.render("OK", True, (255, 255, 255))
        screen.blit(ok_text, (ok_button.x + 25, ok_button.y + 10))

        pygame.display.flip()

        # Wait for the player to click OK
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ok_button.collidepoint(event.pos):
                        waiting = False  # Exit the reward screen
