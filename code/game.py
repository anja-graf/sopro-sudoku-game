######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# Dr. Jakob Prange                   #
# FAI Universität Augsburg           #
# WiSe 2024/25                       #
# Software Assignment                #
######################################

from player import Player
from sudoku import *
import time

class Game:
    """
    The game class controls the game flow as well as the Sudoku field and functions as abstract wrapper for it. 
    Note that a few required methods were renamed or put into other classes for better clarity and distribution.
    """

    def __init__(self, size: int = 9, difficulty:Difficulty = Difficulty.EASY, ui = ...):
        """
        The init method in the game class will create a new game session and call the constructor in the Sudoku class. 
        The number of players in Sudoku is always one, therefore the only parameters here will be 
        the difficulty (easy, medium and difficult) and the size of the Sudoku field (per default 9 with 3x3 grids). 
        To be able to set a high score we also want to implement a timer that measures the needed time.
        """
        self.sudoku = Sudoku(size)
        self.sudoku.create(difficulty)
        # A copy is being created to differentiate between generated and values entered from user
        self.copy_sudoku = Sudoku._deep_copy(self.sudoku.values) 
        self.player = None
        self.hint_counter = 0
        self.ui = ui
        self.time_start = None
        self.time_length = None

    def start_timer(self):
        """This is a helper method to start a timer a soon as a Game is created."""
        self.time_start = time.time()

    def stop_timer(self):
        """This is a helper method to measure the needed time for the sudoku."""
        self.time_length = int(time.time() - self.time_start) # int cast to get seconds
        del self.time_start
        
    def set_player(self,player:Player):
        """Sets a given Player object as the player for the current game session. 
        An add_player() method that was suggested in the given Game class code is not 
        applicable in a Sudoku Game since there is only one player."""
        self.player = player

    def finish_game(self):
        ''' Cleans-up code after a game session ends.'''
        # Anjas TODO Maybe invoke high score saving process or other useful functionality
        del self.sudoku
        del self.copy_sudoku

    def is_finished(self) -> bool: 
        '''Checks if the game is successfully finished by calling the method is_solved() in Sudoku class.
        This is the renamed win_condition() method.'''
        return self.sudoku.is_solved()

    def lose_condition():
        '''In Sudoku a player can not really lose. That is why it is not appointed yet if we want to implement this method. 
        The only thing it could possibly check is if a Sudoku is not solvable, 
        but that should not happen since the program should be able to automatically generate new, and always solvable Sudoku fields.'''
        pass

    def step(self):
        '''One player input in a Sudoku cell, which is in the default Sudoku a number between 1 and 9. 
        Also the player should have the possibility to erase his own previous inputs. 
        '''
        if self.ui.choose_input_options_during_game():
            self.ui.show_current_state()

    def get_current_state(self) -> Sudoku: 
        '''Returns the current Sudoku field of the game session.'''
        return self.sudoku

    def run(self):
        '''Runs a game session interactively until the win condition is reached and the sudoku is fully solved.
        Note that this method should be called from the user_interface. Previously the player 
        should have gotten a welcome and instructions on how to play.
        '''
        self.start_timer()
        self.ui.show_current_state()
        while not self.is_finished():
            self.step()
        self.stop_timer()
        self.ui._bye()
        self.finish_game()
        


if __name__ == "__main__":
    """
    write additional testing code here for things that don't work well as unit tests:
    """
    # Anjas TODO Write Docs and Test
    # Example for how we might test your program:
    game = Game()  # create new game
    game.run()
