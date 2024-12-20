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


class Game:
    """
    The game class controls the game flow as well as the Sudoku field and functions as abstract wrapper for it. 
    Note that a few required methods were renamed or put into other classes for better clarity and distribution.
    """

    def __init__(self, size: int = 9, difficulty = Difficulty.EASY):
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
        

    def start_timer():
        """This is a helper method to start a timer a soon as a Game is created."""
        # Anjas TODO Implement
        pass

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

    def step(self) -> bool :
        '''One player input in a Sudoku cell, which is in the default Sudoku a number between 1 and 9. 
        Also the player should have the possibility to erase his own previous inputs. 
        The return value represents if the step was valid and successful.'''
    
    
        # TODO call user-interface function e.g. get_input()
        # that can separate different game choices (hint, own coordinate_input, show wrong fields,...) 
        # It can return a string representing that choice or, what I would prefer, an enumeration value
        hint = input()
        if hint == "h" or hint == "hint":
            self.hint_counter += 1
            Game.clear()
            print(self.sudoku.show_and_set_hint())
            return True
        
        
        # TODO call user-interface function e.g. x,y = get_coordinates() -> int,int 
        # that reads in coordinates and has at least the functionality like following:
        
        is_valid = False
        while not is_valid:
            # TODO outsource improved version of this in user interface class with error handling
            x = int(input("Type in x coordinate!\t"))
            y = int(input("Type in y coordinate!\t"))
            
            if not self.sudoku.is_valid_coordinate(x,y):
                print("Oh no! This coordinate is not valid!")
            elif not Sudoku.is_empty(self.copy_sudoku,x,y):
                print("Oh no! This field is already prefilled!")
            else:
                is_valid = True
                
                
        # TODO call user-interface function e.g. value = get_value() -> int
        # that reads in a value that should be placed in given coordinates
        # and has at least the functionality like following:
                
        is_valid = False
        while not is_valid:
            # TODO outsource improved version of this in user interface class 
            value = int(input("Type in the value or 0 to empty it\t"))
            is_valid = self.sudoku.is_valid_value(value)
            if not is_valid:
                print("Oh no! This value is not valid!")
        self.sudoku.set(x,y,value)
        print("The value was set successfully!")
        
        Game.clear()
        print(self.sudoku.show_and_set_value(x,y,value,Colors.YELLOW))
        return True
        

    def get_current_state(self) -> Sudoku: 
        '''Returns the current Sudoku field of the game session.'''
        return self.sudoku

    def run(self):
        '''Runs a game session interactively until the win condition is reached and the sudoku is fully solved.
        Note that this method should be called from the user_interface. Previously the player 
        should have gotten a welcome and instructions on how to play.
        '''
        Game.clear()
        print("Welcome!") # TODO delete as soon as implemented and call function that prints a welcome instead
        print(self.get_current_state())
        print("Type in 'h' or 'hint' for a hint\t") # TODO print out instructions
        while not self.is_finished():
            self.step()
            print("Type in 'h' or 'hint' for a hint\t") # TODO print out instructions
        print("Congratulations, you finished the sudoku with " + str(self.hint_counter) + " hints!") 
        # TODO delete as soon as implemented
        self.finish_game()
        
    
    def clear():
        # TODO if we want to have a clearing function like this we have to move it to user_interface class
        from os import system, name
        if name == 'nt': system('cls') # windows
        else: system('clear') # mac and linux, 'posix'


if __name__ == "__main__":
    """
    write additional testing code here for things that don't work well as unit tests:
    """
    # Anjas TODO Write Docs and Test
    # Example for how we might test your program:
    game = Game()  # create new game
    game.run()
