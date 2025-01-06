import os.path
import json
from player import Player
from game import Game


class Persistence:
    """This class controls the saving and loading 
    """

    def __init__(self, filename=os.path.join("code", "data.json")):
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

    def get_players(self):
        """Gets a dict of all players.

        Returns:
            dict: A dictionary of player names (str) to `Player` instances.
        """
        return {name: Player.from_dict({"name": name, "password_hash": hash}) for name, hash in self.data["users"].items()}

    def save_player(self, player: Player):
        """Saves a `Player` instance. Overrides the player if it already exists or creates a new one.

        Args:
            player (Player): The player to save.
        """
        player_dict = player.to_dict()
        name = player_dict["name"]
        hash = player_dict["password_hash"]
        self.data["users"][name] = hash
        self._save_to_json()

    def get_games_for_player(self, player: str):
        """Gets all games for a specific player.

        Args:
            player (str): The player's name.

        Returns:
            list[Game]: List of `Game` instances.
        """
        return [
            Game.from_dict({game_name: game_data})
            for game_name, game_data in self.data["games"].items()
            if game_data["name"] == player
        ]

    def get_game(self, player, game):
        """Gets a game by player and game name.

        Args:
            player (str): The player's name.
            game (str): The game's name.

        Returns:
            Game: The requested `Game` instance.
        """
        for game_name, game_data in self.data["games"].items():
            if game == game_name and game_data["name"] == player:
                # TODO @anja: Bitte noch implementieren
                return Game.from_dict(game_data)
        return None

    def save_game(self, game: Game):
        """Saves a game.

        Args:
            game (Game): The game that is to be saved.
        """
        # TODO @anja: Bitte noch implementieren
        self.data["games"][game.name] = game.to_dict()
        self._save_to_json()

    def _save_to_json(self):
        """Writes all changes of the `data` attribute to the json file.
        """
        with open(self.filename, "w") as data_file:
            json.dump(self.data, data_file, indent=4)

    def get_highscores(self):
        """Returns a formatted string containing all highscores

        Returns:
            str: The highscores string
        """
        # TODO
        pass


if __name__ == "__main__":
    per = Persistence("data.json")
    per.save_player(Player("serafina", "xxx"))
    per.save_player(Player("Anja", "x"))
    print(per.data)
    print(per.get_players())
