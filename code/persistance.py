import os.path
import json
from collections import defaultdict
from game import Game


class Persistance:
    """This class controlls the saving and loading 
    """
    
    def __init__(self, filename):
        """
        speichert json objekte in einer datei und öffnet diese, falls sie schon existiert
        
        Args:
            filename (str): name der json datei (data.json)
        """
        self.filename = filename
        if os.path.isfile(filename) == True:
            with open(filename) as json_data:
                self.data = json.load(json_data)
        else:
            self.data = defaultdict(dict)      
            


    def save_highscore(self, game, name, score):
        self.data[game.name]["games"]["highscores"].append(score)


    def load_highscore(self):
        highscores = list()
        for name in self.data:
            pass

        return highscores

    def save_game(self, game):
        if bool(self.data[game.name]) == False:
            self.data[game.name]["games"] = list()
        
        self.data[game.name]["games"].append({"finished": game.is_finished()})
        self.data[game.name]["games"].append({"difficulty": game.difficulty()})

        with open(self.filename, "w") as json_data:
            json.dump(self.data, json_data)


    def load_game(self, name) -> list[Game]:
        pass

