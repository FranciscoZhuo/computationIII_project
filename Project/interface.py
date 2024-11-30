import pygame

from utils import * # no need to import pygame because the import is in utils
from game import *
from cutscene import cutscene1

def interface():

    # initiating pygame
    pygame.init()
    # creating the screen at the set resolution
    screen = pygame.display.set_mode(resolution)

    corbel_font = pygame.font.SysFont("Corbel", 50) # Mudar na entrega
    comicsans_font = pygame.font.SysFont("Comic Sans MS",50)
    roboto_font = pygame.font.SysFont("Roboto", 50)

    # Text
    start_text = corbel_font.render("Game Start", True, white)
    rules_text = corbel_font.render("Rules", True, white)
    option_text = corbel_font.render("Option", True, white)
    credits_text = corbel_font.render("Credits", True, white)
    quit_text = roboto_font.render("QUIT", True, deep_black)



    gif_frame_bg = 0
    clock_bg = pygame.time.Clock()

    # setting the window title
    pygame.display.set_caption("Surge of the Silent")
    # setting the icon
    pygame.display.set_icon(pygame.image.load("assets/icon.png"))


    #Game Loop
    while True:
        # Event Handling
        for ev in pygame.event.get():
            # Quitting the game with the close button on the window (x)
            if ev.type == pygame.QUIT:
                pygame.quit()

            # Detect if the user clicked on the quit button (450, 600 to 590, 660)
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # mouse <-- (500, 620)
                if 210 <= mouse[0] <= 510 and 530 <= mouse[1] <= 590:
                    # If the user clicks the quit button
                    pygame.quit()

            # Detection clicks on Options (90, 600 to 230, 660)
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 210 <= mouse[0] <= 510 and 390 <= mouse[1] <= 450:
                    # Activate the function that makes the option screen
                    under_construction()

            # Detection clicks on Rules
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 210 <= mouse[0] <= 510 and 320 <= mouse[1] <= 380:
                    under_construction()

            # Detection clicks on Wilderness thingy
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 362 <= mouse[0] <= 662 and 400 <= mouse[1] <= 460:
                    cutscene1()
                    wilderness_explorer()

            # Detection clicks on Credits
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 210 <= mouse[0] <= 510 and 460 <= mouse[1] <= 520:
                    credits_()

        # Background
        clock_bg.tick(fps)
        if gif_frame_bg != 7:
            screen.blit(pygame.image.load(f'assets/MainBG/frame_{gif_frame_bg}.png'), (0, 0))
            gif_frame_bg += 1
        else:
            screen.blit(pygame.image.load(f'assets/MainBG/frame_{gif_frame_bg}.png'), (0, 0))
            gif_frame_bg = 0

        # Bunch of things

        # Get the mouse information
        mouse = pygame.mouse.get_pos()

        # Buttons

        # Wilderness Explorer button

        pygame.draw.rect(screen, light_blue_green, [362, 400, 300, 60], border_radius=20)

        # Text
        start_rect = start_text.get_rect(
            center=(362 + 300 // 2, 400 + 60 // 2)
        )
        # Writing
        screen.blit(start_text, start_rect)

        # Rules
        pygame.draw.rect(screen, grey, [210, 320, 300, 60])
        rules_rect = rules_text.get_rect(
            center=(210 + 300 // 2, 320 + 60 // 2)
        )
        screen.blit(rules_text, rules_rect)

        # Option
        pygame.draw.rect(screen, grey, [210, 390, 300, 60])
        options_rect = option_text.get_rect(
            center=(210 + 300 // 2, 390 + 60 // 2)
        )
        screen.blit(option_text, options_rect)

        # Credit
        pygame.draw.rect(screen, grey, [210, 460, 300, 60])
        credit_rect = credits_text.get_rect(
            center=(210 + 300 // 2, 460 + 60 // 2)
        )
        screen.blit(credits_text, credit_rect)

        # Quit
        pygame.draw.rect(screen, purple, [860, 690, 150, 60], border_radius=20)
        quit_rect = quit_text.get_rect(
            center=(860 + 150 // 2, 690 + 60 // 2)
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
