import os.path
import json
from collections import defaultdict
from player import Player
from game import Game
from sudoku import *
import datetime as dt


class Persistence:
    """This class controls the saving and loading 
    """

    def __init__(self, filename="user-data.json"):
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
        if not "players" in self.data:
            self.data["players"] = dict()
        if not "highscores" in self.data:
            self.data["highscores"] = []

    def get_players(self):
        """Gets a dict of all players.

        Returns:
            dict: A dictionary of player names (str) to `Player` instances.
        """
        return {name: Player.from_dict({"name": name, "password_hash": hash}) for name, hash in self.data["players"].items()}

    def save_player(self, player: Player):
        """Saves a `Player` instance. Either overrides the player if it already exists, or creates a new one.

        Args:
            player (Player): The player which is to be saved.
        """
        new_player_dict = player.to_dict()
        name = new_player_dict["name"]
        hash = new_player_dict["password_hash"]
        self.data["players"][name] = hash
        self._save_to_json()

    @staticmethod
    def save_game(game: Game, path: str=""):
        """Saves a game.

        Args:
            game (Game): The game that is to be saved.
        """
        filename = "Sudoku Game " + str(dt.datetime.now()).replace(':','-')
        with open(os.path.join(path,filename),"w") as f:
            content = "Sudoku Game from " + str(dt.datetime.now())
            if game.ui.player is not None:
                content += ", played by " + game.ui.player.name    
            content += str(game)
            f.write(content)
    
    @staticmethod
    def load_game(path: str) -> Game:
        #TODO Tests and Docstring, maybe validation code that checks if anything was manipulated
        with open(path,"r") as f:
            content = list(f)
            game = Game.str_to_game(content,os.path.basename(path))
            if "played by" in content[0]:
                pass # TODO Player implementation
        return game

    def save_to_json(self):
        """Writes all changes of the `data` attribute to the json file.
        """
        with open(self.filename, "w") as json_data:
            json.dump(self.data, json_data)

    def save_highscore(self, user, game):
        """ Saves highscore into the highscore file after finishing the game
        """
        name = user.name if user is not None else "No logged in player"
        highscore_dict = {
            "player": name,
            "score": Persistence._get_score(game),
            "difficulty": game.get_difficulty().name,
            "hints": game.hint_counter,
            "time": game.time_length
        }
        self.data["highscores"].append(highscore_dict)
        self._save_to_json()

    def get_highscores(self, n):
        """Returns a list of the highscores
        """
        highscore_list = [(highscore["player"], highscore["score"]) for highscore in self.data["highscores"]]
        highscore_list = sorted(highscore_list, key=lambda x: x[1])
        if n < len(highscore_list):
            highscore_list = highscore_list[:n]
        return highscore_list

    def check_path(path:str) -> bool:
        return os.path.exists(path) and os.path.isdir(path)
    
    def check_filepath(path:str) -> bool:
        return os.path.exists(path) and os.path.isfile(path)

    def get_current_dir() -> str:
        return os.getcwd()

    def _save_to_json(self):
        """Writes all changes of the `data` attribute to the json file.
        """
        with open(self.filename, "w") as data_file:
            json.dump(self.data, data_file, indent=4)
        
    def _get_score(game, base_difficulty_value=500, hint_penalty=100):
        score = base_difficulty_value * game.get_difficulty().value
        score -= game.time_length
        score -= hint_penalty * game.hint_counter
        score = 0 if score <= 0 else score
        return score
