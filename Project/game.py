from config import *
import math
import pygame
from enemy import *
from player import Player
from powerups import PowerUpController
from monetarysystem import MonetarySystem
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
    pygame.display.set_caption("Surge of the Silence")

    # Player Setup
    # player = Player() NO NEEDED ANYMORE
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Initialize the bullet group
    bullets = pygame.sprite.Group()

    # Initiaize the enemy group
    enemies = pygame.sprite.Group()
    enemy_spawn_timer = 0


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