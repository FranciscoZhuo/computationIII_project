from config import *
import math
import pygame
from enemy import *
from player import Player
from powerups import PowerUpController
from monetarysystem import MonetarySystem
from shop import *
from inventory import *
from obstacle import *
from health import *


def game_loop():
    player = Player()
    pygame.mixer.music.stop()
    current_state = "main"

    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shop":
            current_state = shop()
        elif current_state == "gameover":
            current_state == game_over(screen)

def game_over(screen):
    """
    Display a game over screen.
    """

    # Background configs
    gif_frame_bg = 0
    clock_bg = pygame.time.Clock()

    bloodcrowfont = pygame.font.Font("assets/bloodcrow.ttf", 35)
    text = bloodcrowfont.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Return to main menu on Enter key
                    from interface import interface
                    interface()
                    return
                elif event.key == pygame.K_ESCAPE:  # Quit game on Escape key
                    pygame.quit()
                    return

        # Background
        clock_bg.tick(20)
        if gif_frame_bg != 125:
            screen.blit(pygame.image.load(f'assets/gameover/frame_{gif_frame_bg}.png'), (0, 0))
            screen.blit(text, text_rect)
            gif_frame_bg += 1
        else:
            from interface import interface
            interface()
            return

        pygame.display.flip()

def execute_game(player: Player):
    """
    Main function to execute the game loop

    """

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()



    # ==== SETTING UP THE GAME ====

    # Setting up the background
    screen = pygame.display.set_mode(resolution)
    background = pygame.image.load("assets/lvl2.jpg").convert()
    background = pygame.transform.scale(background, (width, height))

    profile = pygame.image.load("assets/Profile.png")

    # Setting up Background Music
    pygame.mixer.music.load('assets/BGMusic.mp3')
    pygame.mixer.music.play(-1)

    # Timer Setup
    level_duration = 300  # Level duration in seconds (e.g., 5 minutes)
    start_time = pygame.time.get_ticks()  # Record the start time

    # Screen setup
    pygame.display.set_caption("Surge of the Silence")

    # Player Setup
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Initialize the bullet group
    bullets = pygame.sprite.Group()

    # Initialize the obstacle group
    obstacles = pygame.sprite.Group()

    # Initialize the enemy group
    zombies = pygame.sprite.Group()
    zombies_spawn_timer = 0

    #Initialize the item group
    items_group = pygame.sprite.Group()
    item_spawn_timer = 0

    # Initialize Inventory
    inventory = Inventory()
    for weapon in player.inventory.values():
        inventory.add_item(weapon) # adding weapons to the inventory

    #Initialize the PowerUpController
    power_up_controller = PowerUpController()

    #Initialize Monetary System
    monetary_system = MonetarySystem() #we can put inside of the MonetarySystem() the initial_balance = amount,
    # for example initial_balance = 50, which means the player will always start the game with 50€.

    # Initialize House obstacles using a list and a loop
    house_definitions = [
        (495, 254, 45, 125),
        (542, 185, 28, 195),
        (570, 172, 179, 235),
        (749, 187, 29, 195),
        (778, 249, 81, 135),
        (859, 249, 115, 125)
    ]

    for x, y, hwidth, hheight in house_definitions:
        obstacles.add(Obstacle(x, y, hwidth, hheight))

    # Initialize health bar
    player_health_bar = HealthBar(player.max_health)


    # ==== GAME LOOP ====
    running = True
    while running:
        # Control frame rate
        clock.tick(fps)

        # Set tup the background
        screen.blit(background, (0,0))

        # Calculate dt (delta time: time between frames)
        dt = clock.tick(fps) / 1000.0  # dt is in seconds

        # Calculate elapsed time
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert to seconds
        remaining_time = max(level_duration - elapsed_time, 0)  # Remaining time in seconds

        # End the level when time runs out
        if remaining_time <= 0:
            print("Level Complete!")
            return "main"  # Return to main menu or next level

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    inventory.toggle_visibility()  # Toggle the inventory visibility

                # Check number key presses (1 to 0)
                if pygame.K_1 <= event.key <= pygame.K_9:
                    slot_index = event.key - pygame.K_1  # 1 maps to slot 0, 2 to slot 1, etc.
                    inventory.change_slot(slot_index)
                    selected_weapon = inventory.get_selected_item()
                    if selected_weapon:
                        player.weapon_switching(selected_weapon.name)
        # Shooting
        player.shoot(bullets, zombies)

        # Handle item pickups
        for item in items_group:  # Assuming items_group contains spawnable items
            if pygame.sprite.collide_rect(player, item):
                inventory.add_item({"name": item.name, "icon": item.icon_path})  # Add item with its details
                item.kill()  # Remove the item from the game


        # ==== SPAWN ====

        # Spawn timer
        if zombies_spawn_timer > 0:
            zombies_spawn_timer -= 1

        # Weighted random selection
        zombie_type = random.choices(
                [FastZombie, TankZombie, ExplodingZombie, Enemy],
                weights=[0.2, 0.2, 0.1, 0.5],  # 20% Fast, 20% Tank, 10% Exploding, 50% Normal Enemy
                k=1
            )[0]

        # Spawning the enemies
        if zombies_spawn_timer <= 0:
            # Randomly select a zombie type
            zombie_type = random.choice([FastZombie, TankZombie, ExplodingZombie, NormalZombie])
            new_enemy = zombie_type()  # Instantiate the selected zombie type
            zombies.add(new_enemy)
            zombies_spawn_timer = fps  # Every two seconds




        # ==== CHECKERS ====

        # Checking for collisions between enemies and bullets
        for bullet in bullets:
            collided_zombies = pygame.sprite.spritecollide(bullet, zombies, False)
            for zombie in collided_zombies:
                zombie.take_damage(bullet.damage)
                bullet.kill()  # Destroy the bullet
                if zombie.health <= 0:
                    zombie.kill()  # Destroy the enemy
                    monetary_system.money_earned(10) #Ganha 10€ por zombie derrotado

        # Check for collisions between player and enemies
        for zombie in zombies:
            if pygame.sprite.collide_rect(player, zombie):
                player.take_damage(zombie.damage)  # Player takes 10 damage

        # Check if player's health is zero or less
        if player.health <= 0:
            pygame.mixer.music.stop()
            return "gameover"



        # ==== UPDATES ====

        # Update positions
        player_group.update(dt, obstacles)
        player_health_bar.update(player.health)
        bullets.update()
        # Update zombies with animation
        for zombie in zombies:
            zombie.update(player, dt)



        # Update the draw power-ups
        power_up_controller.update(player,zombies)
        power_up_controller.draw(screen)



        # ==== DRAWS ====

        # Drawing the object
        player_group.draw(screen)
        player.draw_debug_rect(screen)
        zombies.draw(screen)
        for zombie in zombies:
            zombie.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)


        inventory.render(screen)
        screen.blit(profile, (0, 0))


        # Shows monetary balance
        font1 = pygame.font.SysFont("assets/Creepster-Regular.ttf)", 25)
        monetary_system.show_balance(screen, font1, 135, 40)

        # Draw timer on the screen
        font = pygame.font.SysFont("assets/Creepster-Regular.ttf)", 30)
        timer_text = font.render(f"Time Left: {int(remaining_time)}s", True, (128, 0, 128))
        screen.blit(timer_text, (860, 30))

        # Draw the health bar inside the profile
        player_health_bar.draw_in_profile(screen, profile)


        pygame.display.flip()