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
from colors import Colors
from instructions import Instructions
from os import system, name
import keyboard
import time


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
        self._prefilled = False
        self.persistence = Persistence()
        self.difficulty = Difficulty.EASY
        UI._welcome()
        self.choose_input_options_pre_game()

    def _welcome():
        # TODO Animation maybe
        UI.clear()
        print("Welcome to Sudoku!")

    def _bye(self):
        # TODO Animation maybe
        self.save_game_interaction()
        self.save_highscore(game=self.game)
        print("Congratulations, you finished the sudoku within " + str(self.game.time_length) +
              " seconds using " + str(self.game.hint_counter) + " hints!")
        if input("Do you want to play another sudoku? [y]") != "y":
            print("Okay, bye!")
            exit()
        self.game = Game(ui=self)
        self.choose_input_options_pre_game()
        # TODO Save current game option

    def show_current_state(self, clear: bool = True, modified: str = ...):
        if clear:
            UI.clear()
        print("This is the current game state:")
        if modified is ...:
            if self._prefilled:
                self.show_current_state(
                    modified=self.game.show_prefilled_values())
                print(Colors.to_str(
                    "Note that grey colored numbers were prefilled values", Colors.GREY))
            else:
                print(self.game.get_current_state())
        else:
            print(modified)

    def show_blinking_input_signal():
        # >>> blinking
        pass

    def choose_input_options_pre_game(self):
        user_input = ""
        while True:
            Instructions._show_input_options_pre_game(self.difficulty)
            user_input = input().strip().lower()

            if user_input == "r":
                return Instructions.show_rules()
            elif user_input == "h":
                highscore_list = self.persistence.get_highscores(n=10)
                for name, score in highscore_list:
                    print(f"{name}: {score}")
            elif user_input == "o":
                path = self.get_path(file=True)
                try:
                    self.game = Persistence.load_game(path)
                    self.game.ui = self
                except Exception as e:
                    print(Colors.to_err_str(
                        "This file could not be loaded:" + str(e) + "\n\n"))
                    continue
                self.game.run()
            elif user_input == "p":
                self.player = self.select_user()
            elif user_input == "s":
                pass  # TODO set size like
                # self.game = Game(size=16,ui=self)
                # self.game.run()
            elif user_input == "d":
                self.difficulty = self.select_difficulty()
                self.game = Game(ui=self, difficulty=self.difficulty)
            elif user_input == "n":
                self.game.run()
            else:
                print(Colors.to_err_str(
                    "That was no valid input, please try again!"))
                
    def select_user(self):
        """Selects an existing user or creates a new one.

        This method prompts the user to enter their username. If the username exists,
        the user is logged in and their password is validated. If the username does not exist, 
        a new user is created and the user is prompted to select a password.
        """

        print("Please type in your username")
        player_name = input().strip()
        print(f"Hello {player_name}!")
        if player_name in self.persistence.data["players"]:
            hash = self.input_and_validate_password(player_name)
            player = Player(player_name, password_hash=hash)
            #games_played = len(self.persistence.get_games_for_player(player_name))
            #print(f"Welcome back! You have played: {games_played} games.")
            print(f"Welcome back!")
        else:
            password = self.select_password()
            player = Player(player_name, password=password)
            self.persistence.save_player(player)
            print(f"New player created: {player}")
        return player            


    def input_and_validate_password(self, name):
        """
        Prompts the user to input their password and validates it.

        This method ensures that the user enters the correct password to proceed. 
        If the password is correct, the user is logged in. If the password is incorrect, 
        the user is prompted to try again.

        Args:
            None

        Returns:
            str: Returns a string representation of the password hash if the password is correct, allowing the user to proceed. 
            Keeps prompting the user if the password is incorrect.
        """
        saved_player = self.persistence.get_players()[name]
        if not saved_player.has_password():
            return None
        while True:
                print("Please type in your Password")
                password = input()
                if saved_player.validate_credentials(password):
                    print("You are now logged in")
                    return Player.hash_password(password)
                print("You have typed in the wrong password")

    def select_password(self):
        """Prompts the user to select a password.

        This method asks the user if they want to set a password, and if so,
        prompts them to enter one. If the user does not want a password, an empty string is returned.

        Args:
            None

        Returns:
            str: The user's password, or an empty string if no password is set.
        """
        print("Do you want to add a password?")
        while True:
            print("[y] : Yes \n[n] : No")
            answer = input().strip().lower()
            if answer == "n":
                return None
            print("Please enter you password: ")
            if answer == "y":
                s = input().strip()
                if len(s) <= 0:
                    return None
                return s

    def choose_input_options_during_game(self) -> bool:
        user_input = ""
        while True:
            if user_input == "":  # There has been no error
                Instructions._show_input_options_during_game()
            user_input = input().strip().lower()
            if user_input == "r":
                Instructions.show_rules()
                return True
            elif user_input == "h":
                try:
                    self.show_current_state(
                        modified=self.game.sudoku.show_and_set_hint())
                    self.game.hint_counter += 1
                except Exception:
                    self.show_current_state()
                    print(Colors.to_err_str(
                        "This option should only be used if the sudoku field is solvable. Try out w!"))
                return False
            elif user_input == "c":
                # alternative:
                # x, y = self.get_coordinates()
                # value = self.get_value()
                try:
                    while True:  # All None as return value means escape
                        x, y, value = self.get_coordinates_and_values_through_navigating()
                        if x == None or y == None or value == None:
                            break
                        self._set_value(x, y, value)
                except:
                    print(Colors.to_err_str("You might have to execute the program in a separate console because e.g. visual studio codes' console blocks some ansi escape sequences, such as blinking! \
                        \nAlso, if you have linux operating system you need to execute the program as super user (sudo)\n\n"))
                    exit()
                return True
            elif user_input == "u":
                self._prefilled = not self._prefilled
                return True
            elif user_input == "s":
                self.save_game_interaction()
                print("Goodbye, thanks for playing sudoku!")
                exit()
            elif user_input == "w":
                wrong_fields = self.game.sudoku.show_wrong_fields()
                self.show_current_state(modified=wrong_fields)
                if wrong_fields == self.game.sudoku.__str__():
                    print(Colors.to_right_str("You have no mistakes so far!"))
                # TODO remove all wrong fields functionality maybe
                # TODO print important notes for using
                return False
            else:
                print(Colors.to_err_str(
                    "That was no valid input, please try again!"))

    def save_game_interaction(self):
        name, path = self.get_filename_and_path()
        self.game.name = name
        self.game.time_length += self.game.measure_time_needed()
        Persistence.save_game(self.game, path)
        print("The game [" + name + "] was successfully saved at [" + path + "].")

    def get_coordinates(self) -> tuple[int, int]:
        is_valid = False
        while not is_valid:
            try:
                x = int(input("Type in x coordinate (0-" +
                        str(self.game.sudoku.size - 1) + "):\t ").strip())
                y = int(input("Type in y coordinate (0-" +
                        str(self.game.sudoku.size - 1) + "):\t ").strip())
                if not self.game.sudoku.is_valid_coordinate(x, y):
                    print("Oh no! This coordinate is not valid!")
                elif not Sudoku.is_empty(self.game.copy_sudoku, x, y):
                    print("Oh no! This field is already prefilled!")
                else:
                    is_valid = True
                    return x, y
            except ValueError as ve:
                print("Invalid input: " + ve + ". Please try again.")

    def get_coordinates_and_values_through_navigating(self) -> tuple[int | None, int | None, int | None]:
        """
        This method is for navigating through a sudoku field with arrow keys instead of coordinates
        Note that keyboard module needs to be imported first and on some devices, e.g. Linux the execution requires sudo rights!
        """
        # in the middle the distance to all coordinates is minimal
        x = int(self.game.sudoku.size / 2)
        y = x
        value = None
        ch = error = ''
        while ch != 'esc':
            if self._prefilled:
                self.show_current_state(
                    modified=self.game.show_prefilled_values_with_highlighted_cell(x, y, Colors.BLINKING))
                print(Colors.to_str(
                    "Note that grey colored numbers were prefilled values", Colors.GREY))
            else:
                self.show_current_state(
                    modified=self.game.sudoku.show_blinking_cell(x, y))
            Instructions._show_input_options_during_coordinates_values_input()
            if error != '':
                print(Colors.to_err_str(error))
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
                    return x, y, value
                error = "Oh no! This field is already prefilled!"
            elif ch == 'u':
                self._prefilled = not self._prefilled
            elif ch == 'esc':
                break
            elif ch == 'enter':
                while keyboard.is_pressed("enter"):
                    pass
                pass
            else:
                error = "That was no valid input, please try again!"
            if not self.game.sudoku.is_valid_coordinate(x, y):
                raise Exception("This should never happen!")
        UI.flush()
        return None, None, None

    def get_filename_and_path(self) -> tuple[str, str]:
        """
        This method asks the user if it wants to change the filename or path and in that
        case gets the new name. 
        """
        user_input = ""
        path = Persistence.get_current_dir()
        name = self.game.name
        while user_input != "s":
            Instructions._show_input_options_save_game(name, path)
            user_input = input().strip().lower()
            if user_input == "f":
                name = input("Enter a file name!\n")
            elif user_input == "p":
                path = self.get_path()
        return name, path

    def get_path(self, file: bool = False) -> str:
        """
        This is a helper method to get_filename_and_path(). It gets a filepath from
        the users' input and also checks if it is a valid path.
        If file parameter is set to True, the method checks if it is a valid filepath
        (this excludes e.g. directories), which is important for loading a file.
        """
        s = ""
        if file:
            s = "Enter a file path!\n"
        else:
            s = "Enter a path!\n"
        while True:
            path = input(s)
            if file and Persistence.check_filepath(path):
                return path
            if not file and Persistence.check_path(path):
                return path
            else:
                print(Colors.to_err_str("The path is invalid!"))

    def get_value(self) -> int:
        is_valid = False
        while not is_valid:
            try:
                value = int(input(
                    "Type in the value (1-" + str(self.game.sudoku.size) + ") or 0 to empty it:\t ").strip())
                is_valid = self.game.sudoku.is_valid_value(value)
                if not is_valid:
                    print("Oh no! This value is not valid. Please try again.")
            except ValueError:
                print(
                    "Invalid input. Please enter a number between 1 and 9, or 0 to empty the cell."
                )
        return value

    def _set_value(self, x, y, value) -> bool:
        pre_value = self.game.sudoku.values[x][y]
        self.game.sudoku.set(x, y, value)
        UI.clear()
        if self.game.sudoku.is_valid():
            print(self.game.sudoku.show_and_set_value(
                x, y, value, Colors.GREEN))
            print(Colors.to_right_str("This value is compliant to sudoku rules! Press enter to proceed \
                \n[r]: Revoke new value"))
        else:
            print(self.game.sudoku.show_and_set_value(
                x, y, value, Colors.YELLOW))
            print(Colors.to_may_str("This value violates sudoku rules! \
                \nDo you really want to set it? Press enter to proceed \
                \n[r]: Revoke new value"))
        if input() == "r":
            self.game.sudoku.set(x, y, pre_value)
            print("The value was not set!")
            return False
        print("The value was set successfully!")
        return True

    def display(self):
        print(self.game.sudoku)

    def select_size():
        # TODO
        user_input = input()

    def select_difficulty(self):
        """selects the difficulty

        Returns:
            Difficulty: The difficulty which the user has typed into the console
        """

        print("Select your difficulty:")
        while True:
            print("[e] : Easy")
            print("[m] : Medium")
            print("[h] : Hard")
            s = input().strip().lower()
            if s == "e":
                return Difficulty.EASY
            elif s == "m":
                return Difficulty.MEDIUM
            elif s == "h":
                return Difficulty.HARD
            print("Please select one of [e, m, h]!")

    def save_highscore(self, game):
        self.persistence.save_highscore(self.player, game)

    def clear():
        # print('\x1b[2J')
        # TODO if we want to have a clearing function like this we have to move it to user_interface class

        if name == 'nt':
            system('cls')  # windows
        else:
            system('clear')  # mac and linux, 'posix'

    def flush():
        keyboard.press_and_release('enter')
        input("Press enter to proceed!\n")


        # alternative
        # import sys
        # sys.stdout.flush()
if __name__ == "__main__":

    """
    write additional testing code here for things that don't work well as unit tests:
    """
    ui = UI()
