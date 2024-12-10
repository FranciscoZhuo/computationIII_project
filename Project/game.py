from config import *
import math
import pygame
from enemy import Enemy
from player import Player
from shed import shed
from interface import *
from health import HealthBar

def game_loop():
    player = Player()
    current_state = "main"

    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shed":
            current_state = shed(player)

def game_over_screen(screen):
    """
    Display a game over screen.
    """
    bloodcrowfont = pygame.font.Font("assets/bloodcrow.ttf", 35)
    text = bloodcrowfont.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))

    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
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

        pygame.display.flip()

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
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Endless Wilderness Explorer")

    # Player Setup
    # player = Player() NO NEEDED ANYMORE
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Initialize the bullet group
    bullets = pygame.sprite.Group()

    # Initialize the enemy group
    enemies = pygame.sprite.Group()
    enemy_spawn_timer = 0

    #Initialize the health class
    health_bar = HealthBar()


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

        # Shooting
        player.shoot(bullets)

        # Spawn timer
        if enemy_spawn_timer > 0:
            enemy_spawn_timer -= 1

        # Spawning the enemies
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            enemy_spawn_timer = 2 * fps # Every two seconds

        # Checking for collisions between enemies and bullets
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= 5  # Decrease health by 5
                bullet.kill()  # Destroy the bullet
                if enemy.health <= 0:
                    enemy.kill()  # Destroy the enemy

        # Check for collisions between player and enemies
        if pygame.sprite.spritecollide(player, enemies, False):
            if player.take_damage():  # Check cooldown
                health_bar.decrease_health()
                player.register_collision()
                if health_bar.is_empty():
                    print("Game Over!")
                    running = False
                    game_over_screen(screen)

        # Update positions
        player_group.update()
        bullets.update()
        enemies.update(player)

        # Checking if the user goes into the shed area
        if player.rect.right >= width:
            # Change the game state to shed
            return "shed"

        # Drawing the object
        player_group.draw(screen)
        enemies.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # Draw the player's health bar
        health_bar.draw(screen, player.rect)  # Pass player.rect to update method




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