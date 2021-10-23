import math
import random
import time
import pygame
import blocks as nim_blocks


class Nim():

    def __init__(self, initial=[1, 3, 5, 7]):
        """
        Initialize game board.
        Each game board has
            - `piles`: a list of how many elements remain in each pile
            - `player`: 0 or 1 to indicate which player's turn
            - `winner`: None, 0, or 1 to indicate who the winner is
        """
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        """
        Nim.available_actions(piles) takes a `piles` list as input
        and returns all of the available actions `(i, j)` in that state.

        Action `(i, j)` represents the action of removing `j` items
        from pile `i` (where piles are 0-indexed).
        """
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        Nim.other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = Nim.other_player(self.player)

    def move(self, action):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(i, j)`.
        """
        pile, count = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count
        self.switch_player()

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        a = self.q.keys()
        if (tuple(state), action) in self.q.keys():
            return self.q[(tuple(state), action)]
        else:
            return 0

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        self.q[(tuple(state), action)] = old_q + self.alpha * (reward + future_rewards - old_q)


    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        # get all possible actions:
        possible_actions = self.get_sorted_possible_actions(state=state)
        if possible_actions == []:
            return 0
        else:
            return possible_actions[-1][0]

    def get_sorted_possible_actions(self, state):
        # get all possible actions:
        possible_actions = []
        for action in Nim.available_actions(piles=state):
            self.q[(tuple(state), action)] = self.get_q_value(state=state, action=action)
            possible_actions.append((self.q[(tuple(state), action)], (state, action)))
        # find and return highest reward
        possible_actions.sort()
        return possible_actions

    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        possible_actions = self.get_sorted_possible_actions(state=state)
        if epsilon is False or random.random() < (1 - self.epsilon):
            return possible_actions[-1][1][1]
        else:
            return random.choice(tuple(Nim.available_actions(piles=state)))


def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    player = NimAI()

    # Play n games
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Nim()

        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = player.choose_action(game.piles)
            # if i > 9997:
            #     print(action)
            #     print(state)
            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make move
            game.move(action)
            new_state = game.piles.copy()

            # When game is over, update Q values with rewards
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Done training")

    # Return the trained AI
    return player


def play(ai, human_player=None):
    """
    Play human game against the AI.
    `human_player` can be set to 0 or 1 to specify whether
    human player moves first or second.
    """

    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = Nim()

    # Game loop
    while True:

        # Print contents of piles
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print()

        # Compute available actions
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)

        # Let human make a move
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")

        # Have AI make a move
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        # Make move
        game.move((pile, count))

        # Check for winner
        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            return

# Helper functions for GUI:

def reset_dynamic_texts(textsurface):
    SMALL_FONT = pygame.font.SysFont('bahnschrift', 15)
    empty_text = SMALL_FONT.render("", True, (255, 255, 255))
    textsurface[0] = (empty_text, (600, 100))
    textsurface[1] = (empty_text, (600, 114))
    textsurface[2] = (empty_text, (600, 100))
    textsurface[3] = (empty_text, (600, 114))
    return textsurface, empty_text, empty_text


def reset_lines_and_blocks():
    line_confirmed = False
    blocks_confirmed = False
    line_input = None
    blocks_input = None
    return line_confirmed, blocks_confirmed, line_input, blocks_input


def print_last_move(current_game, human_player, textsurface, line, blocks, moves_made):
    SMALL_FONT = pygame.font.SysFont('bahnschrift', 15)
    player = "Human" if current_game.player != human_player else "AI"
    text = SMALL_FONT.render(f"{player} removed {blocks} Blocks from line {line}.", True, (255, 255, 255))
    textsurface.append((text, (600, (180+moves_made*17))))
    moves_made += 1
    return moves_made


def print_winner_message(human_player, winner):
    font = pygame.font.SysFont("bahnschrift", 30)
    small_font = pygame.font.SysFont("bahnschrift", 15)
    if human_player == winner:
        text = font.render("Congratulations, Human! You are the superior being!", True, (0, 0, 0))
    else:
        text = font.render("Muhahaha! You lost, Human! The reign of AI over humanity has begun!", True, (0, 0, 0))
    text2 = small_font.render("Press any key to get back to the menu.", True, (0, 0, 0))
    return text, text2


def draw_playing_screen(screen, piles, textsurface):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (593, 0, 1000, 1000))
    pygame.draw.rect(screen, WHITE, (850, 55, 50, 35), 2)
    pygame.draw.rect(screen, WHITE, (675, 18, 50, 35), 2)
    nim_blocks.drawAllBlocks(screen, piles)
    for text in textsurface:
        screen.blit(text[0], text[1])


def get_initial_textsurface():
    SMALL_FONT = pygame.font.SysFont('bahnschrift', 15)
    FONT = pygame.font.SysFont('bahnschrift', 30)
    textsurface = []
    dynamic_line_confirmed_text0 = SMALL_FONT.render("", True, (255, 255, 255))
    dynamic_line_confirmed_text1 = SMALL_FONT.render("", True, (255, 255, 255))
    dynamic_blocks_confirmed_text0 = SMALL_FONT.render("", True, (255, 255, 255))
    dynamic_blocks_confirmed_text1 = SMALL_FONT.render("", True, (255, 255, 255))
    textsurface.append((dynamic_line_confirmed_text0, (600, 100)))  # dynamic texts need to be at index 0-3!!!
    textsurface.append((dynamic_line_confirmed_text1, (600, 114)))
    textsurface.append((dynamic_blocks_confirmed_text0, (600, 135)))
    textsurface.append((dynamic_blocks_confirmed_text1, (600, 149)))

    text0 = FONT.render('How many blocks do you want to', True, (0, 0, 0))
    text1 = FONT.render('remove and from which Line?', True, (0, 0, 0))
    text2 = FONT.render("Line:", True, (255, 255, 255))
    text3 = FONT.render("Amount of blocks:", True, (255, 255, 255))
    text4 = SMALL_FONT.render("L0", True, (0, 0, 0))
    text5 = SMALL_FONT.render("L1", True, (0, 0, 0))
    text6 = SMALL_FONT.render("L2", True, (0, 0, 0))
    text7 = SMALL_FONT.render("L3", True, (0, 0, 0))

    textsurface.append((text0, (80, 20)))
    textsurface.append((text1, (80, 55)))
    textsurface.append((text2, (600, 20)))
    textsurface.append((text3, (600, 55)))
    textsurface.append((text4, (243, 372)))
    textsurface.append((text5, (168, 452)))
    textsurface.append((text6, (85, 532)))
    textsurface.append((text7, (5, 612)))

    return textsurface