import pygame
import nim_yt.businesslayer_nim.pygame_textinput as pg_textinput
import nim_yt.businesslayer_nim.blocks as nim_blocks
import nim_yt.GUI_nim.gui as nim_gui


def get_line(textinput_line, screen, events, piles, initial_text0, initial_text1):
    """
    :param textinput_line: TextInput Object
    :param screen: gui-screen
    :param events: detected events by pygame (keystrokes)
    :param piles: list of available blocks (at the beginning of game [1, 3, 5, 7])
    :return: int: line, from which blocks are supposed to be removed. None if invalid input

    If line confirmed is false, text input is shown under "Line:", and the resulting input is recognized
        as the line-input and checked for validity accordingly.
    If valid, it is stored as line_input and line_confirmed
        switches to True. Additionally a message "You chose line X. how many Blocks would you like to remove from this
        line?" occurs.
    If invalid the message "Invalid input. This line cannot be chosen" occures on the GUI, but
        disappears when a valid input comes in. A similar error message exists for the textinput_blocks.
    Once a valid input was entered for both, a tuple with both inputs is returned

    """
    screen.blit(textinput_line.get_surface(), (690, 25))
    if textinput_line.update(events):
        line_input = textinput_line.get_text()

        if check_validity_line(line_input, piles) is False:
            text0, text1 = print_message_line(validity=check_validity_line(line_input, piles),
                                              line_input=999)
            return None, text0, text1
        else:
            text0, text1 = print_message_line(validity=check_validity_line(line_input, piles),
                                             line_input=line_input)
            return int(line_input), text0, text1
    else:
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
