######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# Dr. Jakob Prange                   #
# FAI Universität Augsburg           #
# WiSe 2024/25                       #
# Software Assignment                #
######################################

from game import Game
from player import Player

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
        pass

    def load_highscore(self, filename):
        pass

    def add_highscore(self, name, score, scores):
        pass

    def save_highscore(self, scores, filename):
        pass

    def display(self):
        pass

    def frame(self):
        pass

    def wait_for_input(self):
        pass


if __name__ == '__main__':
    '''
    write additional testing code here for things that don't work well as unit tests:
    '''
    ui = UI()
    ...
