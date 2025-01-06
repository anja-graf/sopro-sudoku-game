######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# Dr. Jakob Prange                   #
# FAI Universität Augsburg           #
# WiSe 2024/25                       #
# Software Assignment                #
######################################

from sudoku import *
from game import *
from player import Player
from persistence import Persistence


class UI:
    """
    Class for any inputs and outputs.

    User controls must be implemented in this class!
    """

    def __init__(self):
        """
        Creates a new user interface. Think about which pieces of information you need at this time
        (e.g. players, game mode, time limit, ...) and add them as arguments.
        """
        self.game = Game(ui=self)
        self.player = None
        UI._welcome()
        self.choose_input_options_pre_game()

    def _welcome():
        # TODO Animation maybe
        UI.clear()
        print("Welcome to Sudoku!")
        
    def _bye(self):
        # TODO Animation maybe
        print("Congratulations, you finished the sudoku within " + str(self.game.time_length) +" seconds using " + str(self.game.hint_counter) + " hints!") 
        # TODO Save current game option

    def select_user(self):
        """selects the user, with or without a password
        """

        print("Who are you?")
        user_input = input().strip()
        self.name = s
        print("Hello" + s)
        if user_input in self.persistence.data:
            print(
                "Welcome back\nYou have played: "
                + len(self.persistence.data[s])
                + " Games"
            )
            # wenn passwort vorhanden, eingeben
        else:
            print("Welcome " + s)
            self.persistence.data[s]
            self.password = self.select_password()
            self.player = Player(self.name, self.password)

    def select_game(self):
        
        print("What do you want to do?")
        while True:
            print("[n] New Game")
            print("[c] Continue")
            print("[e] Exit")
            user_input = input().strip().lower()
            if user_input == "e":
                print("Good bye! See you soon")
                return False

            elif user_input == "n":
                # json file geöffnet bzw eine neue datei erstellt
                self.persistence = Persistence("data.json")

                print("Which size do you want?")
                self.size = self.select_size()

                print("Which difficulty do you want?")
                self.difficulty = self.select_difficulty()

                self.game = Game(size=self.size, difficulty=self.difficulty)

            elif user_input == "c":
                if Persistence.load_game() == None:
                    print("Looks like theres no game to continue :(")
                g = Persistence.load_game()
                #?

            print("Invalid Input, please try again!")

    def show_current_state(self,clear:bool = True, modified:str = ...):
        if clear:
            UI.clear()
        print("This is the current game state:")
        if modified is ...:
            print(self.game.get_current_state())
        else:
            print(modified)

    def _show_input_options_pre_game():
        #TODO implement input given game
        print("The following are all the input options before the game:\
            \n[n]: Start a new sudoku game \
            \n[d]: Set the difficulty (easy, medium, hard). The default is easy.\
            \n[s]: Set size of sudoku. The default is 9.\
            \n[p]: Set player. \
            \n[o]: Open game from file. \
            \n[h]: Show all high scores \
            \n[r]: Show rules of sudoku \
            \n-------------------------------------------------------------------------------")

    def _show_input_options_during_game():
        print("The following are all the input options during the game:\
            \n[r]: Show rules of sudoku \
            \n[h]: Give me a hint \
            \n[c]: Type in new value at specified coordinates \
            \n[w]: Show wrong fields \
            \n[s]: Save the game and quit \
            \n-------------------------------------------------------------------------------")
    
    def _show_input_options_during_coordinates_values_input():
        print("Please navigate to the desired field (by pressing arrow keys ↑,↓,→,←) and enter the number (1-9) you want to fill in. Your cursor is at the blinking cell.\
            \nTo empty a cell enter 0.\
            \nTo leave this menu enter escape key.\
            \n-------------------------------------------------------------------------------")
    
    def _show_input_options_save_game(name:str,path:str):
        print("[s]: Save the game and quit \
            \n[f]: Change the current filename [" + str(name) + "] \
            \n[p]: Change the current filepath [" + str(path) + "] \
            \n-------------------------------------------------------------------------------")
    
    def show_blinking_input_signal():
        # >>> blinking
        pass

    def choose_input_options_pre_game(self):
        while True:
            UI._show_input_options_pre_game()
            user_input = input().strip().lower()

            if user_input == "r":
                return UI.show_rules()
            elif user_input == "h":
                pass #TODO show high scores
            elif user_input == "o":
                path = self.get_path(file=True)
                try:
                    self.game = Persistence.load_game(path)
                    self.game.ui = self
                except Exception as e:
                    #TODO not here but in separated colors class
                    print(Colors.RED.value + "This file could not be loaded:" + str(e) + Colors.END.value + "\n\n")
                    continue
                self.game.run()
            elif user_input == "p":
                pass #TODO set player
            elif user_input == "s":
                pass #TODO set size like 
                #self.game = Game(size=16,ui=self)
                #self.game.run()
            elif user_input == "d":
                pass #TODO set difficulty
            elif user_input == "n":
                self.game.run()
            else:
                print("Not a valid input!")
    
    def choose_input_options_during_game(self) -> bool:
        while True:
            UI._show_input_options_during_game()
            user_input = input().strip().lower()
            if user_input == "r":
                UI.show_rules()
                return True
            elif user_input == "h":
                try:
                    self.show_current_state(modified=self.game.sudoku.show_and_set_hint())
                    self.game.hint_counter += 1
                except Exception:
                    self.show_current_state()
                    #Colors
                    print("This option should only be used if the sudoku field is solvable. Try out w!")
                return False
                pass #TODO give hint
            elif user_input == "c":
                #TODO coordinates input
                # alternative:
                # x, y = self.get_coordinates()
                # value = self.get_value()
                try:
                    while True: # All None as return value means escape
                        x,y,value = self.get_coordinates_and_values_through_navigating()
                        if x == None or y == None or value == None: break
                        self._set_value(x,y,value)
                except Exception as e:
                    print(e)
                    #TODO not here but in separated colors class
                    print(Colors.RED.value + "You might have to execute the program in a separate console because e.g. visual studio codes' console blocks some ansi escape sequences, such as blinking! \
                          \nAlso, if you have linux operating system you need to execute the program as super user (sudo)" + Colors.END.value + "\n\n")
                    continue
                return True
            elif user_input == "s":
                # TODO give option to select filename and path
                name, path = self.get_filename_and_path()
                self.game.name = name
                self.game.time_length += self.game.measure_time_needed()
                Persistence.save_game(self.game,path)
                print("The game [" + name + "] was successfully saved at [" + path + "]. \
                    \nGoodbye, thanks for playing sudoku!")
                exit()
            elif user_input == "w":
                wrong_fields = self.game.sudoku.show_wrong_fields()
                self.show_current_state(modified=wrong_fields)
                if wrong_fields == self.game.sudoku.__str__():
                    print(Colors.GREEN.value + "You have no mistakes so far!" + Colors.END.value)
                #TODO remove wrong fields functionality maybe
                #TODO print important notes for using
                return False
            else:
                print(str(user_input) + " is not a valid input!")

    def get_coordinates(self) -> tuple[int,int]:
        is_valid = False
        while not is_valid:
            try:
                x = int(input("Type in x coordinate (0-" + str(self.game.sudoku.size - 1) +"):\t ").strip())
                y = int(input("Type in y coordinate (0-" + str(self.game.sudoku.size - 1) +"):\t ").strip())
                if not self.game.sudoku.is_valid_coordinate(x, y):
                    print("Oh no! This coordinate is not valid!")
                elif not Sudoku.is_empty(self.game.copy_sudoku, x, y):
                    print("Oh no! This field is already prefilled!")
                else:
                    is_valid = True
                    return x, y
            except ValueError as ve:
                print("Invalid input: " + ve + ". Please try again.")

    def get_coordinates_and_values_through_navigating(self) -> tuple[int | None,int | None,int | None]:
        # This is a sketch for navigating through a sudoku field with arrow keys instead of coordinates
        # Note that keyboard module needs to be imported first and on some devices, e.g. Linux the execution requires sudo rights!

        import keyboard
        import time

        x = int(self.game.sudoku.size / 2) # in the middle the distance to all coordinates is minimal
        y = x
        value = None
        ch = error = ''
        while ch != 'esc':
            self.show_current_state(modified=self.game.sudoku.show_blinking_cell(x,y))
            UI._show_input_options_during_coordinates_values_input()
            if error != '':
                print(Colors.RED.value + error + Colors.END.value)
            error = ''
            ch = keyboard.read_key()
            time.sleep(0.2)
            if ch == 'right':
                y = (y + 1) % self.game.sudoku.size
            elif ch == 'left':
                y = (y - 1) % self.game.sudoku.size
            elif ch == 'up':
                x = (x - 1) % self.game.sudoku.size
            elif ch == 'down':
                x = (x + 1) % self.game.sudoku.size
            elif len(ch) == 1 and ch.isdigit():
                if Sudoku.is_empty(self.game.copy_sudoku, x, y):
                    value = int(ch)
                    UI.flush()
                    return x,y,value
                error = "Oh no! This field is already prefilled!"
            elif ch == 'esc':
                break
            elif ch == 'enter':
                while keyboard.is_pressed("enter"):
                    pass
                pass
            else:
                error = "That was no valid input, please try again!"
            if not self.game.sudoku.is_valid_coordinate(x,y): 
                raise Exception("This should never happen!")
        UI.flush()
        return None,None,None
        
    def get_filename_and_path(self) -> tuple[str,str]:
        #TODO Docstring
        user_input = ""
        path = Persistence.get_current_dir()
        name = self.game.name
        while user_input != "s":
            UI._show_input_options_save_game(name,path)
            user_input = input().strip().lower()
            if user_input == "f":
                name = input("Enter a file name!\n")
            elif user_input == "p":
                path = self.get_path()
        return name,path

    def get_path(self,file=False) -> str:
        s = ""
        if file: s = "Enter a file path!\n"
        else: s = "Enter a path!\n"
        while True:
            path = input(s)
            if file and Persistence.check_filepath(path): return path
            if not file and Persistence.check_path(path): return path
            else: print("The path is invalid!")

    def get_value(self) -> int:
        is_valid = False
        while not is_valid:
            try:
                value = int(input("Type in the value (1-" + str(self.game.sudoku.size) +") or 0 to empty it:\t ").strip())
                is_valid = self.game.sudoku.is_valid_value(value)
                if not is_valid:
                    print("Oh no! This value is not valid. Please try again.")
            except ValueError:
                print(
                    "Invalid input. Please enter a number between 1 and 9, or 0 to empty the cell."
                )
        return value        
        
    def _set_value(self,x,y,value) -> bool:
        pre_value = self.game.sudoku.values[x][y]
        self.game.sudoku.set(x, y, value)
        UI.clear()
        if self.game.sudoku.is_valid():
            print(self.game.sudoku.show_and_set_value(x, y, value, Colors.GREEN))
            print(Colors.GREEN.value + "This value is compliant to sudoku rules! \
                \nType in enter to proceed! Press enter to proceed\
                \n[r]: Revoke new value" + Colors.END.value)
        else:
            print(self.game.sudoku.show_and_set_value(x, y, value, Colors.YELLOW))
            print(Colors.YELLOW.value + "This value violates sudoku rules! \
                \nDo you really want to set it? Press enter to proceed\
                \n[r]: Revoke new value" + Colors.END.value)
        if input() == "r": 
            self.game.sudoku.set(x,y,pre_value)
            print("The value was not set!")        
            return False
        print("The value was set successfully!")
        return True

    def show_rules():
        print("Sudoku is a number puzzle played normally on a 9x9 grid, which is divided into 9 smaller 3x3 subgrids. The objective is to fill the grid with numbers from 1 to 9, following three main rules: \
            \n- Row Rule: Each row must contain all the numbers from 1 to 9 without repetition. \
            \n- Column Rule: Each column must also contain all the numbers from 1 to 9 without repetition. \
            \n- Subgrid Rule: Each of the nine 3x3 subgrids must contain all the numbers from 1 to 9 without repetition. \
            \nThe puzzle starts with some numbers already filled in, and the goal is to complete the grid while adhering to these rules.")
        input("Type in enter to proceed!\n")

    def display(self):
        print(self.game.sudoku)

    def select_password(self):
        print("Do you want to add a Password?")
        while True:
            print("[y] : Yes [n] : No")
            answer = input().strip().lower()
            if answer == "n":
                return ""
            print("Please enter you password: ")
            if answer == "y":
                user_input = input()
                return s

    def select_size():
        #TODO 
        user_input = input()


    def select_difficulty(self):
        """selects the difficulty

        Returns:
            Difficulty: the difficulty which the user has typed into the consol
        """

        print("Select your difficulty")
        while True:
            print("[e] : Easy\n[m] : medium\n[h] : hard")
            user_input = input().strip().lower()
            if user_input == "e":
                return Difficulty.EASY
            elif user_input == "m":
                return Difficulty.MEDIUM
            elif user_input == "h":
                return Difficulty.HARD
            print("Please select one of [e, m, h]!")


    def clear():
        #print('\x1b[2J')
        # TODO if we want to have a clearing function like this we have to move it to user_interface class
        from os import system, name
        if name == 'nt': system('cls') # windows
        else: system('clear') # mac and linux, 'posix'

    def flush():
        import keyboard
        keyboard.press_and_release('enter')
        input("Type in enter to proceed!\n")
        # import sys
        # sys.stdout.flush()
if __name__ == "__main__":

    """
    write additional testing code here for things that don't work well as unit tests:
    """
    ui = UI()