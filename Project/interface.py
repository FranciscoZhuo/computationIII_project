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

    # Text
    wilderness_text = corbel_font.render("Wilderness Explorer", True, white)

    start_text = corbel_font.render("Game Start", True, white)
    rules_text = corbel_font.render("Rules", True, white)
    option_text = corbel_font.render("Option", True, white)
    credits_text = corbel_font.render("Credits", True, white)
    quit_text = corbel_font.render("Quit", True, white)

    title_text = comicsans_font.render("Computation III - Projecto", True, glowing_light_red)

    gif_frame = 0
    clock2 = pygame.time.Clock()

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
                if 210 <= mouse[0] <= 510 and 250 <= mouse[1] <= 310:
                    cutscene1()
                    wilderness_explorer()

            # Detection clicks on Credits
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 210 <= mouse[0] <= 510 and 460 <= mouse[1] <= 520:
                    credits_()

        # Background
        clock2.tick(20)
        if gif_frame != 167:
            screen.blit(pygame.image.load(f'assets/MainBack/frame_{gif_frame}.png'), (0, 0))
            gif_frame += 1
        else:
            screen.blit(pygame.image.load(f'assets/MainBack/frame_{gif_frame}.png'), (0, 0))
            gif_frame = 0

        # Bunch of things

        # Get the mouse information
        mouse = pygame.mouse.get_pos()

        # Buttons

        # Wilderness Explorer button

        pygame.draw.rect(screen, red, [210, 250, 300, 60])

        # Text
        start_rect = start_text.get_rect(
            center=(210 + 300 // 2, 250 + 60 // 2)
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
        pygame.draw.rect(screen, grey, [210, 530, 300, 60])
        quit_rect = quit_text.get_rect(
            center=(210 + 300 // 2, 530 + 60 // 2)
        )
        screen.blit(quit_text, quit_rect)

        # Display the tittle
        screen.blit(wilderness_text, (75, 55))

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
