######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# Dr. Jakob Prange                   #
# FAI Universität Augsburg           #
# WiSe 2024/25                       #
# Software Assignment                #
######################################

from player import Player
from sudoku import Sudoku


class Game:
    """
    The game class controls the game flow as well as the Sudoku field. 
    Note that a few required methods were renamed or put into other classes for better clarity and distribution.
    """

    def __init__(self, size, difficulty):
        """
        The init method in the game class will create a new game session and call the constructor in the Sudoku class. 
        The number of players in Sudoku is always one, therefore the only parameters here will be 
        the difficulty (easy, medium and difficult) and the size of the Sudoku field (per default 9 with 3x3 grids). 
        To be able to set a high score we also want to implement a timer that measures the needed time.
        """
        pass

    def start_timer():
        """This is a helper method to start a timer a soon as a Game is created."""

    def set_player(player):
        """Sets a given Player object as the player for the current game session. 
        An add_player() method that was suggested in the given Game class code is not 
        applicable in a Sudoku Game since there is only one player."""

    def finish_game():
        ''' Cleans-up code after a game session ends.'''

    def is_finished() -> bool: 
        '''Checks if the game is successfully finished by calling the method is_solved() in Sudoku class.
        This is the renamed win_condition() method.'''

    def lose_condition():
        '''In Sudoku a player can not really lose. That is why it is not appointed yet if we want to implement this method. 
        The only thing it could possibly check is if a Sudoku is not solvable, 
        but that should not happen since the program should be able to automatically generate new, and always solvable Sudoku fields.'''

    def step(players_input) -> bool :
        '''One player input in a Sudoku cell, which is in the default Sudoku a number between 1 and 9. 
        Also the player should have the possibility to erase his own previous inputs. 
        The return value represents if the step was valid and successful.'''

    def get_current_state() : 
        '''Returns the current Sudoku field of the game session.'''

    def run(): 
        '''Runs a game session interactively until the win condition is reached.'''


if __name__ == "__main__":
    """
    write additional testing code here for things that don't work well as unit tests:
    """

    # Example for how we might test your program:
    game = Game()  # create new game
    for i in range(3):  # run for 3 steps
        game.step()
    game.save_game("saved")  # save game state
    game2 = Game.load_game("saved")  # load game state
    assert game.get_current_state() == game2.get_current_state()
