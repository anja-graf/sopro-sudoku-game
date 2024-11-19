######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# Dr. Jakob Prange                   #
# FAI Universität Augsburg           #
# WiSe 2024/25                       #
# Software Assignment                #
######################################

from player import Player


class Game:

    def __init__(self):
        '''
        Creates a new game session. Think about which pieces of information you need at this time
        (e.g. players, game mode, time limit, ...) and add them as arguments.
        '''
        pass

    def add_player(self, player: Player):
        '''
        Adds a Player object as a player for the current game session.
        '''
        pass

    def save_game(self, filename):
        '''
        '''
        pass

    @classmethod
    def load_game(cls, filename) -> 'Game':
        '''
        '''
        game_object = ...
        ...
        return game_object

    def finish_game(self):
        '''
        Clean-up code after a game session ends.
        '''
        pass

    def win_condition(self):
        '''
        What needs to be true so that a player wins?
        '''
        pass

    def lose_condition(self):
        '''
        What needs to be true so that a player loses?
        '''
        pass

    def step(self):
        '''
        One player turn (for turn-based games), player input (for single-player games) or frame (for Space Invaders).
        '''
        pass

    def get_current_state(self):
        '''
        Returns the current state of the game session.
        '''
        pass

    def run(self):
        '''
        Runs a game session interactively until a win (or lose) condition is reached.
        '''
        pass


if __name__ == '__main__':
    '''
    write additional testing code here for things that don't work well as unit tests:
    '''

    # Example for how we might test your program:
    game = Game()           # create new game
    for i in range(3):               # run for 3 steps
        game.step()
    game.save_game('saved')          # save game state
    game2 = Game.load_game('saved')  # load game state
    assert game.get_current_state() == game2.get_current_state()
