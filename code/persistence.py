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
            
            content += "\n\n" + str(game.sudoku) + \
                    "\nNeeded time: " + str(game.time_length) + " seconds" + \
                    "\nNeeded hints: " + str(game.hint_counter)
            f.write(content)
    
    def load_game(path:str) -> Game:
        #TODO Tests and Docstring, maybe validation code that checks if anything was manipulated
        game = Game()
        sudoku = None
        with open(path,"r") as f:
            game.name = os.path.basename(path)
            content = list(f)
            if "played by" in content[0]:
                pass # TODO Player implementation
            
            sudoku = Sudoku(size=sum(ch == "-" for ch in content[2])) # first vertical line tells sudoku size
            sudoku.values = Persistence._decode_sudoku_str(content,3,len(content) - 3,sudoku.grid)
            game.sudoku = sudoku
            game.time_length = Persistence._decode_time(content[len(content) - 2])
            game.hint_counter = Persistence._decode_hints(content[len(content) - 1])
        return game

    def _decode_sudoku_str(content:str, start:int, end:int, grid:int) -> list[list[int]]:
        values = []
        for i in range(start,end):
            row = content[i] # Pick one line to decode
            translated_row = []
            j = 0
            if "-" in row: continue # Skip horizontal line of '-'
            while j < len(row):
                if row[j] == "|": # Skip vertical line of '|'
                    j += 2
                    continue
                elif row[j].isdigit(): # Number entry in cell of the sudoku field
                    translated_row.append(int(row[j]))
                elif row[j] == " ": # Empty cells are represented by zero
                    translated_row.append(0)
                if len(translated_row) % grid != 0: 
                    j += 1 # in the middle of each grid the numbers have higher distance, 3 in total, to simplify reading
                j += 2 # last number before the next vertical line has lower distance 2
            values.append(translated_row)
        return values

    def _decode_time(content:str) -> int:
        return content[len("Needed time: "):content.find("seconds")]
        
    def _decode_hints(content:str) -> int:
        return content[len("Needed hints: "):]

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
    
# g = Game()
# #g.player = Player(name="testPlayername")
# g.time_length = 2
# Persistence.save_game(g,"/home/anja/Dokumente/")

#Persistence.load_game("/home/anja/Dokumente/Sudoku Game 2025-01-05 18:30:55.260268")

#print(Persistence.check_filepath("/home/anja/Dokumente/Sudoku Game 2025-01-05 18:30:55.260268"))
#print(Persistence.get_current_dir())
print(Persistence.check_path(""))