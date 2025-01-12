######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# Dr. Jakob Prange                   #
# FAI Universität Augsburg           #
# WiSe 2024/25                       #
# Software Assignment                #
######################################

from collections.abc import Generator
from sudoku import *
import time
import datetime as dt


class Game:
    """
    The game class controls the game flow as well as the Sudoku field and functions as abstract wrapper for it. 
    Note that a few required methods were renamed or put into other classes for better clarity and distribution.
    """

    def __init__(self, size: int = 9, difficulty: Difficulty = Difficulty.EASY, ui=...):
        """
        The init method in the game class creates a new game session and calls the constructor in the Sudoku class. 
        The number of players in Sudoku is always one, therefore the only parameters here is 
        the difficulty (easy, medium and difficult) and the size of the Sudoku field (per default 9 with 3x3 grids). 
        To be able to set a high score we also have a timer that measures the needed time.
        As already described in Sudoku constructor the given size has to be a square number. The smallest possible size is 4.

        >>> game = Game()
        >>> game.sudoku.size == 9
        True
        >>> game.sudoku.values == game.copy_sudoku
        True
        >>> game.hint_counter
        0
        >>> game.time_length 
        0
        >>> game.sudoku.get_difficulty(game.sudoku._count_empty_cells()) 
        <Difficulty.EASY: 1>

        >>> new_game = Game(size=-1) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
            ...
        ValueError: This size can not be taken as a valid sudoku size, because it is to small!
        """
        self.sudoku = Sudoku(size)
        self.sudoku.create(difficulty)
        # A copy is being created to differentiate between generated and values entered from user
        self.copy_sudoku = Sudoku._deep_copy(self.sudoku.values)
        self.hint_counter = 0
        self.ui = ui
        self.time_start = None
        self.time_length = 0

        self.name = "Sudoku Game " + str(dt.datetime.now())

    def _start_timer(self):
        """
        This is a helper method to start a timer a soon as a Game is created and run() method called.
        It will set the games attribute 'time_start' to the time the method was called.

        >>> game = Game()
        >>> game._start_timer()
        >>> game.time_start != None
        True
        """
        self.time_start = time.time()

    def measure_time_needed(self) -> int:
        """This is a helper method to measure the needed time for the sudoku in seconds.
        >>> game = Game()
        >>> game._start_timer()
        >>> game.measure_time_needed()
        0
        >>> time.sleep(2)
        >>> game.measure_time_needed()
        2
        """
        return int(time.time() - self.time_start)  # int cast to get seconds

    def finish_game(self):
        ''' Cleans-up code after a game session ends.'''
        self.ui._bye()
        del self.sudoku
        del self.time_start
        del self.copy_sudoku

    def is_finished(self) -> bool:
        '''Checks if the game is successfully finished by calling the method is_solved() in Sudoku class.
        This is the renamed win_condition() method.

        >>> game = Game()
        >>> game.sudoku = Sudoku(size=9,values=[[7, 2, 8, 3, 4, 6, 5, 1, 9], [5, 9, 1, 2, 8, 7, 6, 4, 3], [6, 3, 4, 9, 1, 5, 7, 8, 2], [1, 6, 3, 5, 9, 8, 4, 2, 7], [4, 7, 2, 6, 3, 1, 8, 9, 5], [8, 5, 9, 7, 2, 4, 1, 3, 6], [2, 8, 5, 4, 7, 3, 9, 6, 1], [9, 1, 6, 8, 5, 2, 3, 7, 4], [3, 4, 7, 1, 6, 9, 2, 5, 8]])
        >>> game.sudoku.is_solved()
        True

        >>> game.sudoku.values[0][0] = 0
        >>> game.sudoku.is_solved()
        False
        '''
        return self.sudoku.is_solved()

    def lose_condition(self) -> bool:
        '''In Sudoku a player can not really lose. That is why this method checks is if a Sudoku is still solvable with the current users input. 
        If it is not, lose_condition will return True. In the beginning after creating a new game that can not happen since the program should 
        be able to automatically generate new, and always solvable Sudoku.

        >>> game = Game()
        >>> game.sudoku = Sudoku(values = [[5, 5, 0, 2, 0, 8, 1, 9, 7], [2, 8, 6, 1, 9, 7, 3, 4, 5], [1, 7, 9, 3, 4, 5, 2, 6, 8], [7, 0, 3, 0, 2, 6, 8, 1, 0], [5, 6, 0, 8, 1, 9, 7, 0, 4], [8, 9, 1, 7, 3, 0, 5, 2, 6], [0, 3, 7, 4, 0, 2, 0, 0, 1], [6, 1, 8, 9, 7, 0, 4, 0, 2], [0, 0, 0, 6, 8, 1, 9, 0, 0]])
        >>> game.sudoku.solution = []
        >>> game.lose_condition() 
        True
        '''
        try:
            self.sudoku.solve()
        except Exception as e:
            return str(e) == "Oh no! Seems like this Sudoku is unsolvable :( "
        return False

    def step(self) -> bool:
        '''This method is used for a players' step. This can be entering a new value at a specified 
        coordinate in the sudoku field or getting a hint if the current sudoku field is too 
        hard, etc. every possible thing a user can do while playing.
        Note that the self.ui attribute has to be set, even through not necessary already in the games' constructor!

        >>> game = Game() # doctest: +IGNORE_EXCEPTION_DETAIL
        >>> game.step()
        Traceback (most recent call last):
            ...
        Exception: To play a game and call step() method you have to set the self.ui attribute!                             
        This is a programming error and should never happen.
        '''
        if self.ui is ...:
            raise Exception("To play a game and call step() method you have to set the self.ui attribute! \
                            \nThis is a programming error and should never happen.")
        status = self.ui.choose_input_options_during_game()
        if status:
            self.ui.show_current_state()

    def solve(self) -> Generator:
        """
        This repeatedly applies the show_and_set_hint() method so the player can watch the sudoku solving itself. 
        """
        while not self.sudoku.is_solved():
            self.hint_counter += 1
            yield self.sudoku.show_and_set_hint()

    def get_current_state(self) -> Sudoku:
        '''Returns the current Sudoku field of the game session.'''
        return self.sudoku

    def run(self):
        '''Runs a game session interactively until the win condition is reached and the sudoku is fully solved.
        Note that this method should be called from the user_interface. Previously the player 
        should have gotten a welcome and instructions on how to play.
        If you want to call the run() function you should always set the ui attribute of the game object first!

        >>> game = Game() # doctest: +IGNORE_EXCEPTION_DETAIL
        >>> game.run()
        Traceback (most recent call last):
            ...
        Exception: To play a game and call run() method you have to set the self.ui attribute!                 
        This is a programming error and should never happen.
        '''
        if self.ui is ...:
            raise Exception("To play a game and call run() method you have to set the self.ui attribute! \
                \nThis is a programming error and should never happen.")
        self._start_timer()
        self.ui.show_current_state()
        while not self.is_finished():
            self.step()
        # If the game was interrupted and started again from a saved file the time needed will be added, otherwise self.time_length is 0
        self.time_length += self.measure_time_needed()
        self.finish_game()

    def show_prefilled_values(self) -> str:
        """
        String representation of game, where all prefilled values, saved in the copy_sudoku attribute of the game are colored grey. 
        In difference to that, all numbers entered from the user are white, stand out and can be distinguished.

        >>> game = Game()
        >>> game.sudoku.values = [[0, 7, 0, 2, 9, 3, 5, 8, 1], [0, 5, 1, 0, 0, 7, 0, 2, 9], [2, 3, 9, 8, 1, 5, 7, 6, 0], [1, 2, 5, 4, 7, 8, 6, 9, 3], [0, 0, 0, 1, 5, 2, 0, 4, 7], [4, 8, 7, 9, 0, 6, 0, 0, 5], [3, 4, 6, 5, 0, 9, 0, 7, 8], [7, 1, 8, 3, 0, 4, 9, 5, 2], [0, 9, 0, 7, 0, 1, 4, 3, 6]]
        >>> game.copy_sudoku = game.sudoku.values
        >>> game.show_prefilled_values()
        ' -  -  -  -  -  -  -  -  - \\n|    \\x1b[90m7\\x1b[0m    | \\x1b[90m2\\x1b[0m  \\x1b[90m9\\x1b[0m  \\x1b[90m3\\x1b[0m | \\x1b[90m5\\x1b[0m  \\x1b[90m8\\x1b[0m  \\x1b[90m1\\x1b[0m |\\n|    \\x1b[90m5\\x1b[0m  \\x1b[90m1\\x1b[0m |       \\x1b[90m7\\x1b[0m |    \\x1b[90m2\\x1b[0m  \\x1b[90m9\\x1b[0m |\\n| \\x1b[90m2\\x1b[0m  \\x1b[90m3\\x1b[0m  \\x1b[90m9\\x1b[0m | \\x1b[90m8\\x1b[0m  \\x1b[90m1\\x1b[0m  \\x1b[90m5\\x1b[0m | \\x1b[90m7\\x1b[0m  \\x1b[90m6\\x1b[0m    |\\n -  -  -  -  -  -  -  -  - \\n| \\x1b[90m1\\x1b[0m  \\x1b[90m2\\x1b[0m  \\x1b[90m5\\x1b[0m | \\x1b[90m4\\x1b[0m  \\x1b[90m7\\x1b[0m  \\x1b[90m8\\x1b[0m | \\x1b[90m6\\x1b[0m  \\x1b[90m9\\x1b[0m  \\x1b[90m3\\x1b[0m |\\n|         | \\x1b[90m1\\x1b[0m  \\x1b[90m5\\x1b[0m  \\x1b[90m2\\x1b[0m |    \\x1b[90m4\\x1b[0m  \\x1b[90m7\\x1b[0m |\\n| \\x1b[90m4\\x1b[0m  \\x1b[90m8\\x1b[0m  \\x1b[90m7\\x1b[0m | \\x1b[90m9\\x1b[0m     \\x1b[90m6\\x1b[0m |       \\x1b[90m5\\x1b[0m |\\n -  -  -  -  -  -  -  -  - \\n| \\x1b[90m3\\x1b[0m  \\x1b[90m4\\x1b[0m  \\x1b[90m6\\x1b[0m | \\x1b[90m5\\x1b[0m     \\x1b[90m9\\x1b[0m |    \\x1b[90m7\\x1b[0m  \\x1b[90m8\\x1b[0m |\\n| \\x1b[90m7\\x1b[0m  \\x1b[90m1\\x1b[0m  \\x1b[90m8\\x1b[0m | \\x1b[90m3\\x1b[0m     \\x1b[90m4\\x1b[0m | \\x1b[90m9\\x1b[0m  \\x1b[90m5\\x1b[0m  \\x1b[90m2\\x1b[0m |\\n|    \\x1b[90m9\\x1b[0m    | \\x1b[90m7\\x1b[0m     \\x1b[90m1\\x1b[0m | \\x1b[90m4\\x1b[0m  \\x1b[90m3\\x1b[0m  \\x1b[90m6\\x1b[0m |\\n'
        """
        return self.sudoku.__str__(self.copy_sudoku, Colors.GREY)

    def show_prefilled_values_with_highlighted_cell(self, x, y, color: Colors) -> str:
        """
        String representation of game, where all prefilled values, saved in the copy_sudoku attribute of the game are colored grey. 
        In difference to that, all numbers entered from the user are white, stand out and can be distinguished.

        >>> game = Game()
        >>> game.sudoku.values = [[0, 7, 0, 2, 9, 3, 5, 8, 1], [0, 5, 1, 0, 0, 7, 0, 2, 9], [2, 3, 9, 8, 1, 5, 7, 6, 0], [1, 2, 5, 4, 7, 8, 6, 9, 3], [0, 0, 0, 1, 5, 2, 0, 4, 7], [4, 8, 7, 9, 0, 6, 0, 0, 5], [3, 4, 6, 5, 0, 9, 0, 7, 8], [7, 1, 8, 3, 0, 4, 9, 5, 2], [0, 9, 0, 7, 0, 1, 4, 3, 6]]
        >>> game.copy_sudoku = game.sudoku.values
        >>> game.show_prefilled_values_with_highlighted_cell(1,1,Colors.BLINKING)
        ' -  -  -  -  -  -  -  -  - \\n|    \\x1b[90m7\\x1b[0m    | \\x1b[90m2\\x1b[0m  \\x1b[90m9\\x1b[0m  \\x1b[90m3\\x1b[0m | \\x1b[90m5\\x1b[0m  \\x1b[90m8\\x1b[0m  \\x1b[90m1\\x1b[0m |\\n|    \\x1b[90m\\x1b[5m5\\x1b[0m\\x1b[0m  \\x1b[90m1\\x1b[0m |       \\x1b[90m7\\x1b[0m |    \\x1b[90m2\\x1b[0m  \\x1b[90m9\\x1b[0m |\\n| \\x1b[90m2\\x1b[0m  \\x1b[90m3\\x1b[0m  \\x1b[90m9\\x1b[0m | \\x1b[90m8\\x1b[0m  \\x1b[90m1\\x1b[0m  \\x1b[90m5\\x1b[0m | \\x1b[90m7\\x1b[0m  \\x1b[90m6\\x1b[0m    |\\n -  -  -  -  -  -  -  -  - \\n| \\x1b[90m1\\x1b[0m  \\x1b[90m2\\x1b[0m  \\x1b[90m5\\x1b[0m | \\x1b[90m4\\x1b[0m  \\x1b[90m7\\x1b[0m  \\x1b[90m8\\x1b[0m | \\x1b[90m6\\x1b[0m  \\x1b[90m9\\x1b[0m  \\x1b[90m3\\x1b[0m |\\n|         | \\x1b[90m1\\x1b[0m  \\x1b[90m5\\x1b[0m  \\x1b[90m2\\x1b[0m |    \\x1b[90m4\\x1b[0m  \\x1b[90m7\\x1b[0m |\\n| \\x1b[90m4\\x1b[0m  \\x1b[90m8\\x1b[0m  \\x1b[90m7\\x1b[0m | \\x1b[90m9\\x1b[0m     \\x1b[90m6\\x1b[0m |       \\x1b[90m5\\x1b[0m |\\n -  -  -  -  -  -  -  -  - \\n| \\x1b[90m3\\x1b[0m  \\x1b[90m4\\x1b[0m  \\x1b[90m6\\x1b[0m | \\x1b[90m5\\x1b[0m     \\x1b[90m9\\x1b[0m |    \\x1b[90m7\\x1b[0m  \\x1b[90m8\\x1b[0m |\\n| \\x1b[90m7\\x1b[0m  \\x1b[90m1\\x1b[0m  \\x1b[90m8\\x1b[0m | \\x1b[90m3\\x1b[0m     \\x1b[90m4\\x1b[0m | \\x1b[90m9\\x1b[0m  \\x1b[90m5\\x1b[0m  \\x1b[90m2\\x1b[0m |\\n|    \\x1b[90m9\\x1b[0m    | \\x1b[90m7\\x1b[0m     \\x1b[90m1\\x1b[0m | \\x1b[90m4\\x1b[0m  \\x1b[90m3\\x1b[0m  \\x1b[90m6\\x1b[0m |\\n'
        >>> game.copy_sudoku[0][0] = 1
        >>> game.show_prefilled_values_with_highlighted_cell(1,1,Colors.BLINKING)
        ' -  -  -  -  -  -  -  -  - \\n| \\x1b[90m1\\x1b[0m  \\x1b[90m7\\x1b[0m    | \\x1b[90m2\\x1b[0m  \\x1b[90m9\\x1b[0m  \\x1b[90m3\\x1b[0m | \\x1b[90m5\\x1b[0m  \\x1b[90m8\\x1b[0m  \\x1b[90m1\\x1b[0m |\\n|    \\x1b[90m\\x1b[5m5\\x1b[0m\\x1b[0m  \\x1b[90m1\\x1b[0m |       \\x1b[90m7\\x1b[0m |    \\x1b[90m2\\x1b[0m  \\x1b[90m9\\x1b[0m |\\n| \\x1b[90m2\\x1b[0m  \\x1b[90m3\\x1b[0m  \\x1b[90m9\\x1b[0m | \\x1b[90m8\\x1b[0m  \\x1b[90m1\\x1b[0m  \\x1b[90m5\\x1b[0m | \\x1b[90m7\\x1b[0m  \\x1b[90m6\\x1b[0m    |\\n -  -  -  -  -  -  -  -  - \\n| \\x1b[90m1\\x1b[0m  \\x1b[90m2\\x1b[0m  \\x1b[90m5\\x1b[0m | \\x1b[90m4\\x1b[0m  \\x1b[90m7\\x1b[0m  \\x1b[90m8\\x1b[0m | \\x1b[90m6\\x1b[0m  \\x1b[90m9\\x1b[0m  \\x1b[90m3\\x1b[0m |\\n|         | \\x1b[90m1\\x1b[0m  \\x1b[90m5\\x1b[0m  \\x1b[90m2\\x1b[0m |    \\x1b[90m4\\x1b[0m  \\x1b[90m7\\x1b[0m |\\n| \\x1b[90m4\\x1b[0m  \\x1b[90m8\\x1b[0m  \\x1b[90m7\\x1b[0m | \\x1b[90m9\\x1b[0m     \\x1b[90m6\\x1b[0m |       \\x1b[90m5\\x1b[0m |\\n -  -  -  -  -  -  -  -  - \\n| \\x1b[90m3\\x1b[0m  \\x1b[90m4\\x1b[0m  \\x1b[90m6\\x1b[0m | \\x1b[90m5\\x1b[0m     \\x1b[90m9\\x1b[0m |    \\x1b[90m7\\x1b[0m  \\x1b[90m8\\x1b[0m |\\n| \\x1b[90m7\\x1b[0m  \\x1b[90m1\\x1b[0m  \\x1b[90m8\\x1b[0m | \\x1b[90m3\\x1b[0m     \\x1b[90m4\\x1b[0m | \\x1b[90m9\\x1b[0m  \\x1b[90m5\\x1b[0m  \\x1b[90m2\\x1b[0m |\\n|    \\x1b[90m9\\x1b[0m    | \\x1b[90m7\\x1b[0m     \\x1b[90m1\\x1b[0m | \\x1b[90m4\\x1b[0m  \\x1b[90m3\\x1b[0m  \\x1b[90m6\\x1b[0m |\\n'
        """
        value = self.sudoku.values[x][y]
        copy_value = self.copy_sudoku[x][y]
        if self.copy_sudoku[x][y] == 0:
            self.sudoku.values[x][y] = Colors.to_str(
                self.sudoku.values[x][y], color)
        else:
            self.copy_sudoku[x][y] = Colors.to_str(
                self.sudoku.values[x][y], color)
        prefilled_with_blinking_mix = self.show_prefilled_values().replace(
            color.value + "0", color.value + "_")
        self.sudoku.values[x][y] = value
        self.copy_sudoku[x][y] = copy_value
        return prefilled_with_blinking_mix

    def str_to_game(content: list[str], name: str):
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
        game.copy_sudoku = Sudoku._deep_copy(game.sudoku.values)
        game.time_length = Game._decode_time(content[len(content) - 2])
        game.hint_counter = Game._decode_hints(content[len(content) - 1])
        return game

    def _decode_time(content: str) -> int:
        """
        Helper method to decode needed time so far. It is used in str_to_game() method 
        but only takes the string where the hint count is located in instead of the
        whole file content.

        >>> content = 'Needed time: 123 seconds\\n'
        >>> Game._decode_time(content)
        123
        """

        return int(content[len("Needed time: "):content.find("seconds")])

    def _decode_hints(content: str) -> int:
        """ 
        Helper method to decode needed hints. It is used in str_to_game() method 
        but only takes the string where the hint count is located in instead of the
        whole file content.

        >>> content = 'Needed hints: 123'
        >>> Game._decode_hints(content)
        123
        """
        return int(content[len("Needed hints: "):])

    def _get_initial_empty_cell_count(self) -> int:
        """
        Helper method to count all cells in the initial generated value list 'copy_sudoku'
        that were zero hence empty.
        Note that the _count_empty_cells() method is tested in the sudoku class.
        """
        return Sudoku(size=self.sudoku.size, values=self.copy_sudoku)._count_empty_cells()
        
    def _get_current_empty_cell_count(self) -> int:
        """
        Helper method to count all cells in the current sudoku field, that are zero hence empty.
        Note that the _count_empty_cells() method is tested in the sudoku class.
        """
        return self.sudoku._count_empty_cells()

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
        initial_empty_cell_count = self._get_initial_empty_cell_count()
        current_empty_cell_count = self._get_current_empty_cell_count()
        return str(self.name) + ", " + str(self.get_difficulty()) + ", " +\
            str(self.sudoku.grid) + " x " + str(self.sudoku.grid) + \
            ", Progress: " + \
            str(current_empty_cell_count - initial_empty_cell_count) + \
            "/" + str(initial_empty_cell_count)

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
    
    def get_difficulty(self) -> Difficulty:
        """
        Helper method to get the difficulty for the current game.
        Because the difficulty parameter will not be saved neither in game class 
        nor in sudoku class (not necessary), this has to be determined.
        Note that the get_difficulty() method is tested in the sudoku class.
        """
        return self.sudoku.get_difficulty(self._get_initial_empty_cell_count())

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
