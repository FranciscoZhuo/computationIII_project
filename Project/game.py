from Project.cutscene import cutscene2, cutscene3
from config import *
import math
import pygame
from enemy import *
from player import Player
from powerups import *
from monetarysystem import MonetarySystem
from shop import *
from inventory import *
from obstacle import *
from health import *
from treasurechest import *


# ==== GAME LOOP =====
def game_loop():
    player = Player()
    pygame.mixer.music.stop()
    current_state = "intro1"

    while True:
        if current_state == "intro1":
            current_state = intro1(player)

        elif current_state == "level1":
            current_state = level1(player)

        elif current_state == "shop":
            shop_instance = Shop(player)
            current_state = shop_instance.shop()

        elif current_state == "gameover":
            current_state = game_over()

        elif current_state == "cutscene2":
            current_state = cutscene2()

        elif current_state == "intro2":
            current_state = intro2(player)

        elif current_state == "level2":
            current_state = level2(player)

        elif current_state == "cutscene3":
            current_state = cutscene3()


# ==== INTRO 1 ====

def intro1(player: Player):
    """
    First intro level of the game.

    """

    # ========== Set up ===============

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(resolution)
    background = pygame.image.load("assets/intro level.png").convert()  # Use convert() or convert_alpha()
    profile = pygame.image.load("assets/Profile.png").convert_alpha() # Use convert_alpha() if it has transparency
    font = pygame.font.SysFont("assets/Creepster-Regular.ttf", 25)  # Load font once

    pygame.mixer.music.load('assets/Monologue Tay.mp3')
    pygame.mixer.music.play(1)

    # ============ Initialize ================

    # Initialize Inventory
    inventory = Inventory()
    for weapon in player.inventory.values(): # Assuming player.inventory is defined
        inventory.add_item(weapon)

    # Initialize Health Bar
    player_health_bar = HealthBar(player.max_health)

    # Initialize the Monetary System
    monetary_system = MonetarySystem()

    # Initialize the player
    player_group = pygame.sprite.Group() #Group single player
    player_group.add(player) #Add to the group

    # Initialize the obstacles
    obstacles = pygame.sprite.Group()  # If obstacles are used



    # ========== Game Loop ===================

    running = True
    while running:

        # Control frame rate
        clock.tick(fps)
        # Calculate delta time
        dt = clock.tick(fps) / 1000.0

        # ========== Event Handling ==============

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return

            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_i:
                    inventory.toggle_visibility()
                elif pygame.K_1 <= ev.key <= pygame.K_9: #If event is number pad
                    slot_index = ev.key - pygame.K_1
                    inventory.change_slot(slot_index)
                    selected_weapon = inventory.get_selected_item() #Get selected item
                    if selected_weapon:
                        player.weapon_switching(selected_weapon.name)

        # ==== Updates (Grouped) ====
        player_group.update(dt, obstacles)
        player_health_bar.update(player.health)


        # ========= Level Ending Conditions ===============
        if player.rect.bottom >= height:
            return "level1"  # Return the next game state


        # =============== Draws ======================
        screen.blit(background, (0, 0))
        player_group.draw(screen)

        # ======== User Interface Elements =============
        screen.blit(profile, (0, 0))
        inventory.render(screen)
        player_health_bar.draw_in_profile(screen, profile) #Draw health inside the profile
        monetary_system.show_balance(screen, font, 135, 40)  # Use the pre-loaded font


        pygame.display.flip()



# ==== INTRO 2 ====
def intro2(player: Player):
    """
    First intro level of the game.

    """

    # ========== Set up ===============

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(resolution)
    background = pygame.image.load("assets/intro2.png").convert()  # Use convert() or convert_alpha()
    profile = pygame.image.load("assets/Profile.png").convert_alpha() # Use convert_alpha() if it has transparency
    font = pygame.font.SysFont("assets/Creepster-Regular.ttf", 25)  # Load font once


    # ============ Initialize ================

    # Initialize Inventory
    inventory = Inventory()
    for weapon in player.inventory.values(): # Assuming player.inventory is defined
        inventory.add_item(weapon)

    # Initialize Health Bar
    player_health_bar = HealthBar(player.max_health)

    # Initialize the Monetary System
    monetary_system = MonetarySystem()

    # Initialize the player
    player_group = pygame.sprite.Group() #Group single player
    player_group.add(player) #Add to the group

    # Initialize the obstacles
    obstacles = pygame.sprite.Group()  # If obstacles are used



    # ========== Game Loop ===================

    running = True
    while running:

        # Control frame rate
        clock.tick(fps)
        # Calculate delta time
        dt = clock.tick(fps) / 1000.0

        # ========== Event Handling ==============

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return

            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_i:
                    inventory.toggle_visibility()
                elif pygame.K_1 <= ev.key <= pygame.K_9: #If event is number pad
                    slot_index = ev.key - pygame.K_1
                    inventory.change_slot(slot_index)
                    selected_weapon = inventory.get_selected_item() #Get selected item
                    if selected_weapon:
                        player.weapon_switching(selected_weapon.name)

        # ==== Updates (Grouped) ====
        player_group.update(dt, obstacles)
        player_health_bar.update(player.health)


        # ========= Level Ending Conditions ===============
        if player.rect.bottom >= height:
            return "level2"  # Return the next game state


        # =============== Draws ======================
        screen.blit(background, (0, 0))
        player_group.draw(screen)

        # ======== User Interface Elements =============
        screen.blit(profile, (0, 0))
        inventory.render(screen)
        player_health_bar.draw_in_profile(screen, profile) #Draw health inside the profile
        monetary_system.show_balance(screen, font, 135, 40)  # Use the pre-loaded font


        pygame.display.flip()



# ==== GAME OVER ====
def game_over():
    """
    Display a game over screen.

    """
    screen = pygame.display.set_mode(resolution)
    # Background configs
    gif_frame_bg = 0
    clock_bg = pygame.time.Clock()

    bloodcrowfont = pygame.font.Font("assets/bloodcrow.ttf", 80)
    text = bloodcrowfont.render("Game Over", True, red)
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


# ==== LEVEL 1 ====
def level1(player: Player):
    """
    Main function to execute the game loop

    """

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()



    # ==== SETTING UP THE GAME ====

    # Setting up the background
    screen = pygame.display.set_mode(resolution)
    background = pygame.image.load("assets/fundo game.png").convert()
    background = pygame.transform.scale(background, (width, height))

    profile = pygame.image.load("assets/Profile.png")

    # Setting up Background Music
    pygame.mixer.music.load('assets/BGMusic.mp3')
    pygame.mixer.music.play(-1)

    # Timer Setup
    level_duration = 10  # Level duration in seconds (e.g., 5 minutes)
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


    # Initialize Inventory
    inventory = Inventory()
    for weapon in player.inventory.values():
        inventory.add_item(weapon) # adding weapons to the inventory

    #Initialize the PowerUpController
    power_up_controller = PowerUpController()
    power_up_controller.set_allowed_powerups([LifePowerUp, SlowZombiesPowerUp])  # Restrict power-ups

    # Initialize the chest
    treasure_chest = TreasureChest()
    chest_group = pygame.sprite.Group()  # Group for the chest
    chest_group.add(treasure_chest)

    #Initialize Monetary System
    monetary_system = MonetarySystem() #we can put inside of the MonetarySystem() the initial_balance = amount,
    # for example initial_balance = 50, which means the player will always start the game with 50€.


    # Initialize health bar
    player_health_bar = HealthBar(player.max_health)

    # Fade-in setup
    fade_surface = pygame.Surface(resolution)
    fade_surface.fill((0, 0, 0))
    fade_alpha = 255


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
            # Display the transition message
            fontc = pygame.font.SysFont("assets/Creepster-Regular.ttf", 40)
            message = ("Congratulations for surviving!"
                       " Now entering the shop....")
            start_time = pygame.time.get_ticks()

            while (pygame.time.get_ticks() - start_time) / 1000 < 5:
                screen.fill(deep_black)  # Clear screen with black
                text_surface = fontc.render(message, True, red)
                text_rect = text_surface.get_rect(center=(width // 2, height // 2))
                screen.blit(text_surface, text_rect)
                pygame.display.flip()
                clock.tick(fps)

            return "cutscene2"  # Transition to shop

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



        # ==== SPAWN ====

        # Spawn timer
        if zombies_spawn_timer > 0:
            zombies_spawn_timer -= 1


        # Spawn
        if zombies_spawn_timer <= 0:
            # Randomly select a zombie type
            zombie_type = random.choice([NormalZombie])
            new_enemy = zombie_type()  # Instantiate the selected zombie type
            zombies.add(new_enemy)
            zombies_spawn_timer = fps  # Every two seconds

        #Spawning the chest
        treasure_chest.update()
        if treasure_chest.spawned:
            chest_group.add(treasure_chest)
            print("Chest added to group.")


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



        # Check for collisions between player and treasure chest
        if pygame.sprite.spritecollide(player, chest_group, True):  # Remove chest after collection
            treasure_chest.spawned = False  # Mark the chest as inactive
            running = False  # Pause the game
            treasure_chest.display_reward_screen(screen)
            running=True



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



        # ==== DRAWS ====

        # Drawing the object
        player_group.draw(screen)


        zombies.draw(screen)
        for zombie in zombies:
            zombie.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # draw powerups
        power_up_controller.draw(screen)

        # Render the player
        player.render(screen)

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

        # Draw the treasure chest
        chest_group.draw(screen)


        inventory.render(screen)
        # Apply fade-in effect
        if fade_alpha > 0:
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            fade_alpha -= 5  # Adjust speed as needed

        pygame.display.flip()



# ==== LEVEL 2 ====
def level2(player: Player):
    """
    Main function to execute the game loop

    """

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()



    # ==== SETTING UP THE GAME ====

    # Setting up the background
    screen = pygame.display.set_mode(resolution)
    background = pygame.image.load("assets/fundo game.png").convert()
    background = pygame.transform.scale(background, (width, height))

    profile = pygame.image.load("assets/Profile.png")

    # Setting up Background Music
    pygame.mixer.music.load('assets/BGMusic.mp3')
    pygame.mixer.music.play(-1)

    # Timer Setup
    level_duration = 10  # Level duration in seconds (e.g., 5 minutes)
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


    # Initialize Inventory
    inventory = Inventory()
    for weapon in player.inventory.values():
        inventory.add_item(weapon) # adding weapons to the inventory

    #Initialize the PowerUpController
    power_up_controller = PowerUpController()
    power_up_controller.set_allowed_powerups([LifePowerUp, SlowZombiesPowerUp, InvisibilityPowerUP])  # Restrict power-ups

    # Initialize the chest
    treasure_chest = TreasureChest()
    chest_group = pygame.sprite.Group()  # Group for the chest
    chest_group.add(treasure_chest)

    #Initialize Monetary System
    monetary_system = MonetarySystem() #we can put inside of the MonetarySystem() the initial_balance = amount,
    # for example initial_balance = 50, which means the player will always start the game with 50€.


    # Initialize health bar
    player_health_bar = HealthBar(player.max_health)

    # Fade-in setup
    fade_surface = pygame.Surface(resolution)
    fade_surface.fill((0, 0, 0))
    fade_alpha = 255


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
            # Display the transition message
            fontc = pygame.font.SysFont("assets/Creepster-Regular.ttf", 40)
            message = ("Congratulations for surviving!"
                       " Now entering the shop....")
            start_time = pygame.time.get_ticks()

            while (pygame.time.get_ticks() - start_time) / 1000 < 5:
                screen.fill(deep_black)  # Clear screen with black
                text_surface = fontc.render(message, True, red)
                text_rect = text_surface.get_rect(center=(width // 2, height // 2))
                screen.blit(text_surface, text_rect)
                pygame.display.flip()
                clock.tick(fps)

            return "cutscene3"  # Transition to shop

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



        # ==== SPAWN ====

        # Spawn timer
        if zombies_spawn_timer > 0:
            zombies_spawn_timer -= 1

        # Weighted random selection
        zombie_type = random.choices(
                [FastZombie, TankZombie, NormalZombie],
                weights=[0.2, 0.2, 0.6],  # 20% Fast, 20% Tank, 10% Exploding, 50% Normal Enemy
                k=1
           )[0]


        # Spawn
        if zombies_spawn_timer <= 0:
            # Randomly select a zombie type
            zombie_type = random.choice([NormalZombie, FastZombie, TankZombie])
            new_enemy = zombie_type()  # Instantiate the selected zombie type
            zombies.add(new_enemy)
            zombies_spawn_timer = fps  # Every two seconds

        #Spawning the chest
        treasure_chest.update()
        if treasure_chest.spawned:
            chest_group.add(treasure_chest)
            print("Chest added to group.")


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



        # Check for collisions between player and treasure chest
        if pygame.sprite.spritecollide(player, chest_group, True):  # Remove chest after collection
            treasure_chest.spawned = False  # Mark the chest as inactive
            running = False  # Pause the game
            treasure_chest.display_reward_screen(screen)
            running=True



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



        # ==== DRAWS ====

        # Drawing the object
        player_group.draw(screen)


        zombies.draw(screen)
        for zombie in zombies:
            zombie.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # draw powerups
        power_up_controller.draw(screen, player)

        # Render the player
        player.render(screen)

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

        # Draw the treasure chest
        chest_group.draw(screen)


        inventory.render(screen)
        # Apply fade-in effect
        if fade_alpha > 0:
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            fade_alpha -= 5  # Adjust speed as needed

        pygame.display.flip()