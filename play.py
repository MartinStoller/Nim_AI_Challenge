from nim import train, play


def start_game(training_iterations, player):
    ai = train(training_iterations)
    play(ai, human_player=player)
