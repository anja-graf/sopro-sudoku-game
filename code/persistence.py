import os.path
import json
from collections import defaultdict
from player import Player
from game import Game


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
        if os.path.isfile(filename):
            with open(filename, "r") as json_data:
                self.data = json.load(json_data)
        else:
            self.data = {"users": {}, "games": {}}

    def get_players(self) -> list[Player]:
        """Gets a list of all players.

        Returns:
            list[Player]: List of `Player` instances.
        """
        return [Player.from_dict({"name": name, "data": data}) for name, data in self.data["users"].items()]



    def save_player(self, player: Player):
        """Saves a `Player` instance. Overrides the player if it already exists or creates a new one.

        Args:
            player (Player): The player to save.
        """
        self.data["users"][player.name] = player.to_dict()

        

    def get_games_for_player(self, player_name_: str):
        """Gets all games for a specific player.

        Args:
            player_name (str): The player's name.

        Returns:
            list[Game]: List of `Game` instances.
        """
        return [
            Game.from_dict(game_data)
            for game_name, game_data in self.data["games"].items()
            if game_data["name"] == player_name_
        ]

    def get_game(self, player_name, game_name):
        """Gets a game by player and game name.

        Args:
            player_name (str): The player's name.
            game_name (str): The game's name.

        Returns:
            Game: The requested `Game` instance.
        """
        for game_name_, game_data in self.data["games"].items():
            if game_name_ == game_name and game_data["name"] == player_name:
                return Game.from_dict(game_data)
        return None

    def save_game(self, game: Game):
        """Saves a game.

        Args:
            game (Game): The game that is to be saved.
        """
        self.data["games"][game.name] = game.to_dict()

    def save_to_json(self):
        """Writes all changes of the `data` attribute to the json file.
        """
        with open(self.filename, "w") as json_data:
            json.dump(self.data, json_data)
        

if __name__ == "main":
    per = Persistence("data.json")
    print(per.get_players())

