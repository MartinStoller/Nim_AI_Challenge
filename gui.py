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

FONT = pygame.font.SysFont('bahnschrift', 30)
SMALL_FONT = pygame.font.SysFont('bahnschrift', 15)

current_game = nim.Nim()
human_player = random.randint(0, 1)
ai = nim.train(1000)  # TODO: Show some sort of "Training AI Loading Screen"


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

    # Draw first frame of playing screen:
    piles = current_game.piles
    textsurface = nim.get_initial_textsurface()
    nim.draw_playing_screen(screen=SCREEN, piles=piles, textsurface=textsurface)

    pygame.display.update()
    time.sleep(1)

    while True:
        screen.fill(WHITE)
        pygame.draw.rect(SCREEN, BLACK, (593, 0, 1000, 1000))
        pygame.draw.rect(SCREEN, WHITE, (850, 55, 50, 35), 2)
        pygame.draw.rect(SCREEN, WHITE, (675, 18, 50, 35), 2)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if current_game.player != human_player:  # if it´s AI´s Turn: choose action, make move, print that move on GUI
            ai_line, ai_blocks = ai.choose_action(current_game.piles, epsilon=False)
            time.sleep(1.5)
            current_game.move((ai_line, ai_blocks))
            moves_made = nim.print_last_move(current_game=current_game, human_player=human_player,
                        textsurface=textsurface, line=ai_line, blocks=ai_blocks, moves_made=moves_made)

        else:
            if line_confirmed is False:  # if a valid line as not been chosen yet, wait for valid input:
                line_input, dynamic_line_confirmed_text0, dynamic_line_confirmed_text1 = textinput_nim.get_line(
                    textinput_line=textinput_line, screen=screen, events=events, piles=piles,
                    initial_text0=dynamic_line_confirmed_text0, initial_text1=dynamic_line_confirmed_text1)
                textsurface[0] = (dynamic_line_confirmed_text0, (600, 100))
                textsurface[1] = (dynamic_line_confirmed_text1, (600, 114))
                if line_input is not None:  # if there is a valid input for line
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
                moves_made = nim.print_last_move(current_game=current_game, human_player=human_player,
                             textsurface=textsurface, line=line_input, blocks=blocks_input, moves_made=moves_made)

                # reset parameters:
                textsurface, dynamic_line_confirmed_text0, dynamic_line_confirmed_text1 = nim.reset_dynamic_texts(textsurface)
                line_confirmed, blocks_confirmed, line_input, blocks_input = nim.reset_lines_and_blocks()

                if current_game.winner is None:
                    textinput_line = TextInput()
                elif current_game.winner is not None:
                    gameover_text0, gameover_text1 = nim.print_winner_message(human_player=human_player, winner=current_game.winner)
                    textsurface = []
                    textsurface.append((gameover_text0(200, 200)))
                    textsurface.append((gameover_text1(5, 650)))
                    # TODO: enable press any key to get back to menu

            # draw blocks and blit text:
            for text in textsurface:
                SCREEN.blit(text[0], text[1])
            nim_blocks.drawAllBlocks(SCREEN, current_game.piles)

            pygame.display.update()
            clock.tick(FPS)

# TODO: ADD SOUnD WHEN A MOVE IS MADE AND BACKGROUND MUSIC AND A GAMEOVER SCREEN AND MENU SCREEN  WHICH WAITS FOR ANY KYEPRESS

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    main()
    pygame.quit()
