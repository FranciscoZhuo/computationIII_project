import pygame
from utils import * # no need to import pygame because the import is in utils
from game import *
from cutscene import *

def interface():

    # initiating pygame
    pygame.init()
    # creating the screen at the set resolution
    screen = pygame.display.set_mode(resolution)
    #roboto_font = pygame.font.SysFont("Roboto", 40)
    creepster_font = pygame.font.Font("assets/Creepster-Regular.ttf", 50)

    # Text
    start_text = creepster_font.render("START GAME", True, white)
    rules_text = creepster_font.render("RULES", True, white)
    credits_text = creepster_font.render("CREDITS", True, white)
    quit_text = creepster_font.render("QUIT", True, white)

    # Background configs
    gif_frame_bg = 0
    clock_bg = pygame.time.Clock()

    # setting the window title
    pygame.display.set_caption("Surge of the Silent")
    # setting the icon
    pygame.display.set_icon(pygame.image.load("assets/icon.png"))

    # Play the soundtrack
    pygame.mixer.music.load('assets/Rain and Thunder Sounds.mp3')
    pygame.mixer.music.play(-1)

    # Sound Bar Settings
    volume_bar_visible = False  # Flag to toggle the sound bar
    bar_x, bar_y = 975, 495 # Bottom-right corner
    bar_width, bar_height = 20, 200  # Vertical bar dimensions
    knob_height = 10  # Knob height
    volume = 0.5  # Default volume

    def draw_sound_bar():
        # Draw the vertical sound bar
        pygame.draw.rect(screen, grey, [bar_x, bar_y, bar_width, bar_height], border_radius= 20)
        knob_y = bar_y + int((1 - volume) * bar_height) - knob_height // 2
        pygame.draw.rect(screen, purple, (bar_x, knob_y, bar_width, knob_height))

    # Mute Button Settings
    is_muted = False


    #Game Loop
    while True:
        mouse = pygame.mouse.get_pos() #guarda as coordenadas atuais do cursor do rato

        # Show sound bar if the flag is set
        if volume_bar_visible:
            draw_sound_bar()


        # Event Handling
        for ev in pygame.event.get():
            # Quitting the game with the close button on the window (x)
            if ev.type == pygame.QUIT:
                pygame.quit()

            # to avoid redundancy:
            if ev.type == pygame.MOUSEBUTTONDOWN:  # verifies if there´s a click or movement in the areas of each button
                if 362 < mouse[0] < 662:  # it checks if the mouse click is within the horizontal range of the buttons
                    # it checks if the click matches the vertical range for the buttons:
                    if 325 < mouse[1] < 385:  # START GAME
                        cutscene1()
                        wilderness_explorer()
                    elif 400 < mouse[1] < 460:  # RULES
                        rules_()
                    elif 475 < mouse[1] < 535:  # CREDITS
                        credits_()
                    elif 550 < mouse[1] < 610:  # QUIT
                        pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                # Check if the bottom-right button is clicked
                if 955 < mouse[0] < 1015 and 704 < mouse[1] < 764:
                    volume_bar_visible = not volume_bar_visible


                # Adjust volume if sound bar is visible
                if volume_bar_visible and bar_x < mouse[0] < bar_x + bar_width:
                    if bar_y < mouse[1] < bar_y + bar_height:
                        volume = 1 - (mouse[1] - bar_y) / bar_height  # Calculate volume
                        pygame.mixer.music.set_volume(volume)

            if ev.type == pygame.MOUSEBUTTONDOWN:
                # Dragging functionality for the knob
                if volume_bar_visible:
                    if bar_x < mouse[0] < bar_x + bar_width and bar_y < mouse[1] < bar_y + bar_height:
                        volume = 1 - (mouse[1] - bar_y) / bar_height
                        pygame.mixer.music.set_volume(volume)

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 880 < mouse[0] < 940 and 704 < mouse[1] < 764:
                    is_muted = not is_muted  # Toggle mute state
                    if is_muted:
                        pygame.mixer.music.set_volume(0)  # Mute sound
                    else:
                        pygame.mixer.music.set_volume(volume)  # Unmute sound

        # Background
        clock_bg.tick(fps)
        if gif_frame_bg != 7:
            screen.blit(pygame.image.load(f'assets/MainBG/frame_{gif_frame_bg}.png'), (0, 0))
            gif_frame_bg += 1
        else:
            screen.blit(pygame.image.load(f'assets/MainBG/frame_{gif_frame_bg}.png'), (0, 0))
            gif_frame_bg = 0

        # Draw Sound volume button and set it on
        sound_plus = pygame.image.load("assets/Sound_plus.png")
        sound_minus = pygame.image.load("assets/Sound_minus.png")

        if volume_bar_visible:
            screen.blit(sound_minus, (955, 704))
        else:
            screen.blit(sound_plus, (955, 704))

        # Draw Mute and not mute Button and set it on
        sound_mute = pygame.image.load("assets/Sound_mute.png")
        sound_on = pygame.image.load("assets/Sound_on.png")


        if is_muted:
            screen.blit(sound_mute, (880, 704))
        else:
            screen.blit(sound_on, (880, 704))


        # Show sound bar if the flag is set
        if volume_bar_visible:
            draw_sound_bar()


        # Buttons
        wilderness_color = light_blue_green if 325 < mouse[1] < 385 and 362 < mouse[0] < 662 else purple
        rules_color = light_blue_green if 400 < mouse[1] < 460 and 362 < mouse[0] < 662 else purple
        credits_color = light_blue_green if 475 < mouse[1] < 537 and 362 < mouse[0] < 662 else purple
        quit_color = light_blue_green if 550 < mouse[1] < 610 and 362 < mouse[0] < 662 else purple

        #Centralizing the buttons
        width_button = 300
        height_button = 60
        x_center = resolution[0] // 2 #middle of the width (1024)
        x_button = x_center - width_button // 2


        # Wilderness Explorer button
        pygame.draw.rect(screen, wilderness_color, [x_button, 325, width_button, height_button], border_radius=15)
        pygame.draw.rect(screen, rules_color, [x_button, 400, width_button, height_button], border_radius=15)
        pygame.draw.rect(screen, credits_color, [x_button, 475, width_button, height_button], border_radius=15)
        pygame.draw.rect(screen, quit_color, [x_button, 550, width_button, height_button], border_radius=15)

        # Text
        start_rect = start_text.get_rect(
            center=(x_center, 325 + height_button // 2)
        )
        # Writing
        screen.blit(start_text, start_rect)

        # Rules
        #pygame.draw.rect(screen, grey, [210, 320, 300, 60])
        rules_rect = rules_text.get_rect(
            center=(x_center,400 + height_button // 2)
        )
        screen.blit(rules_text, rules_rect)

        # Credit
        #pygame.draw.rect(screen, grey, [210, 460, 300, 60])
        credit_rect = credits_text.get_rect(
            center=(x_center, 475 + height_button // 2)
        )
        screen.blit(credits_text, credit_rect)

        # Quit
        #pygame.draw.rect(screen, light_blue_green, [860, 690, 150, 60], border_radius=20)
        quit_rect = quit_text.get_rect(
            center=(x_center, 550 + height_button // 2)
        )
        screen.blit(quit_text, quit_rect)

        # Display the tittle
        title = pygame.image.load("assets/Surge Of The Silent.png")
        title = pygame.transform.scale(title, (450, 350))
        screen.blit(title, (287, -70))


        pygame.display.update()


# Under construction screen

def credits_():
    ### BASE SETTINGS ###
    screen = pygame.display.set_mode(resolution)

    comicsansfont = pygame.font.SysFont("Comic Sans MS", 25)
    corbelfont = pygame.font.SysFont("Cobel", 50)

    augusto = comicsansfont.render("Augusto Santos, ajrsantos@novaims.unl.pt", True, white)
    diogo = comicsansfont.render("Diogo Rasteiro, drasteiro@novaims.unl.pt", True, white)
    liah = comicsansfont.render("Liah Rosenfeld, lrosenfel@novaims.unl.pt", True, white)

    while True:
        # quitting the mouse position
        mouse = pygame.mouse.get_pos()

        # Getting the events from the user to detect quitting or returning to interface
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    interface()

        #### DISPLAYING THE CREDITS ####
        screen.fill(deep_black)

        # Display my text
        screen.blit(augusto, (0,0))
        screen.blit(diogo, (0,25))
        screen.blit(liah, (0,50))

        # Drawing the back button [x, y, width, height]
        pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
        back_text = corbelfont.render("Back", True, white)
        back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(back_text, back_rect)

        # As always
        pygame.display.update()

def rules_():
    print("Displaying rules...")


def wilderness_explorer():
    game_loop()

