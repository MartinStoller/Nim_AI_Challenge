import time
import pygame
from pygame_textinput import *
import blocks as nim_blocks
import textinput_nim
import nim
import play
import random

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

current_game = nim.Nim()
human_player = random.randint(0, 1)


def main():
    # SET INITIAL PARAMETERS:
    moves_made = 0  # counter for how many moves were executed so far (important for print_last_move())
    dynamic_line_confirmed_text0 = SMALL_FONT.render("", True, (255, 255, 255))
    dynamic_line_confirmed_text1 = SMALL_FONT.render("", True, (255, 255, 255))
    dynamic_blocks_confirmed_text0 = SMALL_FONT.render("", True, (255, 255, 255))
    dynamic_blocks_confirmed_text1 = SMALL_FONT.render("", True, (255, 255, 255))
    line_confirmed = False  # if True, a valid value for the Line from which to remove Blocks was already chosen by player
    blocks_confirmed = False  # if True a valid value for the number of Blocks, which are to be removed was already entered
    pygame.display.set_caption("Marty´s Coding Palace: Nim Challenge")

    # Create TextInput-objects:
    textinput_line = TextInput()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Load initial Text displays:
    text0 = FONT.render('How many blocks do you want to', True, (0, 0, 0))
    text1 = FONT.render('remove and from which Line?', True, (0, 0, 0))
    text2 = FONT.render("Line:", True, (255, 255, 255))
    text3 = FONT.render("Amount of blocks:", True, (255, 255, 255))
    text4 = SMALL_FONT.render("L0", True, (0, 0, 0))
    text5 = SMALL_FONT.render("L1", True, (0, 0, 0))
    text6 = SMALL_FONT.render("L2", True, (0, 0, 0))
    text7 = SMALL_FONT.render("L3", True, (0, 0, 0))

    textsurface = []
    textsurface.append((dynamic_line_confirmed_text0, (600, 100)))  # dynamic texts need to be at index 0-3!!!
    textsurface.append((dynamic_line_confirmed_text1, (600, 114)))
    textsurface.append((dynamic_line_confirmed_text0, (600, 135)))
    textsurface.append((dynamic_line_confirmed_text1, (600, 149)))

    textsurface.append((text0, (80, 20)))
    textsurface.append((text1, (80, 55)))
    textsurface.append((text2, (600, 20)))
    textsurface.append((text3, (600, 55)))
    textsurface.append((text4, (243, 372)))
    textsurface.append((text5, (168, 452)))
    textsurface.append((text6, (85, 532)))
    textsurface.append((text7, (5, 612)))

    while True:
        piles = current_game.piles
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
                del textinput_line
                textinput_blocks = TextInput()

        if line_confirmed is True and blocks_confirmed is False:  # if a valid line has been chosen but not the Nr of Blocks, wait for valid input:
            blocks_input, dynamic_blocks_confirmed_text0, dynamic_blocks_confirmed_text1 = textinput_nim.get_blocks(
                textinput_blocks=textinput_blocks, line=line_input, screen=screen, events=events, piles=piles,
                initial_text0=dynamic_blocks_confirmed_text0, initial_text1=dynamic_blocks_confirmed_text1)
            textsurface[2] = (dynamic_blocks_confirmed_text0, (600, 135))
            textsurface[3] = (dynamic_blocks_confirmed_text1, (600, 149))
            if blocks_input is not None:
                blocks_confirmed = True

                del textinput_blocks

        if line_confirmed is True and blocks_confirmed is True:
            # if both inputs were entered, make move, print that move on GUI, reset parameters,
            # check if game is over and let AI make the next move otherwise
            # execute move and print it on GUI:
            current_game.move((line_input, blocks_input))
            moves_made = print_last_move(textsurface=textsurface, line=line_input,
                                         blocks=blocks_input, moves_made=moves_made)

            # reset parameters:
            reset_dynamic_texts(textsurface)
            line_confirmed = False
            blocks_confirmed = False
            textinput_line = TextInput()

        # if current_game.winner is not None:
        # TODO
        # TODO make_move(), add summary text of move to GUI and (if necessary) reset parameters such as dynamic texts and booleans,
        #  if game not over, AI makes move and summary gets projected on GUI. If game is over, print summarizing text on GUI and give the option to play again

        for text in textsurface:
            SCREEN.blit(text[0], text[1])

        pygame.display.update()
        clock.tick(FPS)


def reset_dynamic_texts(textsurface):
    empty_text = SMALL_FONT.render("", True, (255, 255, 255))
    textsurface[0] = (empty_text, (600, 100))
    textsurface[1] = (empty_text, (600, 114))
    textsurface[2] = (empty_text, (600, 100))
    textsurface[3] = (empty_text, (600, 114))


def print_last_move(textsurface, line, blocks, moves_made):
    player = "Human" if current_game.player == human_player else "AI"
    text = SMALL_FONT.render(f"{player} removed {blocks} Blocks from line {line}.", True, (255, 255, 255))
    textsurface.append((text, (600, (180+moves_made*17))))
    moves_made += 1
    return moves_made


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    main()
    pygame.quit()
