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
from game import Game
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


    @staticmethod
    def give_instruction():
        print("Welcome to Sudoku: xxx")  
        
        print("[n] New Game")  
        print("[c] Continue")  
        print("[e] Exit")  


    def display(self, sudoku: Sudoku):
        pass

    def read_input(self):
        s = input()
        if s == "e":
            exit()
        elif s == "n":
            pass
            
        elif s == "c":
            pass


if __name__ == '__main__':


    '''
    write additional testing code here for things that don't work well as unit tests:
    '''
    ui = UI()
    ui.give_instruction()
    while (ui.read_input != )
    ...
