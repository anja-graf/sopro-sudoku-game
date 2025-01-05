######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# Dr. Jakob Prange                   #
# FAI Universität Augsburg           #
# WiSe 2024/25                       #
# Software Assignment                #
######################################

from sudoku import *
from game import Game
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
        self.current_game = None
        self.player = None
        UI._welcome()
        UI.choose_input_options_pre_game()

    def _welcome():
        # TODO Animation maybe
        print("Welcome to Sudoku!")

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

    def _show_input_options_pre_game():
        print("The following are all the input options before the game:\
            \n[n]: Start a new sudoku game \
            \n[d]: Set the difficulty (easy, medium, hard). The default is hard.\
            \n[s]: Set size of sudoku. The default is 9.\
            \n[p]: Set player. \
            \n[o]: Open game from file. \
            \n[h]: Show all high scores \
            \n[r]: Show rules of sudoku \
            ")

    def _show_input_options_during_game(self):
        print("The following are all the input options during the game:\
            \n[r]: Show rules of sudoku \
            \n[h]: Give me a Hint \
            \n[c]: Type in Coordinates and value for Input \
            \n[w]: Show wrong fields \
            \n[s]: Save the game")

    def choose_input_options_pre_game():
        while True:
            UI._show_input_options_pre_game()
            user_input = input().strip().lower()

            if user_input == "r":
                return UI.show_rules()
            elif user_input == "h":
                pass #TODO show high scores
            elif user_input == "o":
                pass #TODO open game from file
            elif user_input == "p":
                pass #TODO set player
            elif user_input == "s":
                pass #TODO set size
            elif user_input == "d":
                pass #TODO set difficulty
            elif user_input == "n":
                pass #TODO start new game
            else:
                print("Not a valid input!")
    
    def _show_input_options_during_game():
        while True:
            UI._show_input_options_during_game()
            user_input = input().strip().lower()
            
            if user_input == "r":
                return UI.show_rules()
            elif user_input == "h":
                pass #TODO give hint
            elif user_input == "c":
                #TODO coordinates input
                x, y = UI.input_coordinates()
                UI.input_value(x, y)
                return user_input
            elif user_input == "s":
                pass #TODO save game
            elif user_input == "w":
                pass #TODO show wrong fields
            else:
                print("Not a valid input!")

    def input_coordinates(self):
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

    def show_rules():
        print("Sudoku is a number puzzle played normally on a 9x9 grid, which is divided into 9 smaller 3x3 subgrids. The objective is to fill the grid with numbers from 1 to 9, following three main rules: \
            \n- Row Rule: Each row must contain all the numbers from 1 to 9 without repetition. \
            \n- Column Rule: Each column must also contain all the numbers from 1 to 9 without repetition. \
            \n- Subgrid Rule: Each of the nine 3x3 subgrids must contain all the numbers from 1 to 9 without repetition. \
            \nThe puzzle starts with some numbers already filled in, and the goal is to complete the grid while adhering to these rules.")


    def display(self):
        print(self.current_game.sudoku)

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


if __name__ == "__main__":

    """
    write additional testing code here for things that don't work well as unit tests:
    """
    ui = UI()
    UI.show_rules()
