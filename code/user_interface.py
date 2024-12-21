######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# Dr. Jakob Prange                   #
# FAI Universität Augsburg           #
# WiSe 2024/25                       #
# Software Assignment                #
######################################

from sudoku import Sudoku, Difficulty
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
        
        self.persistance = Persistance("data.json")
        self.current_game = None
        self.name = ""
        self.password = ""

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
            

    @staticmethod
    def give_instruction():
        pass
        
        

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
