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

    def get_players(self) -> list[Player]:
        """Get a list of all players

        Returns:
            list[Player]: List of `Player` instances
        """
        return [Player.from_dict(player_dict) for player_dict in self.data["players"]]

    def save_player(self, player: Player):
        """Saves a `Player` instance. Either overrides the player if it already exists, or creates a new one.

        Args:
            player (Player): The player which is to be saved.
        """
        new_player_dict = player.to_dict()
        replaced = False
        for i, p in enumerate(self.data["players"]):
            if p["name"] == player.name:
                self.data["players"][i] = new_player_dict
                replaced = True
                break

        if replaced == False:
            self.data["players"].append(new_player_dict)

    def get_games_for_player(self, player_name_: str):
        """Gets all games for a player.

        Args:
            player_name (str): The players name.
        """
        pass

    def get_game(self, player_name, game_name):
        """Gets a game by player and game name.
        """
        pass

    def save_game(game: Game, path:str=""):
        """Saves a game.

        Args:
            game (Game): The game that is to be saved.
        """
        if game.name is None:
            game.name = "Sudoku Game " + str(dt.datetime.now())
        with open(os.path.join(path,game.name),"w") as f:
            content = "Sudoku Game from " + str(dt.datetime.now())
            if game.player is not None:
                content += ", played by " + game.player.name    
            content += str(game)
            f.write(content)
    
    def load_game(path:str) -> Game:
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
        pass
    
    def check_path(path:str) -> bool:
        return os.path.exists(path) and os.path.isdir(path)
    
    def check_filepath(path:str) -> bool:
        return os.path.exists(path) and os.path.isfile(path)

    def get_current_dir() -> str:
        return os.getcwd()
