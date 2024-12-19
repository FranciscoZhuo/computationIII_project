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
    texts = ["Well Done...", "Keep fighting....", "Are you still worthy?...", f"Chapter 2: Echoes of Devotion"] # Message from The Great Sage, Heaven's Equal
    text_surfaces = [creepster_font.render(text, True, white) for text in texts]


    # Load the image to display after the texts
    image = pygame.image.load("assets/Caeser Cypher.png").convert_alpha()
    image = pygame.transform.scale(image, (550, 150))  # Resize
    image.set_alpha(0)  # Start with the image fully transparent

    # Play the initial soundtrack
    pygame.mixer.music.load('assets/Heart of Courage.mp3')
    pygame.mixer.music.play()

    # Click ENTER to skip text
    skip_text = creepster_font20.render('Press "ENTER" to skip', True, white)

    skip_rect = skip_text.get_rect(
        center=(800 + 60 // 2, 670 + 20 // 2)
    )



    # Variables for fade effect
    current_item_index = 0
    alpha = 0
    fade_in = True
    fade_duration = 90  # Controls how fast the fade happens
    clock3 = pygame.time.Clock()
    loop_count = 0  # Counter for the number of cycles
    max_loops = 1  # Maximum number of full cycles

    # Variables for fade effect of skip button
    fade_in_complete = False
    fade_in_speed = 0.5
    e_alpha = 0

    running = True
    while running:
        screen.fill(deep_black)

        # Determine if we are displaying text or image
        if current_item_index < len(text_surfaces):
            # Display a text
            current_surface = text_surfaces[current_item_index]
        else:
            # Display the image
            current_surface = image

        # Set the alpha for the current surface and blit it
        current_surface.set_alpha(alpha)
        current_rect = current_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(current_surface, current_rect)


        # Fade logic
        if fade_in: # To fade in
            alpha += 255 // fade_duration # Increases visibilities according to duration
            if alpha >= 255:
                alpha = 255 # Becomes fully opaque
                fade_in = False # Fade in stops
        else: # To fade out
            alpha -= 255 // fade_duration # Decreases the visibilities to duration
            if alpha <= 0:
                alpha = 0 # Becomes fully transparent
                fade_in = True # Fade in starts for next item
                current_item_index += 1  # Move to the next item (text or image)

                # Check if we've cycled through all texts and the image
                if current_item_index >= len(text_surfaces) + 1:
                    loop_count += 1
                    if loop_count >= max_loops:
                        running = False  # Exit the loop after 1 cycles
                    current_item_index = 0  # Reset to the first text for the next loop

        #Fade logic for skip
        if not fade_in_complete: # if not False == True
            e_alpha += fade_in_speed  # Gradually increase alpha
            if e_alpha >= 100:  # Stop once opaque enough
                e_alpha = 100
                fade_in_complete = True # Fade in stops

            # Set alpha
            skip_text.set_alpha(e_alpha)

        # Set the text on the screen
        screen.blit(skip_text, skip_rect)


        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                running = False


        # Skip the initial "Cut Scene" by pressing the Enter button
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pygame.mixer.music.stop()
            running = False


        pygame.display.flip()
        clock3.tick(fps)  # Control the frame rate


def cutscene3():
    # Screen setup
    screen = pygame.display.set_mode(resolution)

    # Font for the text that fades in
    roboto_font = pygame.font.SysFont("Roboto", 40)

    # Font for the skip button
    roboto_font20 = pygame.font.SysFont("Roboto", 20)

    # Text setup
    texts = ["You are deemed worthy...", "I shall lend you my power....", "You are the last of us...",
             f"Chapter 3: The last of us"]  # Message from The Great Sage, Heaven's Equal
    text_surfaces = [roboto_font.render(text, True, white) for text in texts]

    # Load the image to display after the texts
    image = pygame.image.load("assets/Caeser Cypher.png").convert_alpha()
    image = pygame.transform.scale(image, (550, 150))  # Resize
    image.set_alpha(0)  # Start with the image fully transparent

    # Play the initial soundtrack
    pygame.mixer.music.load('assets/Heart of Courage.mp3')
    pygame.mixer.music.play()

    # Click ENTER to skip text
    skip_text = roboto_font20.render('Press "ENTER" to skip', True, white)

    skip_rect = skip_text.get_rect(
        center=(800 + 60 // 2, 670 + 20 // 2)
    )

    # Variables for fade effect
    current_item_index = 0
    alpha = 0
    fade_in = True
    fade_duration = 90  # Controls how fast the fade happens
    clock3 = pygame.time.Clock()
    loop_count = 0  # Counter for the number of cycles
    max_loops = 1  # Maximum number of full cycles

    # Variables for fade effect of skip button
    fade_in_complete = False
    fade_in_speed = 0.5
    e_alpha = 0

    running = True
    while running:
        screen.fill(deep_black)

        # Determine if we are displaying text or image
        if current_item_index < len(text_surfaces):
            # Display a text
            current_surface = text_surfaces[current_item_index]
        else:
            # Display the image
            current_surface = image

        # Set the alpha for the current surface and blit it
        current_surface.set_alpha(alpha)
        current_rect = current_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(current_surface, current_rect)

        # Fade logic
        if fade_in:  # To fade in
            alpha += 255 // fade_duration  # Increases visibilities according to duration
            if alpha >= 255:
                alpha = 255  # Becomes fully opaque
                fade_in = False  # Fade in stops
        else:  # To fade out
            alpha -= 255 // fade_duration  # Decreases the visibilities to duration
            if alpha <= 0:
                alpha = 0  # Becomes fully transparent
                fade_in = True  # Fade in starts for next item
                current_item_index += 1  # Move to the next item (text or image)

                # Check if we've cycled through all texts and the image
                if current_item_index >= len(text_surfaces) + 1:
                    loop_count += 1
                    if loop_count >= max_loops:
                        running = False  # Exit the loop after 1 cycles
                    current_item_index = 0  # Reset to the first text for the next loop

        # Fade logic for skip
        if not fade_in_complete:  # if not False == True
            e_alpha += fade_in_speed  # Gradually increase alpha
            if e_alpha >= 100:  # Stop once opaque enough
                e_alpha = 100
                fade_in_complete = True  # Fade in stops

            # Set alpha
            skip_text.set_alpha(e_alpha)

        # Set the text on the screen
        screen.blit(skip_text, skip_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                running = False

        # Skip the initial "Cut Scene" by pressing the Enter button
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pygame.mixer.music.stop()
            running = False

        pygame.display.flip()
        clock3.tick(fps)  # Control the frame rate

