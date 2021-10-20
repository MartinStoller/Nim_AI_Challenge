import pygame
import pygame_textinput as pg_textinput
import blocks as nim_blocks
import gui as nim_gui


def get_line(textinput_line, screen, events, piles, initial_text0, initial_text1):
    """
    :param textinput_line: TextInput Object
    :param screen: gui-screen
    :param events: detected events by pygame (keystrokes)
    :param piles: list of available blocks (at the beginning of game [1, 3, 5, 7])
    :return: int: line, from which blocks are supposed to be removed. None if invalid input

    checks validity of the input (from which line to remove blocks). If not valid returns None + error messages.
    If valid it returns the input as int + confirming messages
    """
    screen.blit(textinput_line.get_surface(), (690, 25))
    if textinput_line.update(events):
        line_input = textinput_line.get_text()
        if len(str(line_input)) > 0:
            if check_validity_line(line_input, piles) is False:
                text0, text1 = print_message_line(validity=False, line_input=999)
                return None, text0, text1
            else:
                text0, text1 = print_message_line(validity=True, line_input=line_input)
                return int(line_input), text0, text1
    return None, initial_text0, initial_text1  # if no even was detected, keep the text the way it was


def check_validity_line(textinput, piles):
    """
    :param textinput: detected textinput
    :param piles: list of available blocks (at the beginning of game [1, 3, 5, 7])
    :return: True if input is valid, False otherwise
    """
    # Check if input can be converted to int:
    try:
        textinput = int(textinput)
    except:
        return False
    # get valid inputs and check if actual input is part of that.
    valid_inputs = []
    for e in enumerate(piles):
        if e[1] != 0:
            valid_inputs.append(e[0])

    if textinput not in valid_inputs:
        return False
    return True


def print_message_line(validity, line_input):
    """ returns text objects which gets added to the text surface in the main() in GUI"""
    FONT = pygame.font.SysFont('bahnschrift', 15)
    if validity is False:
        text0 = FONT.render("Invalid Input! Please choose a line (0-3), ", True, (255, 255, 255))
        text1 = FONT.render("which contains at least one Block.", True, (255, 255, 255))
    else:
        text0 = FONT.render("How many Blocks would you like to ", True, (255, 255, 255))
        text1 = FONT.render("remove from line " + str(line_input) + "?", True, (255, 255, 255))

    return text0, text1


def get_blocks(textinput_blocks, line, screen, events, piles, initial_text0, initial_text1):
    """
    :param textinput_blocks: TextInput Object
    :param line: the line, which was chosen to remove blocks from
    :param screen: gui-screen
    :param events: detected events by pygame (keystrokes)
    :param piles: list of available blocks (at the beginning of game [1, 3, 5, 7])
    :return: int: line, from which blocks are supposed to be removed. None if invalid input

    checks validity of the input (from which line to remove blocks). If not valid returns None + error messages.
    If valid it returns the input as int + confirming messages
    """
    screen.blit(textinput_blocks.get_surface(), (865, 62))
    if textinput_blocks.update(events):
        blocks_input = textinput_blocks.get_text()
        if len(str(blocks_input))>0:
            if check_validity_blocks(blocks_input, line, piles) is False:
                text0, text1 = print_message_blocks(validity=False, piles=piles, line=line)
                return None, text0, text1
            else:
                text0, text1 = print_message_blocks(validity=True, piles=piles, line=line)
                return int(blocks_input), text0, text1

    return None, initial_text0, initial_text1


def print_message_blocks(validity, piles, line):
    FONT = pygame.font.SysFont('bahnschrift', 15)
    if validity is False:
        text0 = FONT.render("Invalid Input! Line " + str(line) + " contains " + str(piles[line]) + " Blocks.",
                            True, (255, 255, 255))
        text1 = FONT.render("Please choose a number between 1 and " + str(piles[line]), True, (255, 255, 255))
    else:
        text0 = FONT.render("", True, (255, 255, 255))
        text1 = FONT.render("", True, (255, 255, 255))

    return text0, text1


def check_validity_blocks(nr_of_blocks, line, piles):
    # Check if input can be converted to int:
    try:
        nr_of_blocks = int(nr_of_blocks)
    except:
        return False
    # check if input is in allowed range
    if 0 < nr_of_blocks <= piles[line]:
        return True
    return False
