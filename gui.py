import time
import pygame
from pygame_textinput import *
import blocks as nim_blocks
import textinput_nim
import nim
import play
import random
import sys
from Button import Button

#TODO: and show loading screen while A.I is training. different blocks at each difficulty

def run_playingscreen(training_games, SCREEN, clock, faces):
    # SET INITIAL PARAMETERS:
    FPS = 30
    click_sound = pygame.mixer.Sound("pics_and_music/click_sound.wav")
    SMALL_FONT = pygame.font.SysFont('bahnschrift', 15)
    current_game = nim.Nim()
    human_player = random.randint(0, 1)
    ai = nim.train(training_games, SCREEN=SCREEN, clock=clock)  # TODO: Show some sort of "Training AI Loading Screen"
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

    # Draw first frame of playing screen:
    piles = current_game.piles
    textsurface = nim.get_initial_textsurface()
    nim.draw_playing_screen(screen=SCREEN, piles=piles, textsurface=textsurface, faces=faces)

    pygame.display.update()
    time.sleep(1)

    while True:
        SCREEN.fill((255, 255, 255))
        pygame.draw.rect(SCREEN, (0, 0, 0), (593, 0, 1000, 1000))
        pygame.draw.rect(SCREEN, (255, 255, 255), (850, 55, 50, 35), 2)
        pygame.draw.rect(SCREEN, (255, 255, 255), (675, 18, 50, 35), 2)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if current_game.player != human_player:  # if it´s AI´s Turn: choose action, make move, print that move on GUI
            ai_line, ai_blocks = ai.choose_action(current_game.piles, epsilon=False)
            time.sleep(1)
            current_game.move((ai_line, ai_blocks))
            click_sound.play()
            moves_made = nim.print_last_move(current_game=current_game, human_player=human_player,
                        textsurface=textsurface, line=ai_line, blocks=ai_blocks, moves_made=moves_made)

        else:
            if line_confirmed is False:  # if a valid line as not been chosen yet, wait for valid input:
                line_input, dynamic_line_confirmed_text0, dynamic_line_confirmed_text1 = textinput_nim.get_line(
                    textinput_line=textinput_line, screen=SCREEN, events=events, piles=piles,
                    initial_text0=dynamic_line_confirmed_text0, initial_text1=dynamic_line_confirmed_text1)
                textsurface[0] = (dynamic_line_confirmed_text0, (600, 100))
                textsurface[1] = (dynamic_line_confirmed_text1, (600, 114))
                if line_input is not None:  # if there is a valid input for line
                    line_confirmed = True
                    del textinput_line
                    textinput_blocks = TextInput()

            if line_confirmed is True and blocks_confirmed is False:  # if a valid line has been chosen but not the Nr of Blocks, wait for valid input:
                blocks_input, dynamic_blocks_confirmed_text0, dynamic_blocks_confirmed_text1 = textinput_nim.get_blocks(
                    textinput_blocks=textinput_blocks, line=line_input, screen=SCREEN, events=events, piles=piles,
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
                click_sound.play()
                moves_made = nim.print_last_move(current_game=current_game, human_player=human_player,
                             textsurface=textsurface, line=line_input, blocks=blocks_input, moves_made=moves_made)

                # reset parameters:
                textsurface, dynamic_line_confirmed_text0, dynamic_line_confirmed_text1 = nim.reset_dynamic_texts(textsurface)
                line_confirmed, blocks_confirmed, line_input, blocks_input = nim.reset_lines_and_blocks()

                if current_game.winner is None:
                    textinput_line = TextInput()

            run_gameover_screen(winner=current_game.winner, human=human_player, clock=clock,
                                current_game=current_game, SCREEN=SCREEN)

            # draw blocks and blit text:
            for text in textsurface:
                SCREEN.blit(text[0], text[1])
            nim_blocks.drawAllBlocks(SCREEN, current_game.piles, faces=faces)

            pygame.display.update()
            clock.tick(FPS)


def run_gameover_screen(winner, human, clock, current_game, SCREEN):
    FPS = 30
    pygame.display.set_caption("Marty´s Coding Palace: Nim Challenge")
    if winner is not None:
        while True:
            SCREEN.fill((255, 255, 255))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    run_menu_screen(clock=clock, SCREEN=SCREEN)
                    break
            gameover_text0, gameover_text1 = nim.print_winner_message(human_player=human, winner=current_game.winner)
            textsurface = []
            textsurface.append((gameover_text0, (12, 250)))
            textsurface.append((gameover_text1, (5, 670)))

            for text in textsurface:
                SCREEN.blit(text[0], text[1])
            pygame.display.update()
            clock.tick(FPS)


def run_menu_screen(clock, SCREEN):
    FPS = 30
    FONT = pygame.font.SysFont('bahnschrift', 30)
    pygame.display.set_caption("Marty´s Coding Palace: Nim Challenge")
    header_font = pygame.font.SysFont('bahnschrift', 55)
    button100 = Button("Baby A.I.", "(Learns from 100 games against itself)",
                       300, 120, (640, 100), screen=SCREEN, training_iterations=100, clock=clock, elevation=6, faces=0)
    button1k = Button("Normal A.I.", "(Learns from 1k games against itself)",
                       300, 120, (640, 300), screen=SCREEN, training_iterations=1000, clock=clock, elevation=6, faces=1)
    button10k = Button("Marty´s Super A.I. 5000", "(Learns from 10k games against itself)",
                      300, 120, (640, 500), screen=SCREEN, training_iterations=10_000, clock=clock, elevation=6, faces=2)
    while True:
        SCREEN.fill((255, 255, 255))
        pygame.draw.rect(SCREEN, (0, 0, 0), (593, 0, 1000, 1000))

        button100.draw()
        button1k.draw()
        button10k.draw()

        nick_marty_img = pygame.image.load("pics_and_music/nick_n_marty_full_no_white_edges.png")

        textsurface = []
        text0 = FONT.render("Please choose your opponent:", True, (0, 0, 115))
        header = header_font.render("Nim Challenge", True, (0, 0, 115))

        textsurface.append((text0, (100, 300)))
        textsurface.append((header, (120, 230)))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        SCREEN.blit(nick_marty_img, pygame.rect.Rect(-45, 0, 592, 220))
        for text in textsurface:
            SCREEN.blit(text[0], text[1])
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.font.init()
    pygame.mixer.init()
    WIDTH, HEIGHT = 960, 720
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FPS = 30
    clock = pygame.time.Clock()

    click_sound = pygame.mixer.Sound("pics_and_music/click_sound.wav")

    FONT = pygame.font.SysFont('bahnschrift', 30)
    SMALL_FONT = pygame.font.SysFont('bahnschrift', 15)

    run_menu_screen(clock=clock, SCREEN=SCREEN)
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    main()
    pygame.quit()
