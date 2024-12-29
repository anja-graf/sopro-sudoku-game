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
from persistance import Persistance


class UI:
    '''
    Class for any inputs and outputs.

    User controls must be implemented in this class!
    '''

    def __init__(self):
        '''
        Creates a new user interface. Think about which pieces of information you need at this time
        (e.g. players, game mode, time limit, ...) and add them as arguments.
        '''
        self.sudoku = Sudoku()
        self.persistance = None
        self.current_game = None
        self.name = ""
        self.password = ""
        self.x_coordinate = 0
        self.y_coordinate = 0
        

    def select_user(self):
        print("Hello and Welcome to Sudoku: ")
        print("Who are you?")  
        s = input().strip()
        self.name = s
        print("Hello" + s)
        if s in self.persistance.data:
            print("Welcome back\nYou have played: " + len(self.persistance.data[s]) + " Games")
            #wenn passwort vorhanden, eingeben
        else:
            print("Welcome " + s)
            self.persistance.data[s]
            self.password = self.select_password()
            self.player = Player(self.name, self.password)
            
        
    def select_game(self):
        print("What do you want to do?")
        while True:
            print("[n] New Game")  
            print("[c] Continue") 
            print("[e] Exit")  
            s = input().strip().lower()
            if s == "e":
                print("Good bye! See you soon")
                return False
        
            elif s == "n":
            #json file geöffnet bzw eine neue datei erstellt
                self.persistance = Persistance("data.json")

                print("Which size do you want?")
                self.size = self.select_size()

                print("Which difficulty do you want?")
                self.difficulty = self.select_difficulty()
                
                self.game = Game(size=self.size, difficulty=self.difficulty)

            elif s == "c":
                if Persistance.load_game() == None:
                    print("Looks like theres no game to continue :(")
                g = Persistance.load_game()
            

            print("Invalid Input, please try again!")
            

    def choose_input(self):
        print("What do you want to do?")
        #Coordinate Input, Instruction, Hint, Show wrong fields, Leave Game, Show Highscores
        while True:
            print("[i]: Show Instructions")
            print("[h]: Give me a Hint")
            print("[p]: Play the game and type in Coordinates and Value for Input")
            print("[w]: Show wrong fields")
            print("[h]: Show Highscores")
            print("[c]: Clear the terminal")
            print("[e]: Exit the game")
            s = input().strip().lower()

            if s == "i":
                self.give_instruction()

            elif s == "h":
                pass
            elif s == "p":
                self.input_coordinates()

            elif s == "w":   
                pass

            elif s == "h":
                pass

            elif s == "c":
                from os import system, name
                if name == 'nt': system('cls') # windows
                else: system('clear') # mac and linux, 'posix'

            elif s == "e":
                print("Good bye! See you soon")
                return False
            
            else:
                print("Not a valid input!")


    def input_coordinates(self):
        is_valid = False
        while not is_valid:
            try:
                x = int(input("Type in x coordinate (0-8): ").strip())
                y = int(input("Type in y coordinate (0-8): ").strip())
                if not (0 <= x < 9 and 0 <= y < 9):
                    raise ValueError("Coordinates must be between 0 and 8.")
                if not self.sudoku.is_valid_coordinate(x, y):
                    print("Oh no! This coordinate is not valid!")
                elif not Sudoku.is_empty(self.copy_sudoku, x, y):
                    print("Oh no! This field is already prefilled!")
                else:
                    self.x_coordinate = x
                    self.y_coordinate = y
                    is_valid = True
            except ValueError as ve:
                print("Invalid input: "+ ve +". Please try again.")
            


    def input_value(self):
        is_valid = False
        while not is_valid:
            try:
                value = int(input("Type in the value (1-9) or 0 to empty it: ").strip())
                if value == 0 or self.sudoku.is_valid_value(value):
                    self.sudoku.set(self.x_coordinate, self.y_coordinate, value)
                    print("The value was set successfully!")
                    Game.clear()
                    print(self.sudoku.show_and_set_value(self.x_coordinate, self.y_coordinate, value, Colors.YELLOW))
                    return True
                else:
                    print("Oh no! This value is not valid. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9, or 0 to empty the cell.")
            



    @staticmethod
    def give_instruction():
        print("Instrutions:")
        print("How to play Sudoku:")
        print("Sudoku has a 9x9 grid, divided into 9 smaller 3x3 boxes.")
        print("Fill the grid so each row, column, and 3x3 box contains the numbers 1 through 9 without repetition.")
        print("A number can appear only once in each row.")
        print("A number can appear only once in each column.")    
        print("A number can appear only once in each 3x3 box.\n")  
    
        

    def display(self, sudoku: Sudoku):
        print(self.current_game.__str__())

    

    def select_password(self):
        print("Do you want to add a Password?")
        while True:
            print("[y] : Yes [n] : No")
            answer = input().strip().lower()
            if answer == "n":
                return ""
            print("Please enter you password: ")
            if answer == "y":
                s = input()
                return s
        

    def select_size():
        s = input()

    def select_difficulty(self):
        print("Selelect your difficulty")
        while True:
            print("[e] : Easy\n[m] : medium\n[h] : hard")
            s = input().strip().lower()
            if s == "e":
                return Difficulty.EASY
            elif s == "m":
                return Difficulty.MEDIUM
            elif s == "h":
                return Difficulty.HARD
            print("Please select one of [e, m, h]!")
            

if __name__ == '__main__':


    '''
    write additional testing code here for things that don't work well as unit tests:
    '''
    ui = UI()
    ui.select_user()
    

    ...
