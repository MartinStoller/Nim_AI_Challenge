import time

import pygame
import nim_yt.businesslayer_nim.pygame_textinput as pg_textinput
import nim_yt.businesslayer_nim.blocks as nim_blocks
import nim_yt.businesslayer_nim.textinput_nim as textinput_nim

pygame.font.init()
WIDTH, HEIGHT = 960, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.SysFont('bahnschrift', 30)
SMALL_FONT = pygame.font.SysFont('bahnschrift', 15)


def main():
# SET INITIAL PARAMETERS:
    dynamic_line_confirmed_text0 = SMALL_FONT.render("", True, (255, 255, 255))
    dynamic_line_confirmed_text1 = SMALL_FONT.render("", True, (255, 255, 255))
    dynamic_blocks_confirmed_text0 = SMALL_FONT.render("", True, (255, 255, 255))
    dynamic_blocks_confirmed_text1 = SMALL_FONT.render("", True, (255, 255, 255))
    line_confirmed = False  # if True, a valid value for the Line from which to remove Blocks was already chosen by player
    blocks_confirmed = False  # if True a valid value for the number of Blocks, which are to be removed was already entered
    pygame.display.set_caption("Marty´s Coding Palace: Nim Challenge")

    # Create TextInput-objects:
    textinput_line = pg_textinput.TextInput()
    textinput_blocks = pg_textinput.TextInput()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    piles = [1, 3, 5, 7]  # TODO: onec GUI is connected to backend, this line wont be necessary

    # Load initial Text displays:
    textsurface = []
    textsurface.append((dynamic_line_confirmed_text0, (600, 100)))  # dynamic texts need to be at index 0-3!!!
    textsurface.append((dynamic_line_confirmed_text1, (600, 114)))
    textsurface.append((dynamic_line_confirmed_text0, (600, 135)))
    textsurface.append((dynamic_line_confirmed_text1, (600, 149)))
    text0 = FONT.render('How many blocks do you want to', True, (0, 0, 0))  # TODO: replace with a comment about game when it is over (Sth like: Congrats, you won! press Enter if you want to play another round)
    text1 = FONT.render('remove and from which Line?', True, (0, 0, 0))
    text2 = FONT.render("Line:", True, (255, 255, 255))
    text3 = FONT.render("Amount of blocks:", True, (255, 255, 255))
    textsurface.append((text0, (80, 20)))
    textsurface.append((text1, (80, 55)))
    textsurface.append((text2, (600, 20)))
    textsurface.append((text3, (600, 55)))

    while True:
        screen.fill(WHITE)
        pygame.draw.rect(SCREEN, BLACK, (593, 0, 1000, 1000))
        pygame.draw.rect(SCREEN, WHITE, (850, 55, 50, 35), 2)
        pygame.draw.rect(SCREEN, WHITE, (675, 18, 50, 35), 2)

        nim_blocks.drawAllBlocks(SCREEN, piles)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if line_confirmed is False:  # if a valid line as not been chosen yet, wait for valid input:
            line_input, dynamic_line_confirmed_text0, dynamic_line_confirmed_text1 = textinput_nim.get_line(
                textinput_line=textinput_line, screen=screen, events=events, piles=piles,
                initial_text0=dynamic_line_confirmed_text0, initial_text1=dynamic_line_confirmed_text1)
            textsurface[0] = (dynamic_line_confirmed_text0, (600, 100))
            textsurface[1] = (dynamic_line_confirmed_text1, (600, 114))
            if line_input is not None:
                line_confirmed = True

        if line_confirmed is True and blocks_confirmed is False:  # if a valid line has been chosen but not the Nr of Blocks, wait for valid input:
            blocks_input, dynamic_blocks_confirmed_text0, dynamic_blocks_confirmed_text1 = textinput_nim.get_blocks(
                textinput_blocks=textinput_blocks, line=line_input, screen=screen, events=events, piles=piles,
                initial_text0=dynamic_blocks_confirmed_text0, initial_text1=dynamic_blocks_confirmed_text1)
            textsurface[2] = (dynamic_blocks_confirmed_text0, (600, 135))
            textsurface[3] = (dynamic_blocks_confirmed_text1, (600, 149))

        if line_confirmed is True and blocks_confirmed is True:  # if both inputs were entered, make move
            dynamic_line_confirmed_text0 = SMALL_FONT.render("", True, (255, 255, 255))
            dynamic_line_confirmed_text1 = SMALL_FONT.render("", True, (255, 255, 255))
            textsurface[0] = (dynamic_line_confirmed_text0, (600, 100))
            textsurface[1] = (dynamic_line_confirmed_text1, (600, 114))
            # TODO make_move(), add summary text of move to GUI and (if necessary) reset parameters such as dynamic texts and booleans

        for text in textsurface:
            SCREEN.blit(text[0],
                        text[1])

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    main()
    pygame.quit()