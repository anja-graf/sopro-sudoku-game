######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# Dr. Jakob Prange                   #
# FAI Universität Augsburg           #
# WiSe 2024/25                       #
# Software Assignment                #
######################################

from sudoku import Sudoku
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
        persistance = Persistance("data.json")
        self.current_game = None


    @staticmethod
    def give_instruction():
        print("Hello and Welcome to Sudoku: ")
        print("What do you want to do?")  
        
        print("[n] New Game")  
        print("[c] Continue")  
        print("[i] Instructions")  
        print("[e] Exit")  


    def display(self, sudoku: Sudoku):
        print(self.current_game.__str__())


    def read_input(self):
        s = input()
        if s == "e":
            print("Good bye! See you soon")
            return False
        
        elif s == "n":
            #json file geöffnet bzw eine neue datei erstellt
            self.current_game = Game()
            print("Let's start a new game!\nChoose a username:")
            self.select_username()
            #wenn es den user schon gibt und er ein passwort hat: passwort eingeben
            print("Do you want to add a password? [y] [n]")
            #bei n einfach weiter bei y passwort hinzufügen
            self.select_password()

            print("Which size do you want?")
            self.select_size()

            print("Which difficulty do you want?")
            self.select_difficulty()

        elif s == "c":
            if Persistance.load_game() == None:
                print("Looks like theres no game to continue :(")
            g = Persistance.load_game()
            

        print("Invalid Input, please try again!")
            

    def select_username(self):
        s = input()
        

    def select_password(self):
        s = input

    def select_size():
        s = input()

    def wrong_input():
        pass

    def select_difficulty(self):
        print("[e] : Easy\n[m] : medium\n[h] : hard")
        s = input()
        if s == "e":
            self.current_game.difficulty = Difficulty.EASY
        elif s == "m":
            self.current_game.difficulty = Difficulty.MEDIUM
        elif s == "h":
            self.current_game.difficulty = Difficulty.HARD
            

if __name__ == '__main__':


    '''
    write additional testing code here for things that don't work well as unit tests:
    '''
    ui = UI()
    ui.give_instruction()

    while ui.read_input():
        continue

    ...
