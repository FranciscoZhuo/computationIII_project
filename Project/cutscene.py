import pygame
from config import *

def cutscene1():
    # Screen setup
    screen = pygame.display.set_mode(resolution)
    # Font for the text that fades in
    roboto_font = pygame.font.SysFont("Roboto", 40)
    creepster_font = pygame.font.Font("assets/Creepster-Regular.ttf", 50)

    # Font for the skip button
    roboto_font20 = pygame.font.SysFont("Roboto", 20)
    creepster_font20 = pygame.font.Font("assets/Creepster-Regular.ttf", 20)

    # Text setup
    texts = ["Wake up...", "The world needs you again....", "Remember the monkeys...", "Chapter 1: Echoes of Strength", "Kv fvb zapss yltlily tl?"]
    text_surfaces = [creepster_font.render(text, True, white) for text in texts]

    # Play the initial soundtrack
    pygame.mixer.music.load('assets/Heart of Courage.mp3')
    pygame.mixer.music.play()

    # Click ENTER to skip text
    skip_text = creepster_font20.render('Press "ENTER" to skip', True, white)
    skip_rect = skip_text.get_rect(
        center=(screen.get_width() - 100, screen.get_height() - 50)
    )

    # Variables for fade effect
    current_item_index = 0
    alpha = 0
    fade_in = True
    fade_duration = 200  # Controls how fast the fade happens
    clock = pygame.time.Clock()

    # Variables for fade effect of skip button
    fade_in_complete = False
    fade_in_speed = 0.5
    e_alpha = 0

    running = True
    while running:
        screen.fill(deep_black)

        # Display the current text
        if current_item_index < len(text_surfaces):
            current_surface = text_surfaces[current_item_index]
            current_surface.set_alpha(alpha)
            current_rect = current_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(current_surface, current_rect)
        else:
            running = False  # Exit after displaying all texts

        # Fade logic
        if fade_in:
            alpha += 255 // fade_duration
            if alpha >= 255:
                alpha = 255
                fade_in = False
        else:
            alpha -= 255 // fade_duration
            if alpha <= 0:
                alpha = 0
                fade_in = True
                current_item_index += 1

        # Fade logic for skip button
        if not fade_in_complete:
            e_alpha += fade_in_speed
            if e_alpha >= 100:
                e_alpha = 100
                fade_in_complete = True
            skip_text.set_alpha(e_alpha)

        screen.blit(skip_text, skip_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                running = False

        # Skip the cutscene by pressing ENTER
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pygame.mixer.music.stop()
            running = False

        pygame.display.flip()
        clock.tick(fps)  # Control the frame rate



def cutscene2():
    # Screen setup
    screen = pygame.display.set_mode(resolution)
    # Font for the text that fades in
    roboto_font = pygame.font.SysFont("Roboto", 40)
    creepster_font = pygame.font.Font("assets/Creepster-Regular.ttf", 50)

    # Font for the skip button
    roboto_font20 = pygame.font.SysFont("Roboto", 20)
    creepster_font20 = pygame.font.Font("assets/Creepster-Regular.ttf", 20)

    # Text setup
    texts = ["Well Done...", "Keep fighting....", "Only you can do it...", "Chapter 2: Echoes of Devotion",
             "Hyl fvb zapss dvyao pa?"]
    text_surfaces = [creepster_font.render(text, True, white) for text in texts]

    # Play the initial soundtrack
    pygame.mixer.music.load('assets/Heart of Courage.mp3')
    pygame.mixer.music.play()

    # Click ENTER to skip text
    skip_text = creepster_font20.render('Press "ENTER" to skip', True, white)
    skip_rect = skip_text.get_rect(
        center=(screen.get_width() - 100, screen.get_height() - 50)
    )

    # Variables for fade effect
    current_item_index = 0
    alpha = 0
    fade_in = True
    fade_duration = 200  # Controls how fast the fade happens
    clock = pygame.time.Clock()

    # Variables for fade effect of skip button
    fade_in_complete = False
    fade_in_speed = 0.5
    e_alpha = 0

    while True:  # Continue until explicitly returned
        screen.fill(deep_black)

        # Display the current text
        if current_item_index < len(text_surfaces):
            current_surface = text_surfaces[current_item_index]
            current_surface.set_alpha(alpha)
            current_rect = current_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(current_surface, current_rect)
        else:
            pygame.mixer.music.stop()
            return "intro2"  # Return explicitly when all texts are displayed

        # Fade logic
        if fade_in:
            alpha += 255 // fade_duration
            if alpha >= 255:
                alpha = 255
                fade_in = False
        else:
            alpha -= 255 // fade_duration
            if alpha <= 0:
                alpha = 0
                fade_in = True
                current_item_index += 1

        # Fade logic for skip button
        if not fade_in_complete:
            e_alpha += fade_in_speed
            if e_alpha >= 100:
                e_alpha = 100
                fade_in_complete = True
            skip_text.set_alpha(e_alpha)

        screen.blit(skip_text, skip_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                return  # Ensure quit exits the loop completely

        # Skip the cutscene by pressing ENTER
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pygame.mixer.music.stop()
            return "intro2"

        pygame.display.flip()
        clock.tick(fps)  # Control the frame rate


def cutscene3():
    # Screen setup
    screen = pygame.display.set_mode(resolution)
    # Font for the text that fades in
    roboto_font = pygame.font.SysFont("Roboto", 40)
    creepster_font = pygame.font.Font("assets/Creepster-Regular.ttf", 50)

    # Font for the skip button
    roboto_font20 = pygame.font.SysFont("Roboto", 20)
    creepster_font20 = pygame.font.Font("assets/Creepster-Regular.ttf", 20)

    # Text setup
    texts = ["You are deemed worthy...", "You shall became my sucessor...", "Chapter 3: The last of us",
             "Fvb hyl uvd aol uld Nylha Zhnl, Olhclu'z Lxbhs!"]
    text_surfaces = [creepster_font.render(text, True, white) for text in texts]

    # Play the initial soundtrack
    pygame.mixer.music.load('assets/Heart of Courage.mp3')
    pygame.mixer.music.play()

    # Click ENTER to skip text
    skip_text = creepster_font20.render('Press "ENTER" to skip', True, white)
    skip_rect = skip_text.get_rect(
        center=(screen.get_width() - 100, screen.get_height() - 50)
    )

    # Variables for fade effect
    current_item_index = 0
    alpha = 0
    fade_in = True
    fade_duration = 200  # Controls how fast the fade happens
    clock = pygame.time.Clock()

    # Variables for fade effect of skip button
    fade_in_complete = False
    fade_in_speed = 0.5
    e_alpha = 0

    while True:  # Continue until explicitly returned
        screen.fill(deep_black)

        # Display the current text
        if current_item_index < len(text_surfaces):
            current_surface = text_surfaces[current_item_index]
            current_surface.set_alpha(alpha)
            current_rect = current_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(current_surface, current_rect)
        else:
            pygame.mixer.music.stop()
            return "intro3"  # Return explicitly when all texts are displayed

        # Fade logic
        if fade_in:
            alpha += 255 // fade_duration
            if alpha >= 255:
                alpha = 255
                fade_in = False
        else:
            alpha -= 255 // fade_duration
            if alpha <= 0:
                alpha = 0
                fade_in = True
                current_item_index += 1

        # Fade logic for skip button
        if not fade_in_complete:
            e_alpha += fade_in_speed
            if e_alpha >= 100:
                e_alpha = 100
                fade_in_complete = True
            skip_text.set_alpha(e_alpha)

        screen.blit(skip_text, skip_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                return  # Ensure quit exits the loop completely

        # Skip the cutscene by pressing ENTER
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pygame.mixer.music.stop()
            return "intro3"

        pygame.display.flip()
        clock.tick(fps)  # Control the frame rate

