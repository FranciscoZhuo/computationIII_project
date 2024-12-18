import pygame
from config import *
from utils import *
from utils import under_construction


def shop(player):
    # Setup of the background and screen
    background = pygame.image.load("img/farm.png")
    background = pygame.transform.scale(background, resolution)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    # Set the player's position to the left of the screen
    player.rect.left = 0
    player_group = pygame.sprite.Group()
    player_group.add(player)

    special_area = pygame.Rect(530,30,140,140)

    running = True
    while running:
        clock.tick(fps)
        screen.blit(background, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Update their position
        player.update(dt)

        # Detect if the user walks in the speacial area (House)
        if special_area.colliderect(player.rect):
            under_construction()
            # Change player postion to avoind infinite loop
            player.rect.top = 200
            player.rect.left =560

        # Allow a player to return to the previous screen
        if player.rect.left <= 0:
            # Position the player to the right of the screen
            player.rect.left = width - player.rect.width
            return "main"

        # Draw player
        player_group.draw(screen)

        pygame.display.flip()

#Cada uso da habilidade consome uma unidade que o jogador comprou.
#Se o jogador tiver 3 escudos, ele pode usar o escudo 3 vezes antes de precisar comprar mais.
# o uso é limitado ao número de unidades no inventário.