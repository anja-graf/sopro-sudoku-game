######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# Dr. Jakob Prange                   #
# FAI Universität Augsburg           #
# WiSe 2024/25                       #
# Software Assignment                #
######################################

from sudoku import Sudoku, Difficulty, Colors
from game import Game
from player import Player
from persistence import Persistence


class UI:
    """
    Class for user interface handling inputs and outputs for the Sudoku game.

    This class handles user interactions such as selecting a user, starting a game, 
    inputting coordinates and values for the game, and providing instructions.
    """

    def __init__(self):
        """
        Creates a new user interface. Think about which pieces of information you need at this time
        (e.g. players, game mode, time limit, ...) and add them as arguments.
        """
        self.persistence = Persistence()
        self.current_game = None
        self.player = self.select_user()
        self.game = self.select_game()

    def select_user(self):
        """Selects an existing user or creates a new one.

        This method prompts the user to enter their username. If the username exists,
        the user is logged in and their password is validated. If the username does not exist, 
        a new user is created and the user is prompted to select a password.
        """

        print("Hello and Welcome to Sudoku: ")
        print("Who are you?")
        player_name = input().strip()
        print(f"Hello {player_name}!")
        if player_name in self.persistence.data["users"]:
            hash = self.input_and_validate_password(player_name)
            player = Player(player_name, password_hash=hash)
            games_played = len(self.persistence.get_games_for_player(player_name))
            print(f"Welcome back! You have played: {games_played} games.")
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
                    return Player.get_password_hash(password)
                print("You have typed in the wrong password")

    def select_game(self):
        """
        Allows the user to select the type of game action they want to perform.

        This method provides the user with options to start a new game, 
        continue an existing game, or exit. Depending on the user's choice, 
        the game will either start a new game, load an existing game, or exit the application.

        Args:
            None

        Returns:
            bool: Returns `False` if the user exits the game, and `None` otherwise.
        """
        
        print("What do you want to do?")
        while True:
            print("[n] New Game")
            print("[c] Continue")
            print("[e] Exit")
            s = input().strip().lower()
            if s == "e":
                print("Good bye! See you soon")
                exit()

            elif s == "n":
                print("Which size do you want?")
                size = self.select_size()
                print("Which difficulty do you want?")
                difficulty = self.select_difficulty()
                game = Game(size=size, difficulty=difficulty)
                return game

            elif s == "c":
                # TODO:
                # Game braucht: Namen
                # Game braucht: __str__ Methode, die Spielnamen, Difficulty, Size und Fortschritt (also z.B. 15/42 Zahlen eingefuegt) ausgibt
                # Beispiel:
                # [0]: myfirstgame, Easy, 9x9, Progress: 10/42
                # [1]: mysecondgame, Medium, 4x4, Progress: 1/3
                # [2]: blahblahgame, Hard, 16x16, Progress: 0/123
                possible_games = self.persistence.get_games_for_player(self.player.name)
                if len(possible_games) == 0:
                    print("You do not have any open games!")
                    continue
                print("You have the following open games:")
                for i, game in enumerate(possible_games):
                    print(f"  [{i}]: {game}")
                n = int(input().strip())
                print()
                print("Please give the number of the game you want to continue:")
                while n not in range(len(possible_games)):
                    print("Please give one of the provided game numbers!")
                    n = int(input().strip())
                return possible_games[n]
            print("Invalid input, please try again!")

    def choose_input(self):
        """_summary_

        Returns:
            str: the input as a string (i, h, p, w, s, c, e)
            h, w, s should be handled in game class
            i, p, c, e is handled in ui class
        """

        print("What do you want to do?")
        while True:
            print("[i]: Show Instructions")
            print("[h]: Give me a Hint")
            print("[p]: Play the game and type in Coordinates and Value for Input")
            print("[w]: Show wrong fields")
            print("[s]: Show Highscores")
            print("[c]: Clear the terminal")
            print("[e]: Exit the game")
            s = input().strip().lower()

            if s == "i":
                self.give_instruction()
                return s
            
            elif s == "h":
                return s
                
            elif s == "p":
                x, y = self.input_coordinates()
                self.input_value(x, y)
                return s

            elif s == "w":
                return s

            elif s == "s":
                return s

            elif s == "c":
                from os import system, name

                if name == "nt":
                    system("cls")  # windows
                else:
                    system("clear")  # mac and linux, 'posix'
                return s    

            elif s == "e":
                print("Good bye! See you soon")
                return s

            else:
                print("Not a valid input!")

    def input_coordinates(self):

        """
        Prompts the user to input the coordinates for a Sudoku cell.

        This method ensures that the coordinates entered by the user are valid 
        (within the grid range and the cell is not prefilled).

        Args:
            None

        Returns:
            tuple: A tuple `(x, y)` representing the coordinates chosen by the user.
        """

        is_valid = False
        while not is_valid:
            try:
                x = int(input("Type in x coordinate (0-8): ").strip())
                y = int(input("Type in y coordinate (0-8): ").strip())
                if not self.current_game.sudoku.is_valid_coordinate(x, y):
                    print("Oh no! This coordinate is not valid!")
                elif not Sudoku.is_empty(self.copy_sudoku, x, y):
                    print("Oh no! This field is already prefilled!")
                else:
                    is_valid = True
                    return x, y
            except ValueError as ve:
                print("Invalid input: " + ve + ". Please try again.")

    def input_value(self, x, y):
        """
    Prompts the user to input a value for the specified coordinates.

    This method ensures that the value entered by the user is valid 
    (a number between 1 and 9, or 0 to clear the cell). If valid, the value is set in the Sudoku grid.

    Args:
        x (int): The x-coordinate of the Sudoku cell.
        y (int): The y-coordinate of the Sudoku cell.

    Returns:
        bool: `True` if the value was successfully set, otherwise continues prompting the user.
    """    

        is_valid = False
        while not is_valid:
            try:
                value = int(input("Type in the value (1-9) or 0 to empty it: ").strip())
                if self.current_game.sudoku.is_valid_value(value):
                    self.current_game.sudoku.set(x, y, value)
                    print("The value was set successfully!")
                    Game.clear()
                    print(
                        self.current_game.sudoku.show_and_set_value(
                            x, y, value, Colors.YELLOW
                        )
                    )
                    return True
                else:
                    print("Oh no! This value is not valid. Please try again.")
            except ValueError:
                print(
                    "Invalid input. Please enter a number between 1 and 9, or 0 to empty the cell."
                )

    @staticmethod
    def give_instruction():
        """Prints the instructions on how to play Sudoku.
        This static method provides a summary of the rules and gameplay for Sudoku.
        """

        print("Instructions:")
        print("How to play Sudoku:")
        print("Sudoku has a 9x9 grid, divided into 9 smaller 3x3 boxes.")
        print(
            "Fill the grid so each row, column, and 3x3 box contains the numbers 1 through 9 without repetition."
        )
        print("A number can appear only once in each row.")
        print("A number can appear only once in each column.")
        print("A number can appear only once in each 3x3 box.\n")

    def display(self):
        """Displays the current Sudoku grid.
            This method prints the current state of the Sudoku grid to the console.
        """
        print(self.current_game.sudoku)

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
            print("[y] : Yes [n] : No")
            answer = input().strip().lower()
            if answer == "n":
                return None
            print("Please enter you password: ")
            if answer == "y":
                s = input().strip()
                if len(s) <= 0:
                    return None
                return s

    def select_size(self):
        """selects the size

        Returns:
            Size: Has to be a Square Number
        """
        print("Do you want to play with a different size than 9?")
        print("[y]: Yes")
        print("[n]: No")
        s = input().strip().lower()
        if s == "n":
            return 9
        
        while True:
            print("Please type in a positive square number to play with this size:")
            s = int(input().strip())
            if s > 1 and (s ** 0.5).is_integer():
                return s
            print("Please type in a positive square number")


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


if __name__ == "__main__":

    """
    write additional testing code here for things that don't work well as unit tests:
    """
    ui = UI()
