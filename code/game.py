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
import datetime as dt

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
        self.time_length = 0
        
        self.name = "Sudoku Game " + str(dt.datetime.now())

    def start_timer(self):
        """This is a helper method to start a timer a soon as a Game is created."""
        self.time_start = time.time()

    def measure_time_needed(self) -> int:
        """This is a helper method to measure the needed time for the sudoku in seconds."""
        return int(time.time() - self.time_start) # int cast to get seconds
        
    def set_player(self,player:Player):
        """Sets a given Player object as the player for the current game session. 
        An add_player() method that was suggested in the given Game class code is not 
        applicable in a Sudoku Game since there is only one player."""
        self.player = player

    def finish_game(self):
        ''' Cleans-up code after a game session ends.'''
        # Anjas TODO Maybe invoke high score saving process or other useful functionality
        del self.sudoku
        del self.time_start
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

    def step(self) -> bool:
        '''One player input in a Sudoku cell, which is in the default Sudoku a number between 1 and 9. 
        Also the player should have the possibility to erase his own previous inputs. 
        '''
        status = self.ui.choose_input_options_during_game() 
        if status: self.ui.show_current_state()

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
        self.time_length += self.measure_time_needed()
        self.ui._bye()
        self.finish_game()
        
    def show_prefilled_values(self) -> str:
        return self.sudoku.__str__(self.copy_sudoku, Colors.GREY)
    
    def show_prefilled_values_with_highlighted_cell(self,x,y,color:Colors) -> str:
        value = self.sudoku.values[x][y]
        copy_value = self.copy_sudoku[x][y]
        if self.copy_sudoku[x][y] == 0:
            self.sudoku.values[x][y] = Colors.to_str(self.sudoku.values[x][y], color)
        else:
            self.copy_sudoku[x][y] = Colors.to_str(self.sudoku.values[x][y], color)
        prefilled_with_blinking_mix = self.show_prefilled_values().replace(color.value + "0",color.value + "_")
        self.sudoku.values[x][y] = value
        self.copy_sudoku[x][y] = copy_value 
        return prefilled_with_blinking_mix

    def str_to_game(content:list[str],name:str):
        """ This method takes the file content of a saved Game and with that 
        undoes the __str__() method. It returns a new game object.
        Afterwards this game object has its attributes name, sudoku (with values, size and grid), 
        time_length and hint_counter set.
        
        Note that the game.sudoku attribute is tested in str_to_sudoku() method
        >>> content = ['Sudoku Game from 2025-01-06 13:09:09.371111\\n', '\\n', ' -  -  -  -  -  -  -  -  - \\n', '| 1  7    | 3       | 9  4    |\\n', '|    6    | 9  4  5 | 2  1  7 |\\n', '|    5    |    1  7 |    8  6 |\\n', ' -  -  -  -  -  -  -  -  - \\n', '|    8  5 | 7  2  4 | 6     1 |\\n', '| 3     6 | 5  9  8 |    2  4 |\\n', '| 2  4  7 | 6  3  1 | 5  9  8 |\\n', ' -  -  -  -  -  -  -  -  - \\n', '|       8 | 4     9 |         |\\n', '| 7  9  4 | 1  6  2 | 8  5  3 |\\n', '| 6  2  1 | 8  5  3 | 4  7  9 |\\n', '\\n', 'Needed time: 24 seconds\\n', 'Needed hints: 0']
        >>> name = 'Sudoku Game'
        >>> game = Game.str_to_game(content,name)
        >>> game.name
        'Sudoku Game'
        >>> game.time_length
        24
        >>> game.hint_counter
        0
        """
        game = Game()
        game.name = name
        game.sudoku = Sudoku.str_to_sudoku(content)
        game.time_length = Game._decode_time(content[len(content) - 2])
        game.hint_counter = Game._decode_hints(content[len(content) - 1])
        return game

    def _decode_time(content:str) -> int:
        """
        Helper method to decode needed time so far. It is used in str_to_game() method 
        but only takes the string where the hint count is located in instead of the
        whole file content.
        
        >>> content = 'Needed time: 123 seconds\\n'
        >>> Game._decode_time(content)
        123
        """
        
        return int(content[len("Needed time: "):content.find("seconds")])
        
    def _decode_hints(content:str) -> int:
        """ 
        Helper method to decode needed hints. It is used in str_to_game() method 
        but only takes the string where the hint count is located in instead of the
        whole file content.
        
        >>> content = 'Needed hints: 123'
        >>> Game._decode_hints(content)
        123
        """
        return int(content[len("Needed hints: "):])
    
    def info(self) -> str:
        """
        String Representation of the most identifying features to separate current game object from others.
        This is mostly useful for loading a saved game, because the name alone can be changed from User and 
        can be not identifying.
        
        >>> game = Game()
        >>> "3 x 3, Progress: 0/20" in game.info() # e.g. Sudoku Game 2025-01-07 11:11:03.646943, Difficulty.EASY, 3 x 3, Progress: 0/20
        True
        
        >>> new_game = Game(size = 16, difficulty = Difficulty.MEDIUM)
        >>> "Difficulty.MEDIUM, 4 x 4, Progress: 0/128" in new_game.info() # e.g. Sudoku Game 2025-01-07 11:11:03.646943, Difficulty.EASY, 3 x 3, Progress: 0/20
        True
        """
        beginEmptyCellCount = Sudoku(size=self.sudoku.size,values=self.copy_sudoku)._count_empty_cells()
        currentEmptyCellCount = self.sudoku._count_empty_cells()
        return str(self.name) + ", " + str(self.sudoku.get_difficulty(beginEmptyCellCount)) + ", " +\
                str(self.sudoku.grid) + " x " + str(self.sudoku.grid) + \
                ", Progress: " + str(currentEmptyCellCount - beginEmptyCellCount) + "/" + str(beginEmptyCellCount)

    def __str__(self) -> LiteralString | str:
        """
        String representation of a game object and its attributes sudoku, time_length and hint_counter.
        Note that the name will not be included since it is only necessary for saving the game and
        should be equivalent to the files path basename
        
        >>> game = Game()
        >>> game.sudoku.values = [[0, 8, 2, 7, 4, 6, 0, 3, 5], [1, 3, 5, 2, 0, 9, 0, 4, 7], [6, 4, 7, 5, 3, 1, 0, 8, 2], [3, 0, 6, 1, 5, 8, 0, 0, 9], [0, 2, 9, 6, 0, 3, 8, 5, 1], [8, 0, 1, 9, 0, 4, 3, 7, 0], [0, 0, 0, 3, 0, 5, 2, 1, 8], [0, 6, 3, 8, 1, 2, 0, 9, 4], [2, 1, 8, 4, 9, 7, 5, 0, 3]]
        >>> print(game)
        <BLANKLINE>
        <BLANKLINE>
         -  -  -  -  -  -  -  -  - 
        |    8  2 | 7  4  6 |    3  5 |
        | 1  3  5 | 2     9 |    4  7 |
        | 6  4  7 | 5  3  1 |    8  2 |
         -  -  -  -  -  -  -  -  - 
        | 3     6 | 1  5  8 |       9 |
        |    2  9 | 6     3 | 8  5  1 |
        | 8     1 | 9     4 | 3  7    |
         -  -  -  -  -  -  -  -  - 
        |         | 3     5 | 2  1  8 |
        |    6  3 | 8  1  2 |    9  4 |
        | 2  1  8 | 4  9  7 | 5     3 |
        <BLANKLINE>
        Needed time: 0 seconds
        Needed hints: 0
        """
        return "\n\n" + str(self.sudoku) + \
                    "\nNeeded time: " + str(self.time_length) + " seconds" + \
                    "\nNeeded hints: " + str(self.hint_counter) 

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    """
    write additional testing code here for things that don't work well as unit tests:
    """
    # Anjas TODO Write Docs and Test
