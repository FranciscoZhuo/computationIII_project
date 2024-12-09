from config import *
import math
import pygame
from enemy import *
from player import Player
from powerups import PowerUpController
from monetarysystem import MonetarySystem
from shed import shed

def game_loop():
    player = Player()
    current_state = "main"

    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shed":
            current_state = shed(player)


def execute_game(player: Player):
    """
    Main function to execute the game loop

    """

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Setting up the background:
    screen = pygame.display.set_mode(resolution)
    background = pygame.image.load("img/grass.jpg")
    background = pygame.transform.scale(background, (width, height))


    # Screen setup
    pygame.display.set_caption("Surge of the Silence")

    # Player Setup
    # player = Player() NO NEEDED ANYMORE
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Initialize the bullet group
    bullets = pygame.sprite.Group()

    # Initialize the enemy group
    zombies = pygame.sprite.Group()
    zombies_spawn_timer = 0

    #Initialize the PowerUpController
    power_up_controller = PowerUpController()

    #Initialize Monetary System
    monetary_system = MonetarySystem() #we can put inside of the MonetarySystem() the initial_balance = amount,
    # for example initial_balance = 50, which means the player will always start the game with 50€.

    running = True
    while running:
        # Control frame rate
        clock.tick(fps)
        # FIll the background
        screen.blit(background, (0,0))
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # Calculate dt (delta time: time between frames)
        dt = clock.tick(fps) / 1000.0  # dt is in seconds

        # Shooting
        player.shoot(bullets)

        # Spawn timer
        if zombies_spawn_timer > 0:
            zombies_spawn_timer -= 1

        # Spawning the enemies
        if zombies_spawn_timer <= 0:
            # Randomly select a zombie type
            zombie_type = random.choice([FastZombie, TankZombie, ExplodingZombie, Enemy])
            new_enemy = zombie_type()  # Instantiate the selected zombie type
            zombies.add(new_enemy)
            zombies_spawn_timer = 2 * fps  # Every two seconds

        # Weighted random selection
        zombie_type = random.choices(
                [FastZombie, TankZombie, ExplodingZombie, Enemy],
                weights=[0.2, 0.2, 0.1, 0.5],  # 20% Fast, 20% Tank, 10% Exploding, 50% Normal Enemy
                k=1
            )[0]
        new_enemy = zombie_type()

        # Checking for collisions between enemies and bullets
        for bullet in bullets:
            collided_zombies = pygame.sprite.spritecollide(bullet, zombies, False)
            for zombie in collided_zombies:
                zombie.health -= 5  # Decrease health by 5
                bullet.kill()  # Destroy the bullet
                if zombie.health <= 0:
                    zombie.kill()  # Destroy the enemy
                    monetary_system.money_earned(10) #Ganha 10€ por zombie derrotado




        # Update positions
        player_group.update(dt)
        bullets.update()
        zombies.update(player)

        #Update the draw power-ups
        power_up_controller.update(player,zombies)
        power_up_controller.draw(screen)

        # Checking if the user goes into the shed area
        if player.rect.right >= width:
            # Change the game state to shed
            return "shed"

        # Drawing the object
        player_group.draw(screen)
        zombies.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # Shows monetary balance
        font = pygame.font.SysFont("Roboto", 30)
        monetary_system.show_balance(screen,font)

        pygame.display.flip()


def level1(player: Player):
    """

    Executes the first level of the game
    """
    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Setting up the background:
    screen = pygame.display.set_mode(resolution)
    background = pygame.image.load("img/grass.jpg")
    background = pygame.transform.scale(background, (width, height))

    # Screen setup
    screen = pygame.display.set_mode(resolution)